import unittest
from models.compliance_model import ComplianceModel
from app.main import app


class ComplianceModelTest(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.model = ComplianceModel()

    def test_similarity_score(self):
        """Teste para verificar a similaridade entre dois documentos."""
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
        """Teste do endpoint /check_compliance."""
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
