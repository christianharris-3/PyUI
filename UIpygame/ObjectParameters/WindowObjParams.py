from dataclasses import dataclass

from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData


@dataclass
class WindowObjParams(ObjectData, PositionalData, StyleData, BorderData):
    ID = 'Window'
    isolated: bool = False
    auto_shut_windows: list[str] = None