from dataclasses import dataclass

from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData



@dataclass
class RectangleObjParams(ClickableData,ObjectData, PositionalData, StyleData):
    pass