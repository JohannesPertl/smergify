class User:
    def __init__(self, user_name, user_id, user_group=None, ):
        self.user_id = user_id
        self.user_name = user_name
        self.user_group = user_group

    def to_tuple(self):
        return self.user_id, self.user_name
