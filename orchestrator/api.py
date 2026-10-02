import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from orchestrator.loop import run_pipeline

app = FastAPI(title="Agentic Dev Team Orchestrator")

runs: dict[str, dict] = {}  # remembers every run (in memory)


class RunRequest(BaseModel):
    task: str


async def execute(run_id: str, task: str):
    try:
        runs[run_id] = await run_pipeline(task)
    except Exception as e:
        runs[run_id] = {"status": "error", "error": str(e)}


@app.post("/runs")
async def start_run(req: RunRequest, background: BackgroundTasks):
    run_id = uuid.uuid4().hex[:8]
    runs[run_id] = {"status": "running"}
    background.add_task(execute, run_id, req.task)
    return {"run_id": run_id}


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs[run_id]