class MENU(GUI_ITEM):
    def reset(self):
        self.refreshscale()
        self.resetcords()
        self.scalesize = False

    def refresh(self):
        self.refreshscale()
        self.resetcords()
        self.startwidth = self.ui.screenw
        self.startheight = self.ui.screenh
        self.width = self.ui.screenw
        self.height = self.ui.screenh
        self.refreshbound()

    def child_refreshcords(self):
        for a in self.bounditems:
            a.resetcords()

    def drawallmenu(self, screen, obj='self'):
        if obj == 'self':
            bound = self.bounditems
        else:
            bound = obj.bounditems

        for a in bound:
            if a.enabled:
                if type(a) == SCROLLERTABLE:
                    a.smartdraw(screen)
                else:
                    a.draw(screen)
                    self.drawallmenu(screen, a)

    def child_render(self, screen):
        pass

    def draw(self, screen):
        pass
