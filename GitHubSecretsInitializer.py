import base64
import json
import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class GitHubSecretsInitializer:
    def __init__(self, repo_owner, repo_name, github_token):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.github_token = github_token
        self.base_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/actions"
        self.headers = {"Authorization": f"Bearer {self.github_token}"}

    def _get_public_key_url(self):
        return f"{self.base_url}/secrets/public-key"

    def _get_secret_url(self, name):
        return f"{self.base_url}/secrets/{name}"

    def get_public_key(self):
        try:
            response = requests.get(self._get_public_key_url(), headers=self.headers)
            response.raise_for_status()
            public_key = response.json()["key"]
            return rsa.RSAPublicKey.from_base64(public_key)
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving public key: {e}")
            raise

    def _get_secrets_from_file(self, secrets_file):
        try:
            with open(secrets_file, "r") as f:
                secrets = json.load(f)
                if not isinstance(secrets, list):
                    raise ValueError("Secrets file should contain a list of secrets.")
                return secrets
        except (OSError, json.JSONDecodeError) as e:
            print(f"Error loading secrets file: {e}")
            raise

    def _update_secret(self, name, encrypted_value):
        url = self._get_secret_url(name)
        payload = {"encrypted_value": encrypted_value}
        response = requests.put(url, headers=self.headers, json=payload)
        return response

    def update_secrets(self, secrets_file):
        secrets = self._get_secrets_from_file(secrets_file)
        public_key = self.get_public_key()

        for secret in secrets:
            name = secret["name"]
            value = secret["value"]
            encoded_secret_value = base64.b64encode(value.encode("utf-8")).decode("utf-8")
            encrypted_value = public_key.encrypt(encoded_secret_value.encode("utf-8"), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).hex()

            try:
                response = self._update_secret(name, encrypted_value)
                if response.status_code != 201:
                    print(f"Error initializing secret '{name}': {response.json()}")
                else:
                    print(f"Secret '{name}' successfully initialized.")
            except requests.exceptions.RequestException as e:
                print(f"Error initializing secret '{name}': {e}")
