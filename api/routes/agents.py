from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from agents.ai_interviewer import AIInterviewer

router = APIRouter()

# In-memory agent store (replace with DB in production)
agents = {}
interviewers = {}

class Agent(BaseModel):
    id: int
    name: str
    type: str  # e.g., 'virtual', 'human', 'ai'
    description: str = ""

class InterviewRequest(BaseModel):
    session_id: str
    previous_answer: str = None

class AnswerRequest(BaseModel):
    session_id: str
    question: str
    answer: str

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

@router.post("/ai/start/")
def start_interview(req: InterviewRequest):
    interviewer = AIInterviewer()
    interviewers[req.session_id] = interviewer
    question = interviewer.generate_question()
    return {"question": question}

@router.post("/ai/next/")
def next_question(req: InterviewRequest):
    interviewer = interviewers.get(req.session_id)
    if not interviewer:
        raise HTTPException(status_code=404, detail="Session not found.")
    question = interviewer.generate_question(req.previous_answer)
    return {"question": question}

@router.post("/ai/evaluate/")
def evaluate_answer(req: AnswerRequest):
    interviewer = interviewers.get(req.session_id)
    if not interviewer:
        raise HTTPException(status_code=404, detail="Session not found.")
    result = interviewer.evaluate_answer(req.question, req.answer)
    return result

@router.get("/ai/decision/{session_id}")
def get_decision(session_id: str):
    interviewer = interviewers.get(session_id)
    if not interviewer:
        raise HTTPException(status_code=404, detail="Session not found.")
    decision = interviewer.make_decision()
    return {"decision": decision}
