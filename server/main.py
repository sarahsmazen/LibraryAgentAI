import sys
import os
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Setting up project paths for module resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
sys.path.append(current_dir)

# Conditional imports to handle local and package-level execution
try:
    from server.agent import library_agent
    from server.tools import run_query, run_commit
except ImportError:
    from agent import library_agent
    from tools import run_query, run_commit 
   
app = FastAPI(title="Library Desk Agent API")

# --- Data Models (Pydantic) ---

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    response: str

# --- Database Helper Functions ---

def save_message(session_id: str, role: str, content: str):
    """Saves conversation messages to the database as required."""
    sql = "INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)"
    run_commit(sql, (session_id, role, content))

def get_chat_history(session_id: str):
    """Retrieves previous messages to maintain context."""
    sql = "SELECT role, content FROM messages WHERE session_id = ? ORDER BY created_at ASC"
    rows = run_query(sql, (session_id,))
    # SQLite returns tuples; we pass them as (role, content)
    return [(row['role'], row['content']) for row in rows]

# --- API Endpoints ---

@app.get("/")
async def root():
    """Basic health check endpoint."""
    return {"status": "success", "message": "Library AI Server is active"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main communication hub. 
    Processes user input through the AI Agent and maintains session state.
    """
    # Initialize a new session if none is provided
    session_id = request.session_id or str(uuid.uuid4())
    
    # Load past context for the AI
    history = get_chat_history(session_id)
    
    try:
        # 1. Log user message to DB
        save_message(session_id, "user", request.message)
        
        # 2. Invoke the GPT-4o Agent with tools and history
        result = library_agent.invoke({
            "input": request.message,
            "chat_history": history
        })
        
        ai_response = result["output"]
        
        # 3. Log AI response 
        save_message(session_id, "assistant", ai_response)
        
        return ChatResponse(session_id=session_id, response=ai_response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
async def list_sessions():
    """Returns a list of unique chat sessions for the UI selector."""
    sql = "SELECT DISTINCT session_id FROM messages ORDER BY created_at DESC"
    return run_query(sql)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)