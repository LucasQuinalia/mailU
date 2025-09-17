from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from app.routes import email_routes

app = FastAPI()

# CORS básico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(email_routes.router, prefix="/email")

@app.get("/")
def root():
    return {"message": "API funcionando"}

handler = Mangum(app)
