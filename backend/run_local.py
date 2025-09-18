#!/usr/bin/env python3

import sys
import os
from http.server import HTTPServer
from dotenv import load_dotenv
from index import handler

load_dotenv()
sys.path.append(os.path.dirname(__file__))

def run_server():
    port = 8000
    server_address = ('', port)
    
    print(f"Servidor rodando em http://localhost:{port}")
    
    try:
        httpd = HTTPServer(server_address, handler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()

if __name__ == "__main__":
    run_server()
