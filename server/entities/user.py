import logging
import os
import sys
import spotipy
from spotipy import util
from datetime import datetime


class User:
    def __init__(self, user_name, user_group=None, artists=None):
        if artists is None:
            artists = list()
        self.user_name = user_name
        self.user_group = user_group
        self.artists = artists
        self.spotify = None
        self.user_id = None
        self.spotify_id = None
        self.last_updated = None

    def to_tuple(self):
        return self.user_id, self.user_name, self.last_updated
    
    def set_last_updated_to_now(self, datetime_format):
        self.last_updated = datetime.now().strftime(datetime_format)

    def authenticate_spotify(self, app_id, app_secret, redirect_uri, scope, cache_path=None):
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

        self.spotify = spotipy.Spotify(auth=token)
        self.user_id = self.spotify.current_user()["uri"]
        self.spotify_id = self.spotify.current_user()["id"]
