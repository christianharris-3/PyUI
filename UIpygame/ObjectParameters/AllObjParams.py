from dataclasses import dataclass
from UIpygame.DataClasses.BorderData import BorderData
from UIpygame.DataClasses.ClickableData import ClickableData
from UIpygame.DataClasses.ObjectData import ObjectData
from UIpygame.DataClasses.PositionalData import PositionalData
from UIpygame.DataClasses.StyleData import StyleData
from UIpygame.DataClasses.TextData import TextData
import pygame

@dataclass
class AllObjParams(BorderData, ClickableData, ObjectData, PositionalData, StyleData, TextData):
    wallpaper_col: pygame.Color | tuple[int] = (255, 255, 255)