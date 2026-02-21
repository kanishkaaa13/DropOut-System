# app/routers/chatbot.py
from fastapi import APIRouter, Depends
from ..schemas import ChatMessageRequest, ChatMessageResponse
from ..deps import get_current_user

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

@router.post("/", response_model=ChatMessageResponse)
def counseling_chat(req: ChatMessageRequest, user=Depends(get_current_user)):
    base = ""
    if req.student_risk_level == "High":
        base = (
            "You are currently flagged as high risk for dropout. "
            "Focus first on attendance and clearing any backlogs. "
            "Speak to your mentor or counselor this week to make a concrete recovery plan. "
            "Break your study into short, focused sessions and avoid skipping assessments."
        )
    elif req.student_risk_level == "Medium":
        base = (
            "You have some warning signs, but you can easily recover. "
            "Track your weekly attendance and test scores, and schedule extra practice on weaker subjects. "
            "Use a simple daily routine: 2–3 focused study blocks and one revision block."
        )
    else:
        base = (
            "You are currently at low risk. "
            "Maintain your habits, keep attending classes regularly, and do not ignore early signs of stress. "
            "Set clear semester goals for grades, skills, and projects."
        )

    if req.context:
        base += f" Regarding your note: {req.context.strip()}"

    return ChatMessageResponse(reply=base)
