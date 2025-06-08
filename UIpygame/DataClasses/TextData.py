from dataclasses import dataclass
import pygame

@dataclass
class TextData:
    text: str = ""
    text_size: int = 50
    text_col: tuple[int] | pygame.Color = (150, 150, 150)
    text_col_shift: int = 0
    font: str = "calibri"
    bold: bool = False
    pregenerated: bool = False
    text_offset_x: int = 0
    text_offset_y: int = 0
    text_animation_speed: int = 0

    text_center: bool = False

