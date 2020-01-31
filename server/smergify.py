import os
import random
import re
import sys
import yaml

from server import DB
from server.entities import User, Song, Group, Artist

# Constants
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
GROUPS_PATH = os.path.join(ROOT_PATH, "user_groups")

# CONFIG
with open("config.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)


def main():
    # Create and link entities
    groups = create_groups_from_arguments() if arguments_given() else create_all_groups()
    users = create_users_for_groups(groups)
    artists = create_artists_for_users(users)
    songs = create_artist_songs(artists, users[0].spotify)  # Spotify needs a user token to make requests

    # Save to database
    db = DB(CONFIG["database"])
    db.insert_groups(groups)
    db.insert_artists(artists)
    db.insert_users(users)
    db.insert_songs(songs)

    # Create playlists for every user in every group
    for group in groups:
        group_songs = get_songs_for_group(db, group)
        playlist_songs = randomize_songs(group_songs)
        for user in group.users:
            create_or_update_playlist(group.group_name, user, playlist_songs)


# BUG: Playlist must public or else it can't be found
def get_playlist_id_by_name(user, name):
    playlists = user.spotify.user_playlists(user.spotify_id)["items"]
    existing_playlists = [p['id'] for p in playlists if p['name'] == name]
    return existing_playlists[0] if existing_playlists else False


def create_or_update_playlist(name, user, song_ids, public=True):
    playlist_id = get_playlist_id_by_name(user, name)
    if playlist_id:
        # Updating playlist
        user.spotify.user_playlist_replace_tracks(user, playlist_id, song_ids)
    else:
        # Creating new playlist
        playlist = user.spotify.user_playlist_create(user.spotify_id, name, public=public)
        user.spotify.user_playlist_add_tracks(user.user_id, playlist['id'], song_ids)


def arguments_given():
    return len(sys.argv) > 1


def create_group(name):
    group_path = os.path.join(GROUPS_PATH, name)
    return Group(
        group_name=name,
        group_path=group_path
    )


def create_groups_from_arguments():
    groups = list()
    for name in sys.argv:
        new_group = create_group(name)
        groups.append(new_group)
    return groups


def create_all_groups():
    groups = list()
    for f in os.scandir(GROUPS_PATH):
        if f.is_dir():
            new_group = create_group(f.name)
            groups.append(new_group)
    return groups


def create_users_for_groups(groups):
    users_to_return = list()

    for group in groups:
        for file in os.scandir(group.group_path):
            if file.is_file() and file.name.startswith(".cache-"):
                user_name = re.sub(r"\.cache-", "", file.name)  # Read username from cache file by cutting .cache-
                user = User(
                    user_name=user_name,
                    user_group=group
                )
                group.users.append(user)
                users_to_return.append(user)

    return users_to_return


def create_artists_for_users(users):
    artists = list()
    for user in users:
        short_term_artists = create_user_artists_in_term(user, "short_term")
        medium_term_artists = create_user_artists_in_term(user, "medium_term")
        long_term_artists = create_user_artists_in_term(user, "long_term")

        artists += short_term_artists + medium_term_artists + long_term_artists
    return artists


def create_user_artists_in_term(user, time_range):
    artists_to_return = list()

    spotify_artists = (user.spotify.current_user_top_artists(limit=50, time_range=time_range))["items"]
    for artist in spotify_artists:
        name = artist['name']
        id = artist['uri']
        artist = Artist(
            artist_name=name,
            artist_id=id,
            time_range=time_range
        )
        user.artists.append(artist)
        artists_to_return.append(artist)

    return artists_to_return


def create_artist_songs(artists, spotify):
    songs_to_return = list()

    for artist in artists:
        top_tracks = spotify.artist_top_tracks(artist.artist_id)["tracks"]
        for track in top_tracks:
            song_title = track["name"]
            song_id = track["uri"]

            song = Song(
                song_title=song_title,
                song_id=song_id,
                artist=artist)

            songs_to_return.append(song)
            artist.songs.append(song)

    return songs_to_return


def get_songs_for_group(db, group):
    if group.is_pair():
        pair_songs = db.get_matched_song_ids_for_two_users(group)
        if len(pair_songs) > CONFIG['minimum-playlist-size']:
            return pair_songs
    return db.get_matched_song_ids_for_group(group)


def randomize_songs(songs):
    max_size = CONFIG['maximum-playlist-size']
    return songs if len(songs) < max_size else random.sample(songs, max_size)


if __name__ == "__main__":
    main()
