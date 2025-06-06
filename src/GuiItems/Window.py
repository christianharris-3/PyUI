import pygame
import math
from src.GuiItems.GuiItem import GuiItem
from src.Utils.Draw import Draw
from src.Utils.Utils import Utils

class Window(GuiItem):
    def reset(self):
        self.refreshscale()
        self.autoscale()
        self.refreshcords()
        self.resetcords()
        self.refresh()
        self.clearanimations()
        self.opening = self.enabled
        self.canclickout = False
        self.progress = 1

    def clearanimations(self):
        self.animationdata = {'moveleft': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True},
                              'moveright': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True},
                              'moveup': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True},
                              'movedown': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True},
                              'compressleft': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True},
                              'compressright': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True},
                              'compressup': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True},
                              'compressdown': {'active': False, 'progress': 0, 'wave': 'linear', 'forward': True}}

    def refresh(self):
        self.autoscale()
        self.refreshscale()
        self.refreshcords()
        self.refreshglow()
        self.refreshbound()

    def enable(self):
        self.enabled = True
        self.child_autoscale()

    def disable(self):
        self.enabled = False
        self.child_autoscale()

    def open(self, animation='default', animationlength=-1, toggleopen=True):
        if animation == 'default': animation = self.animationtype
        if animationlength == -1: animationlength = self.animationspeed
        if not self.opening:
            self.enable()
            for a in self.autoshutwindows:
                if self.ui.IDs[a] != self:
                    self.ui.IDs[a].shut()
            self.canclickout = False
            self.opening = True
            self.makeanimation(animation, animationlength, False)
        elif toggleopen:
            self.shut()

    def shut(self, animation='default', animationlength=-1):
        if self.opening:
            if animation == 'default': animation = self.animationtype
            if animationlength == -1: animationlength = self.animationspeed
            self.opening = False
            self.makeanimation(animation, flippable=False)
            if animation == 'none': self.disable()

    def makeanimation(self, animation='default', length=-1, forward=True, flippable=True):
        if animation == 'default': animation = self.animationtype
        if length == -1: length = self.animationspeed
        if animation != 'none':
            self.enable()
            for a in animation.split():
                if a.split(':')[0] in list(self.animationdata):
                    if self.animationdata[a.split(':')[0]]['active']:
                        if flippable or self.animationdata[a.split(':')[0]]['forward'] != forward:
                            self.animationdata[a.split(':')[0]]['progress'] = 1 - self.animationdata[a.split(':')[0]][
                                'progress']
                            self.animationdata[a.split(':')[0]]['forward'] = not self.animationdata[a.split(':')[0]][
                                'forward']
                    else:
                        wave = 'sinout'
                        if len(a.split(':')) > 1:
                            if a.split(':')[1] in ['linear', 'sin', 'sinin', 'sinout']:
                                wave = a.split(':')[1]
                        self.animationdata[a.split(':')[0]]['progress'] = 0
                        self.animationdata[a.split(':')[0]]['active'] = True
                        self.animationdata[a.split(':')[0]]['wave'] = wave
                        self.animationdata[a.split(':')[0]]['forward'] = forward
            self.animationlength = length

    def decodeanimations(self):
        xoff = 0
        yoff = 0
        objxoff = 0
        objyoff = 0
        widthoff = 0
        heightoff = 0
        self.progress = 1
        for a in self.animationdata:
            if self.animationdata[a]['active']:
                prog = self.convertprogress(self.animationdata[a])
                if prog != 0: self.progress = 1 - prog
                if 'move' in a:
                    if 'left' in a:
                        xoff -= prog * (self.x + self.width)
                    elif 'right' in a:
                        xoff += prog * (self.ui.screenw / self.scale - self.x)
                    if 'up' in a:
                        yoff -= prog * (self.y + self.height)
                    elif 'down' in a:
                        yoff += prog * (self.ui.screenh / self.scale - self.y)
                elif 'compress' in a:
                    if 'left' in a:
                        widthoff -= prog * (self.width)
                        objxoff += prog * (self.width)
                    elif 'right' in a:
                        widthoff -= prog * (self.width)
                        xoff += prog * (self.width)
                    if 'up' in a:
                        heightoff -= prog * (self.height)
                        objyoff += prog * (self.height)
                    elif 'down' in a:
                        heightoff -= prog * (self.height)
                        yoff += prog * (self.height)
        return xoff, yoff, objxoff, objyoff, widthoff, heightoff

    def moveanimation(self):
        for a in self.animationdata:
            if self.animationdata[a]['active']:
                self.animationdata[a]['progress'] += self.ui.deltatime / self.animationlength
                if self.animationdata[a]['progress'] > 1:
                    self.animationdata[a]['active'] = False
                    if self.animationdata[a]['forward']:
                        self.disable()

    def convertprogress(self, data):
        progress = data['progress']
        wave = data['wave']
        if not data['forward']: progress = 1 - progress
        if wave == 'sinin':
            return math.sin(progress * math.pi / 2)
        elif wave == 'sinout':
            return math.sin((progress - 1) * math.pi / 2) + 1
        elif wave == 'siun':
            return math.sin((progress - 0.5) * math.pi) / 2 + 0.5
        else:
            return progress

    def child_autoscale(self):
        self.refreshnoclickrect()
        self.ui.refreshnoclickrects()
        for a in self.bounditems: a.clickablerect = self.clickablerect

    def refreshnoclickrect(self):
        # Rect,IDs,menu,whitelist (true=all objects in list blocked by noclickrect)
        if self.enabled:
            self.noclickrect = [(pygame.Rect(self.x * self.dirscale[0], self.y * self.dirscale[1],
                                             self.width * self.scale, self.height * self.scale), self.getchildIDs(),
                                 self.getmenu(), False)]
        else:
            self.noclickrect = []

    def binditem(self, obj):
        super().binditem(obj)
        obj.resetcords()
        self.child_autoscale()

    def render(self, screen):
        if self.isolated:
            if not self.ui.mprs[0]:
                self.canclickout = True
            if self.canclickout and self.opening:
                self.getclickedon()
                if self.ui.mprs[0] and not self.holding:
                    self.shut()
        if self.forceholding:
            self.open()
            self.forceholding = False
        self.moveanimation()
        self.xoff, self.yoff, self.objxoff, self.objyoff, self.widthoff, self.heightoff = self.decodeanimations()
        if self.killtime != -1 and self.killtime < self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:

            self.child_render(screen)

            self.ui.drawtosurf(screen, [a.ID for a in self.bounditems], self.col,
                               self.x * self.dirscale[0] + self.xoff * self.scale,
                               self.y * self.dirscale[1] + self.yoff * self.scale, (
                               self.x * self.dirscale[0] + self.objxoff * self.scale,
                               self.y * self.dirscale[1] + self.objyoff * self.scale,
                               (self.width + self.widthoff) * self.scale, (self.height + self.heightoff) * self.scale),
                               'render', self.roundedcorners)

    def child_render(self, screen):
        self.draw(screen)

    def draw(self, screen):
        if self.enabled:
            if self.darken != 0:
                darken = self.darken * self.progress
                darkening = pygame.Surface((self.ui.screenw, self.ui.screenh), pygame.SRCALPHA)
                darkening.fill((0, 0, 0, darken))
                screen.blit(darkening, (0, 0))
            if self.glow != 0:
                screen.blit(self.glowimage, (
                self.x * self.dirscale[0] - self.glow * self.scale, self.y * self.dirscale[1] - self.glow * self.scale))
            if self.backingdraw:
                Draw.rect(screen, self.col, Utils.roundrect(self.x * self.dirscale[0] + self.xoff * self.scale,
                                                      self.y * self.dirscale[1] + self.yoff * self.scale,
                                                      (self.width + self.widthoff) * self.scale,
                                                      (self.height + self.heightoff) * self.scale),
                          border_radius=int(self.roundedcorners * self.scale))
