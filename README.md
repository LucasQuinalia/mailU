# mailU

Classifique rapidamente e-mails, gere respostas automáticas e poupe seu precioso tempo.

## Funcionalidades

- Classificação de e-mails usando `OpenAI API`
- Geração de respostas automáticas com `IA`
- Processamento `NLP` básico (stemming, lemmatization, remoção de stop words)
- Interface web intuitiva
- Suporte a upload de arquivos (.txt, .pdf) ou texto direto

## Configuração

### Backend

1. Navegue para a pasta do backend:
```console
cd backend
```

2. Instale as dependências:
```console
pip install -r requirements.txt
```

3. Configure a variável de ambiente:
```console
# Crie o arquivo .env na pasta backend/
touch .env
```

Adicione sua chave da OpenAI no arquivo `.env`:
```env
OPENAI_API_KEY=sua_chave_da_openai_aqui
```

4. Execute o servidor local:
```console
python3 run_local.py
```

**Nota**: O servidor rodará em `http://localhost:8000`

### Frontend

1. Navegue para a pasta do frontend:
```console
cd frontend
```

2. Instale as dependências:
```console
npm install
```

3. Execute o servidor de desenvolvimento:
```console
npm run dev
```

**Nota**: O frontend rodará em `http://localhost:5173`

## Uso

1. **Acesse a aplicação**: `http://localhost:5173`
2. **Faça upload de um arquivo** (.pdf ou .txt) ou **cole o texto** do e-mail
3. **Clique em "Classificar e-mail e gerar resposta"**
4. **Veja o resultado**: 
   - Classificação (Produtivo/Improdutivo)
   - Resposta automática gerada
   - Botão para copiar a resposta

## Funcionamento

### Com OpenAI API Key
- ✅ Classificação inteligente usando IA
- ✅ Respostas personalizadas geradas pela OpenAI
- ✅ Análise NLP avançada

### Sem OpenAI API Key
- ✅ Sistema funciona com classificação por palavras-chave
- ✅ Respostas pré-definidas (fallback)
- ✅ Todas as funcionalidades básicas disponíveis

## Tecnologias

### Backend
- **FastAPI**: Framework web moderno e rápido
- **OpenAI API**: Integração com GPT-3.5-turbo para IA
- **python-dotenv**: Carregamento de variáveis de ambiente
- **pdfplumber**: Extração de texto de arquivos PDF
- **HTTP Server**: Servidor local para desenvolvimento

### Frontend
- **React**: Biblioteca para interfaces de usuário
- **Vite**: Build tool moderno e rápido
- **CSS Modules**: Estilos organizados por componente

### Funcionalidades
- **Classificação de E-mails**: IA + palavras-chave
- **Geração de Respostas**: OpenAI GPT-3.5-turbo
- **Processamento de Arquivos**: PDF e TXT
- **Interface Responsiva**: Design moderno e intuitivo

## Estrutura do Projeto

    mailU/
    ├── backend/
    │   ├── app/
    │   │   ├── routes/email_routes.py
    │   │   ├── services/openai_service.py
    │   │   ├── utils/file_reader.py
    │   │   └── main.py
    │   └── requirements.txt
    └── frontend/
        ├── src/
        │   ├── components/
        │   │   ├── ResultDisplay/
        │   │   │   ├── index.jsx
        │   │   │   └── result-display.css
        │   │   └──UploadForm/
        │   │   │   ├── index.jsx
        │   │   │   └── upload-form.css
        │   ├── styles/
        │   │   └── App.css
        │   ├── App.jsx
        │   └── main.jsx
        ├── eslint.config.js
        ├── index.html
        ├── package-lock.json
        ├── package.json
        └── vite.config.js

## Troubleshooting

### Problemas Comuns

**1. Erro "OPENAI_API_KEY not found"**
- ✅ **Solução**: Crie o arquivo `.env` na pasta `backend/`
- ✅ **Conteúdo**: `OPENAI_API_KEY=sua_chave_aqui`
- ✅ **Nota**: O sistema funciona sem a API key (modo fallback)

**2. Erro de dependências Python**
- ✅ **Solução**: Verifique se o Python 3 está instalado
- ✅ **Comando**: `python3 --version`

**3. Frontend não conecta com Backend**
- ✅ **Verifique**: Backend rodando em `http://localhost:8000`
- ✅ **Verifique**: Frontend rodando em `http://localhost:5173`

**4. Erro ao processar PDF**
- ✅ **Verifique**: Arquivo PDF contém texto (não apenas imagens)
- ✅ **Formato**: Apenas PDFs com texto extraível

### Dicas de Desenvolvimento

- **Hot Reload**: Ambos os servidores suportam recarregamento automático
- **Logs**: Sistema configurado para logs mínimos (sem spam)
- **API**: Endpoint principal em `/email/classify`
- **CORS**: Configurado para desenvolvimento local
