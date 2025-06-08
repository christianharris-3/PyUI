from dataclasses import dataclass
import pygame


@dataclass
class StyleData:
    backing_col: tuple[int] | pygame.Color = (0, 0, 0)
    backing_col_shift: int = 0
    backing_draw: bool = True
    rounded_corners: int = 0
    antialiasing: bool = True
    glow: int = 0
    glowcol: tuple[int] | pygame.Color = (0,0,0)
