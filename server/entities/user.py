class User:
    def __init__(self, user_name, user_id, first_login, user_group=None,):
        self.user_id = user_id
        self.user_name = user_name
        self.first_login = first_login
        self.user_group = user_group

    def to_tuple(self):
        return self.user_id, self.user_name, self.first_login, self.user_group
