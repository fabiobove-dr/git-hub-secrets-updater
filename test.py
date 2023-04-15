from GitHubSecretsUpdater import GitHubSecretsUpdater

def test():

    
    # Define the necessary variables
    repo_owner = "your-repo-owner"
    repo_name = "your-repo-name"
    github_token = "your-github-token"
    secrets_file_path = "/path/to/secrets/file.json"

    # Initialize the GitHubSecrets object
    github_secrets = GitHubSecretsUpdater(repo_owner, repo_name, github_token, secrets_file_path)

    # Call the initialize_secrets method
    github_secrets.initialize_secrets()