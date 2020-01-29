import paramiko
import yaml
import spotipy
import spotipy.util as util

with open("credentials.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)

SCOPE = "user-top-read"


def user_authentication(user_name):
    # Spotify Auth + .cache File Generierung:
    token = util.prompt_for_user_token(
        username=user_name,
        scope=SCOPE,
        client_id=CONFIG["app_id"],
        client_secret=CONFIG["app_secret"],
        redirect_uri=CONFIG["redirect_uri"],
        show_dialog=True
    )
    if not token:
        user_authentication()


def main():
    # User Input:
    user_name = input("Please enter your username: ")
    user_group = input("Please enter your groupname: ")

    user_authentication(user_name)

    # SSH Connection:
    ssh = create_ssh_connection(
        username=CONFIG["username"],
        hostname=CONFIG["hostname"],
        port=CONFIG["port"],
        rsa_key=CONFIG["private-key-file"],
        password=CONFIG["password"]
    )

    # TODO: transfer cache file to server (target: folder named like group). If folder already exists...

    ssh.close()


def create_ssh_connection(username, hostname, port=22, rsa_key=None, password=None):
    key = paramiko.RSAKey.from_private_key_file(rsa_key, password=password)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(
        hostname=hostname,
        username=username,
        pkey=key,
        port=port
    )

    return ssh


if __name__ == "__main__":
    main()
