import logging
import os
import re
import sys
import yaml
import spotipy
from spotipy import util
from server.entities import Group, User

with open("config.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)

# Constants
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
GROUPS_PATH = os.path.join(ROOT_PATH, "user_groups")
SCOPE = "user-top-read"


def arguments_given():
    return len(sys.argv) > 1


def create_groups_from_arguments():
    groups = list()
    for name in sys.argv:
        groups.append(Group(name))
    return groups


def create_groups_from_path(path):
    groups = list()
    for f in os.scandir(path):
        if f.is_dir():
            groups.append(Group(f.name))
    return groups


def create_users_for_groups(groups):
    users_to_return = list()
    for g in groups:
        group_path = os.path.join(GROUPS_PATH, g.group_name)
        for file in os.scandir(group_path):
            if file.is_file() and file.name.startswith(".cache-"):
                user_name = re.sub(r"\.cache-", "", file.name)  # Read username from cache file by cutting .cache-

                cache_path = os.path.join(group_path, file.name)  # build cache path

                spotify_token = authenticate_user(user_name, cache_path)
                user_id = get_user_id_from_spotify(spotify_token)
                user = User(user_name, user_id, spotify_token, g)
                g.users.append(user)
                users_to_return.append(user)
    return users_to_return


def get_user_id_from_spotify(token):
    spotify = spotipy.Spotify(auth=token)
    user = spotify.current_user()
    return user["uri"]


def authenticate_user(user_name, cache_path):
    token = util.prompt_for_user_token(
        username=user_name,
        scope=SCOPE,
        client_id=CONFIG["app_id"],
        client_secret=CONFIG["app_secret"],
        redirect_uri=CONFIG["redirect_uri"],
        show_dialog=True,
        cache_path=cache_path
    )
    if not token:
        logging.critical(f"File for user authentication named .cache-{user_name} does not exist! Exiting..")
        sys.exit(1)

    return token


def main():
    if arguments_given():
        groups = create_groups_from_arguments()
    else:
        groups = create_groups_from_path(GROUPS_PATH)

    users = create_users_for_groups(groups)


if __name__ == "__main__":
    main()
