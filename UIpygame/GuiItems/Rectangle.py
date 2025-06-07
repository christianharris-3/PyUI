from UIpygame.GuiItems.GuiItem import GuiItem
from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.Utils import Utils

class Rectangle(GuiItem):
    def child_render(self, screen):
        self.getClickedOn()
        self.draw(screen)

    def draw(self, screen):
        if self.enabled:
            if self.glow != 0:
                screen.blit(self.glow_image, (
                    self.x * self.dir_scale[0] - self.glow * self.scale, self.y * self.dir_scale[1] - self.glow * self.scale))
            if self.backing_draw:
                Draw.rect(screen, self.col,
                          Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                          self.height * self.scale), self.border_size * self.scale,
                          border_radius=int(self.rounded_corners * self.scale))
