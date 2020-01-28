class Group:
    def __init__(self, group_name, group_id=None):
        self.group_name = group_name
        self.group_id = group_id

    def to_tuple(self):
        return self.group_name
