from dataclasses import dataclass

from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData
from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.TextData import TextData


@dataclass
class TextObjParams(ObjectData, PositionalData, StyleData, BorderData, TextData):
    ID = "Text"
    border_draw = False
    backing_draw = False