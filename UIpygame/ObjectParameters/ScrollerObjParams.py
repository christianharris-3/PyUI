from dataclasses import dataclass

from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData
from UIpygame.DataClasses.SlideData import SlideData


@dataclass
class ScrollerObjParams(ObjectData, PositionalData, StyleData, BorderData, ClickableData, SlideData):
    ID = "Scroller"
    page_height: int | float = 15
    scroll_bind_list: list[str] = None
