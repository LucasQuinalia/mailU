from __future__ import annotations
import os
import json
import sys
from http.server import BaseHTTPRequestHandler
from typing import Dict, Any
import urllib.parse
import io

sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

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
        elif self.path == '/test':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"message": "Teste funcionando", "path": self.path}
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/email/classify':
            try:
                content_type = self.headers.get('Content-Type', '')
                if 'multipart/form-data' in content_type:
                    content_length = int(self.headers.get('Content-Length', 0))
                    post_data = self.rfile.read(content_length)
                    
                    file = None
                    text = None
                    
                    if b'name="file"' in post_data:
                        start = post_data.find(b'name="file"')
                        if start != -1:
                            file_start = post_data.find(b'\r\n\r\n', start) + 4
                            file_end = post_data.find(b'\r\n--', file_start)
                            if file_end == -1:
                                file_end = len(post_data)
                            file_content = post_data[file_start:file_end]
                            
                            class MockFile:
                                def __init__(self, content, filename):
                                    self.content = content
                                    self.filename = filename
                                    self.file = io.BytesIO(content)
                                
                                def read(self):
                                    return self.content
                            
                            filename = "uploaded_file.pdf"
                            if b'filename=' in post_data[start:file_start]:
                                filename_start = post_data.find(b'filename="', start) + 11
                                filename_end = post_data.find(b'"', filename_start)
                                if filename_start != 10 and filename_end != -1:
                                    filename = post_data[filename_start:filename_end].decode('utf-8')
                            
                            file = MockFile(file_content, filename)
                    
                    if b'name="text"' in post_data:
                        start = post_data.find(b'name="text"')
                        if start != -1:
                            text_start = post_data.find(b'\r\n\r\n', start) + 4
                            text_end = post_data.find(b'\r\n--', text_start)
                            if text_end == -1:
                                text_end = len(post_data)
                            text = post_data[text_start:text_end].decode('utf-8')
                    
                    
                    if file and hasattr(file, 'filename') and file.filename:
                        try:
                            content = file.content
                            
                            text = read_file_content(file.filename, content)
                            
                            if not text or not text.strip():
                                self.send_error_response(400, "Arquivo não contém texto extraível.")
                                return
                        except Exception as e:
                            self.send_error_response(400, f"Erro ao processar arquivo: {str(e)}")
                            return
                    elif not text or not text.strip():
                        self.send_error_response(400, "Nenhum texto fornecido.")
                        return
                    
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
