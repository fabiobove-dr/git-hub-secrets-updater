# Import necessary libraries
import yaml  # Library to parse YAML files
import json  # Library to handle JSON data
import requests  # Library to make HTTP requests
import base64  # Library to encode/decode data in Base64 format

# Main function
if __name__ == "__main__":
    # Load the oauth_settings.yml file
    stream = open('oauth_settings.yml', 'r')  # Open the YAML file in read-only mode
    settings = yaml.load(stream, yaml.SafeLoader)  # Load the YAML data into a dictionary

    # Define the necessary variables
    repo_owner = settings['repo_owner']  # The username of the repository owner
    repo_name = settings['repo_name']  # The name of the repository
    github_token = settings['github_token']  # The personal access token for authentication
    secrets_file_path = "secrets.json"  # The path to the JSON file containing the secrets

    # Construct API URL
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/public-key"  # The URL for the GitHub API endpoint that retrieves the public key
    headers = {"Authorization": f"Bearer {github_token}"}  # The HTTP headers for authentication

    # Send request to GitHub API to get public key ID
    response = requests.get(base_url, headers=headers)  # Send a GET request to the API endpoint to retrieve the public key
    response_json = response.json()  # Parse the response as JSON data
    public_key_id = response_json["key_id"]  # Extract the key ID from the response

    print(f"Public key ID for {repo_owner}/{repo_name}: {public_key_id}")  # Print the key ID to the console

    # Read the secrets from the JSON file
    with open(secrets_file_path, "r") as secrets_file:  # Open the JSON file in read-only mode
        secrets = json.load(secrets_file)  # Load the JSON data into a dictionary

    # Loop through the secrets and create/update them in GitHub
    for secret_name, secret_value in secrets.items():  # Iterate over the key-value pairs in the dictionary
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/actions/secrets/{secret_name}"  # The URL for the GitHub API endpoint that creates/updates a secret
        headers = {"Authorization": f"Bearer {github_token}"}  # The HTTP headers for authentication
        data = {  # The data to send in the request body
            "encrypted_value": base64.b64encode(secret_value.encode("utf-8")).decode("utf-8"),  # The Base64-encoded value of the secret
            "key_id": public_key_id  # The ID of the public key
        }
        response = requests.put(url, headers=headers, json=data)  # Send a PUT request to the API endpoint to create/update the secret
        if response.status_code == 201:  # Check if the request was successful (HTTP status code 201 indicates success)
            print(f"Successfully created/updated secret '{secret_name}'")  # Print a success message to the console
        else:
            print(f"Error creating/updating secret '{secret_name}': {response.text}")  # Print an error message to the console if the request was not successful
