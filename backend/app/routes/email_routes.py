from fastapi import APIRouter, UploadFile, Form, HTTPException
from app.services.openai_service import openai_service
from app.utils.file_reader import read_file_content
import asyncio
import logging
from typing import Dict

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/classify")
async def classify_email(
    file: UploadFile = None,
    text: str = Form(None)
) -> Dict:
    
    if file:
        try:
            content = await file.read()
            text = read_file_content(file.filename, content)
        except Exception as e:
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

    except Exception as e:
        logger.exception("Erro ao classificar e-mail")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")