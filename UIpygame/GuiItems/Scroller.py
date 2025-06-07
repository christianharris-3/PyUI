from UIpygame.GuiItems.GuiItem import GuiItem
import pygame
from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.Draw import Draw


class Scroller(GuiItem):
    def reset(self):
        self.autoScale()
        self.value = self.startp
        self.__inner_height = self.height - self.border_size * 2
        self.prev_holding = self.holding
        self.refreshScale()
        self.refresh()
        self.resetCords()
        self.checkActive()
        self.refreshClickableRect()

    def child_render(self, screen):
        self.checkActive()
        if self.active:
            temp = (self.x, self.y)
            self.getClickedOn(pygame.Rect(self.x * self.dir_scale[0] + self.left_border_size * self.scale,
                                          self.y * self.dir_scale[1] + (self.border_size + self.value * (
                                                  self.__inner_height / (
                                                  self.max_value - self.min_value))) * self.scale,
                                          (self.width - self.left_border_size - self.right_border_size) * self.scale,
                                          ((self.page_height / (
                                                  self.max_value - self.min_value)) * self.__inner_height) * self.scale),
                              smartdrag=False)
            if self.holding:
                self.value = (self.y - temp[1]) * self.dir_scale[1] / self.dir_scale[0] / (
                        self.__inner_height / (self.max_value - self.min_value))
                self.limitPos()
            self.x, self.y = temp
            self.scrollObjects()
            self.draw(screen)

    def child_autoscale(self):
        compress = 1
        if self.screen_compressed:
            if self.y * self.dir_scale[1] + self.height * self.scale > self.ui.screenh:
                compress = 1 - (self.y * self.dir_scale[
                    1] + self.height * self.scale - self.ui.screenh + self.screen_compressed) / (
                                   self.height * self.scale)
        self.height *= compress
        self.__inner_height = self.height - self.border_size * 2
        self.max_value = Utils.relativeToValue(self.start_max_value, self.getMasterWidth() / self.scale,
                                               self.getMasterHeight() / self.scale, self.ui)
        self.min_value = Utils.relativeToValue(self.start_min_value, self.getMasterWidth() / self.scale,
                                               self.getMasterHeight() / self.scale, self.ui)
        self.page_height = Utils.relativeToValue(self.start_page_height, self.getMasterWidth() / self.scale,
                                                 self.getMasterHeight() / self.scale, self.ui) * compress

    def limitPos(self):
        if not self.active:
            self.value = self.min_value
        elif self.value < self.min_value:
            self.value = self.min_value
        elif self.value > self.max_value - self.page_height:
            self.value = self.max_value - self.page_height

    def refresh(self):
        self.autoScale()
        self.refreshCords()
        self.checkActive()
        self.limitPos()
        self.refreshBound()

    def checkActive(self):
        if (self.max_value - self.min_value) > self.page_height:
            self.active = True
        else:
            self.active = False

    def setScroll(self, scroll, relative=False):
        if relative:
            self.value += scroll
        else:
            self.value = scroll
        self.limitPos()

    def setMinValue(self, minp):
        self.start_min_value = minp
        self.autoScale()

    def setMaxValue(self, maxp):
        self.start_max_value = maxp
        self.autoScale()

    def setPageHeight(self, page_height):
        self.start_page_height = page_height
        self.autoScale()

    def scrollObjects(self):
        for a in self.scroll_bind:
            if self.ui.IDs[a].scroll_cords != (self.ui.IDs[a].scroll_cords[0], self.value):
                self.ui.IDs[a].scroll_cords = (self.ui.IDs[a].scroll_cords[0], self.value)
                self.ui.IDs[a].resetCords()

    def child_refreshcords(self):
        if self.max_value - self.min_value == 0:
            self.max_value = self.min_value + 0.1

    ##        self.sliderrect = pygame.Rect(self.x+self.border,self.y+self.border+self.value*(self.__inner_height/(self.max_value-self.min_value)),self.scrollerwidth,self.scrollerheight)

    def draw(self, screen):
        if self.enabled and self.active:
            if self.glow != 0:
                screen.blit(self.glow_image, (
                    self.x * self.dir_scale[0] - self.glow * self.scale,
                    self.y * self.dir_scale[1] - self.glow * self.scale))
            Draw.rect(screen, self.col,
                      Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                      self.height * self.scale), border_radius=int(self.rounded_corners * self.scale))
            Draw.rect(screen, self.scroller_col,
                      Utils.roundRect(self.x * self.dir_scale[0] + self.left_border_size * self.scale,
                                      self.y * self.dir_scale[1] + (self.border + self.value * (
                                              self.__inner_height / (
                                              self.max_value - self.min_value))) * self.scale, (
                                              self.width - self.left_border_size - self.right_border_size) * self.scale,
                                      ((self.page_height / (
                                              self.max_value - self.min_value)) * self.__inner_height) * self.scale),
                      border_radius=int(self.rounded_corners * self.scale))
