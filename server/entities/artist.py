class Artist:
    def __init__(self, artist_id, artist_name):
        self.artist_id = artist_id
        self.artist_name = artist_name

    def to_tuple(self):
        return self.artist_id, self.artist_name
