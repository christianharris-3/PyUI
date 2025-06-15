from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData
from UIpygame.DataClasses.TextData import TextData

import pygame
if TYPE_CHECKING:
    from UIpygame.Widgets.GuiItem import GuiItem

@dataclass
class TableObjParams(BorderData, ClickableData, ObjectData, PositionalData, StyleData, TextData):
    data: list[list[int | str | float | pygame.surface | type(GuiItem)]] = None
    titles: list[int | str | float | pygame.surface | type(GuiItem)] = None
    box_width: int | list[int] = None
    box_height: int | list[int] = None
    line_size: int = 2
    guess_width: int = 100
    guess_height: int = 50