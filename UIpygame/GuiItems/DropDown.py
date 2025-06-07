from UIpygame.GuiItems.Button import Button
from UIpygame.Utils.Utils import Utils

class DropDown(Button):
    def mainbuttonclicked(self):
        if self.drops_down:
            if not self.window.opening:
                self.window.open('compressup', toggleopen=False)
            else:
                self.window.shut('compressup')
        else:
            index = self.options.index(self.active)
            index = (index + 1) % len(self.options)
            self.optionclicked(index)

    def setactive(self, name, command=True):
        if name in self.options:
            self.optionclicked(self.options.index(name), command)
            return True
        return False

    def optionclicked(self, index, command=True):
        self.active = self.options[index]
        if self.drops_down:
            self.titletext.settext(self.options[index])
            self.window.shut('compressup')
        else:
            self.settext(self.options[index])
        if command:
            self.truecommand()

    def refreshoptions(self):
        data = []
        for i, a in enumerate(self.options):
            func = Utils.Funcer(self.optionclicked, index=i)
            data.append([self.ui.makebutton(0, 0, a, self.text_size, font=self.font, bold=self.bold,
                                            text_col=self.text_col, col=self.col, roundedcorners=self.rounded_corners,
                                            command=func.func)])
        self.table.data = data
        self.table.refresh()

    def setoptions(self, options):
        self.options = options
        self.refreshoptions()
        self.window.child_autoscale()
        self.refresh()

    def child_refreshcords(self):
        if hasattr(self, "window"):
            self.window.width = self.width
            self.window.starty = self.height
            self.window.refreshCords()
            self.table.start_width = self.width - self.table.border_size * 2
            self.table.refresh()
