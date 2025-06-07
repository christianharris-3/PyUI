from UIpygame.GuiItems.GuiItem import GuiItem
import pygame
from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.Utils import Utils

class Button(GuiItem):
    def child_gentext(self):
        if (self.img != self.toggle_img) or (self.text != self.toggle_text):
            if type(self.img) != list:
                imgs = [self.toggle_img]
            else:
                imgs = self.toggle_img

            self.toggletextimages = []
            for img in imgs:
                if type(img) == str:
                    if len(imgs) != 1:
                        txt = img
                    else:
                        txt = self.toggle_text
                    self.toggletextimages.append(
                        self.ui.rendertextlined(self.toggle_text, self.text_size, self.text_col, self.toggled_col, self.font,
                                                self.max_width, self.bold, True, center=self.text_center, imgin=True,
                                                img=self.toggle_img, scale=self.scale, linelimit=self.line_limit,
                                                cutstartspaces=True))
                else:
                    self.toggletextimages.append(pygame.transform.scale(img, (
                    self.text_size, img.get_width() * self.text_size / img.get_height())))
                    if self.colorkey != -1: self.toggletextimages[-1].set_colorkey(self.colorkey)
            self.toggletextimage = self.toggletextimages[0]
            if len(self.toggletextimages) != 1:
                self.animating = True
        else:
            self.toggletextimages = self.text_images
            self.toggletextimage = self.toggletextimages[0]

    def child_autoscale(self):
        if len(self.text_images) > 0:
            imgsizes = [a.get_size() for a in self.text_images]
            if self.toggleable: imgsizes += [a.get_size() for a in self.toggletextimages]
            if self.start_width == -1:
                self.width = max([a[0] for a in
                                  imgsizes]) / self.scale + self.horizontal_spacing * 2 + self.left_border_size + self.right_border_size
            if self.start_height == -1:
                self.height = max([a[1] for a in
                                   imgsizes]) / self.scale + self.vertical_spacing * 2 + self.top_border_size + self.bottom_border_size

    ##    def child_refreshcords(self,ui):
    ##        self.colliderect = pygame.Rect(self.x+self.left_border_size,self.y+self.top_border_size,self.width-self.left_border_size-self.right_border_size,self.height-self.top_border_size-self.bottom_border_size)
    def child_render(self, screen):
        self.innerrect = pygame.Rect(
            self.x * self.dir_scale[0] + (self.left_border_size + self.click_down_size * self.holding) * self.scale,
            self.y * self.dir_scale[1] + (self.top_border_size + self.click_down_size * self.holding) * self.scale,
            (self.width - self.left_border_size - self.right_border_size - self.click_down_size * self.holding * 2) * self.scale,
            (self.height - self.top_border_size - self.bottom_border_size - self.click_down_size * self.holding * 2) * self.scale)
        self.clickrect = pygame.Rect(self.x * self.dir_scale[0] + (self.left_border_size - self.clickable_border) * self.scale,
                                     self.y * self.dir_scale[1] + (self.top_border_size - self.clickable_border) * self.scale,
                                     (
                                             self.width - self.left_border_size - self.right_border_size + self.clickable_border * 2) * self.scale,
                                     (
                                             self.height - self.top_border_size - self.bottom_border_size + self.clickable_border * 2) * self.scale)
        self.getClickedOn(self.clickrect)
        if self.clicked_on > -1:
            if self.clicked_on == 0: self.ui.mouseheld[self.click_type][1] -= 1
        self.draw(screen)

    def draw(self, screen):
        if self.enabled:
            self.animatetext()
            col = self.col
            if not self.toggle: col = self.toggled_col
            innerrect = Utils.roundRect(
                self.x * self.dir_scale[0] + (self.left_border_size + self.click_down_size * self.holding) * self.scale,
                self.y * self.dir_scale[1] + (self.top_border_size + self.click_down_size * self.holding) * self.scale,
                (self.width - self.left_border_size - self.right_border_size - self.click_down_size * self.holding * 2) * self.scale,
                (
                        self.height - self.top_border_size - self.bottom_border_size - self.click_down_size * self.holding * 2) * self.scale)
            if self.holding or self.hovering:
                if not self.toggle:
                    col = self.toggled_hover_col
                else:
                    col = self.hover_col
            if self.glow != 0:
                screen.blit(self.glow_image, (
                    self.x * self.dir_scale[0] - self.glow * self.scale, self.y * self.dir_scale[1] - self.glow * self.scale))
            if self.border_draw:
                if self.backing_draw:
                    Draw.rect(screen, self.backing_col,
                              Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                              self.height * self.scale), border_radius=int(self.rounded_corners * self.scale))
                else:
                    Draw.rect(screen, self.backing_col,
                              Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                              self.height * self.scale),
                              int((self.border + self.click_down_size * self.holding) * self.scale),
                              border_radius=int(self.rounded_corners * self.scale))
            if self.backing_draw: Draw.rect(screen, col, innerrect,
                                            border_radius=int((self.rounded_corners - self.border) * self.scale))
            if self.toggle:
                screen.blit(self.textimage, (self.x * self.dir_scale[0] + ((self.width - self.left_border_size - self.right_border_size) / 2 + self.left_border_size + self.text_offset_x) * self.scale - self.textimage.get_width() / 2,
                                             self.y * self.dir_scale[1] + ((self.height - self.top_border_size - self.bottom_border_size) / 2 + self.top_border_size + self.text_offset_y) * self.scale - self.textimage.get_height() / 2))
            else:
                screen.blit(self.toggletextimage, (self.x * self.dir_scale[0] + ((self.width - self.left_border_size - self.right_border_size) / 2 + self.left_border_size + self.text_offset_x) * self.scale - self.toggletextimage.get_width() / 2,
                                                   self.y * self.dir_scale[1] + ((self.height - self.top_border_size - self.bottom_border_size) / 2 + self.top_border_size + self.text_offset_y) * self.scale - self.toggletextimage.get_height() / 2))
