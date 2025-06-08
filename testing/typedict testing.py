from dataclasses import dataclass, replace

class InvalidArguementException(Exception):
    def __init__(self, message, e):
        super().__init__(message)
        self.message = message

@dataclass
class PositionalData:
    x: int = 0
    y: int = 0
    scale: float = 1

@dataclass
class TextData(PositionalData):
    font: str = "calibre"
    size: int = 12
    col: tuple[int, int, int] = (100, 100, 100)

def maketext(**kwargs):
    data =  replace(defaults, **kwargs)
    return data

defaults = TextData()
# defaults.__setattr__("font","no")
var = "font"
defaults = replace(defaults, **kwargs)
defaults.x = 2


data = maketext(size=40, x= 5)
print(data, defaults)