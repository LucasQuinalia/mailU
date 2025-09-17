from fastapi import FastAPI, APIRouter, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
from typing import Dict
from mangum import Mangum

from app.services.openai_service import openai_service
from app.utils.file_reader import read_file_content
import asyncio
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Email Classifier API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def add_cors_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    return response

@app.options("/classify")
async def options_classify():
    return JSONResponse(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true"
        }
    )

@app.post("/classify")
async def classify_email(
    file: UploadFile = None,
    text: str = Form(None)
) -> Dict:
    
    if file:
        try:
            content = await file.read()
            text = read_file_content(file.filename, content)
        except Exception:
            logger.exception("Erro ao ler o arquivo")
            raise HTTPException(status_code=400, detail="Erro ao processar arquivo")

    if not text:
        raise HTTPException(status_code=400, detail="Nenhum texto fornecido")

    try:
        classification_result, nlp_analysis, auto_response = await asyncio.gather(
            asyncio.to_thread(openai_service.classify_with_keywords, text),
            asyncio.to_thread(openai_service.process_text_nlp, text),
            asyncio.to_thread(openai_service.generate_response, text, 
                              openai_service.classify_with_keywords(text)['classification'])
        )

        return {
            "classification": classification_result['classification'],
            "method": classification_result.get('method', 'unknown'),
            "auto_response": auto_response,
            "nlp_summary": {
                "word_count": nlp_analysis['word_count'],
                "unique_words": nlp_analysis['unique_words']
            }
        }

    except Exception:
        logger.exception("Erro ao classificar e-mail")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")

@app.get("/", response_model=Dict)
def root() -> Dict:
    return {"message": "API funcionando"}

handler = Mangum(app)
