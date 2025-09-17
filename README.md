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

1. Instale as dependências:
```console
cd backend
pip install -r requirements.txt
```

2. Configure a variável de ambiente:

```console
touch .env
```

```console
Dentro do arquivo .env:
OPENAI_API_KEY=sua_chave_aqui
```

3. Execute o servidor:
```console
uvicorn app.main:app --reload
```

### Frontend

1. Instale as dependências:
```console
cd frontend
npm install
```

2. Execute o servidor de desenvolvimento:
```console
npm run dev
```

## Uso

- Acesse http://localhost:5173
- Faça upload de um arquivo ou cole o texto do e-mail
- Clique em "Classificar" para obter o resultado
- Se produtivo, será gerada uma resposta automática

## Tecnologias

- `Backend`: FastAPI, OpenAI API, NLTK
- `Frontend`: React, Vite
- `NLP: Stemming`, Lemmatization, Remoção de stop words

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
