from fastapi import APIRouter, UploadFile, Form
from app.services.openai_service import openai_service
from app.utils.file_reader import read_file_content

router = APIRouter()

@router.post("/classify")
async def classify_email(
    file: UploadFile = None,
    text: str = Form(None)
):
    if file:
        content = await file.read()
        text = read_file_content(file.filename, content)

    if not text:
        return {"error": "Nenhum texto fornecido"}

    try:
        classification_result = openai_service.classify_with_keywords(text)
        nlp_analysis = openai_service.process_text_nlp(text)
        auto_response = openai_service.generate_response(
            text, classification_result['classification']
        )

        result = {
            "text": text,
            "classification": classification_result['classification'],
            "confidence": classification_result.get('confidence', 0),
            "method": classification_result.get('method', 'unknown'),
            "auto_response": auto_response,
            "nlp_analysis": nlp_analysis
        }

        return result
    except Exception as e:
        return {"error": f"Erro interno: {str(e)}"}
