from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from typing import Dict

load_dotenv()

FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")

from app.routes import email_routes

app = FastAPI(title="Email Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_routes.router, prefix="/email", tags=["Emails"])

@app.get("/", response_model=Dict)
def root() -> Dict:
    return {"message": "API funcionando"}