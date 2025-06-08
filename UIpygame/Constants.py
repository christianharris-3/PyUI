from enum import Enum
import pygame

class ClickType(Enum):
    LEFT_CLICK: str = 'left_click'
    MIDDLE_CLICK: str = 'middle_click'
    RIGHT_CLICK: str = 'right_click'
class Colours(Enum):
    RED = pygame.Color('red')

class ScaleBy(Enum):
    VERTICAL = 'vertical'
    HORIZONTAL = 'horizontal'
    RELATIVE: str = 'relative'
    MIN: str = 'min'
    MAX: str = 'min'