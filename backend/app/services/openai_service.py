import os
import re
import logging
from typing import Dict, List
from openai import OpenAI
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.stop_words = set(stopwords.words('portuguese'))

        self.productive_keywords = set([
            'reunião', 'projeto', 'trabalho', 'relatório', 'apresentação',
            'deadline', 'prazo', 'cliente', 'negócio', 'proposta',
            'contrato', 'venda', 'compra', 'orçamento', 'custo',
            'desenvolvimento', 'implementação', 'análise', 'estudo',
            'pesquisa', 'investigação', 'colaboração', 'equipe'
        ])
        self.unproductive_keywords = set([
            'promoção', 'desconto', 'oferta', 'grátis', 'ganhe',
            'prêmio', 'sorteio', 'concurso', 'clique aqui', 'link',
            'spam', 'marketing', 'publicidade', 'newsletter',
            'unsubscribe', 'cancele', 'parar de receber'
        ])

    def preprocess_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def remove_stop_words(self, words: List[str]) -> List[str]:
        return [word for word in words if word not in self.stop_words]

    def process_text_nlp(self, text: str) -> Dict:
        processed_text = self.preprocess_text(text)
        tokens = word_tokenize(processed_text, language='portuguese')
        without_stopwords = self.remove_stop_words(tokens)

        return {
            'original': text,
            'processed': processed_text,
            'without_stopwords': ' '.join(without_stopwords),
            'word_count': len(tokens),
            'unique_words': len(set(tokens))
        }

    def classify_with_keywords(self, text: str) -> Dict:
        words_set = set(word_tokenize(text.lower(), language='portuguese'))
        productive_count = len(words_set & self.productive_keywords)
        unproductive_count = len(words_set & self.unproductive_keywords)
        classification = "produtivo" if productive_count > unproductive_count else "improdutivo"

        return {
            'classification': classification,
            'method': 'keyword_fallback',
            'productive_count': productive_count,
            'unproductive_count': unproductive_count
        }

    def extract_name(self, text: str) -> str:
        match = re.search(
            r'(olá|oi|ola|caro|cara)\s+([A-ZÀ-ÿ][a-zà-ÿ]+(?:\s[A-ZÀ-ÿ][a-zà-ÿ]+)*)',
            text, re.IGNORECASE
        )
        return match.group(2).strip() if match else None

    def generate_response(self, text: str, classification: str) -> str:
        name = self.extract_name(text)

        if classification == "produtivo":
            prompt = "Escreva uma resposta educada e profissional em português para este e-mail produtivo, corretamente indentada"
        else:
            prompt = "Escreva uma resposta educada e curta em português para este e-mail que não exige ação, corretamente indentada"

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
            logger.error(f"Erro ao gerar resposta com IA: {str(e)}", exc_info=True)

        if classification == "produtivo":
            return f"Obrigado pelo seu e-mail{', ' + name if name else ''}. Entraremos em contato em breve para discutir os próximos passos!"
        else:
            return f"Seu e-mail foi recebido{', ' + name if name else ''}, mas não exige resposta no momento. Obrigado pelo contato."

openai_service = OpenAIService()