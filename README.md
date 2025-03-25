
# 🔍 Compliance Checker - Verificador de Conformidade

## 📌 Sobre o Projeto

Este projeto é um sistema de conformidade baseado em Inteligência Artificial (IA) feito através da Iniciação Cientifíca minha presente na Universidade de São Paulo e na Universidade Federal do Ceará, que compara um documento submetido com documentos reguladores de referência. Ele analisa a similaridade textual, utilizando técnicas avançadas de processamento de linguagem natural (NLP), e retorna um índice de conformidade expresso em porcentagem.

Este sistema pode ser aplicado em diversos cenários, como:

- Auditorias e Compliance: Avaliação automática de documentos em relação a regulamentos internos ou externos.

- Processos Jurídicos: Comparação de contratos e documentos legais.

- Normas Técnicas: Verificação de aderência a padrões de qualidade.

- Segurança da Informação: Análise de conformidade com políticas de segurança.


## 🚀 Tecnologias Utilizadas

O projeto foi desenvolvido utilizando as seguintes tecnologias:

- Python 3.8+

- Flask (API Web para interface com o usuário)

- NLTK e Scikit-Learn (Processamento de Texto e Similaridade Semântica)

- pdfplumber (Leitura para PDFs)

- SQLite (Banco de Dados para armazenamento de logs e metadados)

- pytest (Testes Automatizados para garantir robustez)


## 📂 Estrutura do Projeto

```bash
 compliance_checker/
│-- app/
│   │-- __init__.py      # Inicializador do módulo
│   │-- main.py          # API Flask
│   │-- similarity.py    # Função de cálculo de similaridade
│   ├── models/
│   │   │-- compliance_model.py  # Modelo de conformidade baseado em IA
│   ├── data/
│   │   ├── reference_docs/      # Documentos regulatórios de referência
│   │   ├── submitted_docs/      # Documentos submetidos para avaliação
│   ├── tests/
│   │   ├── test_api.py          # Testes da API
│   │   ├── test_similarity.py   # Testes das funções de similaridade
│-- README.md
│-- requirements.txt
│-- .gitignore
```

## 📌 Como Usar a API

Faça uma requisição POST para /check_compliance enviando um JSON com os seguintes parâmetros:

``` bash
{
  "doc_reference": "regulamento.pdf",
  "doc_submitted": "Este documento segue as normas."
}
```
O índice de conformidade retornado indica quão similar o documento submetido é em relação ao documento de referência.

## 🔬 Métodos Utilizados para Cálculo da Similaridade

O sistema utiliza diferentes abordagens para mensurar a similaridade textual:

- TF-IDF (Term Frequency-Inverse Document Frequency): Mede a importância de palavras-chave.

- Cosine Similarity: Avalia a similaridade vetorial entre textos.

- Jaccard Similarity: Mede a interseção entre conjuntos de palavras.

- Leitura de PDFs: Se o documento estiver em PDF, ele será processado usando pdfplumber.



