import yaml
import json
import requests
import base64
import requests
import json
import requests
import json


if __name__ == "__main__":
    # Load the oauth_settings.yml file
    stream = open('oauth_settings.yml', 'r')
    settings = yaml.load(stream, yaml.SafeLoader)

    # Define the necessary variables
    repo_owner = settings['repo_owner']
    repo_name = settings['repo_name']
    github_token = settings['github_token']
    secrets_file_path = "secrets.json"

    # Construct API URL
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/public-key"
    headers = {"Authorization": f"Bearer {github_token}"}

    # Send request to GitHub API to get public key ID
    response = requests.get(base_url, headers=headers)
    response_json = response.json()
    public_key_id = response_json["key_id"]

    print(f"Public key ID for {repo_owner}/{repo_name}: {public_key_id}")

    # Read the secrets from the JSON file
    with open(secrets_file_path, "r") as secrets_file:
        secrets = json.load(secrets_file)

    # Loop through the secrets and create/update them in GitHub
    for secret_name, secret_value in secrets.items():
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/{secret_name}"
        headers = {"Authorization": f"Bearer {github_token}"}
        data = {
            "encrypted_value": base64.b64encode(secret_value.encode("utf-8")).decode("utf-8"),
             "key_id": public_key_id
        }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 201:
            print(f"Successfully created/updated secret '{secret_name}'")
        else:
            print(f"Error creating/updating secret '{secret_name}': {response.text}")

