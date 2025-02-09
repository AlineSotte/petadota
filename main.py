import json
import requests

def load_json(file_path: str) -> dict:
    """Lê um arquivo JSON e retorna os dados."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar JSON ({file_path}): {e}")
        return {}

def send_post_request(url: str, data: dict) -> requests.Response:
    """Envia uma requisição POST para a URL especificada com os dados fornecidos."""
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Erro ao enviar POST para {url}: {err}")
        return None

def send_get_request(url: str) -> requests.Response:
    """Envia uma requisição GET para a URL especificada."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as err:
        print(f"Erro ao enviar GET para {url}: {err}")
        return None

def process_responses(dog_response, webhook_response):
    """Processa as respostas das requisições e imprime mensagens de status."""
    if dog_response and dog_response.status_code == 200:
        if webhook_response and webhook_response.status_code == 200:
            print('Enviado com sucesso')
        else:
            print(f'Erro ao enviar webhook: {webhook_response.status_code if webhook_response else "N/A"}')
    else:
        print(f'Erro ao acessar API de cães: {dog_response.status_code if dog_response else "N/A"}')

def main():
    config_path = 'caminho arquivo'
    data_path = 'caminho arquivo'
    
    config = load_json(config_path)
    dog_data = load_json(data_path)
    
    if not config or 'dogs_url' not in config or 'webhook_url' not in config:
        print("Configurações inválidas.")
        return
    
    dog_response = send_get_request(config['dogs_url'])
    webhook_response = send_post_request(config['webhook_url'], dog_data)
    
    process_responses(dog_response, webhook_response)

if __name__ == "__main__":
    main()
