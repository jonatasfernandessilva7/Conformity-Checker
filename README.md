
# 🔍 Conformity-Checker — Verificador de Conformidade

Pequeno projeto para comparar um documento submetido com documentos de
referência e estimar um índice de conformidade. Usa técnicas de NLP: TF‑IDF
e embeddings BERT (via transformers) para medir similaridade.

O repositório fornece:

- Um serviço HTTP (Flask) com dois endpoints principais:
  - POST /get_suggestions — encaminha o texto para um modelo local via
    Ollama e retorna a sugestão (requer Ollama + modelo instalado).
  - POST /check_compliance — calcula uma pontuação de conformidade entre
    dois textos usando `models.ComplianceModel` (BERT embeddings).

## 🧩 Estrutura principal

Principais arquivos e pastas:

- `app/main.py` — API Flask com endpoints `/get_suggestions` e
  `/check_compliance`.
- `models/compliance_model.py` — wrapper de alto nível que usa
  `utils/similaraty.BERTSimilarity`.
- `models/llama_sugestions.py` — exemplo de endpoint que chama Ollama
  (similar ao `app/main.py`).
- `utils/similaraty.py` — TF‑IDF e classe `BERTSimilarity` (transformers).
- `utils/text_processing.py` — pré‑processamento (spaCy) e helpers.
- `data/` — utilitários para salvar/carregar JSON e pastas para documentos.
- `tests/test.py` — testes unitários básicos.

## � Dependências

As dependências estão em `requirements.txt`. Principais pacotes:

- Flask
- torch
- scikit-learn
- transformers
- spacy

Observação: modelos BERT e o pacote `spacy[en]` podem baixar arquivos
grandes ao primeiro uso.

## ⚡ Como executar (Windows / PowerShell)

1) Criar e ativar um ambiente virtual (opcional, recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependências:

```powershell
python -m pip install -r requirements.txt
```

3) (Opcional) Instalar o modelo spaCy em inglês:

```powershell
python -m spacy download en_core_web_sm
```

4) Executar a API Flask:

```powershell
python app\main.py
```

O serviço ficará disponível em http://0.0.0.0:5000 por padrão.

## 🧪 Exemplos de uso

- Chamar `/check_compliance` (com PowerShell curl-like):

```powershell
Invoke-RestMethod -Uri http://localhost:5000/check_compliance -Method POST -Body (@{
    doc_reference = "This is a regulatory document with compliance rules."
    doc_submitted = "This document follows compliance regulations."
} | ConvertTo-Json) -ContentType 'application/json'
```

- Chamar `/get_suggestions` (requer Ollama rodando e modelo instalado):

```powershell
Invoke-RestMethod -Uri http://localhost:5000/get_suggestions -Method POST -Body (@{ input = "Me dê sugestões." } | ConvertTo-Json) -ContentType 'application/json'
```

## ✅ Testes

Executar os testes unitários:

```powershell
python -m unittest discover -s tests -p "test*.py"
```

Obs.: os testes podem demorar na primeira execução (download de pesos
do transformers). Eles assumem que o endpoint `/check_compliance` existe
e que é possível carregar os modelos BERT locais.

## Notas e recomendações

- O endpoint `/get_suggestions` depende do Ollama (https://ollama.ai/).
  Se não quiser usar Ollama, remova/ignore este endpoint.
- Carregar BERT pode consumir muita memória. Para produção, considere:
  - Pré‑computar embeddings e armazená‑los.
  - Usar modelos menores ou serviços especializados.
- Melhorar: adicionar tratamento de PDFs, armazenamento de documentos de
  referência, interface web e testes mais abrangentes.

## Licença

Verifique a licença do projeto (se aplicável) no repositório.



