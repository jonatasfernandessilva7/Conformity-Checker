import ollama
from flask import Flask, request, jsonify
import logging

# Configura logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicia o aplicativo Flask
app = Flask(__name__)


# Endpoint para receber mensagens e retornar as sugestões
@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    try:
        # Pega o texto enviado na requisição
        data = request.get_json()
        user_input = data.get('input', '')

        if not user_input:
            return jsonify({"error": "Input text is required."}), 400

        logger.info(f"Received input: {user_input}")

        # Envia o texto para o modelo Gemma no Ollama
        response = ollama.chat(
            model="gemma3:1b",  # ou "gemma:2b" dependendo do modelo instalado
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


if __name__ == '__main__':
    # Verifica se o modelo está disponível
    try:
        models = ollama.list()
        logger.info(f"Available models: {models}")
    except Exception as e:
        logger.error(f"Error connecting to Ollama: {str(e)}")

    # Rodar a aplicação Flask localmente
    app.run(debug=True, host='0.0.0.0', port=5000)