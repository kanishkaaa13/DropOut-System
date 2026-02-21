# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import UserCreate, UserLogin, Token
from .auth import create_user, get_user, verify_password, create_access_token
from .routers import predict, chatbot

app = FastAPI(title="Dropout Prediction and Counseling API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)
app.include_router(chatbot.router)

@app.post("/auth/register", response_model=Token)
def register(payload: UserCreate):
    if get_user(payload.email):
        raise HTTPException(status_code=400, detail="User already exists")
    create_user(payload.email, payload.password, payload.role)
    token = create_access_token({"sub": payload.email, "role": payload.role})
    return Token(access_token=token)

@app.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token({"sub": user["email"], "role": user["role"]})
    return Token(access_token=token)
