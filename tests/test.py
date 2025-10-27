"""Testes unitários básicos para o modelo de conformidade e API.

Observação: Esses testes assumem que os modelos BERT/transformers estão
disponíveis e que o endpoint `/check_compliance` existe na aplicação.
Dependências pesadas podem tornar esses testes lentos em execução local.
"""

import unittest
from models.compliance_model import ComplianceModel
from app.main import app


class ComplianceModelTest(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.model = ComplianceModel()

    def test_similarity_score(self):
        """Verifica que a similaridade entre dois textos relacionados é >= 0.5.

        Nota: Este teste é um exemplo simples; critérios reais de aceitação
        devem ser definidos conforme o domínio e dados reais.
        """
        doc1 = "This is a regulatory document with compliance rules."
        doc2 = "This document follows compliance regulations."
        score = self.model.compute_similarity(doc1, doc2)
        self.assertGreaterEqual(score, 0.5)  # Esperamos que seja pelo menos 50% similar


class ComplianceAPITest(unittest.TestCase):
    def setUp(self):
        """Configuração inicial da API para testes."""
        self.app = app.test_client()
        self.app.testing = True

    def test_compliance_api(self):
        """Teste do endpoint /check_compliance.

        Este teste envia JSON com os campos esperados e checa a presença
        do campo `conformity_score` na resposta.
        """
        response = self.app.post('/check_compliance', json={
            "doc_reference": "This is a regulatory document with compliance rules.",
            "doc_submitted": "This document follows compliance regulations."
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("conformity_score", data)
        self.assertGreaterEqual(data["conformity_score"], 0.5)  # Esperamos pelo menos 50% de conformidade


if __name__ == "__main__":
    unittest.main()
