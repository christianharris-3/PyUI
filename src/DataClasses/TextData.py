from dataclasses import dataclass
from typing import TYPE_CHECKING
from src.DataClasses.PositionalData import PositionalData
from src.DataClasses.StyleData import StyleData
import pygame

if TYPE_CHECKING:
    pass



@dataclass
class TextData:
    text_col: tuple[int] | pygame.Color = (150, 150, 150)
    text_col_shift: int = 0
    text_size: int = 50
    font: str = "calibri"
    border_col: tuple[int] | pygame.Color = (0, 0, 0)
    border_col_shift: int = 0
    border_size: int = 0
    left_border_size: int = None
    top_border_size: int = None
    right_border_size: int = None
    bottom_border_size: int = None
