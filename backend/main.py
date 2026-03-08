"""
AI Coach Chatbot Backend
FastAPI + Claude API + Supabase
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import anthropic
import os
from datetime import datetime
from supabase import create_client, Client

app = FastAPI(title="AI Coach Bot API")

# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize clients
claude_client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))

# Supabase is optional (for conversation logging)
try:
    supabase: Client = create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )
    SUPABASE_ENABLED = True
except Exception as e:
    print(f"Warning: Supabase not available: {e}")
    supabase = None
    SUPABASE_ENABLED = False

# Request/Response models
class Message(BaseModel):
    content: str
    role: str  # 'user' or 'assistant'

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    conversation_history: Optional[List[Message]] = []

class ChatResponse(BaseModel):
    response: str
    session_id: str
    needs_human: bool = False

# Coach bot system prompt
COACH_SYSTEM_PROMPT = """You are an AI assistant for Mountain Coaching, a life coaching practice helping people with career transitions.

Your personality:
- Warm, encouraging, and supportive
- Professional but friendly
- Empathetic and understanding
- Direct and helpful

Your knowledge base:

PRICING:
- Discovery call: Free (30 minutes)
- 1-on-1 coaching: $200/session (60 minutes)
- 3-month package: $2,400 (12 sessions + email support)
- 6-month package: $4,200 (24 sessions + email + Voxer access)

COACHING STYLE:
- Focuses on career transitions and life purpose
- Uses a blend of positive psychology and practical strategy
- Includes accountability and action planning
- Personalized approach for each client

PROCESS:
1. Free discovery call to assess fit
2. Choose a package
3. Weekly or bi-weekly sessions via Zoom
4. Between-session support via email
5. Regular progress check-ins

WHAT'S INCLUDED:
- Personalized coaching sessions
- Career assessment tools
- Action plans and accountability
- Email support between sessions (3-month and 6-month packages)
- Resource library access
- Voxer voice message access (6-month package only)

SESSION DETAILS:
- Sessions are 60 minutes via Zoom
- Scheduled at mutually convenient times
- Recorded (if client wants) for their reference
- Flexible rescheduling (24-hour notice)

BOOKING:
- Book discovery calls at: calendly.com/mountaincoaching
- Or email: coach@mountaincoaching.com

SPECIALTIES:
- Career transitions (new job, career change, promotions)
- Finding life purpose and meaning
- Work-life balance
- Professional confidence building
- Leadership development

TESTIMONIALS:
"Sarah helped me transition from corporate to entrepreneurship with confidence. Best investment I made." - Mike, 34
"I got promoted within 3 months of coaching. Sarah's approach is practical and powerful." - Lisa, 29

POLICIES:
- 24-hour cancellation policy
- Packages must be used within timeframe (3 or 6 months)
- Satisfaction guarantee on first session
- Confidential and judgment-free space

Instructions:
- Answer questions clearly and warmly
- If asked about booking, provide the Calendly link
- If someone has a complex situation, suggest booking a discovery call
- If you don't know something specific, say "Let me connect you with Sarah directly"
- Keep responses concise (2-3 sentences usually)
- Use the client's name if they provide it
- Ask clarifying questions when needed

IMPORTANT: If someone asks about:
- Medical advice → "I'm not qualified to give medical advice. Please consult a healthcare professional."
- Legal advice → "I'm not a lawyer. Please consult a legal professional."
- Financial advice → "While I can help with career decisions, for specific financial advice, please consult a financial advisor."
- Crisis situations → "If you're in crisis, please call 988 (Suicide & Crisis Lifeline) or go to your nearest emergency room. I'm here for coaching support, not crisis intervention."

If someone seems angry, upset, or the conversation is going poorly:
- Acknowledge their feelings
- Apologize if appropriate
- Offer to connect them with Sarah directly: "I think it would be better if you spoke with Sarah directly. Email coach@mountaincoaching.com or book a call."
"""

@app.get("/")
async def root():
    return {"status": "AI Coach Bot API Running", "version": "1.0"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint
    """
    try:
        # Build conversation history
        messages = []
        if request.conversation_history:
            for msg in request.conversation_history[-10:]:  # Last 10 messages for context
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Call Claude API
        response = claude_client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            system=COACH_SYSTEM_PROMPT,
            messages=messages
        )
        
        assistant_response = response.content[0].text
        
        # Check if human handoff needed
        needs_human = any(phrase in assistant_response.lower() for phrase in [
            "connect you with sarah",
            "speak with sarah directly",
            "i'm not qualified",
            "i don't know"
        ])
        
        # Save to database (optional)
        session_id = request.session_id or f"session_{datetime.now().timestamp()}"
        
        if SUPABASE_ENABLED and supabase:
            try:
                supabase.table("conversations").insert({
                    "session_id": session_id,
                    "user_message": request.message,
                    "bot_response": assistant_response,
                    "needs_human": needs_human,
                    "created_at": datetime.now().isoformat()
                }).execute()
            except Exception as db_error:
                print(f"Database error: {db_error}")
                # Don't fail the request if DB fails
        
        return ChatResponse(
            response=assistant_response,
            session_id=session_id,
            needs_human=needs_human
        )
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "claude_api": "configured" if os.getenv("CLAUDE_API_KEY") else "missing",
        "supabase": "enabled" if SUPABASE_ENABLED else "disabled (optional)"
    }

@app.get("/stats")
async def get_stats():
    """Get conversation stats"""
    if not SUPABASE_ENABLED or not supabase:
        return {
            "total_conversations": 0,
            "timestamp": datetime.now().isoformat(),
            "note": "Database not connected"
        }
    try:
        result = supabase.table("conversations").select("*", count="exact").execute()
        return {
            "total_conversations": result.count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
