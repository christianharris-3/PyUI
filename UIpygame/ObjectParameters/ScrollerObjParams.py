from dataclasses import dataclass

from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData


@dataclass
class ScrollerObjParams(ObjectData, PositionalData, ClickableData, StyleData):
    start_value: int | float = 0
    min_value: int | float = 0
    max_value: int | float = 100

    page_height: int | float = 15
    scroll_bind_list: list[str] = None
