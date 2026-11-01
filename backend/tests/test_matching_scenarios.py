"""
End-to-end Scenario Matching Tests against the 4 Benchmark VCF Scenarios.
"""

from pathlib import Path
from app.bio.vcf_parser import parse_vcf_stream
from app.core.crypto_psi import evaluate_private_intersection, generate_session_salt

MOCK_ROOT = Path("/home/fam/amanah-genome/mock-data")


def test_scenario_1_fully_compatible():
    """Scenario 1: Ahmad & Fatima are both clear -> 100% Compatible."""
    ahmad_vcf = (MOCK_ROOT / "case_01_compatible" / "ahmad_sample.vcf").read_text()
    fatima_vcf = (MOCK_ROOT / "case_01_compatible" / "fatima_sample.vcf").read_text()

    profile_a = parse_vcf_stream(ahmad_vcf)
    profile_b = parse_vcf_stream(fatima_vcf)

    assert profile_a.carrier_genes == []
    assert profile_b.carrier_genes == []

    salt = generate_session_salt()
    result = evaluate_private_intersection(profile_a.carrier_genes, profile_b.carrier_genes, salt)

    assert result.is_compatible is True
    assert result.risk_level == "LOW_RISK_CLEAR"
    assert result.child_risk_probability == 0.0
    assert result.intersecting_genes == []


def test_scenario_2_thalassemia_high_risk():
    """Scenario 2: Both Ahmad & Fatima carry HBB -> High Recessive Risk (25%)."""
    ahmad_vcf = (MOCK_ROOT / "case_02_thalassemia_carrier_both" / "ahmad_sample.vcf").read_text()
    fatima_vcf = (MOCK_ROOT / "case_02_thalassemia_carrier_both" / "fatima_sample.vcf").read_text()

    profile_a = parse_vcf_stream(ahmad_vcf)
    profile_b = parse_vcf_stream(fatima_vcf)

    assert "HBB" in profile_a.carrier_genes
    assert "HBB" in profile_b.carrier_genes

    salt = generate_session_salt()
    result = evaluate_private_intersection(profile_a.carrier_genes, profile_b.carrier_genes, salt)

    assert result.is_compatible is False
    assert result.risk_level == "HIGH_RECESSIVE_RISK"
    assert result.child_risk_probability == 0.25
    assert result.intersecting_genes == ["HBB"]
    assert result.intersecting_gene_details[0].disease_name_en == "Beta-Thalassemia & Sickle Cell Disease"
    assert any("PGT-M" in opt for opt in result.intersecting_gene_details[0].clinical_options)


def test_scenario_3_sma_high_risk():
    """Scenario 3: Both carry SMN1 -> High Recessive Risk (25%)."""
    ahmad_vcf = (MOCK_ROOT / "case_03_sma_carrier_both" / "ahmad_sample.vcf").read_text()
    fatima_vcf = (MOCK_ROOT / "case_03_sma_carrier_both" / "fatima_sample.vcf").read_text()

    profile_a = parse_vcf_stream(ahmad_vcf)
    profile_b = parse_vcf_stream(fatima_vcf)

    assert "SMN1" in profile_a.carrier_genes
    assert "SMN1" in profile_b.carrier_genes

    salt = generate_session_salt()
    result = evaluate_private_intersection(profile_a.carrier_genes, profile_b.carrier_genes, salt)

    assert result.is_compatible is False
    assert result.risk_level == "HIGH_RECESSIVE_RISK"
    assert result.child_risk_probability == 0.25
    assert result.intersecting_genes == ["SMN1"]
    assert result.intersecting_gene_details[0].gene_symbol == "SMN1"


def test_scenario_4_asymmetric_no_overlap():
    """
    Scenario 4: Ahmad carries CFTR, Fatima carries HBB.
    Autosomal recessive requires mutations on the SAME gene for child risk.
    Therefore: Safe / Low Risk Clear, and zero knowledge of partner's variant.
    """
    ahmad_vcf = (MOCK_ROOT / "case_04_asymmetric_no_overlap" / "ahmad_sample.vcf").read_text()
    fatima_vcf = (MOCK_ROOT / "case_04_asymmetric_no_overlap" / "fatima_sample.vcf").read_text()

    profile_a = parse_vcf_stream(ahmad_vcf)
    profile_b = parse_vcf_stream(fatima_vcf)

    assert profile_a.carrier_genes == ["CFTR"]
    assert profile_b.carrier_genes == ["HBB"]

    salt = generate_session_salt()
    result = evaluate_private_intersection(profile_a.carrier_genes, profile_b.carrier_genes, salt)

    assert result.is_compatible is True
    assert result.risk_level == "LOW_RISK_CLEAR"
    assert result.child_risk_probability == 0.0
    assert result.intersecting_genes == []
