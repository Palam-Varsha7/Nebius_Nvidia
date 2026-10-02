import asyncio
from orchestrator.schemas import CodeResult, Finding, TestResult


async def coder_agent(task: str) -> CodeResult:
    await asyncio.sleep(0.5)  # pretend the AI is thinking
    return CodeResult(
        files={"app.py": "print('hello')"},
        notes=f"Fake code for task: {task}",
    )


async def testing_agent(code: CodeResult) -> list[Finding]:
    await asyncio.sleep(0.5)
    return [Finding(agent="testing", severity="low",
                    file="app.py", line=1, message="No tests found")]


async def security_agent(code: CodeResult) -> list[Finding]:
    await asyncio.sleep(0.5)
    return [Finding(agent="security", severity="medium",
                    file="app.py", line=1, message="No input validation")]


async def performance_agent(code: CodeResult) -> list[Finding]:
    await asyncio.sleep(0.5)
    return []  # nothing wrong


async def judge_agent(code: CodeResult, findings: list[Finding]) -> CodeResult:
    await asyncio.sleep(0.5)
    return CodeResult(
        files={"app.py": "print('hello, fixed')"},
        notes=f"Fixed {len(findings)} findings",
    )


async def run_sandbox(code: CodeResult, attempt: int) -> TestResult:
    await asyncio.sleep(0.5)
    # Fake behavior: fail the first time, pass the second time
    if attempt < 2:
        return TestResult(passed=False, stderr="1 test failed")
    return TestResult(passed=True, stdout="All tests passed")