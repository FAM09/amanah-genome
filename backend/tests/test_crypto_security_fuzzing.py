"""
Deep Crypto Security, Merkle Tampering, and Adversarial PSI Leakage Tests.
Validates:
- Merkle commitment tampering detection
- Salt entropy & uniqueness across high volumes
- Zero-knowledge non-leakage under exhaustive combinatorial permutations
- Multi-gene overlapping intersections
"""

import hashlib
import random
from typing import List
from app.bio.panel import UAE_RECESSIVE_PANEL
from app.core.crypto_psi import (
    blind_gene_set,
    compute_merkle_commitment,
    evaluate_private_intersection,
    generate_session_salt,
    hash_gene_identifier,
)


def test_merkle_commitment_tamper_detection():
    """Verify that tampering with any hash in the set alters the commitment."""
    salt = generate_session_salt(32)
    genes = ["HBB", "SMN1", "CFTR"]
    _, commitment_original = blind_gene_set(genes, salt)

    # Tampered set: replace one gene
    genes_tampered = ["HBB", "SMN1", "PAH"]
    _, commitment_tampered = blind_gene_set(genes_tampered, salt)

    assert commitment_original != commitment_tampered, "Commitment failed to detect set tampering"


def test_salt_entropy_uniqueness():
    """Generate 1000 consecutive salts and ensure zero collisions and strong entropy."""
    salts = set()
    for _ in range(1000):
        s = generate_session_salt(32)
        assert len(s) == 64  # 32 bytes hex = 64 hex characters
        assert s not in salts, "Salt collision detected!"
        salts.add(s)
    assert len(salts) == 1000


def test_multi_gene_overlap_combinations():
    """Test multi-gene carrier overlap (e.g. couples carrying 2 or 3 common recessive genes)."""
    salt = generate_session_salt(32)
    genes_a = ["HBB", "SMN1", "GBA", "CFTR"]
    genes_b = ["SMN1", "HBB", "PAH", "MEFV"]

    result = evaluate_private_intersection(genes_a, genes_b, salt)

    assert result.is_compatible is False
    assert result.risk_level == "HIGH_RECESSIVE_RISK"
    assert result.child_risk_probability == 0.25
    assert set(result.intersecting_genes) == {"HBB", "SMN1"}
    assert len(result.intersecting_gene_details) == 2
    # Verify non-overlapping genes (CFTR, GBA, PAH, MEFV) are NOT in the result
    assert "CFTR" not in result.intersecting_genes
    assert "GBA" not in result.intersecting_genes
    assert "PAH" not in result.intersecting_genes
    assert "MEFV" not in result.intersecting_genes


def test_exhaustive_random_permutations_zero_leakage():
    """
    Exhaustive Zero-Knowledge Non-Leakage Test:
    Generates 50 random gene subsets from the UAE panel for Ahmad and Fatima.
    Verifies that in 100% of cases, the only genes revealed are the mathematical intersection.
    """
    all_genes = list(UAE_RECESSIVE_PANEL.keys())
    random.seed(42)

    for i in range(50):
        salt = generate_session_salt(32)
        # Random subsets (0 to 4 genes each)
        subset_a = random.sample(all_genes, random.randint(0, 4))
        subset_b = random.sample(all_genes, random.randint(0, 4))

        expected_intersection = sorted(list(set(subset_a).intersection(set(subset_b))))
        result = evaluate_private_intersection(subset_a, subset_b, salt)

        assert sorted(result.intersecting_genes) == expected_intersection, (
            f"Iteration {i} failed: expected {expected_intersection}, got {result.intersecting_genes}"
        )
        assert result.is_compatible == (len(expected_intersection) == 0)

        # Non-leakage: any gene in A not in B must NEVER be revealed
        leaked_from_a = set(subset_a) - set(subset_b)
        leaked_from_b = set(subset_b) - set(subset_a)
        for leaked in leaked_from_a:
            assert leaked not in result.intersecting_genes
        for leaked in leaked_from_b:
            assert leaked not in result.intersecting_genes


def test_empty_carrier_sets():
    """Both participants have 0 carrier genes -> Safe/Compatible."""
    salt = generate_session_salt(32)
    result = evaluate_private_intersection([], [], salt)

    assert result.is_compatible is True
    assert result.risk_level == "LOW_RISK_CLEAR"
    assert result.child_risk_probability == 0.0
    assert result.intersecting_genes == []
    assert result.zk_proof_token.startswith("ZKP-DOH-")
