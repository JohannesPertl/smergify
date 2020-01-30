import spotipy
import spotipy.util as util
from datetime import date


def get_playlist_id(spotify, user, playlist_name):
    playlists = spotify.user_playlists(user.user_id)
    for playlist in playlists["items"]:
        if playlist['name'] == playlist_name:
            return playlist['id']


def create_playlist(spotify, user, playlist_name):
    spotify.user_playlist_create(user.user_id, playlist_name, public=True, description='new playlist')


def add_tracks_to_playlist(spotify, user, songs, playlist_name):
    song_ids = []
    for song in songs:
        song_ids.append(song.song_id)

    spotify.user_playlist_add_tracks(user.user_id, get_playlist_id(spotify, user, playlist_name), song_ids)


def create(users, songs):
    client_id = "88b65a918f0842528243cd7a0b7c5666"
    client_secret = "3d114ac863654ba19f9d5faae6db4be8"
    playlist_name = "Mix - " + date.today().strftime("%d.%m.%Y")
    for user in users:
        # print(user.user_name)
        scope = "playlist-modify-public user-top-read playlist-modify-private"
        token = util.prompt_for_user_token(user.user_name, scope, client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost')
        if token:
            spotify = spotipy.Spotify(auth=token)
            create_playlist(spotify, user, playlist_name)
            add_tracks_to_playlist(spotify, user, songs, playlist_name)








