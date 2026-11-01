export interface PanelVariant {
  clinvar_id: string;
  rs_id: string;
  hgvs_c: string;
  hgvs_p?: string;
  chrom: string;
  pos: number;
  ref: string;
  alt: string;
  clnsig: string;
}

export interface UAEPanelGene {
  gene_symbol: string;
  disease_name_en: string;
  disease_name_ar: string;
  inheritance: string;
  chromosome: string;
  omim_id: string;
  prevalence_uae: string;
  description_en: string;
  description_ar: string;
  known_pathogenic_variants: PanelVariant[];
  clinical_options: string[];
}

export interface SessionInitResponse {
  session_id: string;
  session_code: string;
  created_at: number;
  session_salt_hint: string;
}

export interface UploadReceipt {
  session_id: string;
  party: 'A' | 'B';
  sample_id: string;
  variants_scanned: number;
  pathogenic_carrier_count: number;
  commitment_hash: string;
  is_ready_for_match: boolean;
}

export interface IntersectionMatchResult {
  is_compatible: boolean;
  risk_level: 'LOW_RISK_CLEAR' | 'HIGH_RECESSIVE_RISK';
  child_risk_probability: number;
  intersecting_genes: string[];
  intersecting_gene_details: UAEPanelGene[];
  party_a_total_carrier_genes: number;
  party_b_total_carrier_genes: number;
  zk_proof_token: string;
  audit_hash: string;
  privacy_guarantee: string;
}

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ClinicalReferralTicket {
  ticket_id: string;
  session_id: string;
  created_at: number;
  status: string;
  intersecting_genes: string[];
  affected_diseases_en: string[];
  affected_diseases_ar: string[];
  child_risk_probability: number;
  recommended_pathway: string;
  doh_clinic_reference: string;
  is_confidential: boolean;
}
