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

class RunCommandAt(Enum):
    START_OF_CLICK = 'start_of_click'
    REPEAT_WHILE_CLICKED = 'repeat_while_clicked'
    END_OF_CLICK = 'end_of_click'

class MouseButton(Enum):
    LEFT_CLICK = 0
    MIDDLE_CLICK = 1
    RIGHT_CLICK = 2