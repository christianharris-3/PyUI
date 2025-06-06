from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pygame


@dataclass
class StyleData:
    backing_col: tuple[int] | pygame.Color = (0, 0, 0)
    backing_col_shift: int = 0
    backing_draw: bool = True
    antialiasing: bool = True
