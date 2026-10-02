import asyncio
from orchestrator import agents_mock as agents

MAX_ATTEMPTS = 3  # never loop forever


async def run_pipeline(task: str) -> dict:
    # Step 1: the Coder writes the first version
    code = await agents.coder_agent(task)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        print(f"--- Attempt {attempt} ---")

        # Step 2: three reviewers run at the same time
        results = await asyncio.gather(
            agents.testing_agent(code),
            agents.security_agent(code),
            agents.performance_agent(code),
        )
        findings = [f for group in results for f in group]
        print(f"Reviewers found {len(findings)} issues")

        # Step 3: the Judge fixes the code
        code = await agents.judge_agent(code, findings)
        print("Judge:", code.notes)

        # Step 4: run it in the sandbox
        test = await agents.run_sandbox(code, attempt)
        print("Tests passed?", test.passed)

        if test.passed:
            return {"status": "passed", "attempts": attempt,
                    "code": code, "findings": findings}

    return {"status": "failed", "attempts": MAX_ATTEMPTS,
            "code": code, "findings": findings}