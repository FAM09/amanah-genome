# Product Requirements Document (PRD) — Amanah-Genome

## 1. Executive Summary
- **Product Name:** Amanah-Genome (أمانة للجينوم)
- **Problem Statement:** Challenge 03 — *Understanding and Reducing Inherited Disease Risk* (Future Health Digital Innovation Challenge, Abu Dhabi).
- **Stakeholders:** Department of Health Abu Dhabi (DoH), Inception (G42), MBZUAI, Microsoft.
- **Mission:** Eliminate the fear, stigma, and delay in pre-marital genetic screening through a privacy-preserving cryptographic match engine and an empathetic, culturally attuned AI counselor that guides at-risk couples to dignified, modern reproductive care (PGT-M/IVF).

---

## 2. Background & The Abu Dhabi Context
- Consanguinity (inter-family marriage) is prevalent in the UAE and Gulf region (30%–50%).
- It carries heightened risks of autosomal recessive disorders (Beta-Thalassemia, Sickle Cell Disease, Cystic Fibrosis, Spinal Muscular Atrophy / SMA).
- **The Core Dilemma:**
  - Traditional hospital pre-marital screening happens downstream (weeks before the wedding).
  - A positive carrier match at that stage creates acute social stigma, family dishonor, and emotional trauma.
  - Furthermore, patients fear that their genetic carrier status will be exposed to extended family members or leaked across clan networks.
- **The Challenge Rule:**
  - Evaluators explicitly stipulate: *"without treating cancelled marriages or any single personal choice as the sole success measure"*. The solution must support informed choice and provide safe pathways to modern healthcare.

---

## 3. Product Pillars & Functional Requirements

### Pillar 1: Bio-Crypto Matching Engine (Deterministic, Zero Halucination)
- **Input:** Standard `.vcf` (Variant Call Format v4.2) files representing patient genomic profiles.
- **Target Disease Panel (UAE Priority Recessive Panel):**
  1. Beta-Thalassemia (`HBB`)
  2. Sickle Cell Disease (`HBB`)
  3. Spinal Muscular Atrophy (`SMN1`)
  4. Cystic Fibrosis (`CFTR`)
  5. Congenital Adrenal Hyperplasia (`CYP21A2`)
  6. Phenylketonuria (`PAH`)
  7. Gaucher Disease (`GBA`)
  8. Tay-Sachs Disease (`HEXA`)
  9. Pompe Disease (`GAA`)
  10. Familial Mediterranean Fever (`MEFV`)
- **Privacy Layer (Private Set Intersection / ZKP Simulation):**
  - DNA files are parsed locally on-device / transient memory.
  - Raw DNA sequences are NEVER stored or transmitted across parties.
  - The engine extracts only pathogenic recessive alleles (Class 4/5 ClinVar), salts and hashes them (`SHA256(locus_id + gene_id + salt)`), and performs a Private Set Intersection (PSI).
  - **Output:** Biner & non-accusatory:
    - *Status A (Harmonious/Clear):* No shared recessive pathogenic variants detected.
    - *Status B (High Recessive Risk Match):* Both individuals carry pathogenic mutations on the same recessive gene ($25\%$ child risk per pregnancy). Neither individual is singled out as the "faulty party".

### Pillar 2: Cultural AI Pre-Conception Companion (Agentic AI)
- **Role:** Plain-language education, psychological comfort, and culturally aligned navigation.
- **Language Support:** English & Arabic (with Gulf/Emirati nuances).
- **Strict Guardrails (Responsible AI & Clinical Boundary):**
  - AI CANNOT diagnose or recommend abortion/cancellation of marriage.
  - AI MUST normalize carrier status (carrier $\neq$ sick; carriers are completely healthy individuals).
  - AI MUST introduce evidence-based, religiously approved solutions available in Abu Dhabi:
    - **PGT-M (Pre-implantation Genetic Testing for Monogenic defects):** Embryo selection during IVF to guarantee healthy offspring.
    - Government funding & support pathways under the Abu Dhabi healthcare system.
- **Source of Truth:** Abu Dhabi Department of Health Premarital Screening Guidelines and Islamic Bioethics rulings on genetic testing.

### Pillar 3: Closed-Loop Counselor Bridge (Human-in-the-Loop)
- If an elevated risk match occurs:
  - The AI locks diagnostic boundaries and presents an action card: *"Connect with a Certified DoH Genetic Counselor"*.
  - Generates a sanitized, encrypted **Clinical Summary Brief** (containing only the affected Gene ID and ClinVar variant ID, without revealing non-consented personal or genomic data).
  - Direct ticket dispatch to the Counselor Portal for an anonymous teleconsultation booking.

---

## 4. User Personas & Flows

### Persona 1: Prospective Couple (Ahmad & Fatima)
1. Ahmad uploads his genomic file (`ahmad_sample.vcf`) into his private portal.
2. Fatima uploads her genomic file (`fatima_sample.vcf`) into her private portal.
3. Both authorize the cryptographic pairing session via a 6-digit session key.
4. The system executes the zero-knowledge intersection in <3 seconds.
5. The couple receives the unified compatibility status.
6. If at-risk, the AI companion greets them with compassionate, culturally sensitive explanation and offers a 1-click booking with a DoH counselor.

### Persona 2: DoH Genetic Counselor (Dr. Mariam)
1. Logs into the Counselor Dashboard.
2. Reviews incoming triage referrals with pre-compiled Clinical Briefs.
3. Initiates a secure, confidential teleconsultation session with the couple.
4. Documents confirmed clinical pathways (e.g., referral to Abu Dhabi IVF/PGT-M Center).

---

## 5. Success Metrics for Hackathon Evaluation
- **Health Impact:** Demonstrates clear prevention pathway for UAE high-prevalence recessive diseases.
- **Privacy & Security:** Zero genomic data retention, verifiable cryptographic matching.
- **Responsible AI:** Zero hallucinations, clear screening vs. diagnosis boundaries, culturally validated tone.
- **Demonstration Experience:** High visual polish, intuitive 3-minute evaluator journey.
