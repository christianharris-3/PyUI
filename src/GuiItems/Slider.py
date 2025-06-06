from src.GuiItems.GuiItem import GuiItem
from src.GuiItems.Button import Button
from src.Utils.Draw import Draw
from src.Utils.Utils import Utils
from src.Utils.ColEdit import ColEdit

class Slider(GuiItem):
    def reset(self):
        self.slider = self.startp
        self.holding = False
        self.prevholding = False
        self.holdingcords = [self.x, self.y]
        self.refreshscale()
        self.resetbutton()
        self.resetcords()
        self.roundedcorners = min([self.roundedcorners, self.width / 2, self.height / 2])

    def refresh(self):
        self.autoscale()
        self.limitpos()
        self.refreshbutton()
        self.refreshglow()
        self.refreshbound()

    def child_refreshcords(self):
        ##        self.
        ##        self.innerrect = pygame.Rect(self.slidercenter[0]-self.slidersize/2+self.border,self.slidercenter[1]-self.slidersize/2+self.border,self.slidersize-self.border*2,self.slidersize-self.border*2)
        self.refreshbuttoncords()

    def resetbutton(self):
        self.getslidercenter()
        try:
            self.bounditems.remove(self.button)
            self.ui.delete(self.button.ID, False)
        except:
            pass
        if type(self.data) == Button:
            self.button = self.data
        else:
            self.button = self.ui.makebutton(0, 0, self.text, self.textsize, Utils.emptyFunction, self.menu,
                                             self.ID + 'button', self.layer + 0.01, self.roundedcorners,
                                             width=self.slidersize, height=self.slidersize, img=self.img,
                                             dragable=self.dragable,
                                             clickdownsize=int(self.slidersize / 15), col=ColEdit.shiftcolor(self.col, -30),
                                             scaleby=self.scaleby)

        if self.direction == 'vertical':
            self.button.startobjanchor = [self.button.width / 2, self.button.height / 2]
        else:
            self.button.startobjanchor = ['w/2', 'h/2']
        self.button.dragable = False
        self.binditem(self.button)

    def getslidercenter(self):
        offset = 0
        if self.containedslider:
            if type(self.data) == Button:
                offset = self.data.width / 2
            else:
                offset = self.slidersize / 2
        if self.maxp - self.minp != 0:
            pos = (self.slider - self.minp) / (self.maxp - self.minp)
        else:
            pos = 0

        self.slidercenter = (
        self.leftborder + offset + (self.width - self.leftborder - self.rightborder - offset * 2) * pos,
        self.height / 2)
        if self.direction == 'vertical':
            if self.containedslider: offset = self.button.height / 2
            self.slidercenter = (self.width / 2, self.upperborder + offset + (
                        self.height - self.upperborder - self.lowerborder - offset * 2) * pos)

    def refreshbuttoncords(self):
        self.getslidercenter()
        self.button.startx = self.slidercenter[0]
        self.button.starty = self.slidercenter[1]
        self.button.startanchor = [0, 0]
        self.button.resetcords(False)

    def refreshbutton(self):
        self.button.refresh()
        self.refreshbuttoncords()

    def updatetext(self):
        if self.boundtext != -1:
            self.boundtext.settext(str(self.slider))

    def child_render(self, screen):
        self.draw(screen)
        if self.button.holding:
            self.movetomouse()
        if self.button.clickedon == self.runcommandat:
            self.command()
        if self.movetoclick: self.movebuttontoclick()

    def movebuttontoclick(self):
        self.getclickedon(Utils.roundrect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                                    self.height * self.scale), False, False)
        if self.clickedon == 0:
            self.button.holding = True
            self.button.holdingcords = [self.button.width / 2, self.button.height / 2]

    def movetomouse(self):
        if self.maxp - self.minp != 0:
            pos = self.scale / (self.maxp - self.minp)
        else:
            pos = 0
        self.slider = (self.ui.mpos[0] - self.x * self.dirscale[0] - self.leftborder * self.scale) / (
                    (self.width - self.leftborder - self.rightborder) * pos) + self.minp
        if self.direction == 'vertical':
            self.slider = (self.ui.mpos[1] - self.y * self.dirscale[1] - self.upperborder * self.scale) / (
                        (self.height - self.upperborder - self.lowerborder) * pos) + self.minp
        if self.increment != 0: self.slider = round(self.slider / self.increment) * self.increment
        self.limitpos()
        self.updatetext()

    def limitpos(self):
        if self.slider > self.maxp:
            self.slider = self.maxp
        elif self.slider < self.minp:
            self.slider = self.minp
        self.refreshbuttoncords()

    def child_autoscale(self):
        self.maxp = Utils.relativetoval(self.startmaxp, self.getmasterwidth() / self.scale,
                                  self.getmasterheight() / self.scale, self.ui)
        self.minp = Utils.relativetoval(self.startminp, self.getmasterwidth() / self.scale,
                                  self.getmasterheight() / self.scale, self.ui)

    def setslider(self, slider, relative=False):
        if relative:
            self.slider += slider
        else:
            self.slider = slider
        self.limitpos()

    def setminp(self, minp):
        self.startminp = minp
        self.autoscale()

    def setmaxp(self, maxp):
        self.startmaxp = maxp
        self.autoscale()

    def draw(self, screen):
        if self.enabled:
            if self.glow != 0:
                screen.blit(self.glowimage, (
                self.x * self.dirscale[0] - self.glow * self.scale, self.y * self.dirscale[1] - self.glow * self.scale))
            Draw.rect(screen, self.bordercol,
                      Utils.roundrect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                                self.height * self.scale), border_radius=int(self.roundedcorners * self.scale))
            if self.slider != self.minp:
                if self.direction == 'vertical':
                    h = ((
                                     self.height - self.upperborder - self.lowerborder - self.button.height * self.containedslider) * (
                                     (self.slider - self.minp) / (
                                         self.maxp - self.minp)) + self.button.height * self.containedslider)
                    w = (self.width - self.leftborder - self.rightborder) - 2 * (
                                self.roundedcorners - abs(int(min([self.roundedcorners, h / 2]))))
                    Draw.rect(screen, self.col, Utils.roundrect(self.x * self.dirscale[0] + self.leftborder * self.scale,
                                                          self.y * self.dirscale[1] + self.upperborder * self.scale,
                                                          w * self.scale, h * self.scale),
                              border_radius=int(self.roundedcorners * self.scale))
                else:
                    w = ((
                                     self.width - self.leftborder - self.rightborder - self.button.width * self.containedslider) * (
                                     (self.slider - self.minp) / (
                                         self.maxp - self.minp)) + self.button.width * self.containedslider)
                    h = (self.height - self.upperborder - self.lowerborder) - 2 * (
                                self.roundedcorners - abs(int(min([self.roundedcorners, w / 2]))))
                    Draw.rect(screen, self.col, Utils.roundrect(self.x * self.dirscale[0] + self.leftborder * self.scale,
                                                          self.y * self.dirscale[1] + (
                                                                      self.height - h) / 2 * self.scale, w * self.scale,
                                                          h * self.scale),
                              border_radius=int(self.roundedcorners * self.scale))
