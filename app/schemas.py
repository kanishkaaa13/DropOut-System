# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal, Dict

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["student", "admin"]

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class PredictionRequest(BaseModel):
    # include main features used in the Kaggle dataset (example subset)
    curricular_units_1st_sem_approved: int
    curricular_units_1st_sem_grade: float
    curricular_units_2nd_sem_approved: int
    curricular_units_2nd_sem_grade: float
    admission_grade: float
    age_at_enrollment: int
    # add more features as per dataset

class PredictionResponse(BaseModel):
    predicted_class: Literal["Dropout", "Enrolled", "Graduate"]
    dropout_risk_level: Literal["Low", "Medium", "High"]
    probabilities: Dict[str, float]

class ChatMessageRequest(BaseModel):
    student_risk_level: Literal["Low", "Medium", "High"]
    context: Optional[str] = None

class ChatMessageResponse(BaseModel):
    reply: str
