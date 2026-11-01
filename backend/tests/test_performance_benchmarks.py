"""
Performance benchmark tests for Amanah-Genome.
Validates latency requirements:
- VCF parsing latency < 100ms
- PSI matching evaluation latency < 200ms
"""

from pathlib import Path
import time
from app.bio.vcf_parser import parse_vcf_stream
from app.core.crypto_psi import evaluate_private_intersection, generate_session_salt

MOCK_ROOT = Path("/home/fam/amanah-genome/mock-data")


def test_vcf_parsing_latency():
    """Verify VCF parsing is executed in transient memory under 100ms."""
    sample_vcf = (MOCK_ROOT / "case_02_thalassemia_carrier_both" / "ahmad_sample.vcf").read_text()

    start = time.perf_counter()
    for _ in range(10):
        parse_vcf_stream(sample_vcf)
    elapsed_ms = ((time.perf_counter() - start) / 10.0) * 1000.0

    print(f"\nAverage VCF parse latency: {elapsed_ms:.2f} ms")
    assert elapsed_ms < 100.0, f"VCF parsing exceeded 100ms SLA ({elapsed_ms:.2f}ms)"


def test_psi_matching_latency():
    """Verify Private Set Intersection matching latency is well under 200ms."""
    genes_a = ["HBB", "CFTR", "PAH", "GBA", "MEFV"]
    genes_b = ["SMN1", "HBB", "GAA", "HEXA", "CYP21A2"]
    salt = generate_session_salt(32)

    start = time.perf_counter()
    for _ in range(20):
        evaluate_private_intersection(genes_a, genes_b, salt)
    elapsed_ms = ((time.perf_counter() - start) / 20.0) * 1000.0

    print(f"\nAverage PSI evaluation latency: {elapsed_ms:.2f} ms")
    assert elapsed_ms < 200.0, f"PSI evaluation exceeded 200ms SLA ({elapsed_ms:.2f}ms)"
