import os
import pdfplumber
from flask import Flask, request, jsonify
from models.compliance_model import ComplianceModel

app = Flask(__name__)
model = ComplianceModel()

REFERENCE_DOCS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/reference_docs/")


def load_reference_document(filename):
    """Carrega o conteúdo do documento de referência, suportando .txt e .pdf."""
    file_path = os.path.join(REFERENCE_DOCS_PATH, filename)

    if not os.path.exists(file_path):
        print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
        return None

    # Identificar a extensão do arquivo
    ext = os.path.splitext(filename)[-1].lower()

    if ext == ".txt":
        # Lê arquivos de texto normalmente
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    elif ext == ".pdf":
        # Extração de texto de PDFs com pdfplumber
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Erro ao processar PDF: {e}")
            return None

    else:
        print(f"Erro: Formato de arquivo '{ext}' não suportado.")
        return None


@app.route('/check_compliance', methods=['POST'])
def check_compliance():
    """Endpoint para verificar conformidade de um documento enviado."""
    data = request.get_json()

    print("Recebido:", data)  # Exibe os dados recebidos no terminal

    if not data:
        return jsonify({"error": "Nenhum JSON recebido ou formato incorreto."}), 400

    if 'doc_reference' not in data or 'doc_submitted' not in data:
        return jsonify({"error": "Faltam parâmetros obrigatórios. Esperado: 'doc_reference' e 'doc_submitted'."}), 400

    reference_text = load_reference_document(data['doc_reference'])
    if reference_text is None:
        return jsonify({"error": f"Documento de referência '{data['doc_reference']}' não encontrado."}), 404

    submitted_text = data['doc_submitted']
    similarity_score = model.compute_similarity(reference_text, submitted_text)

    return jsonify({"conformity_score": round(similarity_score, 2)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
