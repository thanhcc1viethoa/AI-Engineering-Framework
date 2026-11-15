"""AI Orchestrator entrypoint — Requirement.md FR-003/FR-004/FR-005."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import config
from db import init_db
from logger import get_logger
from routers import agents, auth_router, system, tasks, workflows

logger = get_logger("main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    logger.info("Orchestrator started on %s:%s", config.HOST, config.PORT)
    yield


app = FastAPI(title="AI Agent Orchestrator", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router)
app.include_router(tasks.router)
app.include_router(agents.router)
app.include_router(workflows.router)
app.include_router(system.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=False)
