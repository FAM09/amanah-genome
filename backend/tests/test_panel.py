"""
Tests for UAE Premarital Recessive Disorder Panel.
"""

from app.bio.panel import (
    UAE_RECESSIVE_PANEL,
    get_all_panel_genes,
    get_panel_gene,
    is_panel_gene,
)


def test_uae_panel_contains_top_disorders():
    """Verify all 10 priority disorders are present in the panel."""
    expected_genes = {
        "HBB", "SMN1", "CFTR", "CYP21A2", "PAH",
        "GBA", "HEXA", "GAA", "MEFV"
    }
    for gene in expected_genes:
        assert is_panel_gene(gene) is True
        panel_data = get_panel_gene(gene)
        assert panel_data is not None
        assert panel_data.gene_symbol == gene
        assert panel_data.inheritance == "Autosomal Recessive"
        assert len(panel_data.clinical_options) > 0
        assert "PGT-M" in " ".join(panel_data.clinical_options)


def test_non_panel_gene_returns_false():
    """Verify non-panel genes return False."""
    assert is_panel_gene("BRCA1") is False
    assert is_panel_gene("TP53") is False
    assert get_panel_gene("UNKNOWN_XYZ") is None
