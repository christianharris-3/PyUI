from src.DataClasses.PositionalData import PositionalData
from src.DataClasses.StyleData import StyleData
from src.DataClasses.TextData import TextData
from dataclasses import dataclass
from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    pass



@dataclass

class TextBox(PositionalData,StyleData,TextData):
    pass

