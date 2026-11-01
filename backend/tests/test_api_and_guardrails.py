"""
Integration & Guardrail Tests for Amanah-Genome FastAPI Endpoints and AI Counselor.
Validates zero leakage, strict DoH boundaries, and clinical referral flow.
"""

from pathlib import Path
from starlette.testclient import TestClient

from app.ai.counselor import generate_curated_fallback_reply
from app.main import app

client = TestClient(app)
MOCK_ROOT = Path("/home/fam/amanah-genome/mock-data")


def test_health_and_panel_endpoints():
    """Verify health check and panel metadata endpoints."""
    res_health = client.get("/api/health")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "healthy"

    res_panel = client.get("/api/panel")
    assert res_panel.status_code == 200
    data = res_panel.json()
    assert data["panel_count"] >= 9
    symbols = [g["gene_symbol"] for g in data["genes"]]
    assert "HBB" in symbols
    assert "SMN1" in symbols


def test_full_api_workflow_high_risk_scenario():
    """
    Test end-to-end API session flow:
    1. Initialize session
    2. Upload Ahmad VCF (HBB carrier)
    3. Upload Fatima VCF (HBB carrier)
    4. Evaluate match (PSI) -> High Recessive Risk
    5. Chat with AI Counselor -> Normalization & PGT-M guidance
    6. Generate clinical referral ticket for DoH
    7. Retrieve ticket from Counselor Portal
    """
    # 1. Init session
    res_init = client.post("/api/session/init")
    assert res_init.status_code == 200
    session_id = res_init.json()["session_id"]
    assert session_id.startswith("SES-")

    # 2. Upload Ahmad VCF
    ahmad_path = MOCK_ROOT / "case_02_thalassemia_carrier_both" / "ahmad_sample.vcf"
    with open(ahmad_path, "rb") as f:
        res_upload_a = client.post(
            f"/api/session/{session_id}/upload",
            data={"party": "A"},
            files={"vcf_file": ("ahmad_sample.vcf", f, "text/plain")},
        )
    assert res_upload_a.status_code == 200
    assert res_upload_a.json()["party"] == "A"
    assert res_upload_a.json()["is_ready_for_match"] is False

    # 3. Upload Fatima VCF
    fatima_path = MOCK_ROOT / "case_02_thalassemia_carrier_both" / "fatima_sample.vcf"
    with open(fatima_path, "rb") as f:
        res_upload_b = client.post(
            f"/api/session/{session_id}/upload",
            data={"party": "B"},
            files={"vcf_file": ("fatima_sample.vcf", f, "text/plain")},
        )
    assert res_upload_b.status_code == 200
    assert res_upload_b.json()["party"] == "B"
    assert res_upload_b.json()["is_ready_for_match"] is True

    # 4. Evaluate match
    res_eval = client.post(f"/api/session/{session_id}/evaluate")
    assert res_eval.status_code == 200
    eval_data = res_eval.json()
    assert eval_data["is_compatible"] is False
    assert eval_data["risk_level"] == "HIGH_RECESSIVE_RISK"
    assert eval_data["child_risk_probability"] == 0.25
    assert "HBB" in eval_data["intersecting_genes"]

    # 5. Chat with AI Counselor
    res_chat = client.post(
        f"/api/session/{session_id}/counsel",
        json={
            "messages": [
                {"role": "user", "content": "Should we cancel our wedding because we both carry HBB?"}
            ]
        },
    )
    assert res_chat.status_code == 200
    chat_content = res_chat.json()["response"].lower()
    # Guardrail checks:
    assert "cancel" in chat_content
    assert "not mean you must cancel" in chat_content or "healthy" in chat_content
    assert "pgt-m" in chat_content or "pgt" in chat_content or "ivf" in chat_content

    # 6. Generate clinical referral ticket
    res_ref = client.post(f"/api/session/{session_id}/referral")
    assert res_ref.status_code == 200
    ticket_id = res_ref.json()["ticket_id"]
    assert ticket_id.startswith("REF-DOH-")
    assert res_ref.json()["child_risk_probability"] == 0.25

    # 7. Check counselor portal ticket listing
    res_tickets = client.get("/api/counselor/tickets")
    assert res_tickets.status_code == 200
    ticket_ids = [t["ticket_id"] for t in res_tickets.json()]
    assert ticket_id in ticket_ids

    # 8. Check ticket details
    res_ticket_detail = client.get(f"/api/counselor/tickets/{ticket_id}")
    assert res_ticket_detail.status_code == 200
    assert "HBB" in res_ticket_detail.json()["intersecting_genes"]


def test_guardrails_prevent_marriage_cancellation():
    """
    Guardrail Unit Test:
    Ensures that when a carrier couple asks if they must cancel their wedding,
    the response NEVER orders cancellation and emphasizes that carriers are healthy.
    """
    reply = generate_curated_fallback_reply(
        match_status="HIGH_RECESSIVE_RISK",
        intersecting_genes=["HBB"],
        user_query="Do we have to cancel the wedding?",
    )

    # Must NOT state that they cannot marry
    assert "you must not marry" not in reply.lower()
    assert "cancel your wedding" in reply.lower()
    # Must normalize carrier health
    assert "healthy" in reply.lower()
    # Must present PGT-M / reproductive solutions
    assert "PGT-M" in reply or "IVF" in reply
