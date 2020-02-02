import logging
import os
import random
import re
import sys
from datetime import datetime

import yaml

from server.db import DB
from server.entities.artist import Artist
from server.entities.group import Group
from server.entities.playlist import Playlist
from server.entities.song import Song
from server.entities.user import User

# Constants
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
GROUPS_PATH = os.path.join(ROOT_PATH, "user_groups")
SCOPE = "user-top-read playlist-modify-public playlist-modify-private"

# CONFIG
with open(os.path.join(ROOT_PATH, "config.yaml")) as config_file:
    CONFIG = yaml.safe_load(config_file)


def main():
    # Define logging config
    logging.basicConfig(filename=os.path.join(ROOT_PATH, "logs", CONFIG["log-file-name"]), level=logging.INFO)

    # Create and link entities
    groups = create_groups_from_arguments() if arguments_given() else create_all_groups_from_path()
    users = create_users_for_groups(groups)
    artists = create_artists_for_users(users)
    songs = create_artist_songs(artists, users[0].spotify)  # Spotify needs a user token to make requests

    # Save to database
    db = DB(os.path.join(ROOT_PATH, CONFIG["database-name"]))
    db.insert_groups(groups)
    db.insert_artists(artists)
    db.insert_users(users)
    db.insert_songs(songs)

    # Create playlists for every user in every group
    for group in groups:
        playlist_songs = generate_playlist_songs(db, group)
        for user in group.users:
            playlist = Playlist(
                name=group.group_name,
                user=user,
                songs=playlist_songs
            )
            playlist.create_or_update_spotify_playlist()


def randomly_combine_sets(main_set, secondary_set):
    random.shuffle(main_set)
    random.shuffle(secondary_set)

    target_playlist_size = CONFIG['maximum-playlist-size']
    target_main_size = int(target_playlist_size/2)

    combined_set = main_set[:target_main_size]
    while len(combined_set) < target_playlist_size:
        combined_set.append(secondary_set.pop())

    return combined_set


def generate_playlist_songs(db, group):
    non_overlapping_songs = db.get_matched_song_ids_for_group(group)
    if group.is_pair():
        pair_songs = db.get_matched_song_ids_for_two_users(group)
        if len(pair_songs) > CONFIG['minimum-playlist-size']:
            return randomly_combine_sets(pair_songs, non_overlapping_songs)
    return reduce_songs(non_overlapping_songs)


def reduce_songs(songs):
    max_size = CONFIG['maximum-playlist-size']
    return songs if len(songs) < max_size else random.sample(songs, max_size)


def arguments_given():
    return len(sys.argv) > 1


def create_group(name):
    """Create a single group from """
    group_path = os.path.join(GROUPS_PATH, name)
    return Group(
        group_name=name,
        group_path=group_path
    )


def create_groups_from_arguments():
    logging.info(f"[{datetime.now()}] Received new request for group(s) \"{' '.join(sys.argv[1:])}\"")
    groups = list()
    for name in sys.argv[1:]:
        new_group = create_group(name)
        groups.append(new_group)
    return groups


def create_all_groups_from_path():
    logging.info(f"[{datetime.now()}] Received new request for all groups")
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
                user.authenticate_spotify(
                    app_id=CONFIG['app-id'],
                    app_secret=CONFIG['app-secret'],
                    redirect_uri=CONFIG['redirect-uri'],
                    scope=SCOPE
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


if __name__ == "__main__":
    main()
