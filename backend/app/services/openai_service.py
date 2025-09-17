import os
import re
import logging
from typing import Dict, List
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STOP_WORDS = set([
    'a', 'o', 'e', 'de', 'do', 'da', 'em', 'um', 'uma', 'para',
    'com', 'não', 'é', 'ao', 'os', 'as', 'no', 'na', 'por', 'se',
    'dos', 'das', 'como', 'mais', 'mas', 'nao', 'nos', 'nas',
    'email', 'e-mail', 'mail', 'mensagem', 'msg', 'texto'
])

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.stop_words = STOP_WORDS

        self.productive_keywords = set([...])
        self.unproductive_keywords = set([...])

    def preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '', text)
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def tokenize(self, text: str) -> List[str]:
        return text.split()

    def remove_stop_words(self, words: List[str]) -> List[str]:
        return [w for w in words if w not in self.stop_words]

    def process_text_nlp(self, text: str) -> Dict:
        processed = self.preprocess_text(text)
        tokens = self.tokenize(processed)
        tokens_no_stop = self.remove_stop_words(tokens)
        return {
            'original': text,
            'processed': processed,
            'without_stopwords': ' '.join(tokens_no_stop),
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

openai_service = OpenAIService()