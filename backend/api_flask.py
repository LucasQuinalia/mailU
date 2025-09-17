from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.routes.email_routes import classify_email

app = Flask(__name__)
CORS(app)

@app.route('/')
def root():
    return jsonify({"message": "API funcionando"})

@app.route('/email/classify', methods=['POST'])
def classify():
    try:
        # Simular a estrutura do FastAPI
        file = request.files.get('file')
        text = request.form.get('text')
        
        # Chamar a função de classificação
        result = classify_email(file, text)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Handler para Vercel
def handler(request):
    return app(request.environ, lambda *args: None)
