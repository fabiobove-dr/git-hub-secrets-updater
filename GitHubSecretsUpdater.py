import os
import requests
import json

class GitHubSecretsUpdater:
    def __init__(self, repo_owner, repo_name, github_token, secrets_file_path):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token
        self.secrets_file_path = secrets_file_path
    
    def initialize_secrets(self):
        # Read the secrets file
        with open(self.secrets_file_path, "r") as f:
            secrets_data = json.load(f)

        # Initialize each secret
        for secret_name, secret_value in secrets_data.items():
            # Build the URL to create or update the secret
            url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions/secrets/{secret_name}"
            
            # Define the request headers
            headers = {
                "Authorization": f"Bearer {self.github_token}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            # Define the request payload
            payload = {
                "encrypted_value": f"{secret_value}",
                "key_id": f"{os.environ.get('GITHUB_ACTIONS_PUBLIC_KEY_ID')}"
            }
            
            # Send the request to create or update the secret
            response = requests.put(url, headers=headers, json=payload)
            
            # Check the response status code
            if response.status_code == 201:
                print(f"Secret '{secret_name}' created or updated successfully!")
            else:
                print(f"Failed to create or update secret '{secret_name}'. Response: {response.content}")

