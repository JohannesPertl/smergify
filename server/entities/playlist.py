import logging
from datetime import datetime


class Playlist:
    def __init__(self, name, user, songs):
        self.name = name
        self.user = user
        self.songs = songs

    # BUG: Playlist must public or else it can't be found
    def get_id_by_name(self):
        playlists = self.user.spotify.user_playlists(self.user.spotify_id)["items"]
        existing_playlists = [p['id'] for p in playlists if p['name'] == self.name]
        return existing_playlists[0] if existing_playlists else False

    def create_or_update_spotify_playlist(self, public=True):
        """Create new playlist or update the tracks it's already existing"""
        playlist_id = self.get_id_by_name()
        if playlist_id:
            # Updating playlist
            self.user.spotify.user_playlist_replace_tracks(self.user, playlist_id, self.songs)
            logging.info(f"[{datetime.now()}] Playlist \"{self.name}\" was updated for user \"{self.user.user_name}\"")
        else:
            # Creating new playlist
            playlist = self.user.spotify.user_playlist_create(self.user.spotify_id, self.name, public=public)
            self.user.spotify.user_playlist_add_tracks(self.user.user_id, playlist['id'], self.songs)
            logging.info(
                f"[{datetime.now()}] New playlist \"{self.name}\" was created for user \"{self.user.user_name}\"")

