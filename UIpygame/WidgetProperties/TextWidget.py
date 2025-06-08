from abc import ABC, abstractmethod
from UIpygame.Widgets.GuiItem import GuiItem

class TextWidget(GuiItem, ABC):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def genText(self):
        ui = self.ui
        self.current_frame = 0
        if type(self.img) != list:
            imgs = [self.img]
        else:
            imgs = self.img
            if len(imgs) < 1: imgs.append('')

        self.text_images = []
        for img in imgs:
            if type(img) == str:
                if len(imgs) != 1:
                    txt = img
                else:
                    txt = self.text
                self.text_images.append(
                    ui.rendertextlined(txt, self.text_size, self.text_col, self.col, self.font, self.max_width, self.bold,
                                       self.antialiasing, self.text_center, imgin=True, img=img, scale=self.scale,
                                       linelimit=self.line_limit, cutstartspaces=True))
            else:
                self.text_images.append(pygame.transform.scale(img, (
                img.get_width() * (self.text_size / img.get_height()) * self.scale,
                img.get_height() * (self.text_size / img.get_height()) * self.scale)))
            if self.colorkey != -1: self.text_images[-1].set_colorkey(self.colorkey)
        self.textimage = self.text_images[0]
        if len(self.text_images) != 1:
            self.animating = True
        self.childGenText()

    def childGenText(self):
        # this function does not need to be implemented
        pass

    def animateText(self):
        if self.animating:
            self.animate += 1
            if self.animate % self.animation_speed == 0:
                self.current_frame += 1
                if self.current_frame == len(self.text_images):
                    self.current_frame = 0
                self.textimage = self.text_images[self.current_frame]

    def setText(self, text):
        self.text = str(text)
        self.refresh()

    def setTextSize(self, text_size):
        self.text_size = text_size
        self.refresh()

    def setTextCol(self, col):
        self.text_col = col
        self.refresh()
