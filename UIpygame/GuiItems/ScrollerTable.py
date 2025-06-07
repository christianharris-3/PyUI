from UIpygame.GuiItems.Table import Table

class ScrollerTable(Table):
    def render(self, screen):
        if self.kill_time != -1 and self.kill_time < self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            self.child_render(screen)

            alltable = self.getalltableitems()

            for a in [i.ID for i in self.bound_items][:]:
                if a in self.ui.IDs and not (a in alltable):
                    self.ui.IDs[a].render(screen)

            reduce = 0
            if len(self.titles) != 0:
                reduce = (self.line_size + self.boxheights[0])
            self.ui.drawtosurf(screen, alltable, self.backing_col,
                               self.x * self.dir_scale[0] + self.line_size * self.scale,
                               self.y * self.dir_scale[1] + (self.line_size + reduce) * self.scale,
                               (self.x * self.dir_scale[0] + self.line_size * self.scale,
                                self.y * self.dir_scale[1] + (self.line_size + reduce) * self.scale,
                                (self.width - self.line_size * 2) * self.scale,
                                min(self.height - self.line_size * 2 - reduce,
                                    self.scroller.page_height - self.line_size * 2 - reduce) * self.scale),
                               'render', self.rounded_corners)

    def smartdraw(self, screen):
        self.child_render(screen)

        alltable = self.getalltableitems()

        for a in [i.ID for i in self.bound_items][:]:
            if a in self.ui.IDs and not (a in alltable):
                self.ui.IDs[a].draw(screen)

        if len(self.titles) != 0:
            reduce = (self.line_size + self.boxheights[0])
            self.ui.drawtosurf(screen, alltable, self.backing_col,
                               self.x * self.dir_scale[0] + self.line_size * self.scale,
                               self.y * self.dir_scale[1] + (self.line_size + reduce) * self.scale,
                               (self.x * self.dir_scale[0] + self.line_size * self.scale,
                                self.y * self.dir_scale[1] + (self.line_size + reduce) * self.scale,
                                (self.width - self.line_size * 2) * self.scale,
                                min(self.height - self.line_size * 2 - reduce,
                                    self.scroller.page_height - self.line_size * 2 - reduce) * self.scale),
                               'draw', self.rounded_corners)

    def scrollerblocks(self, scroller):
        scroller.limitPos()
        alltable = self.getalltableitems()
        for a in alltable:
            self.ui.IDs[a].scroll_cords = (0, scroller.value)
            self.ui.IDs[a].resetCords()

    def setscroll(self, scroll):
        self.scroller.setScroll(scroll)
        self.scrollerblocks(self.scroller)

    def getheight(self):
        return min(self.height, self.page_height)

    def refresh(self):
        self.refreshScale()
        self.preprocess()
        self.initheightwidth()
        self.estimatewidths()
        self.genText()
        active = self.scroller.active
        self.small_refresh()
        self.scroller.refresh()
        if self.scroller.active != active:
            self.small_refresh()
        self.scrollerblocks(self.scroller)
        self.threadactive = False

    def small_refresh(self):
        self.scroller.autoScale()
        self.scroller.checkActive()
        self.autoScale()
        self.initheightwidth()
        self.refreshGlow()
        self.gettablewidths()
        self.gettableheights()
        self.refreshClickableRect()
        self.refreshCords()
        self.scrollerblocks(self.scroller)
        self.refreshBound()
