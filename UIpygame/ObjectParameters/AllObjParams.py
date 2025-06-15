from dataclasses import dataclass
from UIpygame.ObjectParameters.ButtonObjParams import ButtonObjParams
from UIpygame.ObjectParameters.DropDownObjParams import DropDownObjParams
from UIpygame.ObjectParameters.RectangleObjParams import RectangleObjParams
from UIpygame.ObjectParameters.ScrollerObjParams import ScrollerObjParams
from UIpygame.ObjectParameters.ScrollerTableObjParams import ScrollerTableObjParams
from UIpygame.ObjectParameters.SliderObjParams import SliderObjParams
from UIpygame.ObjectParameters.TableObjParams import TableObjParams
from UIpygame.ObjectParameters.TextboxObjParams import TextboxObjParams
from UIpygame.ObjectParameters.TextObjParams import TextObjParams
from UIpygame.ObjectParameters.WindowObjParams import WindowObjParams
import pygame


@dataclass
class AllObjParams(ButtonObjParams, DropDownObjParams, RectangleObjParams, ScrollerObjParams,
                   ScrollerTableObjParams, SliderObjParams, TableObjParams, TextboxObjParams,
                   TextObjParams, WindowObjParams):
    wallpaper_col: pygame.Color | tuple[int] = (255, 255, 255)