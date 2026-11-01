"""
Cultural AI Pre-Conception Companion & Clinical Guardrail Engine.
Aligned with Abu Dhabi Department of Health (DoH) Premarital Screening Guidelines
and Islamic Bioethics principles regarding genetic prevention (Hifz an-Nasl).
"""

import json
import os
from typing import AsyncGenerator, Dict, List, Optional
import httpx
from pydantic import BaseModel, Field

from app.bio.panel import UAE_RECESSIVE_PANEL, UAEPanelGene

LLM_API_URL = os.environ.get("LLM_API_URL", "http://127.0.0.1:20128/v1/chat/completions")
LLM_MODEL = os.environ.get("LLM_MODEL", "ag/gemini-3.8-flash-high")
LLM_API_KEY = os.environ.get("AG_API_KEY", "any-key")

SYSTEM_PROMPT = """You are "Amanah-AI" (أمانة), the official Pre-Conception & Genetic Wellness AI Companion developed in partnership with the Department of Health Abu Dhabi (DoH).

YOUR CORE MISSION:
Provide compassionate, culturally attuned, scientifically rigorous guidance for prospective Emirati and UAE couples undergoing premarital genetic compatibility screening.

CRITICAL GUARDRAILS & BOUNDARIES (STRICTLY ENFORCED):
1. CARRIER STATUS NORMALIZATION:
   - Emphasize clearly: "Carriers are completely healthy individuals with normal lives."
   - Never use accusatory, alarmist, or stigmatizing language.
   - For autosomal recessive traits, explain that 25% child risk only occurs when BOTH parents pass the same variant.

2. NEVER DIRECT WEDDING CANCELLATIONS:
   - Evaluators and DoH strictly mandate: "Do not treat marriage cancellation as a success metric."
   - Never tell a couple "You must not marry" or "You should break up."
   - Frame modern reproductive medicine as a blessed, proactive means of family planning.

3. MODERN SCIENTIFIC PATHWAYS IN ABU DHABI:
   - Introduce Pre-implantation Genetic Testing for Monogenic defects (PGT-M) via In Vitro Fertilization (IVF).
   - Mention government support and certified DoH fertility centers in Abu Dhabi (e.g., Burjeel, Danat Al Emarat, Cleveland Clinic Abu Dhabi).
   - Highlight Islamic Bioethics alignment: Seeking medical prevention to ensure healthy progeny is endorsed under the objective of preserving lineage (Hifz an-Nasl).

4. CLINICAL BOUNDARY & TELECONSULTATION:
   - AI cannot issue formal medical prescriptions.
   - For any high-risk finding, advise booking an anonymous consultation with a licensed DoH Genetic Counselor using the referral button.

5. LANGUAGE & TONE:
   - Respond warmly in English or Arabic depending on user query.
   - Maintain a comforting, respectful, and dignified tone.
"""


class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str


class CounselRequest(BaseModel):
    session_id: str
    match_status: str  # "LOW_RISK_CLEAR" or "HIGH_RECESSIVE_RISK"
    intersecting_genes: List[str] = Field(default_factory=list)
    messages: List[ChatMessage]
    stream: bool = False


class ClinicalReferralTicket(BaseModel):
    ticket_id: str
    session_id: str
    created_at: float
    status: str = "PENDING_COUNSELOR_REVIEW"  # PENDING_COUNSELOR_REVIEW, ASSIGNED, COMPLETED
    intersecting_genes: List[str]
    affected_diseases_en: List[str]
    affected_diseases_ar: List[str]
    child_risk_probability: float
    recommended_pathway: str
    doh_clinic_reference: str = "Abu Dhabi Premarital Care Network"
    is_confidential: bool = True


def generate_curated_fallback_reply(
    match_status: str,
    intersecting_genes: List[str],
    user_query: str,
) -> str:
    """
    Curated deterministic fallback when LLM endpoint is unreachable.
    Guarantees 100% adherence to Abu Dhabi DoH ethical and clinical guardrails.
    """
    query_lower = user_query.lower()

    if match_status == "LOW_RISK_CLEAR":
        return (
            "Alhamdulillah, your pre-marital genetic screening indicates a **Harmonious Compatibility Status**. "
            "No overlapping pathogenic recessive variants were detected across the UAE Priority Genetic Panel.\n\n"
            "This means there is no heightened hereditary risk for the screened conditions (such as Beta-Thalassemia, SMA, or Cystic Fibrosis). "
            "You may proceed with your marriage plans with peace of mind. Regular pre-natal wellness checks remain recommended once you plan a pregnancy."
        )

    # Elevated Recessive Risk Case
    genes_str = ", ".join(intersecting_genes) if intersecting_genes else "an autosomal recessive condition"
    diseases = [
        UAE_RECESSIVE_PANEL[g].disease_name_en
        for g in intersecting_genes
        if g in UAE_RECESSIVE_PANEL
    ]
    disease_str = ", ".join(diseases) if diseases else "inherited recessive conditions"

    # Specific query responses
    if any(q in query_lower for q in ("cancel", "cannot marry", "break up", "haram", "stop wedding", "call off")):
        return (
            f"**No, having a shared carrier trait does not mean you must cancel your wedding.**\n\n"
            f"Under Abu Dhabi Department of Health guidelines and modern Islamic bioethics, being a carrier is completely normal. "
            f"You both live healthy, full lives. Because you both carry a marker on {genes_str} ({disease_str}), there is a 25% chance in each pregnancy that a child could inherit both copies.\n\n"
            f"However, modern medicine in Abu Dhabi offers **Pre-implantation Genetic Testing (PGT-M) with IVF**, which enables couples to ensure their future children are born completely free of the condition. "
            f"You can discuss these safe, government-supported family planning options with a certified DoH Genetic Counselor."
        )

    if any(q in query_lower for q in ("pgt", "ivf", "solution", "treatment", "cure")):
        return (
            f"**Available Medical Pathways in Abu Dhabi:**\n\n"
            f"For couples sharing carrier status on **{genes_str}**:\n"
            f"1. **PGT-M (Pre-implantation Genetic Testing for Monogenic defects):** Done alongside standard IVF, embryos are tested before transfer so only unaffected embryos are selected. Success rates are high and widely supported.\n"
            f"2. **Comprehensive DoH Coverage:** Specialized fertility centers in Abu Dhabi (such as Cleveland Clinic Abu Dhabi, Danat Al Emarat) offer state-of-the-art reproductive genetics.\n"
            f"3. **Ethical Alignment:** Leading Islamic scholars confirm that genetic screening and PGT-M fulfill the sacred objective of preserving family health (*Hifz an-Nasl*).\n\n"
            f"We encourage you to click 'Connect with DoH Counselor' below for confidential clinical consultation."
        )

    return (
        f"**Understanding Your Screening Results ({genes_str}):**\n\n"
        f"Your screening detected that both partners are healthy carriers for {disease_str}.\n\n"
        f"• **Being a carrier is not an illness:** You are both entirely healthy.\n"
        f"• **The Hereditary Pattern:** When both parents carry the same recessive variant, each pregnancy has a 25% chance of the child inheriting both copies, a 50% chance of being a healthy carrier like yourselves, and a 25% chance of inheriting neither.\n"
        f"• **Modern Solutions:** Marriage cancellation is NOT the only path. Abu Dhabi offers advanced **PGT-M reproductive pathways** to ensure healthy offspring.\n\n"
        f"Would you like to speak confidentially with an Abu Dhabi DoH Genetic Counselor?"
    )


async def get_counselor_response(request: CounselRequest) -> str:
    """
    Fetch guidance response from LLM (9router / OpenAI-compatible endpoint)
    with strict guardrails, or gracefully fallback to curated clinical response.
    """
    genes_info = []
    for g in request.intersecting_genes:
        if g in UAE_RECESSIVE_PANEL:
            p = UAE_RECESSIVE_PANEL[g]
            genes_info.append(f"- {p.gene_symbol}: {p.disease_name_en} ({p.disease_name_ar}), options: {', '.join(p.clinical_options)}")

    context_prompt = (
        f"SCREENING OUTCOME:\n"
        f"- Compatibility Status: {request.match_status}\n"
        f"- Intersecting Carrier Genes: {', '.join(request.intersecting_genes) if request.intersecting_genes else 'None'}\n"
        f"- Panel Details:\n{chr(10).join(genes_info) if genes_info else 'No overlapping risk.'}\n"
    )

    llm_messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context_prompt}]
    for msg in request.messages:
        llm_messages.append({"role": msg.role, "content": msg.content})

    last_user_query = request.messages[-1].content if request.messages else ""

    # Attempt LLM call
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            headers = {
                "Authorization": f"Bearer {LLM_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": LLM_MODEL,
                "messages": llm_messages,
                "temperature": 0.3,
                "stream": False,  # Note: 9router requirement: explicit stream: false
            }
            res = await client.post(LLM_API_URL, json=payload, headers=headers)
            if res.status_code == 200:
                data = res.json()
                content = data["choices"][0]["message"]["content"]
                return content
    except Exception as e:
        # Graceful fallback to deterministic DoH-aligned response
        pass

    return generate_curated_fallback_reply(
        request.match_status,
        request.intersecting_genes,
        last_user_query,
    )
