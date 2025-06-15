from dataclasses import dataclass

from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData
from UIpygame.DataClasses.SlideData import SlideData

from UIpygame.Widgets.Button import Button
from UIpygame.Constants import Direction


@dataclass
class SliderObjParams(ObjectData, PositionalData, StyleData, ClickableData, SlideData):
    ID = "Slider"
    slider_increment: int | float = 0
    slider_size: int | float = None
    slider_button: Button = None
    direction: Direction = Direction.HORIZONTAL
    contained_slider: bool = False
    move_to_click: bool = True
