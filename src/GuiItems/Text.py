from src.GuiItems.GuiItem import GuiItem
from src.Utils.Draw import Draw
from src.Utils.Utils import Utils

class Text(GuiItem):
    def reset(self):
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.resetcords()
        self.refreshcords()
        self.refreshglow()
    def child_autoscale(self):
        if self.startwidth == -1:
            self.width = max([a.get_width() for a in self.textimages])/self.scale+self.horizontalspacing*2
        if self.startheight == -1:
            self.height = max([a.get_height() for a in self.textimages])/self.scale+self.verticalspacing*2
    def child_render(self,screen):
        self.getclickedon()
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            self.animatetext()
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.backingdraw:
                Draw.rect(screen,self.col,Utils.roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
            if self.borderdraw:
                Draw.rect(screen,self.bordercol,Utils.roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),self.border*self.scale,border_radius=int(self.roundedcorners*self.scale))
            if self.pregenerated:
                if self.textcenter:
                    try:
                        screen.blit(self.textimage,(self.x*self.dirscale[0]+self.width/2*self.scale-self.textimage.get_width()/2,self.y*self.dirscale[1]+self.height/2*self.scale-self.textimage.get_height()/2))
                    except:
                        print('error in drawing',self.ID)
                else:
                    try:
                        screen.blit(self.textimage,(self.x*self.dirscale[0]+(self.horizontalspacing+self.textoffsetx)*self.scale,self.y*self.dirscale[1]+(self.verticalspacing+self.textoffsetx)*self.scale))
                    except:
                        print('error in drawing',self.ID)
            else:
                self.ui.write(screen,self.x*self.dirscale[0]+(self.horizontalspacing+self.textoffsetx)*self.scale,self.y*self.dirscale[1]+(self.verticalspacing+self.textoffsetx)*self.scale,self.text,self.textsize*self.scale,self.textcol,self.textcenter,self.font,self.bold,self.antialiasing)
    def refresh(self):
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.refreshcords()
        self.refreshglow()
        self.resetcords()
        self.refreshbound()
        self.refreshclickablerect()
