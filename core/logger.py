class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Logger(metaclass=Singleton):
    def __init__(self, level: str):
        levels = {
            "DEBUG": 1,
            "INFO": 2,
            "WARN": 3,
            "ERROR": 4
        }
        self.level = levels.get(level.upper(), 1)

    def debug(self, message):
        if self.level <= 1:
            print(message)

    def info(self, message):
        if self.level <= 2:
            print(message)

    def warn(self, message):
        if self.level <= 3:
            print(message)

    def error(self, message):
        if self.level <= 4:
            print(message)
