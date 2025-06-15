from dataclasses import dataclass

from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData
from UIpygame.DataClasses.TextData import TextData

import pygame
import math


@dataclass
class TextboxObjParams(ObjectData, PositionalData, BorderData, ClickableData, StyleData, TextData):
    text_lines: int = 1
    line_limit: int = math.inf
    selected_highlight_col:  int | tuple[int] | pygame.Color = 20 # int offset from backing_col
    selected_highlight_shrink_size: int = 0
    cursor_height: int = None
    char_limit: int = math.inf
    nums_only: bool = False
    enter_returns: bool = False
    command_if_enter: bool = True
    command_if_key: bool = False
    image_display: bool = False
    attach_scroller: bool = True
    scroll_edits_number: bool = True
    min_number: int | float = -math.inf
    max_number: int | float = math.inf
    number_wrap_around: bool = False




