import asyncio
from orchestrator.loop import run_pipeline

result = asyncio.run(run_pipeline("Make a hello world app"))
print("RESULT:", result["status"], "after", result["attempts"], "attempts")