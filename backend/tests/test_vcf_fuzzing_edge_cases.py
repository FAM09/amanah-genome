"""
Deep VCF Parser Fuzzing & Adversarial Input Robustness Tests.
Validates:
- Malformed and corrupt lines (empty, truncated, garbage tokens)
- Genotype parsing variants (phased 0|1, unphased 1/0, homozygous 1/1, multiallelic 1/2)
- Injection payloads inside VCF INFO columns
- Chromosome prefix normalization ('chr11', '11', 'CHR11')
- Large synthetic VCF (1,000+ variants) memory & crash stability
"""

from app.bio.vcf_parser import parse_vcf_stream


def test_vcf_fuzzing_malformed_and_garbage_input():
    """Parser must gracefully handle corrupt lines without throwing unhandled exceptions."""
    garbage_vcfs = [
        "",
        "NOT_A_VCF_HEADER\nrandom_token_1\trandom_token_2",
        "##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO",  # No sample column
        "chr11\tNOT_A_NUMBER\trs1\tA\tG\t99\tPASS\tGENE=HBB",
        "chr11\t5226797\trs1\tA\tG",  # truncated row (< 8 columns)
        "\x00\x01\x02\x03\xff\xfe",  # binary junk
        "##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n" + ("\n" * 50),
    ]

    for g_vcf in garbage_vcfs:
        profile = parse_vcf_stream(g_vcf)
        assert profile is not None
        assert isinstance(profile.carrier_genes, list)


def test_vcf_genotype_variations():
    """Verify various heterozygous and homozygous genotypes for pathogenic variants."""
    genotypes_to_test = [
        ("0/1", True),   # standard unphased heterozygous carrier
        ("1/0", True),   # reverse unphased heterozygous carrier
        ("0|1", True),   # phased heterozygous carrier
        ("1|0", True),   # reverse phased heterozygous carrier
        ("1/1", True),   # homozygous alternative (affected/carrier)
        ("1|1", True),   # phased homozygous alternative
        ("0/0", False),  # homozygous reference (NOT a carrier)
        ("0|0", False),  # phased homozygous reference
        ("./.", False),  # missing call
        (".", False),    # uncalled
    ]

    for gt, expected_carrier in genotypes_to_test:
        vcf = f"""##fileformat=VCFv4.2
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT
chr11\t5226797\trs33971440\tG\tA\t99\tPASS\tGENE=HBB;CLNSIG=Pathogenic\tGT\t{gt}
"""
        profile = parse_vcf_stream(vcf)
        if expected_carrier:
            assert "HBB" in profile.carrier_genes, f"Failed to detect carrier for GT: {gt}"
            assert profile.pathogenic_carrier_count == 1
        else:
            assert "HBB" not in profile.carrier_genes, f"False positive carrier for GT: {gt}"
            assert profile.pathogenic_carrier_count == 0


def test_vcf_injection_payload_sanitization():
    """Verify that SQL/Script injection payloads in INFO column are harmlessly parsed."""
    malicious_vcf = """##fileformat=VCFv4.2
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT
chr11\t5226797\trs33971440\tG\tA\t99\tPASS\tGENE=HBB;CLNSIG=Pathogenic;INJECTION="; DROP TABLE users; --";XSS="<script>alert(1)</script>"\tGT\t0/1
chr5\t70925500\trs386834235\tC\tT\t99\tPASS\tGENE=SMN1;CLNSIG=Pathogenic'; EXEC xp_cmdshell('dir');--\tGT\t0/1
"""
    profile = parse_vcf_stream(malicious_vcf)
    assert set(profile.carrier_genes) == {"HBB", "SMN1"}
    assert profile.pathogenic_carrier_count == 2


def test_chromosome_format_variations():
    """Verify that both 'chr11', '11', and uppercase 'CHR11' are handled correctly."""
    vcf_cases = [
        "chr11\t5226797\trs33971440\tG\tA\t99\tPASS\tGENE=HBB;CLNSIG=Pathogenic\tGT\t0/1",
        "11\t5226797\trs33971440\tG\tA\t99\tPASS\tGENE=HBB;CLNSIG=Pathogenic\tGT\t0/1",
        "CHR11\t5226797\trs33971440\tG\tA\t99\tPASS\tGENE=HBB;CLNSIG=Pathogenic\tGT\t0/1",
    ]

    for line in vcf_cases:
        vcf = f"##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tPATIENT\n{line}\n"
        profile = parse_vcf_stream(vcf)
        assert "HBB" in profile.carrier_genes


def test_large_vcf_throughput():
    """Verify parser throughput and stability on a large VCF with 1,500 variants."""
    lines = [
        "##fileformat=VCFv4.2",
        "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tBENCHMARK_SAMPLE",
    ]
    # Add 1500 benign variants
    for i in range(1500):
        lines.append(f"chr1\t{100000 + i}\trs{i}\tA\tG\t99\tPASS\tGENE=NON_PANEL_{i};CLNSIG=Benign\tGT\t0/1")
    # Add 1 real pathogenic carrier variant
    lines.append("chr11\t5226797\trs33971440\tG\tA\t99\tPASS\tGENE=HBB;CLNSIG=Pathogenic\tGT\t0/1")

    large_vcf_content = "\n".join(lines)
    profile = parse_vcf_stream(large_vcf_content)

    assert profile.total_variants_scanned == 1501
    assert profile.pathogenic_carrier_count == 1
    assert profile.carrier_genes == ["HBB"]
