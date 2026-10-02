import asyncio
import time
from orchestrator import agents_mock as agents

MAX_ATTEMPTS = 3  # never loop forever


async def run_pipeline(task: str, events: list | None = None) -> dict:
    if events is None:
        events = []

    def log(agent: str, message: str):
        events.append({"time": time.time(), "agent": agent, "message": message})
        print(f"[{agent}] {message}")

    log("orchestrator", f"Starting task: {task}")

    # Step 1: the Coder writes the first version
    log("coder", "Writing code...")
    code = await agents.coder_agent(task)
    log("coder", "First version ready")

    for attempt in range(1, MAX_ATTEMPTS + 1):
        log("orchestrator", f"Attempt {attempt} of {MAX_ATTEMPTS}")

        # Step 2: three reviewers run at the same time
        log("reviewers", "Testing, security and performance checks running")
        results = await asyncio.gather(
            agents.testing_agent(code),
            agents.security_agent(code),
            agents.performance_agent(code),
        )
        findings = [f for group in results for f in group]
        log("reviewers", f"Found {len(findings)} issues")

        # Step 3: the Judge fixes the code
        log("judge", "Fixing issues...")
        code = await agents.judge_agent(code, findings)
        log("judge", code.notes)

        # Step 4: run it in the sandbox
        log("sandbox", "Running tests...")
        test = await agents.run_sandbox(code, attempt)
        log("sandbox", "Tests passed" if test.passed else "Tests failed")

        if test.passed:
            log("orchestrator", "Done: all tests passed")
            return {"status": "passed", "attempts": attempt,
                    "code": code, "findings": findings}

    log("orchestrator", "Gave up: max attempts reached")
    return {"status": "failed", "attempts": MAX_ATTEMPTS,
            "code": code, "findings": findings}