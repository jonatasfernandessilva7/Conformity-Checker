"""Funções utilitárias para salvar e carregar dados JSON.

Fornece wrappers simples para gravar e ler arquivos JSON em um
diretório (padrão: `data/`). Essas funções são usadas pelo projeto
para armazenar metadados ou resultados de processamento.
"""

import os
import json


def save_json(data, filename, directory="data"):
    """Salva um dicionário como um arquivo JSON.

    Args:
        data (dict): O objeto/dicionário a ser salvo.
        filename (str): Nome do arquivo JSON a ser criado (ex.: "a.json").
        directory (str): Diretório onde o arquivo será salvo. Cria o
            diretório se não existir.

    Returns:
        str: Caminho completo do arquivo salvo.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    filepath = os.path.join(directory, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    return filepath


def load_json(filename, directory="data"):
    """Carrega e retorna o conteúdo de um arquivo JSON.

    Args:
        filename (str): Nome do arquivo JSON a ser lido.
        directory (str): Diretório onde o arquivo está localizado.

    Returns:
        dict: Conteúdo do arquivo JSON como dicionário Python.

    Raises:
        FileNotFoundError: Se o arquivo não existir no diretório.
    """
    filepath = os.path.join(directory, filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"O arquivo {filepath} não foi encontrado.")

    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# Teste rápido das funções quando executado como script
if __name__ == "__main__":
    sample_data = {"example": "This is a test."}
    save_json(sample_data, "sample.json")
    loaded_data = load_json("sample.json")
    print("Dados carregados:", loaded_data)
