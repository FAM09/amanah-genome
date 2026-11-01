"""
Session Management & Bio-Crypto Matching REST Endpoints.
Zero-knowledge genomic pairing and Private Set Intersection (PSI).
"""

import time
from typing import Dict, List, Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel, Field

from app.bio.panel import get_all_panel_genes
from app.bio.vcf_parser import parse_vcf_stream
from app.core.crypto_psi import (
    IntersectionMatchResult,
    blind_gene_set,
    evaluate_private_intersection,
    generate_session_salt,
)

router = APIRouter(prefix="/api/session", tags=["Session & Matching"])


class CreateSessionResponse(BaseModel):
    session_id: str
    session_code: str
    created_at: float
    session_salt_hint: str  # first 8 chars of salt for audit


class UploadReceipt(BaseModel):
    session_id: str
    party: str  # "A" or "B"
    sample_id: str
    variants_scanned: int
    pathogenic_carrier_count: int
    commitment_hash: str
    is_ready_for_match: bool


# Ephemeral in-memory store for active pairing sessions (Transient & Zero-DNA retention)
ACTIVE_SESSIONS: Dict[str, dict] = {}


@router.post("/init", response_model=CreateSessionResponse)
def initialize_session():
    """Create a new ephemeral pairing session with session salt and 6-digit code."""
    salt = generate_session_salt(32)
    session_id = f"SES-{salt[:8].upper()}"
    session_code = f"AMN-{salt[8:12].upper()}"
    now = time.time()

    ACTIVE_SESSIONS[session_id] = {
        "session_id": session_id,
        "session_code": session_code,
        "session_salt": salt,
        "created_at": now,
        "party_a": None,
        "party_b": None,
        "match_result": None,
    }

    return CreateSessionResponse(
        session_id=session_id,
        session_code=session_code,
        created_at=now,
        session_salt_hint=salt[:8],
    )


@router.get("/{session_id}/status")
def get_session_status(session_id: str):
    """Retrieve pairing readiness status."""
    if session_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    sess = ACTIVE_SESSIONS[session_id]
    return {
        "session_id": session_id,
        "session_code": sess["session_code"],
        "party_a_uploaded": sess["party_a"] is not None,
        "party_b_uploaded": sess["party_b"] is not None,
        "is_ready_for_match": (sess["party_a"] is not None) and (sess["party_b"] is not None),
        "is_evaluated": sess["match_result"] is not None,
    }


@router.post("/{session_id}/upload", response_model=UploadReceipt)
async def upload_vcf(
    session_id: str,
    party: str = Form(..., description="'A' for Partner 1, 'B' for Partner 2"),
    vcf_file: UploadFile = File(..., description="Variant Call Format (.vcf) file"),
):
    """
    Upload and parse VCF file in transient memory.
    Raw DNA is NEVER written to disk. Only salted hashes and Merkle commitment are retained.
    """
    if session_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    party_key = party.upper().strip()
    if party_key not in ("A", "B"):
        raise HTTPException(status_code=400, detail="Party must be 'A' or 'B'")

    # Read VCF directly into memory buffer
    content_bytes = await vcf_file.read()
    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Invalid file encoding. UTF-8 standard VCF required.")

    # 1. Parse and filter for UAE panel pathogenic carriers in transient memory
    profile = parse_vcf_stream(content_str, sample_name_override=vcf_file.filename)

    # 2. Blind carrier gene set with session salt
    salt = ACTIVE_SESSIONS[session_id]["session_salt"]
    hash_map, commitment = blind_gene_set(profile.carrier_genes, salt)

    # 3. Store only blinded state in session
    party_data = {
        "sample_id": profile.sample_id,
        "raw_carrier_genes": profile.carrier_genes,  # Kept in memory only until match evaluation
        "hash_map": hash_map,
        "commitment": commitment,
        "variants_scanned": profile.total_variants_scanned,
        "pathogenic_carrier_count": profile.pathogenic_carrier_count,
    }

    if party_key == "A":
        ACTIVE_SESSIONS[session_id]["party_a"] = party_data
    else:
        ACTIVE_SESSIONS[session_id]["party_b"] = party_data

    is_ready = (
        ACTIVE_SESSIONS[session_id]["party_a"] is not None
        and ACTIVE_SESSIONS[session_id]["party_b"] is not None
    )

    return UploadReceipt(
        session_id=session_id,
        party=party_key,
        sample_id=profile.sample_id,
        variants_scanned=profile.total_variants_scanned,
        pathogenic_carrier_count=profile.pathogenic_carrier_count,
        commitment_hash=commitment,
        is_ready_for_match=is_ready,
    )


@router.post("/{session_id}/evaluate", response_model=IntersectionMatchResult)
def evaluate_match(session_id: str):
    """
    Execute Private Set Intersection (PSI) between Partner A and Partner B.
    Computes exact intersection over salted hashes without leaking non-overlapping variants.
    """
    if session_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    sess = ACTIVE_SESSIONS[session_id]
    if not sess["party_a"] or not sess["party_b"]:
        raise HTTPException(
            status_code=400,
            detail="Both Partner A and Partner B must upload their VCF before evaluation."
        )

    genes_a = sess["party_a"]["raw_carrier_genes"]
    genes_b = sess["party_b"]["raw_carrier_genes"]
    salt = sess["session_salt"]

    result = evaluate_private_intersection(genes_a, genes_b, salt)
    sess["match_result"] = result

    return result
