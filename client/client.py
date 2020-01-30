import paramiko
import yaml
import spotipy.util as util

# get credentials from yaml
with open("credentials.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)

# permissions for spotify app
SCOPE = "user-top-read"


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

    cache_file = ".cache-" + user_name
    server_path = CONFIG["server-path"]

    # FTP client:
    ftp_client = ssh.open_sftp()

    # List files on server:
    dirs = ftp_client.listdir(server_path)

    # check + create directory for group:
    create_group_folder_serverside(dirs, server_path, user_group, ftp_client)

    # File transfer to server:
    target_path = server_path + user_group + "/" + cache_file
    transfer_file(ftp_client, cache_file, target_path)

    ftp_client.close()
    ssh.close()


# Spotify authentication + cache-file generation:
def user_authentication(user_name):
    token = util.prompt_for_user_token(
        username=user_name,
        scope=SCOPE,
        client_id=CONFIG["app-id"],
        client_secret=CONFIG["app-secret"],
        redirect_uri=CONFIG["redirect-uri"],
        show_dialog=True
    )
    if not token:
        user_authentication(user_name)


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


def transfer_file(ftp_client, source_path, target_path):
    ftp_client.put(source_path, target_path)


def create_group_folder_serverside(dirs, path, group_name, ftp_client):
    if group_name not in dirs:
        ftp_client.mkdir(path + group_name)


if __name__ == "__main__":
    main()
