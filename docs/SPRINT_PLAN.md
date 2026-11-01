# 20-Day Sprint Plan — Amanah-Genome

**Milestone Target:** Working Prototype + Video Demo ready before **20 November 2026**.  
**Execution Standard:** Phased delivery with automated tests and verification after each phase ("kerjakan per fase lalu testing").

---

## Phase 1: Bio-Crypto Matching Engine & Synthetic VCF Generator (Days 1–4)
- [x] **Task 1.1:** Setup Python virtual environment (`backend/.venv`) with FastAPI, pydantic, pycryptodome / hashlib.
- [x] **Task 1.2:** Build synthetic VCF generator (`generate_mock_vcf.py`) to produce 4 distinct benchmark scenarios:
  - Scenario 1: Fully compatible (No carrier overlap).
  - Scenario 2: High-Risk Match (Both carry Beta-Thalassemia / `HBB`).
  - Scenario 3: High-Risk Match (Both carry Spinal Muscular Atrophy / `SMN1`).
  - Scenario 4: Asymmetric carrier (Ahmad carries `CFTR`, Fatima carries `HBB` — No overlap).
- [x] **Task 1.3:** Implement VCF Parser & ClinVar Recessive Panel filter for top 10 UAE disorders.
- [x] **Task 1.4:** Implement Private Set Intersection (PSI) crypto engine with session salt.
- [x] **Task 1.5:** Write pytest test suite verifying 100% accuracy and zero leakage of non-overlapping variants.

---

## Phase 2: Cultural AI Companion & Backend API (Days 5–8)
- [x] **Task 2.1:** Implement FastAPI REST endpoints:
  - `POST /api/session/init`
  - `POST /api/session/{session_id}/upload`
  - `POST /api/session/{session_id}/evaluate`
  - `POST /api/session/{session_id}/counsel` (LLM companion with guardrails & fallback)
  - `POST /api/session/{session_id}/referral`
- [x] **Task 2.2:** Craft Cultural & Clinical System Prompts with strict Abu Dhabi DoH guidelines (Arabic + English).
- [x] **Task 2.3:** Add guardrail unit tests (ensuring LLM never reveals individual carrier attribution and never orders wedding cancellations).

---

## Phase 3: Interactive Frontend (React + Vite + Tailwind) (Days 9–13)
- [x] **Task 3.1:** Scaffold React + Vite app with Tailwind CSS and Lucide icons.
- [x] **Task 3.2:** Build **Couple Portal**:
  - Dual drag-and-drop VCF upload zone.
  - Interactive "Zero-Knowledge Cryptographic Hashing" visual animation.
  - Compatibility status card (Clear vs Elevated Risk).
  - Interactive AI Counselor chat interface.
  - "Book DoH Genetic Counselor" modal with clinical brief preview.
- [x] **Task 3.3:** Build **Counselor Portal**:
  - Live triage queue showing incoming risk tickets.
  - Sanitized clinical brief viewer (Affected gene, ClinVar ref, PGT-M pathway recommendation).
  - Teleconsultation intake handler.
- [x] **Task 3.4:** Polish UI styling with an Abu Dhabi Health institutional theme (emerald green, pearl white, clean modern typography).

---

## Phase 4: System Integration & End-to-End Testing (Days 14–16)
- [x] **Task 4.1:** End-to-end integration between Frontend and Backend (serving built dist at `/app`).
- [x] **Task 4.2:** Run full user journey tests across all 4 mock scenarios.
- [x] **Task 4.3:** Verify performance (matching evaluation latency 0.09ms < 200ms, VCF parse 0.05ms < 100ms).
- [x] **Task 4.4:** Containerize with Docker / docker-compose for easy local reproduction.

---

## Phase 5: Submission Deliverables (Days 17–20)
- [x] **Task 5.1:** Produce 3-Minute Demonstration Video Script & Storyboard (`docs/DEMO_VIDEO_SCRIPT.md`).
- [x] **Task 5.2:** Finalize Technical Architecture & Responsible AI Governance Document (`docs/TECHNICAL_ARCHITECTURE_AND_RESPONSIBLE_AI_GOVERNANCE.md`).
- [x] **Task 5.3:** Ready for prototype evaluation and Hack2skill platform submission.
