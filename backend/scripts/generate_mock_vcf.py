"""
Synthetic VCF v4.2 Generator for UAE Premarital Screening Scenarios.
Generates realistic, standardized VCF files for benchmark testing and evaluation.
"""

import os
from pathlib import Path
from typing import List, Optional

VCF_HEADER_TEMPLATE = """##fileformat=VCFv4.2
##fileDate=20261101
##source=AmanahGenomeSyntheticGeneratorV1
##reference=GRCh38
##INFO=<ID=GENE,Number=1,Type=String,Description="HGNC Gene Symbol">
##INFO=<ID=CLNSIG,Number=1,Type=String,Description="ClinVar Clinical Significance">
##INFO=<ID=CLNDN,Number=1,Type=String,Description="ClinVar Disease Name">
##INFO=<ID=RS,Number=1,Type=String,Description="dbSNP ID">
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency in Regional Population">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
##FORMAT=<ID=DP,Number=1,Type=Integer,Description="Read Depth">
##FORMAT=<ID=GQ,Number=1,Type=Integer,Description="Genotype Quality">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	{sample_name}
"""

# Sample background benign variants to ensure realistic genomic noise
BENIGN_BACKGROUND = [
    ("chr1", 1010020, "rs1800001", "A", "G", "GENE=MTHFR;CLNSIG=Benign;CLNDN=Common_variant;AF=0.45", "0/1"),
    ("chr2", 2341050, "rs2234002", "C", "T", "GENE=ABCA1;CLNSIG=Benign;CLNDN=Benign_polymorphism;AF=0.32", "0/0"),
    ("chr19", 44908684, "rs429358", "T", "C", "GENE=APOE;CLNSIG=Benign/Risk_factor;CLNDN=ApoE3/4;AF=0.15", "0/1"),
]

# Pathogenic Carrier Variants for Top UAE Panel
PATHOGENIC_HBB_THALASSEMIA = (
    "chr11", 5226797, "rs33971440", "G", "A",
    "GENE=HBB;CLNSIG=Pathogenic;CLNDN=Beta-Thalassemia;RS=rs33971440;AF=0.042", "0/1"
)

PATHOGENIC_HBB_SICKLE = (
    "chr11", 5227002, "rs334", "T", "A",
    "GENE=HBB;CLNSIG=Pathogenic;CLNDN=Sickle_Cell_Disease;RS=rs334;AF=0.035", "0/1"
)

PATHOGENIC_SMN1_SMA = (
    "chr5", 70925500, "rs386834235", "C", "T",
    "GENE=SMN1;CLNSIG=Pathogenic;CLNDN=Spinal_Muscular_Atrophy;RS=rs386834235;AF=0.025", "0/1"
)

PATHOGENIC_CFTR = (
    "chr7", 117559590, "rs113993960", "ATCT", "A",
    "GENE=CFTR;CLNSIG=Pathogenic;CLNDN=Cystic_Fibrosis;RS=rs113993960;AF=0.018", "0/1"
)

PATHOGENIC_CYP21A2 = (
    "chr6", 32040000, "rs6467", "C", "G",
    "GENE=CYP21A2;CLNSIG=Pathogenic;CLNDN=Congenital_Adrenal_Hyperplasia;RS=rs6467;AF=0.015", "0/1"
)

PATHOGENIC_PAH = (
    "chr12", 102844400, "rs5030858", "C", "T",
    "GENE=PAH;CLNSIG=Pathogenic;CLNDN=Phenylketonuria;RS=rs5030858;AF=0.010", "0/1"
)


def build_vcf_text(sample_name: str, variants: List[tuple]) -> str:
    """Build standardized VCF string with header and variant records."""
    header = VCF_HEADER_TEMPLATE.format(sample_name=sample_name)
    rows = []
    for chrom, pos, var_id, ref, alt, info, gt in variants:
        row = f"{chrom}\t{pos}\t{var_id}\t{ref}\t{alt}\t99\tPASS\t{info}\tGT:DP:GQ\t{gt}:45:99"
        rows.append(row)
    return header + "\n".join(rows) + "\n"


def generate_all_mock_scenarios(output_base_dir: str):
    """
    Generate 4 benchmark test scenarios into output directory:
    - Case 01: Fully compatible (No carrier mutations)
    - Case 02: High-Risk Match: Beta-Thalassemia (both carry HBB)
    - Case 03: High-Risk Match: Spinal Muscular Atrophy (both carry SMN1)
    - Case 04: Asymmetric Carrier: Ahmad(CFTR) + Fatima(HBB) -> Safe/Compatible
    """
    base = Path(output_base_dir)

    # Scenario 1: Fully Compatible
    case_1_dir = base / "case_01_compatible"
    case_1_dir.mkdir(parents=True, exist_ok=True)
    vcf_1_ahmad = build_vcf_text("AHMAD_CLEAR", BENIGN_BACKGROUND)
    vcf_1_fatima = build_vcf_text("FATIMA_CLEAR", BENIGN_BACKGROUND)
    (case_1_dir / "ahmad_sample.vcf").write_text(vcf_1_ahmad, encoding="utf-8")
    (case_1_dir / "fatima_sample.vcf").write_text(vcf_1_fatima, encoding="utf-8")

    # Scenario 2: High-Risk Beta-Thalassemia (Both carry HBB)
    case_2_dir = base / "case_02_thalassemia_carrier_both"
    case_2_dir.mkdir(parents=True, exist_ok=True)
    vcf_2_ahmad = build_vcf_text("AHMAD_HBB_CARRIER", BENIGN_BACKGROUND + [PATHOGENIC_HBB_THALASSEMIA])
    vcf_2_fatima = build_vcf_text("FATIMA_HBB_CARRIER", BENIGN_BACKGROUND + [PATHOGENIC_HBB_THALASSEMIA])
    (case_2_dir / "ahmad_sample.vcf").write_text(vcf_2_ahmad, encoding="utf-8")
    (case_2_dir / "fatima_sample.vcf").write_text(vcf_2_fatima, encoding="utf-8")

    # Scenario 3: High-Risk SMA (Both carry SMN1)
    case_3_dir = base / "case_03_sma_carrier_both"
    case_3_dir.mkdir(parents=True, exist_ok=True)
    vcf_3_ahmad = build_vcf_text("AHMAD_SMN1_CARRIER", BENIGN_BACKGROUND + [PATHOGENIC_SMN1_SMA])
    vcf_3_fatima = build_vcf_text("FATIMA_SMN1_CARRIER", BENIGN_BACKGROUND + [PATHOGENIC_SMN1_SMA])
    (case_3_dir / "ahmad_sample.vcf").write_text(vcf_3_ahmad, encoding="utf-8")
    (case_3_dir / "fatima_sample.vcf").write_text(vcf_3_fatima, encoding="utf-8")

    # Scenario 4: Asymmetric Carrier (Ahmad CFTR, Fatima HBB -> Fully Compatible, No Overlap)
    case_4_dir = base / "case_04_asymmetric_no_overlap"
    case_4_dir.mkdir(parents=True, exist_ok=True)
    vcf_4_ahmad = build_vcf_text("AHMAD_CFTR_CARRIER", BENIGN_BACKGROUND + [PATHOGENIC_CFTR])
    vcf_4_fatima = build_vcf_text("FATIMA_HBB_CARRIER", BENIGN_BACKGROUND + [PATHOGENIC_HBB_THALASSEMIA])
    (case_4_dir / "ahmad_sample.vcf").write_text(vcf_4_ahmad, encoding="utf-8")
    (case_4_dir / "fatima_sample.vcf").write_text(vcf_4_fatima, encoding="utf-8")

    print(f"Generated 4 benchmark scenarios in: {base.resolve()}")


if __name__ == "__main__":
    mock_dir = os.environ.get("MOCK_DATA_DIR", "/home/fam/amanah-genome/mock-data")
    generate_all_mock_scenarios(mock_dir)
