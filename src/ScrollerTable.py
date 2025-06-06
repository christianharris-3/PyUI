class SCROLLERTABLE(TABLE):
    def render(self, screen):
        if self.killtime != -1 and self.killtime < self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            self.child_render(screen)

            alltable = self.getalltableitems()

            for a in [i.ID for i in self.bounditems][:]:
                if a in self.ui.IDs and not (a in alltable):
                    self.ui.IDs[a].render(screen)

            reduce = 0
            if len(self.titles) != 0:
                reduce = (self.linesize + self.boxheights[0])
            self.ui.drawtosurf(screen, alltable, self.backingcol,
                               self.x * self.dirscale[0] + self.linesize * self.scale,
                               self.y * self.dirscale[1] + (self.linesize + reduce) * self.scale,
                               (self.x * self.dirscale[0] + self.linesize * self.scale,
                                self.y * self.dirscale[1] + (self.linesize + reduce) * self.scale,
                                (self.width - self.linesize * 2) * self.scale,
                                min(self.height - self.linesize * 2 - reduce,
                                    self.scroller.pageheight - self.linesize * 2 - reduce) * self.scale),
                               'render', self.roundedcorners)

    def smartdraw(self, screen):
        self.child_render(screen)

        alltable = self.getalltableitems()

        for a in [i.ID for i in self.bounditems][:]:
            if a in self.ui.IDs and not (a in alltable):
                self.ui.IDs[a].draw(screen)

        reduce = 0
        if len(self.titles) != 0:
            reduce = (self.linesize + self.boxheights[0])
            self.ui.drawtosurf(screen, alltable, self.backingcol,
                               self.x * self.dirscale[0] + self.linesize * self.scale,
                               self.y * self.dirscale[1] + (self.linesize + reduce) * self.scale,
                               (self.x * self.dirscale[0] + self.linesize * self.scale,
                                self.y * self.dirscale[1] + (self.linesize + reduce) * self.scale,
                                (self.width - self.linesize * 2) * self.scale,
                                min(self.height - self.linesize * 2 - reduce,
                                    self.scroller.pageheight - self.linesize * 2 - reduce) * self.scale),
                               'draw', self.roundedcorners)

    def scrollerblocks(self, scroller):
        scroller.limitpos()
        alltable = self.getalltableitems()
        for a in alltable:
            self.ui.IDs[a].scrollcords = (0, scroller.scroll)
            self.ui.IDs[a].resetcords()

    def setscroll(self, scroll):
        self.scroller.setscroll(scroll)
        self.scrollerblocks(self.scroller)

    def getheight(self):
        return min(self.height, self.pageheight)

    def refresh(self):
        self.refreshscale()
        self.preprocess()
        self.initheightwidth()
        self.estimatewidths()
        self.gentext()
        active = self.scroller.active
        self.small_refresh()
        self.scroller.refresh()
        if self.scroller.active != active:
            self.small_refresh()
        self.scrollerblocks(self.scroller)
        self.threadactive = False

    def small_refresh(self):
        self.scroller.autoscale()
        self.scroller.checkactive()
        self.autoscale()
        self.initheightwidth()
        self.refreshglow()
        self.gettablewidths()
        self.gettableheights()
        self.refreshclickablerect()
        self.refreshcords()
        self.scrollerblocks(self.scroller)
        self.refreshbound()
