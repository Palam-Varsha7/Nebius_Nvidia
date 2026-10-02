import asyncio
from orchestrator import agents_mock as agents
from orchestrator.loop import run_pipeline, MAX_ATTEMPTS
from orchestrator.schemas import TestResult


def test_passes_after_retry():
    result = asyncio.run(run_pipeline("hello"))
    assert result["status"] == "passed"
    assert result["attempts"] == 2


def test_records_events():
    events = []
    asyncio.run(run_pipeline("hello", events))
    agents_seen = {e["agent"] for e in events}
    assert {"coder", "reviewers", "judge", "sandbox"} <= agents_seen


def test_gives_up_after_max_attempts(monkeypatch):
    async def always_fail(code, attempt):
        return TestResult(passed=False, stderr="boom")

    monkeypatch.setattr(agents, "run_sandbox", always_fail)
    result = asyncio.run(run_pipeline("hello"))
    assert result["status"] == "failed"
    assert result["attempts"] == MAX_ATTEMPTS