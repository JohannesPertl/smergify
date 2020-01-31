class Group:
    def __init__(self, group_name, group_id=None, users=None):
        if users is None:
            users = list()
        self.group_name = group_name
        self.users = users
        self.group_id = group_id

    def to_tuple(self):
        return None, self.group_name
