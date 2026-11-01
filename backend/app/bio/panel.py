"""
UAE Priority Premarital Screening Panel (Autosomal Recessive Disorders)
Curated in accordance with Abu Dhabi Department of Health (DoH) Premarital Screening Guidelines
and ClinVar Class 4/5 (Likely Pathogenic / Pathogenic) variants.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class PanelVariant(BaseModel):
    clinvar_id: str
    rs_id: str
    hgvs_c: str
    hgvs_p: Optional[str] = None
    chrom: str
    pos: int
    ref: str
    alt: str
    clnsig: str = "Pathogenic"


class UAEPanelGene(BaseModel):
    gene_symbol: str
    disease_name_en: str
    disease_name_ar: str
    inheritance: str = "Autosomal Recessive"
    chromosome: str
    omim_id: str
    prevalence_uae: str
    description_en: str
    description_ar: str
    known_pathogenic_variants: List[PanelVariant] = Field(default_factory=list)
    clinical_options: List[str] = Field(default_factory=list)


# Top 10 Priority Recessive Disorders in the UAE / GCC region
UAE_RECESSIVE_PANEL: Dict[str, UAEPanelGene] = {
    "HBB": UAEPanelGene(
        gene_symbol="HBB",
        disease_name_en="Beta-Thalassemia & Sickle Cell Disease",
        disease_name_ar="أنيميا البحر الأبيض المتوسط وفقر الدم المنجلي",
        chromosome="11",
        omim_id="613985",
        prevalence_uae="High (Carrier frequency ~8.5% in UAE population)",
        description_en="Severe inherited blood disorder impairing hemoglobin production, causing chronic anemia and organ damage.",
        description_ar="اضطراب وراثي حاد في الدم يقلل من إنتاج الهيموغلوبين ويسبب فقر دم مزمن وتلف الأعضاء.",
        clinical_options=[
            "Pre-implantation Genetic Testing for Monogenic defects (PGT-M) via IVF",
            "Prenatal diagnosis (CVS/Amniocentesis) in licensed DoH centers",
            "Lifelong transfusion & iron chelation therapy or curative stem cell transplantation"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000015467",
                rs_id="rs33971440",
                hgvs_c="c.92+1G>A",
                hgvs_p="p.?",
                chrom="chr11",
                pos=5226797,
                ref="G",
                alt="A",
                clnsig="Pathogenic"
            ),
            PanelVariant(
                clinvar_id="VCV000015124",
                rs_id="rs334",
                hgvs_c="c.20A>T",
                hgvs_p="p.Glu7Val",
                chrom="chr11",
                pos=5227002,
                ref="T",
                alt="A",
                clnsig="Pathogenic"
            ),
            PanelVariant(
                clinvar_id="VCV000015469",
                rs_id="rs34598529",
                hgvs_c="c.92+5G>C",
                hgvs_p="p.?",
                chrom="chr11",
                pos=5226793,
                ref="G",
                alt="C",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "SMN1": UAEPanelGene(
        gene_symbol="SMN1",
        disease_name_en="Spinal Muscular Atrophy (SMA)",
        disease_name_ar="ضمور العضلات الشوكي",
        chromosome="5",
        omim_id="253300",
        prevalence_uae="High (~1 in 40 carrier frequency in GCC)",
        description_en="Progressive motor neuron loss leading to severe muscle weakness and respiratory compromise.",
        description_ar="فقدان تدريجي للخلايا العصبية الحركية يؤدي إلى ضعف شديد في العضلات وصعوبة في التنفس.",
        clinical_options=[
            "PGT-M embryo selection during IVF (DoH sponsored programs)",
            "Early post-natal gene therapy (e.g., Onasemnogene abeparvovec / Zolgensma)",
            "Nusinersen (Spinraza) / Risdiplam medical management"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000021650",
                rs_id="rs386834235",
                hgvs_c="c.840C>T",
                hgvs_p="p.=",
                chrom="chr5",
                pos=70925500,
                ref="C",
                alt="T",
                clnsig="Pathogenic"
            ),
            PanelVariant(
                clinvar_id="VCV000976451",
                rs_id="rs1555589139",
                hgvs_c="c.835-44_835-43del",
                hgvs_p="p.?",
                chrom="chr5",
                pos=70925450,
                ref="AG",
                alt="A",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "CFTR": UAEPanelGene(
        gene_symbol="CFTR",
        disease_name_en="Cystic Fibrosis",
        disease_name_ar="التليف الكيسي",
        chromosome="7",
        omim_id="219700",
        prevalence_uae="Moderate (~1 in 50 carrier frequency)",
        description_en="Multi-system disorder causing thick mucus buildup in lungs, digestive system, and chronic infections.",
        description_ar="اضطراب يصيب عدة أجهزة في الجسم ويؤدي إلى تراكم مخاط سميك في الرئتين والجهاز الهضمي.",
        clinical_options=[
            "PGT-M pre-implantation genetic screening",
            "CFTR potentiator/corrector targeted therapies (e.g. Trikafta)",
            "Specialized pediatric pulmonology care pathways in Abu Dhabi"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000007105",
                rs_id="rs113993960",
                hgvs_c="c.1521_1523delCTT",
                hgvs_p="p.Phe508del",
                chrom="chr7",
                pos=117559590,
                ref="ATCT",
                alt="A",
                clnsig="Pathogenic"
            ),
            PanelVariant(
                clinvar_id="VCV000053994",
                rs_id="rs78655421",
                hgvs_c="c.1652G>A",
                hgvs_p="p.Gly551Asp",
                chrom="chr7",
                pos=117560100,
                ref="G",
                alt="A",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "CYP21A2": UAEPanelGene(
        gene_symbol="CYP21A2",
        disease_name_en="Congenital Adrenal Hyperplasia (CAH)",
        disease_name_ar="تضخم الغدة الكظرية الخلقي",
        chromosome="6",
        omim_id="201910",
        prevalence_uae="High (~1 in 4,000 live births in consanguineous unions)",
        description_en="Deficiency in 21-hydroxylase leading to adrenal crisis, salt-wasting, and ambiguous genitalia.",
        description_ar="نقص إنزيم 21-هيدروكسيلاز مما يؤدي إلى اختلال الهرمونات وفقدان الأملاح الحاد.",
        clinical_options=[
            "PGT-M IVF pathway",
            "Prenatal maternal dexamethasone under clinical trial supervision",
            "Lifelong hormone replacement therapy (hydrocortisone + fludrocortisone)"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000012130",
                rs_id="rs6467",
                hgvs_c="c.293-13C>G",
                hgvs_p="p.?",
                chrom="chr6",
                pos=32040000,
                ref="C",
                alt="G",
                clnsig="Pathogenic"
            ),
            PanelVariant(
                clinvar_id="VCV000012135",
                rs_id="rs6474",
                hgvs_c="c.518T>A",
                hgvs_p="p.Ile173Asn",
                chrom="chr6",
                pos=32040200,
                ref="T",
                alt="A",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "PAH": UAEPanelGene(
        gene_symbol="PAH",
        disease_name_en="Phenylketonuria (PKU)",
        disease_name_ar="بيلة الفينيل كيتون",
        chromosome="12",
        omim_id="261600",
        prevalence_uae="Moderate (~1 in 10,000 live births)",
        description_en="Inability to break down phenylalanine, causing severe intellectual disability without strict dietary control.",
        description_ar="عدم القدرة على تكسير الأحماض الأمينية مما يسبب تراكم الفينيل ألانين وتلف عصبي دون حمية صارمة.",
        clinical_options=[
            "PGT-M embryo selection",
            "Strict lifelong low-phenylalanine medical nutrition",
            "Sapropterin dihydrochloride (Kuvan) or Pegvaliase enzyme substitution"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000000570",
                rs_id="rs5030858",
                hgvs_c="c.1222C>T",
                hgvs_p="p.Arg408Trp",
                chrom="chr12",
                pos=102844400,
                ref="C",
                alt="T",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "GBA": UAEPanelGene(
        gene_symbol="GBA",
        disease_name_en="Gaucher Disease",
        disease_name_ar="مرض غوشيه",
        chromosome="1",
        omim_id="230800",
        prevalence_uae="Moderate",
        description_en="Glucocerebrosidase deficiency causing lipid accumulation in spleen, liver, bone marrow, and severe bone crises.",
        description_ar="نقص إنزيم الجلوكوسيريبروسيداز يؤدي لتراكم الدهون بالطحال والكبد ونخاع العظم.",
        clinical_options=[
            "PGT-M premarital intervention",
            "Regular intravenous enzyme replacement therapy (ERT - Imiglucerase)",
            "Substrate reduction therapy (SRT)"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000004289",
                rs_id="rs76763715",
                hgvs_c="c.1226A>G",
                hgvs_p="p.Asn409Ser",
                chrom="chr1",
                pos=155235843,
                ref="A",
                alt="G",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "HEXA": UAEPanelGene(
        gene_symbol="HEXA",
        disease_name_en="Tay-Sachs Disease",
        disease_name_ar="مرض تاي ساكس",
        chromosome="15",
        omim_id="272800",
        prevalence_uae="Present across regional consanguineous clusters",
        description_en="Fatal neurodegenerative disorder causing progressive destruction of nerve cells in the brain and spinal cord.",
        description_ar="مرض تنكس عصبي مميت يسبب تدميراً تدريجياً للخلايا العصبية في الدماغ والحبل الشوكي.",
        clinical_options=[
            "PGT-M pre-implantation genetic screening (highest clinical priority)",
            "Comprehensive palliative and neurological support"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000012211",
                rs_id="rs121907974",
                hgvs_c="c.1278insTATC",
                hgvs_p="p.Tyr427fs",
                chrom="chr15",
                pos=72346280,
                ref="T",
                alt="TTATC",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "GAA": UAEPanelGene(
        gene_symbol="GAA",
        disease_name_en="Pompe Disease (Glycogen Storage Disease Type II)",
        disease_name_ar="مرض بومبي",
        chromosome="17",
        omim_id="232300",
        prevalence_uae="Moderate in GCC region",
        description_en="Acid alpha-glucosidase deficiency leading to cardiac hypertrophy and progressive skeletal muscle weakness.",
        description_ar="نقص إنزيم ألفا جلوكوسيداز الحمضي مما يؤدي إلى تضخم القلب وضعف تدريجي بالعضلات.",
        clinical_options=[
            "PGT-M reproductive care pathway",
            "Enzyme replacement therapy (Alglucosidase alfa / Nexviazyme)",
            "Multidisciplinary cardiopulmonary monitoring"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000004028",
                rs_id="rs386834236",
                hgvs_c="c.-32-13T>G",
                hgvs_p="p.?",
                chrom="chr17",
                pos=80106970,
                ref="T",
                alt="G",
                clnsig="Pathogenic"
            ),
        ]
    ),
    "MEFV": UAEPanelGene(
        gene_symbol="MEFV",
        disease_name_en="Familial Mediterranean Fever (FMF)",
        disease_name_ar="حمى البحر الأبيض المتوسط العائلية",
        chromosome="16",
        omim_id="249100",
        prevalence_uae="High regional carrier prevalence (up to 1 in 15 in Arab populations)",
        description_en="Recurrent autoinflammatory fevers, painful serositis, and long-term risk of systemic amyloidosis.",
        description_ar="نوبات متكررة من الحمى والتهاب الأغشية المصلية وخطر الداء النشواني الكلوي على المدى الطويل.",
        clinical_options=[
            "PGT-M pre-implantation counseling",
            "Daily Colchicine prophylaxis to prevent amyloidosis and attacks",
            "Biologic therapies (IL-1 inhibitors such as Anakinra / Canakinumab)"
        ],
        known_pathogenic_variants=[
            PanelVariant(
                clinvar_id="VCV000002538",
                rs_id="rs28940578",
                hgvs_c="c.2080A>G",
                hgvs_p="p.Met694Val",
                chrom="chr16",
                pos=3243950,
                ref="A",
                alt="G",
                clnsig="Pathogenic"
            ),
            PanelVariant(
                clinvar_id="VCV000002537",
                rs_id="rs28940579",
                hgvs_c="c.2082G>A",
                hgvs_p="p.Met694Ile",
                chrom="chr16",
                pos=3243952,
                ref="G",
                alt="A",
                clnsig="Pathogenic"
            ),
        ]
    ),
}


def get_panel_gene(gene_symbol: str) -> Optional[UAEPanelGene]:
    """Retrieve panel information for a specific gene symbol."""
    return UAE_RECESSIVE_PANEL.get(gene_symbol.upper())


def is_panel_gene(gene_symbol: str) -> bool:
    """Check if gene is part of the UAE premarital screening panel."""
    return gene_symbol.upper() in UAE_RECESSIVE_PANEL


def get_all_panel_genes() -> List[UAEPanelGene]:
    """Return all panel definitions."""
    return list(UAE_RECESSIVE_PANEL.values())
