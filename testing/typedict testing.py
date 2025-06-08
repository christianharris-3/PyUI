from dataclasses import dataclass

class InvalidArguementException(Exception):
    def __init__(self, message, e):
        super().__init__(message)
        self.message = message

@dataclass
class TextData:
    font: str = "calibre"
    size: int = 12
    col: tuple[int, int, int] = (100, 100, 100)


def maketext(**kwargs):
    try:
        data = TextData(**kwargs)
    except Exception as e:
        print(e.__traceback__)
        raise InvalidArguementException("message",e) from None
    return data

data = maketext(size=40, penis=20)
print(data)