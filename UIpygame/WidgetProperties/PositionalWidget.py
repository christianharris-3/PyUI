from abc import ABC, abstractmethod
from UIpygame.Widgets.GuiItem import GuiItem
from UIpygame.Utils.Utils import Utils
import numpy as np

class PositionalWidget(GuiItem, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initial_pos = np.array([self._gui_item_data.x, self._gui_item_data.y])
        self.initial_dimensions = np.array([self._gui_item_data.width, self._gui_item_data.height])

        self.center = self._gui_item_data.center
        self.initial_anchor = self._gui_item_data.anchor
        self.initial_obj_anchor = self._gui_item_data.anchor

    def getDrawRect(self):
        self.getChildren()

    def refreshCords(self):
        parent_dimensions = self.getParentDimensions()
        self.unscaled_pos = Utils.initialPosToValuePos(self.initial_pos, parent_dimensions, self.ui)
        self.unscaled_dimensions = Utils.initialPosToValuePos(self.initial_dimensions, parent_dimensions, self.ui)


        self.anchor_pixels = Utils.initialPosToValuePos(self.initial_anchor, parent_dimensions, self.ui)
        self.obj_anchor_pixels = Utils.initialPosToValuePos(self.initial_obj_anchor, self.getDimensions(), self.ui)


    def resetCords(self, scalereset=True):
        ui = self.ui
        if scalereset: self.refreshScale()
        self.anchor = self.start_anchor[:]

        master = self.master[0]
        if len(self.master) > 1:
            if 'animate' in self.true_menu:
                for a in self.master:
                    if ui.active_menu in a.truemenu:
                        master = a
            else:
                for a in self.master:
                    if not (ui.active_menu in a.truemenu):
                        master = a
                        break

        w = self.getMasterWidth()
        h = self.getMasterHeight()

        self.anchor[0] = Utils.relativeToValue(self.anchor[0], w, h, ui)
        self.anchor[1] = Utils.relativeToValue(self.anchor[1], w, h, ui)

        self.obj_anchor = self.start_obj_anchor[:]
        self.obj_anchor[0] = Utils.relativeToValue(self.obj_anchor[0], self.width, self.height, ui)
        self.obj_anchor[1] = Utils.relativeToValue(self.obj_anchor[1], self.width, self.height, ui)

        self.x = int(master.x * master.dirscale[0] + self.anchor[0] + (
                self.start_x - self.obj_anchor[0] - self.scroll_cords[0]) * self.scale) / self.dir_scale[0]
        self.y = int(master.y * master.dirscale[1] + self.anchor[1] + (
                self.start_y - self.obj_anchor[1] - self.scroll_cords[1]) * self.scale) / self.dir_scale[1]

        self.refreshCords()
        for a in self.bound_items:
            a.resetCords()
        self.refreshClickableRect()

    def refreshScale(self):
        if self.scale_by == -1:
            self.scale = self.ui.scale
        elif self.scale_by == 'vertical':
            self.scale = self.ui.dir_scale[1]
        else:
            self.scale = self.ui.dir_scale[0]

        self.dir_scale = self.ui.dir_scale[:]
        if not self.scale_size: self.scale = 1
        if not self.scale_x: self.dir_scale[0] = 1
        if not self.scale_y: self.dir_scale[1] = 1

    def autoScale(self):
        w = self.getMasterWidth() / self.scale
        h = self.getMasterHeight() / self.scale
        if self.start_width != -1: self.width = Utils.relativeToValue(self.start_width, w, h, self.ui)
        if self.start_max_width != -1: self.max_width = Utils.relativeToValue(self.start_max_width, w, h, self.ui)
        if self.start_height != -1: self.height = Utils.relativeToValue(self.start_height, w, h, self.ui)
        self.refreshClickableRect()
        self.childAutoScale()

    def smartCords(self, x=None, y=None, startset=True, accountscroll=False):
        scr = [0, 0]
        if accountscroll:
            scr = self.scroll_cords[:]

        if x is not None:
            self.x = x
            if startset: self.start_x = ((self.x + scr[0]) * self.dir_scale[0] + self.obj_anchor[0] * self.scale -
                                         self.anchor[0]) / self.scale - self.master[0].x
        if y is not None:
            self.y = y
            if startset: self.start_y = ((self.y + scr[1]) * self.dir_scale[1] + self.obj_anchor[1] * self.scale -
                                         self.anchor[1]) / self.scale - self.master[0].y


    def setX(self, x: int|float|str):
        self.initial_x = x
    def setY(self, y: int|float|str):
        self.initial_y = y


    def getX(self) -> int|float:
        return self.pos[0]

    def getY(self) -> int|float:
        return self.pos[1]

    def getDimensions(self):
        return self.dimensions
