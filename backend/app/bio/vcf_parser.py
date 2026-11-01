"""
VCF v4.2 Parser and ClinVar Recessive Pathogen Extractor.
Parses genomic variant files, filters for UAE Priority Panel recessive carrier variants,
and extracts gene carrier sets in transient memory (zero disk retention of raw DNA).
"""

import io
from typing import Dict, List, Optional, Set, Tuple
from pydantic import BaseModel, Field

from app.bio.panel import UAE_RECESSIVE_PANEL, is_panel_gene


class DetectedVariant(BaseModel):
    chrom: str
    pos: int
    rs_id: str
    ref: str
    alt: str
    gene: str
    clnsig: str
    disease_name: Optional[str] = None
    genotype: str  # e.g., "0/1" (carrier) or "1/1" (homozygous)
    is_carrier: bool = True


class CarrierProfile(BaseModel):
    sample_id: str
    total_variants_scanned: int = 0
    pathogenic_carrier_count: int = 0
    carrier_genes: List[str] = Field(default_factory=list)
    variants: List[DetectedVariant] = Field(default_factory=list)


def parse_info_field(info_str: str) -> Dict[str, str]:
    """Parse standard VCF INFO field into key-value pairs."""
    data = {}
    for item in info_str.split(";"):
        if not item:
            continue
        if "=" in item:
            key, val = item.split("=", 1)
            data[key.strip()] = val.strip()
        else:
            data[item.strip()] = "true"
    return data


def parse_vcf_stream(vcf_content: str, sample_name_override: Optional[str] = None) -> CarrierProfile:
    """
    Parse a VCF content string in transient memory.
    Filters for ClinVar Class 4/5 (Likely_pathogenic, Pathogenic) mutations
    occurring in autosomal recessive panel genes where genotype is heterozygous (0/1, 0|1)
    or homozygous alt (1/1, 1|1).
    """
    lines = vcf_content.splitlines()
    sample_id = sample_name_override or "UNKNOWN_SAMPLE"
    total_scanned = 0
    carrier_genes_set: Set[str] = set()
    detected_variants: List[DetectedVariant] = []

    header_cols = []
    sample_idx = 9  # default VCF sample column index

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Header parsing
        if line.startswith("##"):
            continue

        if line.startswith("#CHROM"):
            header_cols = line.split("\t")
            if len(header_cols) > 9:
                if not sample_name_override:
                    sample_id = header_cols[9]
                sample_idx = 9
            continue

        # Data rows
        parts = line.split("\t")
        if len(parts) < 8:
            continue

        total_scanned += 1
        chrom, pos_str, var_id, ref, alt, qual, filt, info_str = parts[:8]
        try:
            pos = int(pos_str)
        except ValueError:
            continue

        # Extract genotype if sample column exists
        genotype = "0/1"
        if len(parts) > sample_idx:
            format_col = parts[8] if len(parts) > 8 else "GT"
            sample_col = parts[sample_idx]
            format_keys = format_col.split(":")
            sample_values = sample_col.split(":")
            if "GT" in format_keys:
                gt_idx = format_keys.index("GT")
                if gt_idx < len(sample_values):
                    genotype = sample_values[gt_idx]

        # Check if genotype indicates presence of alternate allele (0/1, 1/0, 1/1, 0|1, 1|0, 1|1)
        has_alt = any(a in genotype for a in ("1", "2"))
        if not has_alt:
            continue

        info = parse_info_field(info_str)
        gene = info.get("GENE")
        clnsig = info.get("CLNSIG", "").lower()
        clndn = info.get("CLNDN", "")

        # Fallback gene matching by position/chrom in UAE panel if GENE is omitted in INFO
        if not gene:
            clean_chrom = chrom.lower().replace("chr", "")
            for p_gene, p_data in UAE_RECESSIVE_PANEL.items():
                if p_data.chromosome.lower() == clean_chrom:
                    for pv in p_data.known_pathogenic_variants:
                        if abs(pv.pos - pos) <= 100:  # Match locus proximity
                            gene = p_gene
                            if not clnsig:
                                clnsig = "pathogenic"
                            break
                    if gene:
                        break

        if not gene:
            continue

        gene = gene.upper()
        if not is_panel_gene(gene):
            continue

        # Verify clinical significance (Pathogenic or Likely_pathogenic)
        is_pathogenic = any(
            term in clnsig
            for term in ("pathogenic", "likely_pathogenic", "pathogenic/likely_pathogenic")
        )

        # Benign check exclusion
        if "benign" in clnsig and not is_pathogenic:
            continue

        if is_pathogenic:
            carrier_genes_set.add(gene)
            detected_variants.append(
                DetectedVariant(
                    chrom=chrom,
                    pos=pos,
                    rs_id=var_id if var_id != "." else info.get("RS", "."),
                    ref=ref,
                    alt=alt,
                    gene=gene,
                    clnsig=info.get("CLNSIG", "Pathogenic"),
                    disease_name=clndn or UAE_RECESSIVE_PANEL[gene].disease_name_en,
                    genotype=genotype,
                    is_carrier=True,
                )
            )

    return CarrierProfile(
        sample_id=sample_id,
        total_variants_scanned=total_scanned,
        pathogenic_carrier_count=len(detected_variants),
        carrier_genes=sorted(list(carrier_genes_set)),
        variants=detected_variants,
    )
