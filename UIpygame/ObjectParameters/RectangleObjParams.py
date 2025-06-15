from dataclasses import dataclass

from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData



@dataclass
class RectangleObjParams(ObjectData, PositionalData, BorderData, StyleData, ClickableData):
    ID = 'Rectangle'