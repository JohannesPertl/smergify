class User:
    def __init__(self, user_name, user_id, first_login):
        self.user_id = user_id
        self.user_name = user_name
        self.first_login = first_login

    def to_tuple(self):
        return self.user_id, self.user_name, self.first_login
