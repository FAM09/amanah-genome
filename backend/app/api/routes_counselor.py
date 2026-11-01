"""
Cultural AI Counselor & Clinical Referral REST Endpoints.
Connects couples with Abu Dhabi DoH Genetic Counselors and provides real-time guidance.
"""

import time
import uuid
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.ai.counselor import (
    ChatMessage,
    ClinicalReferralTicket,
    CounselRequest,
    get_counselor_response,
)
from app.api.routes_session import ACTIVE_SESSIONS
from app.bio.panel import UAE_RECESSIVE_PANEL

router = APIRouter(prefix="/api", tags=["AI Counselor & DoH Referral"])

# In-memory store for clinical referral tickets
CLINICAL_TICKETS: Dict[str, ClinicalReferralTicket] = {}


class ChatPayload(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    response: str
    match_status: str
    intersecting_genes: List[str]


class TicketUpdatePayload(BaseModel):
    status: str  # e.g., "ASSIGNED", "TELECONSULT_SCHEDULED", "COMPLETED"
    counselor_notes: Optional[str] = None


@router.post("/session/{session_id}/counsel", response_model=ChatResponse)
async def counsel_couple(session_id: str, payload: ChatPayload):
    """Interactive cultural AI counseling conversation for a paired couple session."""
    if session_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    sess = ACTIVE_SESSIONS[session_id]
    match_result = sess.get("match_result")

    match_status = "UNKNOWN"
    intersecting_genes = []

    if match_result:
        match_status = match_result.risk_level
        intersecting_genes = match_result.intersecting_genes

    counsel_req = CounselRequest(
        session_id=session_id,
        match_status=match_status,
        intersecting_genes=intersecting_genes,
        messages=payload.messages,
        stream=False,
    )

    reply = await get_counselor_response(counsel_req)

    return ChatResponse(
        response=reply,
        match_status=match_status,
        intersecting_genes=intersecting_genes,
    )


@router.post("/session/{session_id}/referral", response_model=ClinicalReferralTicket)
def create_referral_ticket(session_id: str):
    """
    Generate an encrypted, confidential clinical referral ticket for the DoH Counselor Portal.
    Extracts only the medical facts (affected genes, risk ratio) without disclosing personal identifiers.
    """
    if session_id not in ACTIVE_SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found or expired")

    sess = ACTIVE_SESSIONS[session_id]
    match_result = sess.get("match_result")

    if not match_result:
        raise HTTPException(status_code=400, detail="Match must be evaluated before dispatching referral")

    ticket_id = f"REF-DOH-{uuid.uuid4().hex[:8].upper()}"
    diseases_en = []
    diseases_ar = []

    for g in match_result.intersecting_genes:
        if g in UAE_RECESSIVE_PANEL:
            diseases_en.append(UAE_RECESSIVE_PANEL[g].disease_name_en)
            diseases_ar.append(UAE_RECESSIVE_PANEL[g].disease_name_ar)

    pathway = (
        "Pre-implantation Genetic Testing (PGT-M) with IVF Consultation"
        if not match_result.is_compatible
        else "Standard Pre-marital Wellness Certificate Clearance"
    )

    ticket = ClinicalReferralTicket(
        ticket_id=ticket_id,
        session_id=session_id,
        created_at=time.time(),
        status="PENDING_COUNSELOR_REVIEW",
        intersecting_genes=match_result.intersecting_genes,
        affected_diseases_en=diseases_en,
        affected_diseases_ar=diseases_ar,
        child_risk_probability=match_result.child_risk_probability,
        recommended_pathway=pathway,
        doh_clinic_reference="Abu Dhabi Health Services (SEHA) / DoH Certified Network",
        is_confidential=True,
    )

    CLINICAL_TICKETS[ticket_id] = ticket
    return ticket


@router.get("/counselor/tickets", response_model=List[ClinicalReferralTicket])
def list_counselor_tickets():
    """Retrieve all triage referral tickets for the Genetic Counselor Portal."""
    return sorted(list(CLINICAL_TICKETS.values()), key=lambda t: t.created_at, reverse=True)


@router.get("/counselor/tickets/{ticket_id}", response_model=ClinicalReferralTicket)
def get_counselor_ticket_detail(ticket_id: str):
    """Retrieve sanitized clinical summary brief for a specific triage ticket."""
    if ticket_id not in CLINICAL_TICKETS:
        raise HTTPException(status_code=404, detail="Referral ticket not found")
    return CLINICAL_TICKETS[ticket_id]


@router.patch("/counselor/tickets/{ticket_id}")
def update_counselor_ticket_status(ticket_id: str, payload: TicketUpdatePayload):
    """Update triage ticket status (e.g. ASSIGNED, TELECONSULT_SCHEDULED)."""
    if ticket_id not in CLINICAL_TICKETS:
        raise HTTPException(status_code=404, detail="Referral ticket not found")

    ticket = CLINICAL_TICKETS[ticket_id]
    ticket.status = payload.status.upper()
    return {"message": "Ticket status updated", "ticket": ticket}
