from typing import Self


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls) -> Self:
        return cls._instance


if __name__ == '__main__':
    class Test(Singleton):
        pass


    a = Test()
    b = Test()

    print(a is b)  # True
    print(a, b)  # True
