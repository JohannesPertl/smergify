class User:
    def __init__(self, user_name, user_id, spotify_token, user_group=None, artists=None):
        if artists is None:
            artists = list()
        self.artists = artists
        self.user_name = user_name
        self.user_id = user_id
        self.user_token = spotify_token
        self.user_group = user_group

    def to_tuple(self):
        return self.user_id, self.user_name
