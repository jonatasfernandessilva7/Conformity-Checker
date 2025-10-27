"""Ferramentas de pré-processamento e medidas de similaridade.

Contém funções para limpeza e normalização de texto (spaCy) e funções
de similaridade (TF-IDF e BERT). Esses utilitários são usados pelo
pipeline de avaliação de conformidade.
"""

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import re
import torch
from transformers import BertTokenizer, BertModel


def preprocess_text(text):
    """Pré-processa texto: minúsculas, remoção de stopwords e lematização.

    Args:
        text (str): Texto bruto de entrada.

    Returns:
        str: Texto processado pronto para vetorização.
    """
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())

    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)


def compute_tfidf_similarity(doc1, doc2):
    """Calcula similaridade TF-IDF entre dois documentos.

    Args:
        doc1 (str): Primeiro documento processado.
        doc2 (str): Segundo documento processado.

    Returns:
        float: Pontuação de similaridade TF-IDF.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([doc1, doc2])
    similarity = (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]
    return similarity


def compute_bert_similarity(doc1, doc2):
    """Calcula similaridade entre dois textos usando embeddings BERT.

    Observação: Carregar o modelo BERT pode ser custoso. Use com cautela
    em produção ou pré-compute embeddings quando possível.
    """
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
    model = BertModel.from_pretrained("bert-base-uncased")

    def get_embedding(text):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1)

    embedding1 = get_embedding(doc1)
    embedding2 = get_embedding(doc2)

    similarity = torch.cosine_similarity(embedding1, embedding2)
    return similarity.item()


if __name__ == "__main__":
    # Exemplo de documentos
    doc_reference = "This is a sample regulatory document with compliance rules."
    doc_submitted = "This document follows compliance regulations and rules."

    # Processar textos
    processed_ref = preprocess_text(doc_reference)
    processed_sub = preprocess_text(doc_submitted)

    # Calcular similaridade TF-IDF
    similarity_score_tfidf = compute_tfidf_similarity(processed_ref, processed_sub)
    print(f"Nível de conformidade (TF-IDF): {similarity_score_tfidf:.2f}")

    # Calcular similaridade BERT
    similarity_score_bert = compute_bert_similarity(processed_ref, processed_sub)
    print(f"Nível de conformidade (BERT): {similarity_score_bert:.2f}")
