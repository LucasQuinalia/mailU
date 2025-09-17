import os
import re
import logging
from typing import Dict, List
import openai
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

STOP_WORDS = set([
    'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para',
    'com', 'não', 'é', 'ao', 'os', 'as', 'no', 'na', 'por', 'se',
    'dos', 'das', 'como', 'mais', 'mas', 'nao', 'nos', 'nas',
    'email', 'e-mail', 'mail', 'mensagem', 'msg', 'texto'
])

PRODUCTIVE_KEYWORDS = set([
    'reunião', 'projeto', 'trabalho', 'relatório', 'apresentação',
    'deadline', 'prazo', 'cliente', 'negócio', 'proposta',
    'contrato', 'venda', 'compra', 'orçamento', 'custo',
    'desenvolvimento', 'implementação', 'análise', 'estudo',
    'pesquisa', 'investigação', 'colaboração', 'equipe'
])

UNPRODUCTIVE_KEYWORDS = set([
    'promoção', 'desconto', 'oferta', 'grátis', 'ganhe',
    'prêmio', 'sorteio', 'concurso', 'clique aqui', 'link',
    'spam', 'marketing', 'publicidade', 'newsletter',
    'unsubscribe', 'cancele', 'parar de receber'
])

class OpenAIService:
    def __init__(self):
        self.client = openai
        self.stop_words = STOP_WORDS
        self.productive_keywords = PRODUCTIVE_KEYWORDS
        self.unproductive_keywords = UNPRODUCTIVE_KEYWORDS
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def tokenize(self, text: str) -> List[str]:
        return word_tokenize(text)

    def remove_stop_words(self, words: List[str]) -> List[str]:
        return [w for w in words if w not in self.stop_words]

    def lemmatize_words(self, words: List[str]) -> List[str]:
        return [self.lemmatizer.lemmatize(w) for w in words]

    def process_text_nlp(self, text: str) -> Dict:
        processed = self.preprocess_text(text)
        tokens = self.tokenize(processed)
        tokens_no_stop = self.remove_stop_words(tokens)
        lemmatized = self.lemmatize_words(tokens_no_stop)
        return {
            'original': text,
            'processed': processed,
            'without_stopwords': ' '.join(tokens_no_stop),
            'lemmatized': lemmatized,
            'word_count': len(tokens),
            'unique_words': len(set(tokens))
        }

    def classify_with_keywords(self, text: str) -> Dict:
        words_set = set(self.tokenize(text.lower()))
        productive_count = len(words_set & self.productive_keywords)
        unproductive_count = len(words_set & self.unproductive_keywords)
        classification = "produtivo" if productive_count > unproductive_count else "improdutivo"
        return {
            'classification': classification,
            'method': 'keyword_fallback',
            'productive_count': productive_count,
            'unproductive_count': unproductive_count
        }

    def generate_response(self, text: str, classification: str) -> str:
        name = self.extract_name(text)
        if classification == "produtivo":
            prompt = f"Escreva uma resposta educada e profissional em português para este e-mail produtivo"
        else:
            prompt = f"Escreva uma resposta educada e curta em português para este e-mail que não exige ação"
        if name:
            prompt += f", direcionando ao remetente chamado {name}"
        prompt += f":\n\"{text}\""

        try:
            response = self.client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=300
            )
            return response.choices[0].message['content'].strip()
        except Exception as e:
            logger.error(f"Erro ao gerar resposta com IA: {str(e)}", exc_info=True)
            if classification == "produtivo":
                return f"Obrigado pelo seu e-mail{', ' + name if name else ''}. Entraremos em contato em breve!"
            else:
                return f"Seu e-mail foi recebido{', ' + name if name else ''}, mas não exige resposta no momento."

    def extract_name(self, text: str) -> str:
        match = re.search(r'(olá|oi|ola|caro|cara)\s+([A-ZÀ-ÿ][a-zà-ÿ]+(?:\s[A-ZÀ-ÿ][a-zà-ÿ]+)*)', text, re.IGNORECASE)
        return match.group(2).strip() if match else None

openai_service = OpenAIService()