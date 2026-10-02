# Nebius_Nvidia
# Agentic Dev Team

A multi-agent system that helps software engineers. Built for the
Nebius x NVIDIA Global AI Hackathon (Coding and Agentic Engineering track).

## How it works

User task -> Coder -> (Testing + Security + Performance, in parallel)
-> Judge -> Sandbox tests -> pass: done / fail: Judge fixes again (max 3 attempts)

## Setup

```
pip install fastapi uvicorn pydantic python-dotenv openai
```

## Run the orchestrator

```
python -m uvicorn orchestrator.api:app --reload
```

Open http://127.0.0.1:8000/docs to try the API.

## API

- `POST /runs` with `{"task": "..."}` starts a run and returns `{"run_id": "..."}`
- `GET /runs/{run_id}` returns the status (`running`, `passed`, `failed`, `error`),
  the code, the findings, and a live `events` list showing which agent is working.

## Project layout

- `orchestrator/schemas.py`: data shapes shared by all agents
- `orchestrator/agents_mock.py`: placeholder agents (replace with real ones)
- `orchestrator/loop.py`: the pipeline (Coder -> reviewers -> Judge -> sandbox)
- `orchestrator/api.py`: web endpoints
- `run.py`: quick terminal test


## License

MIT