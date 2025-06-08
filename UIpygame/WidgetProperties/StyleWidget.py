from abc import ABC, abstractmethod
import pygame

from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.Utils import Utils
from UIpygame.WidgetProperties.PositionalWidget import PositionalWidget
from UIpygame.Widgets.GuiItem import GuiItem

class StyleWidget(PositionalWidget, GuiItem, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def refreshGlow(self):
        if self.glow != 0:
            self.glow_image = pygame.Surface(
                ((self.glow * 2 + self.width) * self.scale, (self.glow * 2 + self.height) * self.scale),
                pygame.SRCALPHA)
            Draw.glow(self.glow_image, Utils.roundRect(self.glow * self.scale, self.glow * self.scale, self.width * self.scale,
                                                       self.height * self.scale), int(self.glow * self.scale), self.glow_col)

