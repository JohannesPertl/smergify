import glob
import os

import paramiko
import spotipy.util as util
import yaml

# get credentials from yaml
with open("config.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)

# permissions for spotify app
SCOPE = "user-top-read playlist-modify-public playlist-modify-private"


def main():
    # SSH Connection:
    ssh = create_ssh_connection(
        username=CONFIG["username"],
        hostname=CONFIG["hostname"],
        port=CONFIG["port"],
        rsa_key=CONFIG["private-key-file"],
        password=CONFIG["password"]
    )

    # User input for group-name:
    user_group = input_group_name()

    # FTP client:
    ftp_client = ssh.open_sftp()

    # Define paths
    server_path = CONFIG["server-path-to-groups"]

    # List files on server:
    dirs = ftp_client.listdir(server_path)

    # check + create directory for group:
    create_group_folder_serverside(dirs, server_path, user_group, ftp_client)

    # Get user input from 2 users + authenticate both + transfer .cache files to server
    user_list = []
    while True:
        user_name = input_user_name(user_list)

        user_authentication(user_name)

        cache_file = ".cache-" + user_name
        target_path = server_path + user_group + "/" + cache_file
        transfer_file(ftp_client, cache_file, target_path)

        user_list.append(user_name)
        if len(user_list) == 2:
            break

    ftp_client.close()

    # Execute Smergify remote from server
    stdin, stdout, stderr = ssh.exec_command("bash " + CONFIG["smergify-start-script"] + " " + user_group)

    ssh.close()

    delete_cache_files_on_client()


# Validate group name
def input_group_name():
    while True:
        group_name = input("Please enter your groupname: ")
        if group_name:
            group_name.replace(" ", "")  # Remove whitespace
            return group_name


# Validate username
def input_user_name(existing_users):
    while True:
        user_name = input("Please enter your username: ")
        if user_name and user_name not in existing_users:
            return user_name


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


def delete_cache_files_on_client():
    for f in glob.glob(".cache-*"):
        os.remove(f)


if __name__ == "__main__":
    main()
