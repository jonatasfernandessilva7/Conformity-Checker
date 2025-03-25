import ollama
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    try:
        # Verifica se há dados JSON e extrai o input
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        user_input = data.get('input', '')

        if not user_input:
            return jsonify({"error": "Input text is required"}), 400

        # Chama o modelo Gemma (verifique o nome exato do modelo instalado)
        response = ollama.chat(
            model="gemma3:1b",  # Pode ser "gemma:2b" ou outro modelo disponível
            messages=[{
                "role": "user",
                "content": user_input
            }]
        )

        # A resposta correta está em response['message']['content']
        if 'message' in response and 'content' in response['message']:
            return jsonify({"suggestion": response['message']['content']})
        else:
            return jsonify({"error": "Unexpected response format from Ollama"}), 500

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    # Verifica se o Ollama está rodando e o modelo está disponível
    try:
        models = ollama.list()
        print("Modelos disponíveis:", models)
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Erro ao conectar com Ollama: {e}")
        print("Certifique-se que o Ollama está instalado e rodando")