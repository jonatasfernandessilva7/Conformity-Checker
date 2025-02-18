from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import BertTokenizer, BertModel


def compute_tfidf_similarity(doc1, doc2):
    """Calcula a similaridade entre dois documentos usando TF-IDF."""
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
    return similarity


class BERTSimilarity:
    """Classe para calcular similaridade entre textos usando embeddings do BERT."""

    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")

    def get_embedding(self, text):
        """Gera a representação vetorial (embedding) de um texto."""
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

    def compute_similarity(self, doc1, doc2):
        """Calcula a similaridade entre dois documentos usando BERT embeddings."""
        embedding1 = self.get_embedding(doc1)
        embedding2 = self.get_embedding(doc2)
        similarity = torch.cosine_similarity(embedding1, embedding2)
        return similarity.item()
