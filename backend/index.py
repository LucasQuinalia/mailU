from __future__ import annotations
import os
import json
import sys
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any
import cgi
import io

# Adicionar o diretório app ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Importar os serviços
from app.services.openai_service import openai_service
from app.utils.file_reader import read_file_content

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "API funcionando"}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/email/classify':
            try:
                # Parse do form data
                content_type = self.headers.get('Content-Type', '')
                if 'multipart/form-data' in content_type:
                    form = cgi.FieldStorage(
                        fp=self.rfile,
                        headers=self.headers,
                        environ={'REQUEST_METHOD': 'POST'}
                    )
                    
                    file = form.getfirst('file')
                    text = form.getfirst('text')
                    
                    # Processar arquivo se fornecido
                    if file and hasattr(file, 'filename') and file.filename:
                        content = file.file.read()
                        text = read_file_content(file.filename, content)
                    
                    if not text:
                        self.send_error_response(400, "Nenhum texto fornecido")
                        return
                    
                    # Classificar usando o serviço real
                    classification_result = openai_service.classify_with_keywords(text)
                    nlp_analysis = openai_service.process_text_nlp(text)
                    auto_response = openai_service.generate_response(text, classification_result['classification'])
                    
                    response = {
                        "classification": classification_result['classification'],
                        "method": classification_result.get('method', 'unknown'),
                        "auto_response": auto_response,
                        "nlp_summary": {
                            "word_count": nlp_analysis['word_count'],
                            "unique_words": nlp_analysis['unique_words']
                        }
                    }
                    
                    self.send_success_response(response)
                else:
                    self.send_error_response(400, "Content-Type deve ser multipart/form-data")
            except Exception as e:
                self.send_error_response(500, f"Erro interno: {str(e)}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
    
    def send_success_response(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        response = {"error": message}
        self.wfile.write(json.dumps(response).encode())
