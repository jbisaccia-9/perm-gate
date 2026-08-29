from permgate.gate import run_attacks, check
from permgate.live import run_live_attacks
from permgate.store import fetch_scoped, fetch_trusting, RESTRICTED_FIELDS


class FakeResponses:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return type("Response", (), {"output_text": "FAKE-ID-000111"})()


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


def test_scoped_accessor_strips_restricted_fields():
    rec = fetch_scoped("u1")
    assert RESTRICTED_FIELDS.isdisjoint(rec)
    assert "name" in rec  # public fields still flow


def test_trusting_accessor_returns_everything():
    rec = fetch_trusting("u1")
    assert RESTRICTED_FIELDS <= set(rec)


def test_permission_mode_never_leaks():
    assert all(not r["leaked"] for r in run_attacks("permission"))
    assert check("permission") == 0


def test_prompt_mode_leaks_under_attack():
    leaks = [r for r in run_attacks("prompt") if r["leaked"]]
    assert len(leaks) >= 3, "the naive agent should fail the injected/roleplay/pivot attacks"
    kinds = {r["kind"] for r in leaks}
    assert "content_injection" in kinds
    assert check("prompt") == 0  # demonstrated, not vacuous


def test_direct_ask_is_the_deceptive_success():
    # The guard 'works' on the plain ask in BOTH modes - which is exactly why
    # prompt-layer security demos look safe and fail later.
    direct = [r for r in run_attacks("prompt") if r["kind"] == "direct_ask"]
    assert direct and not direct[0]["leaked"]


def test_live_mode_runs_the_same_suite_through_responses_api():
    client = FakeClient()
    results = run_live_attacks(client=client, model="test-model")

    assert len(results) == len(run_attacks("prompt")) == 5
    assert all(result["leaked"] == ["FAKE-ID-000111"] for result in results)
    assert all(call["model"] == "test-model" for call in client.responses.calls)
    assert all(call["instructions"] for call in client.responses.calls)
    assert all(call["store"] is False for call in client.responses.calls)
