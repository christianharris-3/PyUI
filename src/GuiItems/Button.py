from src.GuiItems.GuiItem import GuiItem
import pygame
from src.Utils.Draw import Draw
from src.Utils.Utils import Utils

class Button(GuiItem):
    def child_gentext(self):
        if (self.img != self.toggleimg) or (self.text != self.toggletext):
            if type(self.img) != list:
                imgs = [self.toggleimg]
            else:
                imgs = self.toggleimg

            self.toggletextimages = []
            for img in imgs:
                if type(img) == str:
                    if len(imgs) != 1:
                        txt = img
                    else:
                        txt = self.toggletext
                    self.toggletextimages.append(
                        self.ui.rendertextlined(self.toggletext, self.textsize, self.textcol, self.togglecol, self.font,
                                                self.maxwidth, self.bold, True, center=self.textcenter, imgin=True,
                                                img=self.toggleimg, scale=self.scale, linelimit=self.linelimit,
                                                cutstartspaces=True))
                else:
                    self.toggletextimages.append(pygame.transform.scale(img, (
                    self.textsize, img.get_width() * self.textsize / img.get_height())))
                    if self.colorkey != -1: self.toggletextimages[-1].set_colorkey(self.colorkey)
            self.toggletextimage = self.toggletextimages[0]
            if len(self.toggletextimages) != 1:
                self.animating = True
        else:
            self.toggletextimages = self.textimages
            self.toggletextimage = self.toggletextimages[0]

    def child_autoscale(self):
        if len(self.textimages) > 0:
            imgsizes = [a.get_size() for a in self.textimages]
            if self.toggleable: imgsizes += [a.get_size() for a in self.toggletextimages]
            if self.startwidth == -1:
                self.width = max([a[0] for a in
                                  imgsizes]) / self.scale + self.horizontalspacing * 2 + self.leftborder + self.rightborder
            if self.startheight == -1:
                self.height = max([a[1] for a in
                                   imgsizes]) / self.scale + self.verticalspacing * 2 + self.upperborder + self.lowerborder

    ##    def child_refreshcords(self,ui):
    ##        self.colliderect = pygame.Rect(self.x+self.leftborder,self.y+self.upperborder,self.width-self.leftborder-self.rightborder,self.height-self.upperborder-self.lowerborder)
    def child_render(self, screen):
        self.innerrect = pygame.Rect(
            self.x * self.dirscale[0] + (self.leftborder + self.clickdownsize * self.holding) * self.scale,
            self.y * self.dirscale[1] + (self.upperborder + self.clickdownsize * self.holding) * self.scale,
            (self.width - self.leftborder - self.rightborder - self.clickdownsize * self.holding * 2) * self.scale,
            (self.height - self.upperborder - self.lowerborder - self.clickdownsize * self.holding * 2) * self.scale)
        self.clickrect = pygame.Rect(self.x * self.dirscale[0] + (self.leftborder - self.clickableborder) * self.scale,
                                     self.y * self.dirscale[1] + (self.upperborder - self.clickableborder) * self.scale,
                                     (
                                                 self.width - self.leftborder - self.rightborder + self.clickableborder * 2) * self.scale,
                                     (
                                                 self.height - self.upperborder - self.lowerborder + self.clickableborder * 2) * self.scale)
        self.getclickedon(self.clickrect)
        if self.clickedon > -1:
            if self.clickedon == 0: self.ui.mouseheld[self.clicktype][1] -= 1
        self.draw(screen)

    def draw(self, screen):
        if self.enabled:
            self.animatetext()
            col = self.col
            if not self.toggle: col = self.togglecol
            innerrect = Utils.roundrect(
                self.x * self.dirscale[0] + (self.leftborder + self.clickdownsize * self.holding) * self.scale,
                self.y * self.dirscale[1] + (self.upperborder + self.clickdownsize * self.holding) * self.scale,
                (self.width - self.leftborder - self.rightborder - self.clickdownsize * self.holding * 2) * self.scale,
                (
                            self.height - self.upperborder - self.lowerborder - self.clickdownsize * self.holding * 2) * self.scale)
            if self.holding or self.hovering:
                if not self.toggle:
                    col = self.togglehovercol
                else:
                    col = self.hovercol
            if self.glow != 0:
                screen.blit(self.glowimage, (
                self.x * self.dirscale[0] - self.glow * self.scale, self.y * self.dirscale[1] - self.glow * self.scale))
            if self.borderdraw:
                if self.backingdraw:
                    Draw.rect(screen, self.backingcol,
                              Utils.roundrect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                                        self.height * self.scale), border_radius=int(self.roundedcorners * self.scale))
                else:
                    Draw.rect(screen, self.backingcol,
                              Utils.roundrect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                                        self.height * self.scale),
                              int((self.border + self.clickdownsize * self.holding) * self.scale),
                              border_radius=int(self.roundedcorners * self.scale))
            if self.backingdraw: Draw.rect(screen, col, innerrect,
                                           border_radius=int((self.roundedcorners - self.border) * self.scale))
            if self.toggle:
                screen.blit(self.textimage, (self.x * self.dirscale[0] + ((self.width - self.leftborder - self.rightborder) / 2 + self.leftborder + self.textoffsetx) * self.scale - self.textimage.get_width() / 2,
                                             self.y * self.dirscale[1] + ((self.height - self.upperborder - self.lowerborder) / 2 + self.upperborder + self.textoffsety) * self.scale - self.textimage.get_height() / 2))
            else:
                screen.blit(self.toggletextimage, (self.x * self.dirscale[0] + ((self.width - self.leftborder - self.rightborder) / 2 + self.leftborder + self.textoffsetx) * self.scale - self.toggletextimage.get_width() / 2,
                                                   self.y * self.dirscale[1] + ((self.height - self.upperborder - self.lowerborder) / 2 + self.upperborder + self.textoffsety) * self.scale - self.toggletextimage.get_height() / 2))
