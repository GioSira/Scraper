from enum import Enum, auto


class BrowserType(Enum):
    FIREFOX = auto()
    CHROME = auto()
    IE = auto()
    TOR = auto()

    def equals(self, string):
        return self.name == string
