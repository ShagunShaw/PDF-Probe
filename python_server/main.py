from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

from vectors import create_vector, get_response         # Import functions from vectors.py file

app = FastAPI(
    title="PDF Probe",
    description="Backend API for Chrome Extension",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(                 # TODO: Review CORS settings later
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

firstQuestion= True
vector_store= None

class ChatRequest(BaseModel):
    page_url: str
    question: str

class ChatResponse(BaseModel):
    response: str
    status: str
    status_code: int

# Routes
@app.get("/")
async def root():
    return {
        "message": "AI PDF Assistant API is running! 🚀",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/api/chat")
async def chat(request: ChatRequest) -> ChatResponse:
    global firstQuestion, vector_store

    try:
        if not request.question or not request.question.strip():
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        
        response= ""
        if(firstQuestion):
            firstQuestion= False
            vector_store= create_vector(request.page_url)
            response= get_response(vector_store, request.question)
        else:
            response= get_response(vector_store, request.question)
        
        return ChatResponse(
            response=response,
            status="success",
            status_code= 200
        )
    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("🚀 Starting AI PDF Assistant API on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)