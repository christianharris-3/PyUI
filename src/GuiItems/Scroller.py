from src.GuiItems.GuiItem import GuiItem
import pygame
from src.Utils.Utils import Utils
from src.Utils.Draw import Draw

class Scroller(GuiItem):
    def reset(self):
        self.autoscale()
        self.scroll = self.startp
        self.scheight = self.height - self.border * 2
        self.prevholding = self.holding
        self.refreshscale()
        self.refresh()
        self.resetcords()
        self.checkactive()
        self.refreshclickablerect()

    def child_render(self, screen):
        self.checkactive()
        if self.active:
            temp = (self.x, self.y)
            self.getclickedon(pygame.Rect(self.x * self.dirscale[0] + self.leftborder * self.scale,
                                          self.y * self.dirscale[1] + (self.border + self.scroll * (
                                                      self.scheight / (self.maxp - self.minp))) * self.scale,
                                          (self.width - self.leftborder - self.rightborder) * self.scale,
                                          ((self.pageheight / (self.maxp - self.minp)) * self.scheight) * self.scale),
                              smartdrag=False)
            if self.holding:
                self.scroll = (self.y - temp[1]) * self.dirscale[1] / self.dirscale[0] / (
                            self.scheight / (self.maxp - self.minp))
                self.limitpos()
            self.x, self.y = temp
            self.scrollobjects()
            self.draw(screen)

    def child_autoscale(self):
        compress = 1
        if self.screencompressed:
            if self.y * self.dirscale[1] + self.height * self.scale > self.ui.screenh:
                compress = 1 - (self.y * self.dirscale[
                    1] + self.height * self.scale - self.ui.screenh + self.screencompressed) / (
                                       self.height * self.scale)
        self.height *= compress
        self.scheight = self.height - self.border * 2
        self.maxp = Utils.relativetoval(self.startmaxp, self.getmasterwidth() / self.scale,
                                  self.getmasterheight() / self.scale, self.ui)
        self.minp = Utils.relativetoval(self.startminp, self.getmasterwidth() / self.scale,
                                  self.getmasterheight() / self.scale, self.ui)
        self.pageheight = Utils.relativetoval(self.startpageheight, self.getmasterwidth() / self.scale,
                                        self.getmasterheight() / self.scale, self.ui) * compress

    def limitpos(self):
        if not self.active:
            self.scroll = self.minp
        elif self.scroll < self.minp:
            self.scroll = self.minp
        elif self.scroll > self.maxp - self.pageheight:
            self.scroll = self.maxp - self.pageheight

    def refresh(self):
        self.autoscale()
        self.refreshcords()
        self.checkactive()
        self.limitpos()
        self.refreshbound()

    def checkactive(self):
        if (self.maxp - self.minp) > self.pageheight:
            self.active = True
        else:
            self.active = False

    def setscroll(self, scroll, relative=False):
        if relative:
            self.scroll += scroll
        else:
            self.scroll = scroll
        self.limitpos()

    def setminp(self, minp):
        self.startminp = minp
        self.autoscale()

    def setmaxp(self, maxp):
        self.startmaxp = maxp
        self.autoscale()

    def setpageheight(self, pageheight):
        self.startpageheight = pageheight
        self.autoscale()

    def scrollobjects(self):
        for a in self.scrollbind:
            if self.ui.IDs[a].scrollcords != (self.ui.IDs[a].scrollcords[0], self.scroll):
                self.ui.IDs[a].scrollcords = (self.ui.IDs[a].scrollcords[0], self.scroll)
                self.ui.IDs[a].resetcords()

    def child_refreshcords(self):
        if self.maxp - self.minp == 0: self.maxp = self.minp + 0.1

    ##        self.sliderrect = pygame.Rect(self.x+self.border,self.y+self.border+self.scroll*(self.scheight/(self.maxp-self.minp)),self.scrollerwidth,self.scrollerheight)

    def draw(self, screen):
        if self.enabled and self.active:
            if self.glow != 0:
                screen.blit(self.glowimage, (
                self.x * self.dirscale[0] - self.glow * self.scale, self.y * self.dirscale[1] - self.glow * self.scale))
            Draw.rect(screen, self.col,
                      Utils.roundrect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                                self.height * self.scale), border_radius=int(self.roundedcorners * self.scale))
            Draw.rect(screen, self.scrollercol, Utils.roundrect(self.x * self.dirscale[0] + self.leftborder * self.scale,
                                                          self.y * self.dirscale[1] + (self.border + self.scroll * (
                                                                      self.scheight / (
                                                                          self.maxp - self.minp))) * self.scale, (
                                                                      self.width - self.leftborder - self.rightborder) * self.scale,
                                                          ((self.pageheight / (
                                                                      self.maxp - self.minp)) * self.scheight) * self.scale),
                      border_radius=int(self.roundedcorners * self.scale))
