from abc import ABC
import time
import pygame
from src.Utils.Utils import Utils
from src.Utils.ColEdit import ColEdit
from src.Utils.Draw import Draw
from src.Utils.Collision import Collision
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Scroller import Scroller


class GuiItem(ABC):
    def __init__(self, **kwargs):
        try:
            self.gui_item_data = self.getDataClass(**kwargs)
        except TypeError as e:
            error = TypeError(self.__class__.__name__ + "() {}".format(str(e)[11:]))
            raise error from None
        return
        self.splitDataClasses()
        self.creationLogic()

        if True:
            defaulttype = type(self)
            if 'defaulttype' in args: defaulttype = args['defaulttype']
            for var in Style.objectdefaults[defaulttype]:
                if not (var in args):
                    args[var] = Style.objectdefaults[type(self)][var]
                elif args[var] == Style.universaldefaults[var]:
                    args[var] = Style.objectdefaults[type(self)][var]

            args = Utils.filloutargs(args)
            ui = args.pop('ui')
            self.ui = ui

            self.enabled = args['enabled']
            self.center = args['center']
            if args['centery'] == -1:
                self.centery = self.center
            else:
                self.centery = args['centery']
            self.x = args['x']
            self.y = args['y']
            self.startx = args['x']
            self.starty = args['y']
            self.startanchor = list(args['anchor'])
            self.startobjanchor = list(args['objanchor'])
            if self.center and self.startobjanchor[0] == 0: self.startobjanchor[0] = 'w/2'
            if self.centery and self.startobjanchor[1] == 0: self.startobjanchor[1] = 'h/2'
            self.scrollcords = args['scrollcords']
            self.refreshbind = list(args['refreshbind'])[:]
            if type(args['presskeys']) == list:
                self.presskeys = args['presskeys'][:]
            else:
                self.presskeys = [args['presskeys']]

            self.startwidth = args['width']
            self.startheight = args['height']
            self.width = Utils.relativetoval(args['width'], ui.screenw, ui.screenh, ui)
            self.height = Utils.relativetoval(args['height'], ui.screenw, ui.screenh, ui)
            self.roundedcorners = args['roundedcorners']
            self.scalesize = args['scalesize']
            if args['scalex'] == -1:
                self.scalex = self.scalesize
            else:
                self.scalex = args['scalex']
            if args['scaley'] == -1:
                self.scaley = self.scalesize
            else:
                self.scaley = args['scaley']
            self.scaleby = args['scaleby']
            self.glow = args['glow']
            self.refreshscale()
            self.border = args['border']
            if args['upperborder'] == -1:
                self.upperborder = self.border
            else:
                self.upperborder = args['upperborder']
            if args['lowerborder'] == -1:
                self.lowerborder = self.border
            else:
                self.lowerborder = args['lowerborder']
            if args['leftborder'] == -1:
                self.leftborder = self.border
            else:
                self.leftborder = args['leftborder']
            if args['rightborder'] == -1:
                self.rightborder = self.border
            else:
                self.rightborder = args['rightborder']

            self.menu = args['menu']
            self.truemenu = self.menu
            if type(self.truemenu) == str: self.truemenu = [self.truemenu]
            self.behindmenu = args['behindmenu']
            if args['killtime'] == -1:
                self.killtime = -1
            else:
                self.killtime = time.time() + args['killtime']
            self.layer = args['layer']
            if args['ID'] == '': args['ID'] = args['text']

            self.text = str(args['text'])
            self.textsize = args['textsize']
            self.img = args['img']
            self.font = args['font']
            self.bold = args['bold']
            self.antialiasing = args['antialiasing']
            self.pregenerated = args['pregenerated']
            self.textcenter = args['textcenter']
            self.startmaxwidth = args['maxwidth']
            self.maxwidth = args['maxwidth']
            self.textimages = []
            self.toggletextimages = []

            self.col = args['col']
            self.textcol = args['textcol']
            self.backingcol = ColEdit.autoshiftcol(args['backingcol'], self.col, 20)
            self.bordercol = self.backingcol
            self.glowcol = ColEdit.autoshiftcol(args['glowcol'], self.col, -20)
            self.hovercol = ColEdit.autoshiftcol(args['hovercol'], self.col, -20)
            self.togglecol = ColEdit.autoshiftcol(args['togglecol'], self.col, -50)
            self.togglehovercol = ColEdit.autoshiftcol(args['togglehovercol'], self.togglecol, -20)
            self.selectcol = ColEdit.autoshiftcol(args['selectcol'], self.col, 20)
            self.scrollercol = ColEdit.autoshiftcol(args['scrollercol'], self.col, -30)
            self.slidercol = ColEdit.autoshiftcol(args['slidercol'], self.col, -30)
            self.sliderbordercol = ColEdit.autoshiftcol(args['sliderbordercol'], self.col, -10)
            self.colorkey = args['colorkey']

            self.clickdownsize = args['clickdownsize']
            self.textoffsetx = args['textoffsetx']
            self.textoffsety = args['textoffsety']
            self.dragable = args['dragable']
            self.spacing = args['spacing']
            self.verticalspacing = args['verticalspacing']
            self.horizontalspacing = args['horizontalspacing']
            if args['spacing'] != -1:
                self.verticalspacing = self.spacing
                self.horizontalspacing = self.spacing

            self.toggle = args['toggle']
            self.toggleable = args['toggleable']
            if args['toggletext'] == -1:
                self.toggletext = args['text']
            else:
                self.toggletext = args['toggletext']
            if args['toggleimg'] == -1:
                self.toggleimg = args['img']
            else:
                self.toggleimg = args['toggleimg']
            self.bindtoggle = args['bindtoggle']

            self.clicktype = args['clicktype']
            self.startclickablerect = args['clickablerect']
            self.clickablerect = args['clickablerect']
            self.noclickrect = []
            self.noclickrectsapplied = []
            self.clickableborder = args['clickableborder']
            self.clickedon = -1
            self.holding = False
            self.forceholding = False
            self.hovering = False
            self.animating = False
            self.animationspeed = args['animationspeed']
            self.animate = 0
            self.currentframe = 0
            self.command = args['command']
            self.runcommandat = args['runcommandat']

            self.lines = args['lines']
            self.linelimit = args['linelimit']
            self.attachscroller = args['attachscroller']
            if self.linelimit == -1:
                if self.attachscroller:
                    self.linelimit = 100
                else:
                    self.linelimit = self.lines
            self.intscroller = args['intscroller']
            self.intwraparound = args['intwraparound']
            self.selectbordersize = args['selectbordersize']
            self.selectshrinksize = args['selectshrinksize']
            self.cursorsize = args['cursorsize']
            self.chrlimit = args['chrlimit']
            self.numsonly = args['numsonly']
            self.allowedcharacters = args['allowedcharacters']
            self.enterreturns = args['enterreturns']
            self.commandifenter = args['commandifenter']
            self.commandifkey = args['commandifkey']
            self.imgdisplay = args['imgdisplay']

            self.tableobject = False
            self.data = args['data']
            self.titles = args['titles']
            self.splitcellchar = args['splitcellchar']
            self.table = 0
            self.linesize = args['linesize']
            self.boxwidth = args['boxwidth']
            self.boxheight = args['boxheight']
            self.guessheight = args['guessheight']
            self.guesswidth = args['guesswidth']
            self.scroller = args['scroller']
            self.compress = args['compress']

            self.animationtype = args['animationtype']
            self.options = args['options']
            self.dropsdown = args['dropsdown']
            if len(self.options) > 0: self.active = self.options[args['startoptionindex']]

            self.backingdraw = args['backingdraw']
            self.borderdraw = args['borderdraw']
            self.startpageheight = args['pageheight']
            self.pageheight = Utils.relativetoval(args['pageheight'], ui.screenw, ui.screenh, ui)

            self.startminp = args['minp']
            self.minp = Utils.relativetoval(args['minp'], ui.screenw, ui.screenh, ui)
            self.startmaxp = args['maxp']
            self.maxp = Utils.relativetoval(args['maxp'], ui.screenw, ui.screenh, ui)
            self.startp = args['startp']
            self.increment = args['increment']
            self.containedslider = args['containedslider']
            if args['slidersize'] == -1:
                self.slidersize = self.height * 2
                if self.containedslider: self.slidersize = self.height - self.upperborder - self.lowerborder
                if args['direction'] == 'vertical':
                    self.slidersize = self.width * 2
                    if self.containedslider: self.slidersize = self.width - self.leftborder - self.rightborder
            else:
                self.slidersize = args['slidersize']
            if args['sliderroundedcorners'] == -1:
                self.sliderroundedcorners = args['roundedcorners']
            else:
                self.sliderroundedcorners = args['sliderroundedcorners']
            self.direction = args['direction']
            self.containedslider = args['containedslider']
            self.movetoclick = args['movetoclick']
            self.scrollbind = args['scrollbind']
            self.screencompressed = args['screencompressed']

            self.onitem = False
            self.master = [Utils.EmptyObject(0, 0, ui.screenw, ui.screenh)]
            self.bounditems = args['bounditems'][:]
            ui.addid(args['ID'], self)
            for a in self.bounditems:
                self.binditem(a)
            self.empty = False

            self.isolated = args['isolated']
            self.darken = args['darken']
            self.autoshutwindows = args['autoshutwindows']
            for a in self.bounditems:
                self.binditem(a)
            self.reset()
            pygame.event.pump()

    def getDataClass(self):
        '''
        Returns the dataclass which is used for the object
        '''
        raise NotImplementedError("Please Implement this method")

    def splitDataClasses(self):
        print(self.getDataClass().__bases__[0] == object)

    def creationLogic(self):
        pass

    def __str__(self):
        return '<' + str(type(self)).split("'")[1] + f' ID:{self.ID}>'

    def __repr__(self):
        return '<' + str(type(self)).split("'")[1] + f' ID:{self.ID}>'

    def reset(self):
        self.autoscale()
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.refreshcords()
        self.resetcords()
        self.refresh()

    def refresh(self):
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.resetcords()
        self.refreshglow()
        self.refreshbound()
        self.refreshclickablerect()

    def gentext(self):
        ui = self.ui
        self.currentframe = 0
        if type(self.img) != list:
            imgs = [self.img]
        else:
            imgs = self.img
            if len(imgs) < 1: imgs.append('')

        self.textimages = []
        for img in imgs:
            if type(img) == str:
                if len(imgs) != 1:
                    txt = img
                else:
                    txt = self.text
                self.textimages.append(
                    ui.rendertextlined(txt, self.textsize, self.textcol, self.col, self.font, self.maxwidth, self.bold,
                                       self.antialiasing, self.textcenter, imgin=True, img=img, scale=self.scale,
                                       linelimit=self.linelimit, cutstartspaces=True))
            else:
                self.textimages.append(pygame.transform.scale(img, (
                img.get_width() * (self.textsize / img.get_height()) * self.scale,
                img.get_height() * (self.textsize / img.get_height()) * self.scale)))
            if self.colorkey != -1: self.textimages[-1].set_colorkey(self.colorkey)
        self.textimage = self.textimages[0]
        if len(self.textimages) != 1:
            self.animating = True
        self.child_gentext()

    def refreshglow(self):
        if self.glow != 0:
            self.glowimage = pygame.Surface(
                ((self.glow * 2 + self.width) * self.scale, (self.glow * 2 + self.height) * self.scale),
                pygame.SRCALPHA)
            Draw.glow(self.glowimage, Utils.roundrect(self.glow * self.scale, self.glow * self.scale, self.width * self.scale,
                                                self.height * self.scale), int(self.glow * self.scale), self.glowcol)

    def refreshbound(self):
        for a in self.refreshbind:
            if a in self.ui.IDs:
                self.ui.IDs[a].refresh()

    def animatetext(self):
        if self.animating:
            self.animate += 1
            if self.animate % self.animationspeed == 0:
                self.currentframe += 1
                if self.currentframe == len(self.textimages):
                    self.currentframe = 0
                self.textimage = self.textimages[self.currentframe]

    def resetcords(self, scalereset=True):
        ui = self.ui
        if scalereset: self.refreshscale()
        self.anchor = self.startanchor[:]

        master = self.master[0]
        if len(self.master) > 1:
            if 'animate' in self.truemenu:
                for a in self.master:
                    if ui.activemenu in a.truemenu:
                        master = a
            else:
                for a in self.master:
                    if not (ui.activemenu in a.truemenu):
                        master = a
                        break

        w = self.getmasterwidth()
        h = self.getmasterheight()

        self.anchor[0] = Utils.relativetoval(self.anchor[0], w, h, ui)
        self.anchor[1] = Utils.relativetoval(self.anchor[1], w, h, ui)

        self.objanchor = self.startobjanchor[:]
        self.objanchor[0] = Utils.relativetoval(self.objanchor[0], self.width, self.height, ui)
        self.objanchor[1] = Utils.relativetoval(self.objanchor[1], self.width, self.height, ui)

        self.x = int(master.x * master.dirscale[0] + self.anchor[0] + (
                    self.startx - self.objanchor[0] - self.scrollcords[0]) * self.scale) / self.dirscale[0]
        self.y = int(master.y * master.dirscale[1] + self.anchor[1] + (
                    self.starty - self.objanchor[1] - self.scrollcords[1]) * self.scale) / self.dirscale[1]

        self.refreshcords()
        for a in self.bounditems:
            a.resetcords()
        self.refreshclickablerect()

    def refreshcords(self):
        self.refreshscale()
        self.child_refreshcords()

    def refreshscale(self):
        if self.scaleby == -1:
            self.scale = self.ui.scale
        elif self.scaleby == 'vertical':
            self.scale = self.ui.dirscale[1]
        else:
            self.scale = self.ui.dirscale[0]

        self.dirscale = self.ui.dirscale[:]
        if not self.scalesize: self.scale = 1
        if not self.scalex: self.dirscale[0] = 1
        if not self.scaley: self.dirscale[1] = 1

    def autoscale(self):
        w = self.getmasterwidth() / self.scale
        h = self.getmasterheight() / self.scale
        if self.startwidth != -1: self.width = Utils.relativetoval(self.startwidth, w, h, self.ui)
        if self.startmaxwidth != -1: self.maxwidth = Utils.relativetoval(self.startmaxwidth, w, h, self.ui)
        if self.startheight != -1: self.height = Utils.relativetoval(self.startheight, w, h, self.ui)
        self.refreshclickablerect()
        self.child_autoscale()

    def refreshclickablerect(self):
        w = self.getmasterwidth() / self.scale
        h = self.getmasterheight() / self.scale
        if self.startclickablerect != -1:
            rx, ry, rw, rh = self.startclickablerect
            xstart = self.master[0].x * self.master[0].dirscale[0]
            ystart = self.master[0].y * self.master[0].dirscale[1]
            ow = self.getmasterwidth() / self.scale
            oh = self.getmasterheight() / self.scale
            if type(self) == ScrollerTable:
                self.pageheight = Utils.relativetoval(self.startpageheight, w, h, self.ui)
                oh = self.pageheight
            if type(self) in [ScrollerTable, Table]:
                xstart = self.x * self.dirscale[0]
                ystart = self.y * self.dirscale[1]
                ow = self.width
                oh = self.height
            self.clickablerect = pygame.Rect(xstart + Utils.relativetoval(rx, w, h, self.ui),
                                             ystart + Utils.relativetoval(ry, w, h, self.ui),
                                             Utils.relativetoval(rw, ow, oh, self.ui) * self.scale,
                                             Utils.relativetoval(rh, ow, oh, self.ui) * self.scale)
        else:
            self.clickablerect = self.startclickablerect

    def render(self, screen):
        if self.killtime != -1 and self.killtime < self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            self.child_render(screen)
            for a in [i.ID for i in self.bounditems][:]:
                if a in self.ui.IDs:
                    self.ui.IDs[a].render(screen)

    def smartcords(self, x=None, y=None, startset=True, accountscroll=False):
        scr = [0, 0]
        if accountscroll:
            scr = self.scrollcords[:]

        if x is not None:
            self.x = x
            if startset: self.startx = ((self.x + scr[0]) * self.dirscale[0] + self.objanchor[0] * self.scale -
                                        self.anchor[0]) / self.scale - self.master[0].x
        if y is not None:
            self.y = y
            if startset: self.starty = ((self.y + scr[1]) * self.dirscale[1] + self.objanchor[1] * self.scale -
                                        self.anchor[1]) / self.scale - self.master[0].y

    def binditem(self, item, replace=True, resetcords=True):
        if item != self:
            for a in item.master:
                if type(a) == Utils.EmptyObject:
                    item.master.remove(a)
            if item.onitem and replace:
                for a in item.master:
                    if type(a) != Utils.EmptyObject:
                        if item in a.bounditems:
                            a.bounditems.remove(item)
            if not (item in self.bounditems):
                self.bounditems.append(item)
            item.onitem = True
            if replace:
                item.master = [self]
            else:
                item.master.append(self)
            self.bounditems.sort(key=lambda x: x.layer, reverse=False)
            if resetcords: item.resetcords()

    def setmenu(self, menu):
        self.menu = menu
        self.truemenu = self.menu
        if type(self.truemenu) == str: self.truemenu = [self.truemenu]

        for a in self.master:
            if type(a) in [WindowedMenu, Menu]:
                a.bounditems.remove(self)
        self.master = []
        for a in self.truemenu:
            if a in self.ui.windowedmenunames:
                self.ui.windowedmenus[self.ui.windowedmenunames.index(a)].binditem(self, False, False)
        self.ui.refreshitems()
        self.resetcords()

    def getmenu(self):
        if type(self.master[0]) in [WindowedMenu, Menu]:
            return self.master[0].menu
        else:
            return self.master[0].getmenu()

    def getmasterwidth(self):
        w = self.ui.screenw
        if self.onitem:
            w = self.master[0].width * self.master[0].scale
        return w

    def getmasterheight(self):
        h = self.ui.screenh
        if self.onitem:
            h = self.master[0].height * self.master[0].scale
        return h

    def getchildIDs(self):
        lis = [self.ID]
        lis += sum([a.getchildIDs() for a in self.bounditems], [])
        return lis

    def getenabled(self):
        if not self.enabled:
            return False
        else:
            return self.master[0].getenabled()

    def settext(self, text):
        self.text = str(text)
        self.refresh()

    def settextsize(self, textsize):
        self.textsize = textsize
        self.refresh()

    def setwidth(self, width):
        self.startwidth = width
        self.autoscale()

    def setheight(self, height):
        self.startheight = height
        self.autoscale()

    def settextcol(self, col):
        self.textcol = col
        self.refresh()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def enabledtoggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def getwidth(self):
        return self.width

    def getheight(self):
        return self.height

    def child_gentext(self):
        pass

    def child_refreshcords(self):
        pass

    def child_autoscale(self):
        pass

    def refreshnoclickrect(self):
        pass

    def press(self):
        for a in self.bindtoggle:
            if a != self.ID:
                self.ui.IDs[a].toggle = False
        if self.toggleable:
            self.toggle = not self.toggle
        self.command()

    ##        prevmenu = self.ui.activemenu
    ##        if prevmenu!=self.ui.activemenu:
    ##            temp = self.ui.mprs,self.ui.mpos
    ##            self.ui.mprs = [0,0,0]
    ##            self.ui.mpos = [-100000,-100000]
    ##            self.render(pygame.Surface((10,10)))
    ##            self.ui.mprs,self.ui.mpos = temp

    def getclickedon(self, rect='default', runcom=True, drag=True, smartdrag=True):
        ui = self.ui
        if rect == 'default':
            rect = pygame.Rect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                               self.height * self.scale)
        self.clickedon = -1
        self.hovering = False
        mpos = ui.mpos
        if self.forceholding:
            if not self.holding:
                self.clickedon = 0
            else:
                self.clickedon = 1
            self.holding = True
            return False
        if rect.collidepoint(mpos) and (self.clickablerect == -1 or self.clickablerect.collidepoint(mpos)) and not (
        Collision.collidepointrects(mpos, self.noclickrectsapplied)):
            if ui.mprs[self.clicktype] and (ui.mouseheld[self.clicktype][1] > 0 or self.holding):
                if ui.mouseheld[self.clicktype][1] == ui.buttondowntimer:
                    self.clickedon = 0
                    self.holding = True
                    self.holdingcords = [(mpos[0]) - rect.x, (mpos[1]) - rect.y]
                    if self.runcommandat < 2 and runcom:
                        self.press()
            else:
                self.hovering = True
        if ui.mprs[self.clicktype] and self.holding:
            if self.clickedon != 0:
                self.clickedon = 1
            if self.dragable and drag:
                if type(self) == Scroller:
                    account = [0, -self.border]
                else:
                    account = [-rect.x + self.x * self.dirscale[0], -rect.y + self.y * self.dirscale[1]]
                if smartdrag:
                    self.smartcords((mpos[0] - self.holdingcords[0] + account[0]) / self.dirscale[0],
                                    (mpos[1] - self.holdingcords[1] + account[1]) / self.dirscale[1])
                else:
                    self.x = (mpos[0] - self.holdingcords[0] + account[0]) / self.dirscale[0]
                    self.y = (mpos[1] - self.holdingcords[1] + account[1]) / self.dirscale[1]
                self.centerx = self.x + self.width / 2
                self.centery = self.y + self.height / 2
                for a in self.bounditems:
                    a.resetcords(ui)
            if self.runcommandat == 1 and runcom:
                self.command()
        elif not ui.mprs[self.clicktype]:
            if self.holding:
                self.clickedon = 2
                if rect.collidepoint(mpos) and self.runcommandat > 0 and runcom:
                    self.press()
            self.holding = False
        return False