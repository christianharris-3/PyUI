from UIpygame.Widgets.GuiItem import GuiItem
from UIpygame.Widgets.Button import Button
from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.ColEdit import ColEdit

class Slider(GuiItem):
    def reset(self):
        self.slider = self.startp
        self.holding = False
        self.prev_holding = False
        self.holding_cords = [self.x, self.y]
        self.refreshScale()
        self.resetButton()
        self.resetCords()
        self.rounded_corners = min([self.rounded_corners, self.width / 2, self.height / 2])

    def refresh(self):
        self.autoScale()
        self.limitpos()
        self.refreshbutton()
        self.refreshGlow()
        self.refreshBound()

    def childRefreshCords(self):
        ##        self.
        ##        self.innerrect = pygame.Rect(self.slidercenter[0]-self.slider_size/2+self.border_size,self.slidercenter[1]-self.slider_size/2+self.border_size,self.slider_size-self.border_size*2,self.slider_size-self.border_size*2)
        self.refreshButtonCords()

    def resetButton(self):
        self.getSliderCenter()
        try:
            self.bound_items.remove(self.button)
            self.ui.delete(self.button.ID, False)
        except:
            pass
        if type(self.data) == Button:
            self.button = self.data
        else:
            self.button = self.ui.makeButton(0, 0, self.text, self.text_size, Utils.emptyFunction, self.menu,
                                             self.ID + 'button', self.layer + 0.01, self.rounded_corners,
                                             width=self.slider_size, height=self.slider_size, img=self.img,
                                             dragable=self.dragable,
                                             clickdownsize=int(self.slider_size / 15), col=ColEdit.shiftcolor(self.col, -30),
                                             scale_by=self.scale_by)

        if self.direction == 'vertical':
            self.button.start_obj_anchor = [self.button.width / 2, self.button.height / 2]
        else:
            self.button.start_obj_anchor = ['w/2', 'h/2']
        self.button.dragable = False
        self.bindItem(self.button)

    def getSliderCenter(self):
        offset = 0
        if self.contained_slider:
            if type(self.data) == Button:
                offset = self.data.width / 2
            else:
                offset = self.slider_size / 2
        if self.maxp - self.minp != 0:
            pos = (self.slider - self.minp) / (self.maxp - self.minp)
        else:
            pos = 0

        self.slidercenter = (
        self.left_border_size + offset + (self.width - self.left_border_size - self.right_border_size - offset * 2) * pos,
        self.height / 2)
        if self.direction == 'vertical':
            if self.contained_slider: offset = self.button.height / 2
            self.slidercenter = (self.width / 2, self.top_border_size + offset + (
                        self.height - self.top_border_size - self.bottom_border_size - offset * 2) * pos)

    def refreshButtonCords(self):
        self.getSliderCenter()
        self.button.start_x = self.slidercenter[0]
        self.button.start_y = self.slidercenter[1]
        self.button.start_anchor = [0, 0]
        self.button.resetCords(False)

    def refreshbutton(self):
        self.button.refresh()
        self.refreshButtonCords()

    def updatetext(self):
        if self.boundtext != -1:
            self.boundtext.setText(str(self.slider))

    def child_render(self, screen):
        self.draw(screen)
        if self.button.holding:
            self.movetomouse()
        if self.button.clicked_on == self.run_command_at:
            self.command()
        if self.move_to_click: self.movebuttontoclick()

    def movebuttontoclick(self):
        self.getClickedOn(Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                          self.height * self.scale), False, False)
        if self.clicked_on == 0:
            self.button.holding = True
            self.button.holding_cords = [self.button.width / 2, self.button.height / 2]

    def movetomouse(self):
        if self.maxp - self.minp != 0:
            pos = self.scale / (self.maxp - self.minp)
        else:
            pos = 0
        self.slider = (self.ui.mpos[0] - self.x * self.dir_scale[0] - self.left_border_size * self.scale) / (
                    (self.width - self.left_border_size - self.right_border_size) * pos) + self.minp
        if self.direction == 'vertical':
            self.slider = (self.ui.mpos[1] - self.y * self.dir_scale[1] - self.top_border_size * self.scale) / (
                        (self.height - self.top_border_size - self.bottom_border_size) * pos) + self.minp
        if self.increment != 0: self.slider = round(self.slider / self.increment) * self.increment
        self.limitpos()
        self.updatetext()

    def limitpos(self):
        if self.slider > self.maxp:
            self.slider = self.maxp
        elif self.slider < self.minp:
            self.slider = self.minp
        self.refreshButtonCords()

    def childAutoScale(self):
        self.maxp = Utils.relativeToValue(self.startmaxp, self.getMasterWidth() / self.scale,
                                          self.getMasterHeight() / self.scale, self.ui)
        self.minp = Utils.relativeToValue(self.startminp, self.getMasterWidth() / self.scale,
                                          self.getMasterHeight() / self.scale, self.ui)

    def setslider(self, slider, relative=False):
        if relative:
            self.slider += slider
        else:
            self.slider = slider
        self.limitpos()

    def setminp(self, minp):
        self.startminp = minp
        self.autoScale()

    def setmaxp(self, maxp):
        self.startmaxp = maxp
        self.autoScale()

    def draw(self, screen):
        if self.enabled:
            if self.glow != 0:
                screen.blit(self.glow_image, (
                    self.x * self.dir_scale[0] - self.glow * self.scale, self.y * self.dir_scale[1] - self.glow * self.scale))
            Draw.rect(screen, self.border_col,
                      Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                      self.height * self.scale), border_radius=int(self.rounded_corners * self.scale))
            if self.slider != self.minp:
                if self.direction == 'vertical':
                    h = ((
                                     self.height - self.top_border_size - self.bottom_border_size - self.button.height * self.contained_slider) * (
                                     (self.slider - self.minp) / (
                                         self.maxp - self.minp)) + self.button.height * self.contained_slider)
                    w = (self.width - self.left_border_size - self.right_border_size) - 2 * (
                            self.rounded_corners - abs(int(min([self.rounded_corners, h / 2]))))
                    Draw.rect(screen, self.col, Utils.roundRect(self.x * self.dir_scale[0] + self.left_border_size * self.scale,
                                                                self.y * self.dir_scale[1] + self.top_border_size * self.scale,
                                                                w * self.scale, h * self.scale),
                              border_radius=int(self.rounded_corners * self.scale))
                else:
                    w = ((
                                     self.width - self.left_border_size - self.right_border_size - self.button.width * self.contained_slider) * (
                                     (self.slider - self.minp) / (
                                         self.maxp - self.minp)) + self.button.width * self.contained_slider)
                    h = (self.height - self.top_border_size - self.bottom_border_size) - 2 * (
                            self.rounded_corners - abs(int(min([self.rounded_corners, w / 2]))))
                    Draw.rect(screen, self.col, Utils.roundRect(self.x * self.dir_scale[0] + self.left_border_size * self.scale,
                                                                self.y * self.dir_scale[1] + (
                                                                      self.height - h) / 2 * self.scale, w * self.scale,
                                                                h * self.scale),
                              border_radius=int(self.rounded_corners * self.scale))
