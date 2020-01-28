from server.entities import User


def test():
    joe = User("1", "Joe", "time")
    tom = User("2", "Tom", "time")
    list = [joe.to_array(), tom.to_array()]
    print(list)


if __name__ == "__main__":
    test()
