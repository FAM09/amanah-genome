export interface MockScenario {
  id: string;
  title: string;
  badge: string;
  badgeColor: string;
  description: string;
  ahmadLabel: string;
  fatimaLabel: string;
  ahmadVcf: string;
  fatimaVcf: string;
}

const BASE_HEADER = `##fileformat=VCFv4.2
##source=AmanahGenomeSyntheticGeneratorV1
##reference=GRCh38
##INFO=<ID=GENE,Number=1,Type=String,Description="HGNC Gene Symbol">
##INFO=<ID=CLNSIG,Number=1,Type=String,Description="ClinVar Clinical Significance">
##INFO=<ID=CLNDN,Number=1,Type=String,Description="ClinVar Disease Name">
##INFO=<ID=RS,Number=1,Type=String,Description="dbSNP ID">
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE
chr1\t1010020\trs1800001\tA\tG\t99\tPASS\tGENE=MTHFR;CLNSIG=Benign;CLNDN=Common_variant\tGT\t0/1
chr2\t2341050\trs2234002\tC\tT\t99\tPASS\tGENE=ABCA1;CLNSIG=Benign;CLNDN=Benign_polymorphism\tGT\t0/0
`;

const HBB_ROW = `chr11\t5226797\trs33971440\tG\tA\t99\tPASS\tGENE=HBB;CLNSIG=Pathogenic;CLNDN=Beta-Thalassemia;RS=rs33971440\tGT\t0/1\n`;
const SMN1_ROW = `chr5\t70925500\trs386834235\tC\tT\t99\tPASS\tGENE=SMN1;CLNSIG=Pathogenic;CLNDN=Spinal_Muscular_Atrophy;RS=rs386834235\tGT\t0/1\n`;
const CFTR_ROW = `chr7\t117559590\trs113993960\tATCT\tA\t99\tPASS\tGENE=CFTR;CLNSIG=Pathogenic;CLNDN=Cystic_Fibrosis;RS=rs113993960\tGT\t0/1\n`;

export const MOCK_SCENARIOS: MockScenario[] = [
  {
    id: 'case_01',
    title: 'Scenario 1: Harmonious & Compatible',
    badge: '100% Compatible',
    badgeColor: 'bg-emerald-900/60 text-emerald-300 border-emerald-700/50',
    description: 'Ahmad & Fatima carry only benign population polymorphisms. No carrier overlap.',
    ahmadLabel: 'Ahmad (Clear - No pathogenic variants)',
    fatimaLabel: 'Fatima (Clear - No pathogenic variants)',
    ahmadVcf: BASE_HEADER,
    fatimaVcf: BASE_HEADER,
  },
  {
    id: 'case_02',
    title: 'Scenario 2: High Risk Beta-Thalassemia',
    badge: '25% Child Risk (HBB)',
    badgeColor: 'bg-rose-900/60 text-rose-300 border-rose-700/50',
    description: 'Both Ahmad & Fatima carry the pathogenic HBB mutation (c.92+1G>A). Requires PGT-M guidance.',
    ahmadLabel: 'Ahmad (Carrier HBB:c.92+1G>A)',
    fatimaLabel: 'Fatima (Carrier HBB:c.92+1G>A)',
    ahmadVcf: BASE_HEADER + HBB_ROW,
    fatimaVcf: BASE_HEADER + HBB_ROW,
  },
  {
    id: 'case_03',
    title: 'Scenario 3: High Risk Spinal Muscular Atrophy',
    badge: '25% Child Risk (SMN1)',
    badgeColor: 'bg-amber-900/60 text-amber-300 border-amber-700/50',
    description: 'Both Ahmad & Fatima carry pathogenic SMN1 (c.840C>T). Requires gene therapy & PGT-M pathway.',
    ahmadLabel: 'Ahmad (Carrier SMN1:c.840C>T)',
    fatimaLabel: 'Fatima (Carrier SMN1:c.840C>T)',
    ahmadVcf: BASE_HEADER + SMN1_ROW,
    fatimaVcf: BASE_HEADER + SMN1_ROW,
  },
  {
    id: 'case_04',
    title: 'Scenario 4: Asymmetric Carrier (Zero-Knowledge)',
    badge: 'Safe & Compatible (0% Risk)',
    badgeColor: 'bg-blue-900/60 text-blue-300 border-blue-700/50',
    description: 'Ahmad carries CFTR, Fatima carries HBB. Autosomal recessive condition requires both; marriage is safe. Zero leakage of non-overlapping variants.',
    ahmadLabel: 'Ahmad (Carrier CFTR - Cystic Fibrosis)',
    fatimaLabel: 'Fatima (Carrier HBB - Thalassemia)',
    ahmadVcf: BASE_HEADER + CFTR_ROW,
    fatimaVcf: BASE_HEADER + HBB_ROW,
  },
];
