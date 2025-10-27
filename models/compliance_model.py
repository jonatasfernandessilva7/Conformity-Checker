"""Camada simples de modelo de conformidade.

Este módulo encapsula a lógica de cálculo de similaridade usada para
medir o nível de conformidade entre um documento de referência e um
documento submetido. A implementação atual usa a classe `BERTSimilarity`
definida em `utils/similaraty.py`.
"""

import torch
from utils.similaraty import BERTSimilarity


class ComplianceModel:
    """Interface de alto nível para cálculo de conformidade.

    A classe delega o cálculo de similaridade para uma implementação de
    similaridade (no momento, BERT). Mantém a API simples com um único
    método público `compute_similarity`.
    """

    def __init__(self):
        """Inicializa o objeto e carrega o modelo de similaridade.

        Notas:
            - A inicialização pode carregar modelos BERT grandes e consumir
              memória; carregue esse objeto uma vez (por ex. por injeção
              de dependência) e reutilize quando possível.
        """
        self.similarity_model = BERTSimilarity()

    def compute_similarity(self, doc1, doc2):
        """Calcula a similaridade entre dois documentos de texto.

        Args:
            doc1 (str): Texto do documento de referência.
            doc2 (str): Texto do documento submetido.

        Returns:
            float: Similaridade entre 0.0 e 1.0 (valores maiores indicam
                   maior similaridade / conformidade).
        """
        return self.similarity_model.compute_similarity(doc1, doc2)


# Teste rápido do modelo quando executado como script
if __name__ == "__main__":
    model = ComplianceModel()
    doc_reference = "This is a sample regulatory document with compliance rules."
    doc_submitted = "This document follows compliance regulations and rules."

    similarity_score = model.compute_similarity(doc_reference, doc_submitted)
    print(f"Nível de conformidade (BERT): {similarity_score:.2f}")
