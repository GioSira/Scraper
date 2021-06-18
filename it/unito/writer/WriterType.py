from enum import Enum, auto


class WriterType(Enum):
    SIMPLE = auto()
    XLS = auto()
    LOG = auto()
    JSON = auto()

    def equals(self, string):
        return self.name == string
