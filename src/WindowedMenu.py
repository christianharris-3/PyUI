class WINDOWEDMENU(GUI_ITEM):
    def reset(self):
        self.truedarken = self.darken
        self.resetcords()
        self.refresh()
        for a in self.ui.items:
            if a.menu == self.menu and a!=self and not(type(a) in [MENU]) and type(a.master[0]) in [MENU,WINDOWEDMENU]:
                self.binditem(a)
                a.refresh()
        self.ui.delete(f'auto_generated_menu:{self.menu}',False)
        self.bounditems.sort(key=lambda x: x.layer,reverse=False)
    def refresh(self):
        self.autoscale()
        self.refreshscale()
        self.refreshcords()
        self.refreshglow()
        self.refreshbound()
    def child_refreshcords(self):
        for a in self.bounditems:
            a.resetcords()
    def child_render(self,screen):
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            darkening = pygame.Surface((self.ui.screenw,self.ui.screenh),pygame.SRCALPHA)
            darkening.fill((0,0,0,self.darken))
            screen.blit(darkening,(0,0))
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.backingdraw:
                draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),self.border,border_radius=int(self.roundedcorners*self.scale))
