from dataclasses import dataclass
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData
from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.TextData import TextData


@dataclass
class TextObjParams(PositionalData, StyleData, BorderData, TextData):
    ID: str = "Text"