from abc import ABC, abstractmethod

from UIpygame.WidgetProperties.PositionalWidget import PositionalWidget
from UIpygame.Widgets.GuiItem import GuiItem
import pygame

class ClickableWidget(PositionalWidget, GuiItem, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clickable = self._gui_item_data.clickable
        self.clickable_rect = self._gui_item_data.clickable_rect
        self.command = self._gui_item_data.command
        self.run_command_at = self._gui_item_data.run_command_at

    def press(self):
        for a in self.bind_toggle:
            if a != self.ID:
                self.ui.IDs[a].toggle = False
        if self.toggleable:
            self.toggle = not self.toggle
        self.command()

    def getClickedOn(self, rect='default', runcom=True, drag=True, smartdrag=True):
        ui = self.ui
        if rect == 'default':
            rect = pygame.Rect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                               self.height * self.scale)
        self.clicked_on = -1
        self.hovering = False
        mpos = ui.mpos
        if self.force_holding:
            if not self.holding:
                self.clicked_on = 0
            else:
                self.clicked_on = 1
            self.holding = True
            return False
        if rect.collidepoint(mpos) and (self.clickable_rect == -1 or self.clickable_rect.collidepoint(mpos)) and not (
        Collision.collidepointrects(mpos, self.no_click_rects_applied)):
            if ui.mprs[self.click_type] and (ui.mouseheld[self.click_type][1] > 0 or self.holding):
                if ui.mouseheld[self.click_type][1] == ui.buttondowntimer:
                    self.clicked_on = 0
                    self.holding = True
                    self.holding_cords = [(mpos[0]) - rect.x, (mpos[1]) - rect.y]
                    if self.run_command_at < 2 and runcom:
                        self.press()
            else:
                self.hovering = True
        if ui.mprs[self.click_type] and self.holding:
            if self.clicked_on != 0:
                self.clicked_on = 1
            if self.dragable and drag:
                if type(self) == Scroller:
                    account = [0, -self.border]
                else:
                    account = [-rect.x + self.x * self.dir_scale[0], -rect.y + self.y * self.dir_scale[1]]
                if smartdrag:
                    self.smartCords((mpos[0] - self.holding_cords[0] + account[0]) / self.dir_scale[0],
                                    (mpos[1] - self.holding_cords[1] + account[1]) / self.dir_scale[1])
                else:
                    self.x = (mpos[0] - self.holding_cords[0] + account[0]) / self.dir_scale[0]
                    self.y = (mpos[1] - self.holding_cords[1] + account[1]) / self.dir_scale[1]
                self.centerx = self.x + self.width / 2
                self.center_y = self.y + self.height / 2
                for a in self.bound_items:
                    a.resetCords(ui)
            if self.run_command_at == 1 and runcom:
                self.command()
        elif not ui.mprs[self.click_type]:
            if self.holding:
                self.clicked_on = 2
                if rect.collidepoint(mpos) and self.run_command_at > 0 and runcom:
                    self.press()
            self.holding = False
        return False

    def refreshClickableRect(self):
        w = self.getMasterWidth() / self.scale
        h = self.getMasterHeight() / self.scale
        if self.start_clickable_rect != -1:
            rx, ry, rw, rh = self.start_clickable_rect
            xstart = self.master[0].x * self.master[0].dirscale[0]
            ystart = self.master[0].y * self.master[0].dirscale[1]
            ow = self.getMasterWidth() / self.scale
            oh = self.getMasterHeight() / self.scale
            if type(self) == ScrollerTable:
                self.page_height = Utils.relativeToValue(self.start_page_height, w, h, self.ui)
                oh = self.page_height
            if type(self) in [ScrollerTable, Table]:
                xstart = self.x * self.dir_scale[0]
                ystart = self.y * self.dir_scale[1]
                ow = self.width
                oh = self.height
            self.clickable_rect = pygame.Rect(xstart + Utils.relativeToValue(rx, w, h, self.ui),
                                              ystart + Utils.relativeToValue(ry, w, h, self.ui),
                                              Utils.relativeToValue(rw, ow, oh, self.ui) * self.scale,
                                              Utils.relativeToValue(rh, ow, oh, self.ui) * self.scale)
        else:
            self.clickable_rect = self.start_clickable_rect