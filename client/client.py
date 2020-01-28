import paramiko
import yaml


with open("credentials.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)


def main():
    # TODO: get user_name and user_group as input - for multiple users (dictionary of users = { "user" : "group"} ) - till exit

    ssh = create_ssh_connection(
        CONFIG["username"],
        CONFIG["hostname"],
        CONFIG["port"],
        CONFIG["private-key-file"],
        CONFIG["password"]
    )
    # TODO: get user token for spotify via prompt to create for each user in dict one cache file
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
