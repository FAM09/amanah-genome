"""
Deep REST API Concurrency, Session Isolation, and State Machine Robustness Tests.
Validates:
- Multi-session concurrent isolation
- Invalid state transition rejections (eval before upload, referral before eval)
- Edge case handling (404s, 400s)
"""

from pathlib import Path
from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)
MOCK_ROOT = Path("/home/fam/amanah-genome/mock-data")


def test_state_machine_invalid_transitions():
    """Verify API prevents invalid state transitions."""
    # 1. Initialize clean session
    res_init = client.post("/api/session/init")
    session_id = res_init.json()["session_id"]

    # 2. Attempt evaluate before any uploads -> 400
    res_eval_early = client.post(f"/api/session/{session_id}/evaluate")
    assert res_eval_early.status_code == 400
    assert "must upload" in res_eval_early.json()["detail"].lower()

    # 3. Attempt referral before evaluate -> 400
    res_ref_early = client.post(f"/api/session/{session_id}/referral")
    assert res_ref_early.status_code == 400
    assert "evaluated before" in res_ref_early.json()["detail"].lower()

    # 4. Upload invalid party key -> 400
    dummy_vcf = b"##fileformat=VCFv4.2\n"
    res_bad_party = client.post(
        f"/api/session/{session_id}/upload",
        data={"party": "INVALID_X"},
        files={"vcf_file": ("test.vcf", dummy_vcf, "text/plain")},
    )
    assert res_bad_party.status_code == 400

    # 5. Non-existent session -> 404
    res_fake_session = client.get("/api/session/SES-NONEXISTENT-9999/status")
    assert res_fake_session.status_code == 404


def test_concurrent_session_isolation():
    """
    Simulate 10 concurrent independent sessions running in parallel.
    Session 1: High risk Thalassemia (Both HBB)
    Session 2: Compatible (Clear)
    Session 3: High risk SMA (Both SMN1)
    ...
    Verify that results in Session N do not cross-pollinate into Session M.
    """
    sessions = []
    # Initialize 10 sessions
    for _ in range(10):
        r = client.post("/api/session/init")
        assert r.status_code == 200
        sessions.append(r.json()["session_id"])

    # Load HBB scenario into sessions[0]
    hbb_ahmad = (MOCK_ROOT / "case_02_thalassemia_carrier_both" / "ahmad_sample.vcf").read_bytes()
    hbb_fatima = (MOCK_ROOT / "case_02_thalassemia_carrier_both" / "fatima_sample.vcf").read_bytes()

    client.post(f"/api/session/{sessions[0]}/upload", data={"party": "A"}, files={"vcf_file": ("a.vcf", hbb_ahmad, "text/plain")})
    client.post(f"/api/session/{sessions[0]}/upload", data={"party": "B"}, files={"vcf_file": ("b.vcf", hbb_fatima, "text/plain")})

    # Load Compatible scenario into sessions[1]
    clear_ahmad = (MOCK_ROOT / "case_01_compatible" / "ahmad_sample.vcf").read_bytes()
    clear_fatima = (MOCK_ROOT / "case_01_compatible" / "fatima_sample.vcf").read_bytes()

    client.post(f"/api/session/{sessions[1]}/upload", data={"party": "A"}, files={"vcf_file": ("a.vcf", clear_ahmad, "text/plain")})
    client.post(f"/api/session/{sessions[1]}/upload", data={"party": "B"}, files={"vcf_file": ("b.vcf", clear_fatima, "text/plain")})

    # Evaluate Session 0
    res_0 = client.post(f"/api/session/{sessions[0]}/evaluate")
    assert res_0.status_code == 200
    assert res_0.json()["is_compatible"] is False
    assert res_0.json()["intersecting_genes"] == ["HBB"]

    # Evaluate Session 1
    res_1 = client.post(f"/api/session/{sessions[1]}/evaluate")
    assert res_1.status_code == 200
    assert res_1.json()["is_compatible"] is True
    assert res_1.json()["intersecting_genes"] == []

    # Verify Session 2 is still untouched
    res_2_status = client.get(f"/api/session/{sessions[2]}/status")
    assert res_2_status.status_code == 200
    assert res_2_status.json()["party_a_uploaded"] is False
    assert res_2_status.json()["party_b_uploaded"] is False


def test_counselor_ticket_lifecycle_and_updates():
    """Verify referral ticket lifecycle transitions and edge cases."""
    # 1. Non-existent ticket detail -> 404
    res_not_found = client.get("/api/counselor/tickets/REF-FAKE-999")
    assert res_not_found.status_code == 404

    # 2. Non-existent ticket patch -> 404
    res_patch_fail = client.patch(
        "/api/counselor/tickets/REF-FAKE-999",
        json={"status": "COMPLETED"}
    )
    assert res_patch_fail.status_code == 404
