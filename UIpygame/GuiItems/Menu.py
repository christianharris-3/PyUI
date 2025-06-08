from UIpygame.GuiItems.GuiItem import GuiItem
from UIpygame.GuiItems.ScrollerTable import ScrollerTable

class Menu(GuiItem):
    def reset(self):
        self.refreshScale()
        self.resetCords()
        self.scalesize = False

    def refresh(self):
        self.refreshScale()
        self.resetCords()
        self.startwidth = self.ui.screenw
        self.startheight = self.ui.screenh
        self.width = self.ui.screenw
        self.height = self.ui.screenh
        self.refreshBound()

    def childRefreshCords(self):
        for a in self.bound_items:
            a.resetCords()

    def drawallmenu(self, screen, obj='self'):
        if obj == 'self':
            bound = self.bound_items
        else:
            bound = obj.bound_items

        for a in bound:
            if a.enabled:
                if type(a) == ScrollerTable:
                    a.smartdraw(screen)
                else:
                    a.draw(screen)
                    self.drawallmenu(screen, a)

    def child_render(self, screen):
        pass

    def draw(self, screen):
        pass
