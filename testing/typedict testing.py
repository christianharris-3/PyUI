from dataclasses import dataclass, replace
import numpy as np
np.array

class InvalidArguementException(Exception):
    """
    and what if i docstring it here
    :param whatevenisthis: hi there
    """
    whatevenishthis = 12
    def __init__(self, message, e):
        """
        this is a very informative doc string
        :param message: this is a cool message
        :param e:
        """
        super().__init__(message)
        self.message = message

@dataclass
class PositionalData:
    """
    This is a super class with some variables
    """
    x: int = 0
    y: int = 0
    scale: float = 1

@dataclass
class TextData(PositionalData):
    __doc__=super.__doc__+"""
    this is a subclass with some variables
    """
    font: str = "calibre"
    size: int = 12
    col: tuple[int, int, int] = (100, 100, 100)

def maketext(**kwargs):
    """
    adoiajdia
    :param kwargs:
    :return:
    """
    data =  replace(defaults, **kwargs)
    return data

defaults = TextData()
PositionalData()
# defaults.__setattr__("font","no")
var = "font"
defaults = replace(defaults, **kwargs)
defaults.x = 2

InvalidArguementException()
maketext()

data = maketext(size=40, x= 5)
print(data, defaults)