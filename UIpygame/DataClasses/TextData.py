from dataclasses import dataclass
import pygame

@dataclass
class TextData:
    text: str | pygame.Surface = ""
    text_size: int = 50
    text_col: tuple[int] | pygame.Color = (150, 150, 150)
    text_col_shift: int = 0
    font: str = "calibri"
    bold: bool = False
    pregenerate_text: bool = True
    text_offset_x: int = 0
    text_offset_y: int = 0
    text_animation_speed: int = 0
    text_center: bool = False
    spacing: int | float | list[int|float, int|float] = 5
    text_max_width: int = None
    image_display: bool = True



