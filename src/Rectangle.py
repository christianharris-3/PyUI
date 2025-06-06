
class RECT(GUI_ITEM):
    def child_render(self, screen):
        self.getclickedon()
        self.draw(screen)

    def draw(self, screen):
        if self.enabled:
            if self.glow != 0:
                screen.blit(self.glowimage, (
                self.x * self.dirscale[0] - self.glow * self.scale, self.y * self.dirscale[1] - self.glow * self.scale))
            if self.backingdraw:
                draw.rect(screen, self.col,
                          roundrect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                                    self.height * self.scale), self.border * self.scale,
                          border_radius=int(self.roundedcorners * self.scale))
