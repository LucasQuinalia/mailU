from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Dict
from mangum import Mangum

FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", "https://mailu-frontend.vercel.app").split(",")

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

handler = Mangum(app)