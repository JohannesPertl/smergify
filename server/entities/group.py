class Group:
    def __init__(self, group_name, group_id=None, users=None):
        self.group_name = group_name
        self.group_id = group_id
        self.users = users

    def to_tuple(self):
        return self.group_name, self.group_id, self.users
