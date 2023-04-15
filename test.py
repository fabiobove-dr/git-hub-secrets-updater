import yaml
from GitHubSecretsUpdater import GitHubSecretsUpdater


def test():
    # Load the oauth_settings.yml file
    stream = open('oauth_settings.yml', 'r')
    settings = yaml.load(stream, yaml.SafeLoader)

    # Define the necessary variables
    repo_owner = settings['repo_owner']
    repo_name = settings['repo_name']
    github_token = settings['github_token']
    secrets_file_path = "secrets.json"

    # Initialize the GitHubSecrets object
    github_secrets = GitHubSecretsUpdater(repo_owner, repo_name, github_token, secrets_file_path)

    # Call the initialize_secrets method
    github_secrets.initialize_secrets()