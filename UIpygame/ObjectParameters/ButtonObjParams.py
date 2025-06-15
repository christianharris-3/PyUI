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
class ButtonObjParams(ObjectData, PositionalData, StyleData, BorderData, ClickableData, TextData):
    ID: str = 'Button'
    hover_backing_col: int | tuple[int] | pygame.Color = -20  # int offset from backing_col

    toggleable: bool = False
    toggle_state: bool = False
    toggle_text: str = ""
    toggle_backing_col: int | tuple[int] | pygame.Color = -50 # int offset from backing_col
    toggle_hover_backing_col: int | tuple[int] | pygame.Color = -20 # int offset from toggle_backing_col

    bind_toggle: list[GuiItem | str] = None

    click_down_size: int = 4
    expand_click_hitbox: int = 0

    press_keys: list[pygame.constants] = None

