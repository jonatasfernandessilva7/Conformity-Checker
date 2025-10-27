"""Testes unitários expandidos para o sistema de conformidade.

Este módulo contém testes mais abrangentes para:
1. Diferentes tipos de entrada (texto curto/longo, diferentes idiomas)
2. Casos de erro (entradas inválidas)
3. Validação do formato da resposta da API
4. Testes para os utilitários
"""

import unittest
from models.compliance_model import ComplianceModel
from app.main import app
from utils.text_processing import preprocess_text, compute_tfidf_similarity, compute_bert_similarity
from utils.similaraty import BERTSimilarity
import json


class ComplianceModelTest(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.model = ComplianceModel()
        # Exemplos de documentos para teste
        self.doc_regulatory = """
        This document outlines the regulatory compliance requirements.
        All organizations must follow these guidelines:
        1. Data protection measures
        2. Security protocols
        3. Regular auditing
        """
        self.doc_compliant = """
        Our organization implements strict data protection measures and
        security protocols. We conduct regular audits to ensure compliance
        with all guidelines.
        """
        self.doc_non_compliant = """
        This is a completely unrelated document about cooking recipes.
        How to make a delicious chocolate cake...
        """

    def test_similarity_score(self):
        """Verifica similaridade entre textos relacionados."""
        doc1 = "This is a regulatory document with compliance rules."
        doc2 = "This document follows compliance regulations."
        score = self.model.compute_similarity(doc1, doc2)
        self.assertGreaterEqual(score, 0.5)

    def test_high_similarity(self):
        """Testa alta similaridade entre documentos relacionados."""
        score = self.model.compute_similarity(self.doc_regulatory, self.doc_compliant)
        self.assertGreaterEqual(score, 0.7)  # Deve ter alta similaridade

    def test_low_similarity(self):
        """Testa baixa similaridade entre documentos não relacionados."""
        score = self.model.compute_similarity(self.doc_regulatory, self.doc_non_compliant)
        self.assertLess(score, 0.3)  # Deve ter baixa similaridade

    def test_empty_documents(self):
        """Testa comportamento com documentos vazios."""
        score = self.model.compute_similarity("", "")
        self.assertIsInstance(score, float)  # Deve retornar um float mesmo com entrada vazia

    def test_unicode_text(self):
        """Testa suporte a caracteres Unicode/non-ASCII."""
        doc1 = "Documento com acentuação é válido também! 🔍"
        doc2 = "Teste de acentuação é importante. 📝"
        score = self.model.compute_similarity(doc1, doc2)
        self.assertIsInstance(score, float)


class TextProcessingTest(unittest.TestCase):
    """Testes para funções de processamento de texto."""

    def setUp(self):
        self.text1 = "The quick brown fox jumps over the lazy dog."
        self.text2 = "A quick brown dog jumps over the sleeping fox."

    def test_preprocess_text(self):
        """Testa pré-processamento básico de texto."""
        processed = preprocess_text(self.text1)
        self.assertIsInstance(processed, str)
        self.assertTrue(len(processed) > 0)
        # Não deve conter stopwords comuns
        self.assertNotIn("the", processed.lower().split())

    def test_tfidf_similarity(self):
        """Testa cálculo de similaridade TF-IDF."""
        score = compute_tfidf_similarity(self.text1, self.text2)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)

    def test_bert_similarity(self):
        """Testa cálculo de similaridade via BERT."""
        score = compute_bert_similarity(self.text1, self.text2)
        self.assertGreaterEqual(score, -1)
        self.assertLessEqual(score, 1)


class ComplianceAPITest(unittest.TestCase):
    def setUp(self):
        """Configuração inicial da API para testes."""
        self.app = app.test_client()
        self.app.testing = True
        self.valid_payload = {
            "doc_reference": "This is a regulatory document with compliance rules.",
            "doc_submitted": "This document follows compliance regulations."
        }

    def test_compliance_api(self):
        """Teste básico do endpoint /check_compliance."""
        response = self.app.post('/check_compliance', json=self.valid_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("conformity_score", data)
        self.assertGreaterEqual(data["conformity_score"], 0.5)

    def test_missing_fields(self):
        """Testa erro quando campos obrigatórios estão faltando."""
        # Teste sem doc_reference
        response = self.app.post('/check_compliance', json={
            "doc_submitted": "Some text"
        })
        self.assertEqual(response.status_code, 400)

        # Teste sem doc_submitted
        response = self.app.post('/check_compliance', json={
            "doc_reference": "Some text"
        })
        self.assertEqual(response.status_code, 400)

    def test_empty_fields(self):
        """Testa erro quando campos estão vazios."""
        response = self.app.post('/check_compliance', json={
            "doc_reference": "",
            "doc_submitted": ""
        })
        self.assertEqual(response.status_code, 400)

    def test_invalid_json(self):
        """Testa erro com JSON inválido."""
        response = self.app.post('/check_compliance', data="invalid json")
        self.assertEqual(response.status_code, 400)

    def test_large_documents(self):
        """Testa processamento de documentos grandes."""
        large_text = "word " * 1000  # Texto com 1000 palavras
        response = self.app.post('/check_compliance', json={
            "doc_reference": large_text,
            "doc_submitted": large_text
        })
        self.assertEqual(response.status_code, 200)

    def test_unicode_support(self):
        """Testa suporte a caracteres Unicode/non-ASCII na API."""
        response = self.app.post('/check_compliance', json={
            "doc_reference": "Texto com acentuação é válido! 🔍",
            "doc_submitted": "Mais um texto com acentuação. 📝"
        })
        self.assertEqual(response.status_code, 200)


class GetSuggestionsAPITest(unittest.TestCase):
    """Testes para o endpoint /get_suggestions."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_suggestions_basic(self):
        """Teste básico do endpoint /get_suggestions."""
        response = self.app.post('/get_suggestions', json={
            "input": "Como melhorar a conformidade?"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("suggestion", data)

    def test_missing_input(self):
        """Testa erro quando input está faltando."""
        response = self.app.post('/get_suggestions', json={})
        self.assertEqual(response.status_code, 400)

    def test_empty_input(self):
        """Testa erro quando input está vazio."""
        response = self.app.post('/get_suggestions', json={"input": ""})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()