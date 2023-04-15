import yaml
from GitHubSecretsInitializer import GitHubSecretsInitializer


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
    github_secrets = GitHubSecretsUpdater(repo_owner, repo_name, github_token)

    try:
        github_secrets.initialize_secrets(secrets_file_path)
    except Exception as e:
        print(f"Error initializing secrets: {e}")


if __name__ == '__main__':
    test()