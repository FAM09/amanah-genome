# Amanah-Genome (أمانة للجينوم)
**Zero-Knowledge Pre-Marital Genetic Compatibility & Cultural Care Bridge**

Target Competition: **Future Health Digital Innovation Challenge 2026 (Abu Dhabi - GITEX 2026)**  
Co-creators: **Department of Health Abu Dhabi, Inception (G42), MBZUAI, Microsoft**  
Focus Area: **Focus Area 01 — Fertility**  
Challenge Statement: **[03] Understanding and Reducing Inherited Disease Risk**  
Deadline Prototype: **20 November 2026** (Awards: 7–11 December 2026 at GITEX, Total: USD 105,000)

---

## 1. Project Directory Structure
```
/home/fam/amanah-genome/
├── docs/
│   ├── PRD.md               # Detailed Product Requirements & Domain Specs
│   ├── ARCHITECTURE.md      # Bio-crypto engine & LLM guardrails
│   └── SPRINT_PLAN.md       # Phased 20-day sprint checklist
├── backend/                 # FastAPI, Python 3.11, bio-crypto engine, RAG agent
│   ├── app/
│   │   ├── core/            # Cryptographic PSI (Private Set Intersection) & hashing
│   │   ├── bio/             # VCF v4.2 synthetic parser & ClinVar pathogen panel
│   │   ├── ai/              # Cultural AI Companion (LangChain/LiteLLM + Guardrails)
│   │   └── api/             # REST endpoints (/upload, /match, /chat, /referral)
│   ├── tests/               # Test suites for deterministic zero-knowledge matching
│   └── requirements.txt
├── frontend/                # React + Vite + Tailwind CSS + Lucide icons
│   ├── src/
│   │   ├── components/      # UI components (File upload, ZK animation, Care portal)
│   │   ├── pages/           # Couple Portal, Counselor Portal, Audit log
│   └── package.json
└── mock-data/               # Realistic synthetic VCF files for UAE carrier panels
    ├── case_01_compatible/
    ├── case_02_thalassemia_carrier_both/
    ├── case_03_sickle_cell_carrier_both/
    └── case_04_sma_carrier_both/
```

---

## 2. Quick Execution Guide for Developer Profile (@billgates1520_bot)
Read the full specs in:
1. `docs/PRD.md`
2. `docs/ARCHITECTURE.md`
3. `docs/SPRINT_PLAN.md`

Start with **Phase 1: Bio-Crypto Matching Engine & Synthetic VCF Generator** (`docs/SPRINT_PLAN.md`).
