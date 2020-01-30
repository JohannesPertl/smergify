import logging
import os
import re
import sys

import spotipy
import yaml
from spotipy import util

from server.entities import Group, User, Artist

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
        client_id=CONFIG["app-id"],
        client_secret=CONFIG["app-secret"],
        redirect_uri=CONFIG["redirect-uri"],
        show_dialog=True,
        cache_path=cache_path
    )
    if not token:
        logging.critical(f"File for user authentication named .cache-{user_name} does not exist! Exiting..")
        sys.exit(1)

    return token


def create_top_artists_from_user(user, time_range):
    artists = list()
    spotify = spotipy.Spotify(auth=user.token)
    spotify_artists = (spotify.current_user_top_artists(limit=50, time_range=time_range))["items"]
    for a in spotify_artists:
        name = a['name']
        id = a['uri']
        artist = Artist(
            artist_name=name,
            artist_id=id,
            time_range=time_range
        )
        artists.append(artist)
    return artists


def create_artists_for_users(users):
    artists = list()
    for u in users:
        short_term_artists = create_top_artists_from_user(u, "short_term")
        medium_term_artists = create_top_artists_from_user(u, "medium_term")
        long_term_artists = create_top_artists_from_user(u, "long_term")

        artists += short_term_artists + medium_term_artists + long_term_artists

    return artists


def main():
    if arguments_given():
        groups = create_groups_from_arguments()
    else:
        groups = create_groups_from_path(GROUPS_PATH)

    users = create_users_for_groups(groups)
    artists = create_artists_for_users(users)


if __name__ == "__main__":
    main()
