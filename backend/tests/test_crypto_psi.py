"""
Unit tests for Private Set Intersection (PSI) and Cryptographic Commitment.
"""

from app.core.crypto_psi import (
    blind_gene_set,
    compute_merkle_commitment,
    evaluate_private_intersection,
    generate_session_salt,
    hash_gene_identifier,
)


def test_salted_hash_uniqueness():
    """Verify that distinct salts produce completely different hashes for the same gene."""
    salt_1 = generate_session_salt(32)
    salt_2 = generate_session_salt(32)

    assert salt_1 != salt_2
    hash_1 = hash_gene_identifier("HBB", salt_1)
    hash_2 = hash_gene_identifier("HBB", salt_2)

    assert hash_1 != hash_2
    assert len(hash_1) == 64  # SHA-256 hexdigest


def test_commitment_determinism():
    """Commitment should be deterministic for the same list of hashes."""
    hashes = ["abc123", "def456", "789xyz"]
    c1 = compute_merkle_commitment(hashes)
    c2 = compute_merkle_commitment(list(reversed(hashes)))  # sorted internally
    assert c1 == c2


def test_psi_intersection_accuracy():
    """Intersection should identify exact overlapping genes."""
    salt = generate_session_salt(32)
    genes_a = ["HBB", "CFTR", "PAH"]
    genes_b = ["SMN1", "HBB", "GBA"]

    result = evaluate_private_intersection(genes_a, genes_b, salt)

    assert result.is_compatible is False
    assert result.risk_level == "HIGH_RECESSIVE_RISK"
    assert result.child_risk_probability == 0.25
    assert result.intersecting_genes == ["HBB"]
    assert len(result.intersecting_gene_details) == 1
    assert result.intersecting_gene_details[0].gene_symbol == "HBB"
    assert result.zk_proof_token.startswith("ZKP-DOH-")


def test_psi_zero_leakage_guarantee():
    """
    Zero-knowledge non-leakage check:
    When Ahmad carries CFTR and Fatima carries HBB, the intersection MUST be empty.
    Neither participant gets any trace or revelation of the other's gene.
    """
    salt = generate_session_salt(32)
    genes_ahmad = ["CFTR"]
    genes_fatima = ["HBB"]

    result = evaluate_private_intersection(genes_ahmad, genes_fatima, salt)

    assert result.is_compatible is True
    assert result.risk_level == "LOW_RISK_CLEAR"
    assert result.child_risk_probability == 0.0
    assert result.intersecting_genes == []
    assert len(result.intersecting_gene_details) == 0
