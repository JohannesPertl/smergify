class Song:
    def __init__(self, song_id, song_title, artist):
        self.song_id = song_id
        self.song_title = song_title
        self.artist = artist

    def to_tuple(self):
        return self.song_id, self.song_title, self.artist.artist_id
