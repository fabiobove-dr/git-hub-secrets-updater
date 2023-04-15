# git-hub-secrets-updater
 a simple script that updates your secrets for a repo based on the content of a json file

# What you need ?
    - oauth_settings.yml file, which is something like:
        repo_owner: "some-strange-name-goes-here"
        repo_name: "foo-mega-wooo-repo"
        github_token: "asdasdadaklfafafmamfa_donthopethisworks_asdadakkkosda"

<<<<<<< HEAD
    - <b>secrets.json** file, contains the secrets you want to set:
=======
    - secrets.json file, contains the secrets you want to set:
>>>>>>> 1b4839607f4c29f75352b49824177ed95ef4ce7a
        {
            "SHHH": "something_to_hide",
            "MMMM": "secret_text"
        }

      *Note* if the secret exists it gets updated
