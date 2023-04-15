import os
import requests
import json

class GitHubSecretsUpdater:
    def __init__(self, repo_owner: str, repo_name: str, github_token: str, secrets_file_path: str) -> None:
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token
        self.secrets_file_path = secrets_file_path
    
    def initialize_secrets(self) -> None:
        try:
            with open(self.secrets_file_path, "r") as f:
                secrets_data = json.load(f)
        except Exception as e:
            print(f"An error occurred while reading the secrets file: {e}")
            return
        
        for secret_name, secret_value in secrets_data.items():
            try:
                url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/secrets/{secret_name}"
                headers = {
                    "Authorization": f"Bearer {self.github_token}",
                    "Accept": "application/vnd.github.v3+json"
                }
                payload = {
                    "encrypted_value": f"{secret_value}",
                    "key_id": f"{os.environ.get('GITHUB_ACTIONS_PUBLIC_KEY_ID')}"
                }
                response = requests.put(url, headers=headers, json=payload)
                response.raise_for_status()
                
                print(f"Secret '{secret_name}' created or updated successfully!")
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error: {errh}")
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                print(f"An error occurred while sending the request: {err}")
    
