"""Funções de similaridade textual.

Contém uma implementação TF-IDF simples e uma classe que usa BERT para
gerar embeddings e calcular similaridade por cosseno. Essas funções são
úteis para medir o nível de correspondência entre dois textos.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import BertTokenizer, BertModel


def compute_tfidf_similarity(doc1, doc2):
    """Calcula a similaridade TF-IDF entre dois textos.

    Args:
        doc1 (str): Primeiro documento / texto.
        doc2 (str): Segundo documento / texto.

    Returns:
        float: Similaridade (produto interno normalizado) entre os vetores
               TF-IDF dos dois documentos.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
    return similarity


class BERTSimilarity:
    """Classe para calcular similaridade entre textos usando embeddings do BERT.

    Nota: O carregamento dos pesos do BERT pode ser custoso (download e
    memória). Em ambientes restritos, considere usar modelos menores ou
    embeddings pré-computados.
    """

    def __init__(self):
        # Carrega tokenizer e modelo BERT (padrão 'bert-base-uncased')
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        self.model = BertModel.from_pretrained("bert-base-uncased")

    def get_embedding(self, text):
        """Gera a representação vetorial (embedding) de um texto.

        O embedding retornado é a média do last_hidden_state ao longo das
        posições de sequência (pooling por média).
        """
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

    def compute_similarity(self, doc1, doc2):
        """Calcula a similaridade por cosseno entre dois documentos.

        Returns:
            float: Valor da similaridade entre -1.0 e 1.0 (normalmente >=0 para
                   textos similares).
        """
        embedding1 = self.get_embedding(doc1)
        embedding2 = self.get_embedding(doc2)
        similarity = torch.cosine_similarity(embedding1, embedding2)
        return similarity.item()
