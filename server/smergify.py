from server.entities import User


def test():
    joe = User("1", "Joe", "time")
    tom = User("2", "Tom", "time")
    list = [joe.to_tuple(), tom.to_tuple()]
    print(list)


if __name__ == "__main__":
    test()
