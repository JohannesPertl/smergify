from server.entities import User


def test():
    joe = User("1", "Joe", "time")

    print(joe.convert_to_array())


if __name__ == "__main__":
    test()
