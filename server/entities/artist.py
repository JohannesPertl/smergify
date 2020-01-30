class Artist:
    def __init__(self, artist_id, artist_name, time_range, songs=None):
        if songs is None:
            songs = list()
        self.artist_id = artist_id
        self.artist_name = artist_name
        self.time_range = time_range
        self.songs = songs

    def to_tuple(self):
        return self.artist_id, self.artist_name
