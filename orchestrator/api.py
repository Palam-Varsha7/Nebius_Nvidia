import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from orchestrator.loop import run_pipeline

app = FastAPI(title="Agentic Dev Team Orchestrator")

runs: dict[str, dict] = {}  # remembers every run (in memory)


class RunRequest(BaseModel):
    task: str


async def execute(run_id: str, task: str):
    events = runs[run_id]["events"]
    try:
        result = await run_pipeline(task, events)
        result["events"] = events
        runs[run_id] = result
    except Exception as e:
        events.append({"agent": "orchestrator", "message": f"Error: {e}"})
        runs[run_id] = {"status": "error", "error": str(e), "events": events}


@app.post("/runs")
async def start_run(req: RunRequest, background: BackgroundTasks):
    run_id = uuid.uuid4().hex[:8]
    runs[run_id] = {"status": "running", "events": []}
    background.add_task(execute, run_id, req.task)
    return {"run_id": run_id}


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    if run_id not in runs:
        raise HTTPException(status_code=404, detail="Run not found")
    return runs[run_id]