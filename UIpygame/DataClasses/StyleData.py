from dataclasses import dataclass
import pygame


@dataclass
class StyleData:
    backing_col: int | tuple[int] | pygame.Color = 0 # int offset from the default backing_col
    backing_draw: bool = True
    rounded_corners: int = 0
    antialiasing: bool = True
    glow_size: int = 0
    glow_col: tuple[int] | pygame.Color = None
