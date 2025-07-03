from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

# In-memory agent store (replace with DB in production)
agents = {}

class Agent(BaseModel):
    id: int
    name: str
    type: str  # e.g., 'virtual', 'human', 'ai'
    description: str = ""

@router.post("/agents/", response_model=Agent)
def create_agent(agent: Agent):
    if agent.id in agents:
        raise HTTPException(status_code=400, detail="Agent ID already exists.")
    agents[agent.id] = agent
    return agent

@router.get("/agents/", response_model=List[Agent])
def list_agents():
    return list(agents.values())

@router.get("/agents/{agent_id}", response_model=Agent)
def get_agent(agent_id: int):
    agent = agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found.")
    return agent

@router.delete("/agents/{agent_id}")
def delete_agent(agent_id: int):
    if agent_id not in agents:
        raise HTTPException(status_code=404, detail="Agent not found.")
    del agents[agent_id]
    return {"detail": "Agent deleted."}
