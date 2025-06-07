from UIpygame.Utils.Draw import Draw
from UIpygame.Utils import Utils
import pygame
from UIpygame.GuiItems.GuiItem import GuiItem
from UIpygame.GuiItems.Menu import Menu

class WindowedMenu(GuiItem):
    def reset(self):
        self.truedarken = self.darken
        self.resetCords()
        self.refresh()
        for a in self.ui.items:
            if a.menu == self.menu and a != self and not (type(a) in [Menu]) and type(a.master[0]) in [Menu,
                                                                                                       WindowedMenu]:
                self.binditem(a)
                a.refresh()
        self.ui.delete(f'auto_generated_menu:{self.menu}', False)
        self.bound_items.sort(key=lambda x: x.layer, reverse=False)

    def refresh(self):
        self.autoScale()
        self.refreshScale()
        self.refreshCords()
        self.refreshGlow()
        self.refreshBound()

    def child_refreshcords(self):
        for a in self.bound_items:
            a.resetCords()

    def child_render(self, screen):
        self.draw(screen)

    def draw(self, screen):
        if self.enabled:
            darkening = pygame.Surface((self.ui.screenw, self.ui.screenh), pygame.SRCALPHA)
            darkening.fill((0, 0, 0, self.darken))
            screen.blit(darkening, (0, 0))
            if self.glow != 0:
                screen.blit(self.glow_image, (
                    self.x * self.dir_scale[0] - self.glow * self.scale, self.y * self.dir_scale[1] - self.glow * self.scale))
            if self.backing_draw: Draw.rect(screen, self.col,
                                            Utils.roundrect(self.x * self.dir_scale[0], self.y * self.dir_scale[1],
                                                            self.width * self.scale, self.height * self.scale),
                                            self.border, border_radius=int(self.rounded_corners * self.scale))
