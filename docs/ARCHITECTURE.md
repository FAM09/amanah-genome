# Technical Architecture — Amanah-Genome

## 1. System High-Level Topology

```
+---------------------------------------------------------------------------------+
|                                 FRONTEND (SPA)                                  |
|   React 18 + Vite + Tailwind CSS + Lucide Icons + Framer Motion                 |
|                                                                                 |
|   [ Couple Portal: Dual-Upload | ZK-Animation | AI Chat | Counselor Booking ]   |
|   [ Counselor Portal: Triage Queue | Clinical Brief Viewer | Disposition ]      |
+----------------------------------------+----------------------------------------+
                                         | HTTPS / WebSocket (JSON)
                                         v
+---------------------------------------------------------------------------------+
|                            BACKEND (FastAPI / Python 3.11)                      |
|                                                                                 |
|  [ API Router ]                                                                 |
|    - POST /api/session/create -> generates paired session code                 |
|    - POST /api/vcf/upload     -> parses & hashes VCF client-side/transient     |
|    - POST /api/match/evaluate -> executes Private Set Intersection (PSI)       |
|    - POST /api/ai/counsel     -> streaming LLM companion with guardrails        |
|    - POST /api/triage/refer   -> creates encrypted clinical ticket for DoH      |
|                                                                                 |
|  [ Core Bio-Crypto Engine ]                                                     |
|    - VCF Parser: Extracts ClinVar Class 4/5 (Likely Pathogenic / Pathogenic)    |
|    - Gene Normalizer: Maps variants to HGNC canonical genes (e.g., HBB, SMN1)   |
|    - PSI / ZKP Module: Salting & Hashing: H(gene_id + variant_key)             |
|                                                                                 |
|  [ Responsible AI & Guardrail Layer ]                                           |
|    - LLM: OpenAI / Claude / Local 9Router (ag/gemini-3.8-flash-high)            |
|    - System Prompt: Cultural & Clinical Safety Rules (Abu Dhabi DoH Protocol)   |
|    - Safety Boundary: Strict refusal on diagnosis/abortion advice               |
+---------------------------------------------------------------------------------+
```

---

## 2. Bio-Crypto Logic: Private Set Intersection (PSI)

### Variant Call Format (VCF) Parsing:
- Standard VCF fields: `#CHROM`, `POS`, `ID`, `REF`, `ALT`, `INFO`.
- `INFO` annotation contains ClinVar clinical significance (e.g., `CLNSIG=Pathogenic`).

### Algorithmic Flow:
1. Patient A uploads `A.vcf` $\rightarrow$ engine extracts set of pathogenic recessive carrier genes: $S_A = \{ \text{HBB}, \text{CFTR} \}$.
2. Patient B uploads `B.vcf` $\rightarrow$ engine extracts set of pathogenic recessive carrier genes: $S_B = \{ \text{HBB}, \text{PAH} \}$.
3. Hashing with session salt $K$:
   $$\text{HashSet}_A = \{ \text{HMAC}_K(g) \mid g \in S_A \}$$
   $$\text{HashSet}_B = \{ \text{HMAC}_K(g) \mid g \in S_B \}$$
4. Intersection:
   $$R = \text{HashSet}_A \cap \text{HashSet}_B$$
5. If $|R| == 0$: Both individuals are clear of matching recessive conditions.
6. If $|R| > 0$: Both individuals carry mutations on the same recessive gene (e.g., $HBB$).
   - The match triggers a high-recessive risk notice ($25\%$ inheritance probability).
   - Crucially: **Neither partner knows which other non-matching carriers the other holds**. (e.g., Ahmad never knows Fatima carries `PAH`, and Fatima never knows Ahmad carries `CFTR`).

---

## 3. Cultural AI Guardrail Protocol

### System Prompt Directive:
- **Tone:** Empathetic, culturally respectful, non-alarmist, scientifically rigorous.
- **Key Concepts to Reinforce:**
  1. *Carrier is healthy:* Carrying one recessive gene does not cause illness.
  2. *Destiny & Science Harmonized:* Seeking medical solutions (such as PGT-M / IVF) is an approved and proactive way to protect family lineage.
  3. *Zero Judgment:* Never tell the couple they "should not marry". Explain the clinical options supported by the Abu Dhabi government.
- **Hard Boundaries:**
  - If asked *"Who gave this to me?"* $\rightarrow$ Explain that human genetics is shared across generations and the system protects individual privacy by design.
  - If asked for medical prescriptions $\rightarrow$ Defer to DoH counselor immediately.
