import json
import requests

dog_data = {
    "name": "Pipoca",
    "breed": "Labrador",
    "age": 2,
    "color": "Amarelo",
    "location": "Juiz de Fora",
    "adoption_status": "Available"
}

def load_config(config_file: str) -> dict:
    """Lê um arquivo JSON e retorna as configurações."""
    try:
        with open(config_file, "r") as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erro ao carregar configuração: {e}")
        return {}

def send_request(url: str, data: dict) -> requests.Response:
    """Envia uma requisição POST para a URL fornecida."""
    try:
        response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
        response.raise_for_status() 
        return response
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except requests.RequestException as req_err:
        print(f"Erro de requisição: {req_err}")
    return None

def send_webhook(dog: dict, config_file: str) -> None:
    """Envia os dados do cachorro para a API e Webhook."""
    config = load_config(config_file)
    
    if not config or "webhook_url" not in config or "dogs_url" not in config:
        print("Erro: Configuração inválida ou URLs ausentes.")
        return
    
    response_api = send_request(config["dogs_url"], dog)
    if response_api:
        print("API: Enviado com sucesso.")
    else:
        print("Erro ao enviar para a API.")
    
    response_webhook = send_request(config["webhook_url"], dog)
    if response_webhook:
        print("Webhook: Enviado com sucesso.")
    else:
        print("Erro ao enviar para o Webhook.")

def main(dog: dict, config_file: str = "config.json") -> None:
    """Executa o envio dos dados do cachorro."""
    send_webhook(dog, config_file)

if __name__ == "__main__":
    main(dog_data)
