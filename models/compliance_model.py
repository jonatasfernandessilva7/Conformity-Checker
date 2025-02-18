import torch
from utils.similaraty import BERTSimilarity


class ComplianceModel:
    def __init__(self):
        """Inicializa o modelo de conformidade usando BERTSimilarity."""
        self.similarity_model = BERTSimilarity()

    def compute_similarity(self, doc1, doc2):
        """Calcula a similaridade entre dois documentos."""
        return self.similarity_model.compute_similarity(doc1, doc2)


# Teste do modelo
if __name__ == "__main__":
    model = ComplianceModel()
    doc_reference = "This is a sample regulatory document with compliance rules."
    doc_submitted = "This document follows compliance regulations and rules."

    similarity_score = model.compute_similarity(doc_reference, doc_submitted)
    print(f"Nível de conformidade (BERT): {similarity_score:.2f}")
