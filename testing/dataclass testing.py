from dataclasses import dataclass, replace

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

@dataclass
class SliderData(PositionalData):
    size: int = 3
    max_value: int = 20


slider = SliderData(size=5,x=6)
text = TextData(size=30,y=20)
final = replace(text, **slider.__dict__)
print(final)