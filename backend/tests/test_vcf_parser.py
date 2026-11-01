"""
Unit tests for VCF Parser & ClinVar Recessive Pathogen Extractor.
"""

from app.bio.vcf_parser import parse_vcf_stream


def test_parse_clean_compatible_vcf():
    """VCF containing only benign variants should yield zero pathogenic carrier genes."""
    vcf_text = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	AHMAD
chr1	1010020	rs1800001	A	G	99	PASS	GENE=MTHFR;CLNSIG=Benign	GT	0/1
chr2	2341050	rs2234002	C	T	99	PASS	GENE=ABCA1;CLNSIG=Benign	GT	0/0
"""
    profile = parse_vcf_stream(vcf_text)
    assert profile.sample_id == "AHMAD"
    assert profile.pathogenic_carrier_count == 0
    assert profile.carrier_genes == []


def test_parse_pathogenic_carrier_vcf():
    """VCF containing heterozygous pathogenic HBB mutation should be correctly extracted."""
    vcf_text = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	FATIMA
chr11	5226797	rs33971440	G	A	99	PASS	GENE=HBB;CLNSIG=Pathogenic;CLNDN=Beta-Thalassemia	GT	0/1
chr1	1010020	rs1800001	A	G	99	PASS	GENE=MTHFR;CLNSIG=Benign	GT	0/1
"""
    profile = parse_vcf_stream(vcf_text)
    assert profile.sample_id == "FATIMA"
    assert profile.pathogenic_carrier_count == 1
    assert "HBB" in profile.carrier_genes
    assert profile.variants[0].gene == "HBB"
    assert profile.variants[0].genotype == "0/1"
    assert profile.variants[0].is_carrier is True


def test_homozygous_reference_ignored():
    """Genotype 0/0 (homozygous normal reference) should not be marked as a carrier."""
    vcf_text = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	USER
chr11	5226797	rs33971440	G	A	99	PASS	GENE=HBB;CLNSIG=Pathogenic	GT	0/0
"""
    profile = parse_vcf_stream(vcf_text)
    assert profile.carrier_genes == []
    assert profile.pathogenic_carrier_count == 0
