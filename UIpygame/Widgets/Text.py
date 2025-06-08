from UIpygame.Widgets.GuiItem import GuiItem
from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.Utils import Utils

class Text(GuiItem):
    def reset(self):
        self.refreshScale()
        self.genText()
        self.autoScale()
        self.resetCords()
        self.refreshCords()
        self.refreshGlow()
    def childAutoScale(self):
        if self.start_width == -1:
            self.width = max([a.get_width() for a in self.text_images]) / self.scale + self.horizontal_spacing * 2
        if self.start_height == -1:
            self.height = max([a.get_height() for a in self.text_images]) / self.scale + self.vertical_spacing * 2
    def child_render(self,screen):
        self.getClickedOn()
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            self.animateText()
            if self.glow!=0:
                screen.blit(self.glow_image, (self.x * self.dir_scale[0] - self.glow * self.scale, self.y * self.dir_scale[1] - self.glow * self.scale))
            if self.backing_draw:
                Draw.rect(screen, self.col, Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale, self.height * self.scale), border_radius=int(self.rounded_corners * self.scale))
            if self.border_draw:
                Draw.rect(screen, self.border_col, Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale, self.height * self.scale), self.border * self.scale, border_radius=int(self.rounded_corners * self.scale))
            if self.pre_generate_text:
                if self.text_center:
                    try:
                        screen.blit(self.textimage, (self.x * self.dir_scale[0] + self.width / 2 * self.scale - self.textimage.get_width() / 2, self.y * self.dir_scale[1] + self.height / 2 * self.scale - self.textimage.get_height() / 2))
                    except:
                        print('error in drawing',self.ID)
                else:
                    try:
                        screen.blit(self.textimage, (self.x * self.dir_scale[0] + (self.horizontal_spacing + self.text_offset_x) * self.scale, self.y * self.dir_scale[1] + (self.vertical_spacing + self.text_offset_x) * self.scale))
                    except:
                        print('error in drawing',self.ID)
            else:
                self.ui.write(screen, self.x * self.dir_scale[0] + (self.horizontal_spacing + self.text_offset_x) * self.scale, self.y * self.dir_scale[1] + (self.vertical_spacing + self.text_offset_x) * self.scale, self.text, self.text_size * self.scale, self.text_col, self.text_center, self.font, self.bold, self.antialiasing)
    def refresh(self):
        self.refreshScale()
        self.genText()
        self.autoScale()
        self.refreshCords()
        self.refreshGlow()
        self.resetCords()
        self.refreshBound()
        self.refreshClickableRect()
