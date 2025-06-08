from dataclasses import dataclass, replace
import pygame


@dataclass
class BorderData:
    border_col: tuple[int] | pygame.Color = (0, 0, 0)
    border_col_shift: int = 0
    border_size: int = 0
    left_border_size: int = None
    top_border_size: int = None
    right_border_size: int = None
    bottom_border_size: int = None
