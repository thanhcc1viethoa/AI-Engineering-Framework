from fastapi import APIRouter, Depends, HTTPException

from auth import require_auth
from models import Agent
from services import agent_manager

router = APIRouter(prefix="/agents", tags=["agents"], dependencies=[Depends(require_auth)])


@router.get("", response_model=list[Agent])
async def list_agents() -> list[Agent]:
    return agent_manager.list_agents()


@router.get("/{agent_id}", response_model=Agent)
async def get_agent(agent_id: str) -> Agent:
    agent = agent_manager.get_agent(agent_id)
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
