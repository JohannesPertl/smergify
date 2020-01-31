import logging
import os
import sys

import spotipy
import yaml
from spotipy import util

SCOPE = "user-top-read playlist-modify-public user-top-read playlist-modify-private"
with open("config.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)


class User:
    def __init__(self, user_name, user_group=None, artists=None):
        if artists is None:
            artists = list()
        self.user_name = user_name
        self.user_group = user_group
        self.artists = artists
        self.spotify = self.authenticate(
            CONFIG["app-id"],
            CONFIG["app-secret"],
            CONFIG["redirect-uri"],
            SCOPE
        )
        self.user_id = self.get_uri_from_spotify()
        self.spotify_id = self.get_id_from_spotify()

    def to_tuple(self):
        return self.user_id, self.user_name

    def get_uri_from_spotify(self):
        user = self.spotify.current_user()
        return user["uri"]

    def get_id_from_spotify(self):
        user = self.spotify.current_user()
        return user["id"]

    def authenticate(self, app_id, app_secret, redirect_uri, scope, cache_path=None):
        if cache_path is None:
            group_path = self.user_group.group_path
            file_name = ".cache-" + self.user_name
            cache_path = os.path.join(group_path, file_name)

        token = util.prompt_for_user_token(
            username=self.user_name,
            scope=scope,
            client_id=app_id,
            client_secret=app_secret,
            redirect_uri=redirect_uri,
            show_dialog=True,
            cache_path=cache_path
        )
        if not token:
            logging.critical(f"File for user authentication named .cache-{self.user_name} does not exist! Exiting..")
            sys.exit(1)

        return spotipy.Spotify(auth=token)
