import spotipy
from spotipy import util
import yaml
import sys
import os
from server.entities import User
from server.entities import Group
from server.entities import Artist
from server.entities import Song

with open("config.yaml") as config_file:
    CONFIG = yaml.safe_load(config_file)

ROOT_PATH = os.path.dirname(os.path.realpath(__file__))


def check_arguments():
    if len(sys.argv) >= 1:
        group_folder = sys.argv[1]
        print(group_folder)


def main():
    for subdir, dirs, files in os.walk(ROOT_PATH + "/user_groups"):
        for file in files:
            # print os.path.join(subdir, file)
            filepath = subdir + os.sep + file

            print(subdir)
            print(filepath)

    # for username in user_list:
    #     # Authenticate via existing cache file or in browser and then paste the uri
    #     token = util.prompt_for_user_token(
    #         username, CONFIG['scope'],
    #         client_id=CONFIG['app_id'],
    #         client_secret=CONFIG['app_secret'],
    #         redirect_uri='http://localhost',  # TODO: Use smergify.duckdns.org with simple index.html apache server
    #         show_dialog=True
    #     )
    #
    #     if token:
    #         spotify = spotipy.Spotify(auth=token)
    #         # Top artists of user, possible time_range: short_term, medium_term, long_term
    #         artists = (spotify.current_user_top_artists(limit=50, offset=0, time_range='long_term'))['items']
    #         print(artists)
    #         artist_names = list(map((lambda artist: artist['name']), artists))
    #         # TODO: More variables for artist
    #             # * URI for artist_top_tracks
    #
    #
    #         print(spotify.artist_top_tracks("spotify:artist:0GDGKpJFhVpcjIGF8N6Ewt"))
    #         # TODO: Remove
    #         # for name in artist_names:
    #             # print(name)
    #
    #         # TODO: Merge artists into combined lists (differences, matches)
    #
    #         # TODO: Create playlist of combined artists (use artist_top_tracks for tracks)
    #         # TODO: 1. Playlist of matches
    #         #       2. Playlist of differences
    #
    #         # Implement other functions to generate playlist
    #             # TODO: Read lable from artist, create playlist based on lable


if __name__ == "__main__":
    main()
