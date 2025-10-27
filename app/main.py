"""API simples para obter sugestões de um modelo local via Ollama.

Este módulo expõe um endpoint Flask `/get_suggestions` que recebe um
JSON com a chave `input` contendo o texto do usuário e retorna a
sugestão gerada pelo modelo instalado no Ollama.

Observações:
- Requer o serviço Ollama rodando localmente e um modelo compatível
  (por exemplo, `gemma3:1b`).
- Em produção, ajuste os parâmetros de `ollama.chat` (temperature,
  num_predict) conforme necessário e proteja o endpoint.
"""

import ollama
from flask import Flask, request, jsonify
import logging
from models.compliance_model import ComplianceModel

# Configura logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicia o aplicativo Flask
app = Flask(__name__)


@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    """Recebe um JSON com chave 'input' e retorna sugestão do modelo.

    Espera um corpo JSON como: {"input": "texto do usuário"}.

    Retorna JSON com `suggestion` em caso de sucesso ou mensagem de
    erro com o código HTTP apropriado.

    Erros possíveis:
    - 400: Requisição inválida ou `input` ausente.
    - 500: Erro interno (ex.: falha ao chamar Ollama ou formato
           inesperado de resposta).
    """
    try:
        # Pega o texto enviado na requisição
        data = request.get_json()
        user_input = data.get('input', '')

        if not user_input:
            return jsonify({"error": "Input text is required."}), 400

        logger.info(f"Received input: {user_input}")

        # Envia o texto para o modelo Gemma no Ollama
        response = ollama.chat(
            model="llama3.2:latest",  # ou "gemma:2b" dependendo do modelo instalado
            messages=[
                {"role": "user", "content": user_input}
            ],
            options={
                'temperature': 0.7,
                'num_predict': 128
            }
        )

        # Extrai e retorna a resposta do modelo
        if 'message' in response and 'content' in response['message']:
            response_message = response['message']['content']
            logger.info(f"Generated response: {response_message}")
            return jsonify({"suggestion": response_message})
        else:
            logger.error(f"Unexpected response format: {response}")
            return jsonify({"error": "Unexpected response format from Ollama"}), 500

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"error": str(e)}), 500



@app.route('/check_compliance', methods=['POST'])
def check_compliance():
    """Endpoint simples para avaliar conformidade entre dois textos.

    Espera JSON com chaves: `doc_reference` e `doc_submitted`.
    Retorna JSON com `conformity_score` (float entre 0 e 1).
    """
    try:
        data = request.get_json()
        doc_ref = data.get('doc_reference', '')
        doc_sub = data.get('doc_submitted', '')

        if not doc_ref or not doc_sub:
            return jsonify({"error": "doc_reference and doc_submitted are required."}), 400

        model = ComplianceModel()
        score = model.compute_similarity(doc_ref, doc_sub)

        # Garantir tipo serializável (float nativo)
        return jsonify({"conformity_score": float(score)}), 200
    except Exception as e:
        logger.error(f"Error in check_compliance: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Verifica se o modelo está disponível
    try:
        models = ollama.list()
        logger.info(f"Available models: {models}")
    except Exception as e:
        logger.error(f"Error connecting to Ollama: {str(e)}")

    # Rodar a aplicação Flask localmente
    app.run(debug=True, host='0.0.0.0', port=5000)