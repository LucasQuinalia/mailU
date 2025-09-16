import os
import re
import requests
from typing import Dict, List
from openai import OpenAI

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAPI_KEY"))

        self.stop_words = set([
            'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para',
            'com', 'não', 'é', 'ao', 'os', 'as', 'no', 'na', 'por', 'se',
            'dos', 'das', 'como', 'mais', 'mas', 'nao', 'nos', 'nas'
        ])
        self.stop_words.update(['email', 'e-mail', 'mail', 'mensagem', 'msg', 'texto'])

    # ----------------- NLP Básico -----------------
    def preprocess_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def remove_stop_words(self, text: str) -> str:
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())
        return ' '.join([word for word in words if word not in self.stop_words])

    def apply_stemming(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())

    def apply_lemmatization(self, text: str) -> List[str]:
        return re.findall(r'\b[a-zA-ZÀ-ÿ]+\b', text.lower())

    def process_text_nlp(self, text: str) -> Dict:
        processed_text = self.preprocess_text(text)
        without_stopwords = self.remove_stop_words(processed_text)
        stemmed = self.apply_stemming(processed_text)
        lemmatized = self.apply_lemmatization(processed_text)
        return {
            'original': text,
            'processed': processed_text,
            'without_stopwords': without_stopwords,
            'stemmed': stemmed,
            'lemmatized': lemmatized,
            'word_count': len(stemmed),
            'unique_words': len(set(stemmed))
        }

    # ----------------- Classificação por palavras-chave -----------------
    def classify_with_keywords(self, text: str) -> Dict:
        text_lower = text.lower()
        productive_keywords = [
            'reunião', 'projeto', 'trabalho', 'relatório', 'apresentação',
            'deadline', 'prazo', 'cliente', 'negócio', 'proposta',
            'contrato', 'venda', 'compra', 'orçamento', 'custo',
            'desenvolvimento', 'implementação', 'análise', 'estudo',
            'pesquisa', 'investigação', 'colaboração', 'equipe'
        ]
        unproductive_keywords = [
            'promoção', 'desconto', 'oferta', 'grátis', 'ganhe',
            'prêmio', 'sorteio', 'concurso', 'clique aqui', 'link',
            'spam', 'marketing', 'publicidade', 'newsletter',
            'unsubscribe', 'cancele', 'parar de receber'
        ]
        productive_count = sum(1 for k in productive_keywords if k in text_lower)
        unproductive_count = sum(1 for k in unproductive_keywords if k in text_lower)
        classification = "produtivo" if productive_count > unproductive_count else "improdutivo"
        confidence = 75
        return {
            'classification': classification,
            'confidence': confidence,
            'method': 'keyword_fallback',
            'productive_count': productive_count,
            'unproductive_count': unproductive_count
        }

    # ----------------- Geração de resposta automática -----------------
    def generate_response(self, text: str, classification: str) -> str:
        name = None
        match = re.search(r'(olá|oi|ola|caro|cara)\s+([A-ZÀ-ÿ][a-zà-ÿ]+)', text, re.IGNORECASE)
        if match:
            name = match.group(2).strip()

        if classification == "produtivo":
            prompt = f"Escreva uma resposta educada e profissional em português para este e-mail produtivo"
        else:
            prompt = f"Escreva uma resposta educada e curta em português para este e-mail que não exige ação"

        if name:
            prompt += f", direcionando ao remetente chamado {name}"

        prompt += f":\n\"{text}\""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro ao gerar resposta com IA: {str(e)}")

        # fallback simples
        if classification == "produtivo":
            return f"Obrigado pelo seu e-mail{', ' + name if name else ''}. Entraremos em contato em breve para discutir os próximos passos!"
        else:
            return f"Seu e-mail foi recebido{', ' + name if name else ''}, mas não exige resposta no momento. Obrigado pelo contato."


# --- Instância pronta para uso ---
openai_service = OpenAIService()
