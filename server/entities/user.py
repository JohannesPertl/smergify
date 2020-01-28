class User:
    def __init__(self, name, id, first_login):
        self.id = id
        self.name = name
        self.first_login = first_login

    def convert_to_array(self):
        return [(self.id, self.name, self.first_login)]
