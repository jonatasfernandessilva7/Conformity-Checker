import os
import json


def save_json(data, filename, directory="data"):
    """Salva um dicionário como um arquivo JSON no diretório especificado."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return filepath


def load_json(filename, directory="data"):
    """Carrega um arquivo JSON do diretório especificado e retorna seu conteúdo."""
    filepath = os.path.join(directory, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado.")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# Teste das funções
if __name__ == "__main__":
    sample_data = {"example": "This is a test."}
    save_json(sample_data, "sample.json")
    loaded_data = load_json("sample.json")
    print("Dados carregados:", loaded_data)
