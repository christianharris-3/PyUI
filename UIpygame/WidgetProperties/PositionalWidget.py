from abc import ABC, abstractmethod
from UIpygame.Widgets.GuiItem import GuiItem
from UIpygame.Utils.Utils import Utils
from UIpygame.Constants import ScaleBy as ScaleBy
import numpy as np

class PositionalWidget(GuiItem, ABC):
    def __init__(self, obj_params):
        super().__init__(obj_params)
        self.initial_pos = np.array([obj_params.x, obj_params.y])
        self.initial_dimensions = np.array([obj_params.width, obj_params.height])

        self.center = obj_params.center
        self.initial_anchor = obj_params.anchor
        self.initial_obj_anchor = obj_params.anchor
        self.do_pos_scaling = obj_params.do_pos_scaling
        self.do_dimensions_scaling = obj_params.do_dimensions_scaling

        self.refreshCords()

    def refreshScale(self):
        self.refreshDimensions()
        self.refreshPos()

    def refreshPos(self):
        parent_dimensions = self.getParentDimensions()

        unscaled_pos = Utils.initialPosToValuePos(self.initial_pos, parent_dimensions, self.ui)
        anchor_pixels = Utils.initialPosToValuePos(self.initial_anchor, parent_dimensions, self.ui)
        obj_anchor_pixels = Utils.initialPosToValuePos(self.initial_obj_anchor, self.getDrawDimensions(), self.ui)


        self.draw_pos = (self.getParentDrawPos() + anchor_pixels +
                         (unscaled_pos - obj_anchor_pixels - self.scroll_cords) @ self.__getPosScalingMatrix())

        for child in self.getChildren():
            child.refreshPos()

    def refreshDimensions(self):
        parent_dimensions = self.getParentDimensions()
        unscaled_dimensions = Utils.initialPosToValuePos(self.initial_dimensions, parent_dimensions, self.ui)
        self.draw_dimensions = self.__getDimensionsScalingMatrix() @ unscaled_dimensions

        for child in self.getChildren():
            child.refreshDimensions()

    def __getPosScalingMatrix(self) -> np.ndarray:
        return self.__getDirScale(
            Utils.getBaseDirScaleValue(
                self.ui.dir_scale,
                self.do_pos_scaling
            )
        )

    def __getDimensionsScalingMatrix(self) -> np.ndarray:
        return self.__getDirScale(
            Utils.getBaseDirScaleValue(
                self.ui.dir_scale,
                self.do_dimensions_scaling,
            )
        )
    def __getDirScale(self, ui_dir_scale=None)  -> np.ndarray:
        """
        returns a matrix to multiply position values by
        :param ui_dir_scale: ui.dir_scale value, leave as none to assign to ui.dir_scale, can be overwritten to custom value
        :return: 2x2 np.array, matrix to multiply position by
        """
        if ui_dir_scale is None:
            ui_dir_scale = self.ui.dir_scale
        match self.scale_by:
            case ScaleBy.MIN:
                return np.identity(2) * min(ui_dir_scale)
            case ScaleBy.MAX:
                return np.identity(2) * max(ui_dir_scale)
            case ScaleBy.HORIZONTAL:
                return np.identity(2) * ui_dir_scale[0]
            case ScaleBy.VERTICAL:
                return np.identity(2) * ui_dir_scale[1]
            case ScaleBy.RELATIVE:
                return np.diag(ui_dir_scale)
        raise Exception(f"Unrecognised value of scale_by in object {self}")

    # def resetCords(self, scalereset=True):
    #     ui = self.ui
    #     if scalereset: self.refreshScale()
    #     self.anchor = self.start_anchor[:]
    #
    #     master = self.master[0]
    #     if len(self.master) > 1:
    #         if 'animate' in self.true_menu:
    #             for a in self.master:
    #                 if ui.active_menu in a.truemenu:
    #                     master = a
    #         else:
    #             for a in self.master:
    #                 if not (ui.active_menu in a.truemenu):
    #                     master = a
    #                     break
    #
    #     w = self.getParentWidth()
    #     h = self.getParentHeight()
    #
    #     self.anchor[0] = Utils.relativeToValue(self.anchor[0], w, h, ui)
    #     self.anchor[1] = Utils.relativeToValue(self.anchor[1], w, h, ui)
    #
    #     self.obj_anchor = self.start_obj_anchor[:]
    #     self.obj_anchor[0] = Utils.relativeToValue(self.obj_anchor[0], self.width, self.height, ui)
    #     self.obj_anchor[1] = Utils.relativeToValue(self.obj_anchor[1], self.width, self.height, ui)
    #
    #     self.x = int(master.x * master.dir_scale[0] + self.anchor[0] + (
    #             self.start_x - self.obj_anchor[0] - self.scroll_cords[0]) * self.scale) / self.dir_scale[0]
    #     self.y = int(master.y * master.dir_scale[1] + self.anchor[1] + (
    #             self.start_y - self.obj_anchor[1] - self.scroll_cords[1]) * self.scale) / self.dir_scale[1]
    #
    #     self.refreshCords()
    #     for a in self.bound_items:
    #         a.resetCords()
    #     self.refreshClickableRect()


    # def autoScale(self):
    #     w = self.getMasterWidth() / self.scale
    #     h = self.getMasterHeight() / self.scale
    #     if self.start_width != -1: self.width = Utils.relativeToValue(self.start_width, w, h, self.ui)
    #     if self.start_max_width != -1: self.max_width = Utils.relativeToValue(self.start_max_width, w, h, self.ui)
    #     if self.start_height != -1: self.height = Utils.relativeToValue(self.start_height, w, h, self.ui)
    #     self.refreshClickableRect()
    #     self.childAutoScale()

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
        self.refreshPos()
    def setY(self, y: int|float|str):
        self.initial_y = y
        self.refreshPos()

    def getX(self) -> int|float:
        return self.draw_pos[0]

    def getY(self) -> int|float:
        return self.draw_pos[1]

    def getDrawDimensions(self):
        return self.draw_dimensions

    def getDrawPos(self):
        return self.draw_pos
