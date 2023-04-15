# git-hub-secrets-updater
    A simple python script that updates the secrets of a repo based on the content of a json file

# Why?
    The other day i wanted to create an old repo from scratch, the only issue? It had way toooo many secrets.
    Imagine you need to create secrets for a repo that uses: EC2, Docker Hub, MS Graph APIs, Django, Posrgres.
    I bet you'll like this quick fix.

# What you need ?
    - **oauth_settings.yml** file, which is something like:
        repo_owner: "some-strange-name-goes-here"
        repo_name: "foo-mega-wooo-repo"
        github_token: "asdasdadaklfafafmamfa_donthopethisworks_asdadakkkosda"

    - **secrets.json** file, contains the secrets you want to set:
        {
            "SHHH": "something_to_hide",
            "MMMM": "secret_text"
        }

      *Note* if the secret exists it gets updated
    
    - Open a terminal, write this:
        initialize_create_secrets.py

# Cheers!
    Fabio