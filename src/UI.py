import pygame
import time
import math
import ctypes
import threading

from src.Utils.Utils import Utils
from src.Utils.Draw import Draw
from src.Utils.ColEdit import ColEdit
from src.Utils.Collision import Collision

from src.GuiItems.Button import Button
from src.GuiItems.DropDown import DropDown
from src.GuiItems.Table import Table
from src.GuiItems.Textbox import Textbox
from src.GuiItems.Text import Text
from src.GuiItems.Scroller import Scroller
from src.GuiItems.Slider import Slider
from src.GuiItems.Menu import Menu
from src.GuiItems.Window import Window
from src.GuiItems.Rectangle import Rectangle
from src.GuiItems.WindowedMenu import WindowedMenu
from src.GuiItems.ScrollerTable import ScrollerTable
from src.Style import Style
from src.Animation import Animation


class UI:
    def __init__(self, scale=1, PyUItitle=True):
        pygame.key.set_repeat(350, 31)
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)

        self.scale = scale
        self.dirscale = [1, 1]
        self.mouseheld = [[0, 0], [0, 0], [0, 0]]

        self.buttons = []
        self.tables = []
        self.textboxes = []
        self.texts = []
        self.scrollers = []
        self.sliders = []
        self.animations = []
        self.rects = []
        self.dropdowns = []
        self.windows = []
        self.noclickrects = []
        self.selectedtextbox = -1
        self.IDs = {}
        self.items = []
        self.buttonkeys = {}
        self.holdingtracker = []

        self.images = []
        self.getscreen()
        self.inbuiltimages = {}

        self.activemenu = 'main'
        self.framemenu = 'main'
        self.windowedmenus = []
        self.automenus = []
        self.windowedmenunames = []
        self.backchain = []
        self.queuedmenumove = [0, []]
        self.prevmenumove = []
        self.buttondowntimer = 9

        self.fullscreen = False
        self.exit = False
        self.blockf11 = 0

        self.clipboard = pygame.scrap.get('str')

        self.timetracker = time.perf_counter()

        self.scrolllimit = 100
        self.escapeback = True
        self.backquits = True
        self.scrollwheelscrolls = True
        self.idmessages = False
        self.queuemenumove = True
        self.roundedbezier = True
        self.rendershapefunctions = {'tick': self.rendershapetick, 'cross': self.rendershapecross,
                                     'arrow': self.rendershapearrow, 'settings': self.rendershapesettings,
                                     'play': self.rendershapeplay, 'pause': self.rendershapepause,
                                     'skip': self.rendershapeskip, 'circle': self.rendershapecircle,
                                     'rect': self.rendershaperect, 'clock': self.rendershapeclock,
                                     'loading': self.rendershapeloading, 'dots': self.rendershapedots,
                                     'logo': self.rendershapelogo}
        self.renderedshapes = {}

        self.resizable = True
        self.fullscreenable = True
        self.autoscale = 'width'
        tempscreen = pygame.display.get_surface()
        self.basescreensize = [tempscreen.get_width(), tempscreen.get_height()]
        self.checkcaps()
        if self.scale != 1: self.setscale(self.scale)
        self.styleload_default()

        self.PyUItitle = PyUItitle
        if PyUItitle:
            self.logo = self.rendershapelogo('logo', 50, (0, 0, 0), (255, 255, 255), False)
            self.logo.set_colorkey((255, 255, 255))
            pygame.display.set_icon(self.logo)
            pygame.display.set_caption('PyUI Application')
        self.loadtickdata()

    def checkcaps(self):
        try:
            hllDll = ctypes.WinDLL("User32.dll")
            self.capslock = bool(hllDll.GetKeyState(0x14))
        except:
            self.capslock = False

    def styleset(self, **args):
        marked = {}
        for a in args:
            if (a in Style.defaults):
                Style.defaults[a] = args[a]
                for b in Style.objectdefaults:
                    Style.objectdefaults[b][a] = args[a]
            elif a == 'wallpapercol':
                exec(f'Style.{a} = {args[a]}')
            else:
                marked[a] = args[a]

        for a in marked:
            if a.split('_')[0] in UI.objectkey:
                Style.objectdefaults[UI.objectkey[a.split('_')[0]]][a.split('_', 1)[1]] = args[a]

    def styleget(self, var):
        split = var.split('_')
        if split[0] in UI.objectkey:
            return Style.objectdefaults[UI.objectkey[split[0]]][split[1]]
        else:
            return Style.defaults[split[0]]

    def styleload_soundium(self):
        self.styleset(col=(16, 163, 127), textcol=(255, 255, 255), wallpapercol=(62, 63, 75), textsize=24,
                      roundedcorners=5, spacing=5, clickdownsize=2, scalesize=False)

    def styleload_default(self):
        self.styleset(roundedcorners=0, center=False, textsize=50, font='calibri', bold=False, antialiasing=True,
                      border=3, scalesize=True, glow=0, col=(150, 150, 150),
                      clickdownsize=4, clicktype=0, textoffsetx=0, textoffsety=0, clickableborder=0, lines=1,
                      textcenter=False, linesize=2, backingdraw=True, borderdraw=True,
                      animationspeed=30, containedslider=False, movetoclick=True, isolated=True, darken=60,
                      window_darken=0, textcol=(0, 0, 0), verticalspacing=2, horizontalspacing=8,
                      text_animationspeed=5, text_backingdraw=False, text_borderdraw=False, text_verticalspacing=3,
                      text_horizontalspacing=3, dropdown_animationspeed=15,
                      textbox_verticalspacing=2, textbox_horizontalspacing=6, table_textcenter=True,
                      button_textcenter=True, guesswidth=100, guessheight=100)

    def styleload_black(self):
        self.styleset(textcol=(0, 0, 0), backingcol=(0, 0, 0), hovercol=(255, 255, 255), bordercol=(0, 0, 0),
                      verticalspacing=3, textsize=30, col=(255, 255, 255), clickdownsize=1)

    def styleload_blue(self):
        self.styleset(col=(35, 0, 156), textcol=(230, 246, 219), wallpapercol=(0, 39, 254), textsize=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, roundedcorners=4)

    def styleload_green(self):
        self.styleset(col=(87, 112, 86), textcol=(240, 239, 174), wallpapercol=(59, 80, 61), textsize=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, roundedcorners=4)

    def styleload_lightblue(self):
        self.styleset(col=(82, 121, 214), textcol=(56, 1, 103), wallpapercol=(228, 242, 253), textsize=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, roundedcorners=4)

    def styleload_teal(self):
        self.styleset(col=(109, 123, 152), textcol=(176, 243, 174), wallpapercol=(69, 65, 88), textsize=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, roundedcorners=4)

    def styleload_brown(self):
        self.styleset(col=(39, 75, 91), textcol=(235, 217, 115), wallpapercol=(40, 41, 35), textsize=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, roundedcorners=4)

    def styleload_red(self):
        self.styleset(col=(152, 18, 20), textcol=(234, 230, 133), wallpapercol=(171, 19, 18), spacing=3,
                      clickdownsize=2, textsize=40, horizontalspacing=8, roundedcorners=5)

    def __scaleset__(self, scale):
        self.scale = scale
        self.dirscale = [self.screenw / self.basescreensize[0], self.screenh / self.basescreensize[1]]
        ##        for a in self.automenus+self.windowedmenus:
        ##            a.refresh()
        ##            a.resetcords()
        self.refreshall()
        for a in self.items:
            checker = (a.width, a.height)
            a.autoscale()
            if type(a) in [Table, ScrollerTable]:
                a.small_refresh()
            if (a.width, a.height) != checker or a.scalesize:
                a.refresh()
            if a.clickablerect != -1:
                a.refreshclickablerect()

    def setscale(self, scale):
        pygame.event.post(
            pygame.event.Event(pygame.VIDEORESIZE, w=self.basescreensize[0] * scale, h=self.basescreensize[1] * scale))

    def quit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def refreshall(self):
        for a in self.automenus + self.windowedmenus:
            self.refreshbound(a)

    def refreshbound(self, obj):
        pre = obj.enabled
        obj.enabled = False
        obj.refresh()
        obj.resetcords()
        obj.enabled = pre
        for b in obj.bounditems:
            self.refreshbound(b)

    def getscreen(self):
        sc = pygame.display.get_surface()
        self.screenw = sc.get_width()
        self.screenh = sc.get_height()

    def rendergui(self, screen):
        windowedmenubackings = [a.behindmenu for a in self.windowedmenus]
        self.breakrenderloop = False
        self.animate()
        self.framemenu = self.activemenu
        for i, a in enumerate(self.automenus):
            if self.framemenu in a.truemenu:
                a.render(screen)
        for a in self.windowedmenus:
            if self.framemenu in a.truemenu:
                if pygame.Rect(a.x * a.dirscale[0], a.y * a.dirscale[1], a.width * a.scale,
                               a.height * a.scale).collidepoint(self.mpos):
                    self.drawmenu(a.behindmenu, screen)
                else:
                    if a.isolated:
                        self.drawmenu(a.behindmenu, screen)
                        if self.mprs[0] and self.mouseheld[0][1] == self.buttondowntimer:
                            self.menuback()
                    else:
                        self.rendermenu(a.behindmenu, screen)
                a.render(screen)

    def rendermenu(self, menu, screen):
        if f'auto_generate_menu:{menu}' in self.IDs:
            self.IDs[f'auto_generate_menu:{menu}'].render(screen)

    def drawmenu(self, menu, screen):
        if f'auto_generate_menu:{menu}' in self.IDs:
            self.IDs[f'auto_generate_menu:{menu}'].drawallmenu(screen)

    def loadtickdata(self):
        t = time.perf_counter()
        self.deltatime = 60 * (t - self.timetracker)
        self.timetracker = t
        self.blockf11 -= 1
        self.mpos = list(pygame.mouse.get_pos())
        self.mprs = pygame.mouse.get_pressed()
        self.kprs = pygame.key.get_pressed()
        self.time = time.time()
        for a in range(3):
            if self.mprs[a] and not self.mouseheld[a][0]:
                self.mouseheld[a] = [1, self.buttondowntimer]
            elif self.mprs[a]:
                self.mouseheld[a][1] -= 1
            if not self.mprs[a]: self.mouseheld[a][0] = 0

        clearout = []
        for a in self.holdingtracker:
            if not self.kprs[a[0]]:
                clearout.append(a[:])
        for b in clearout:
            self.holdingtracker.remove(b)
            b[1].forceholding = False

        events = pygame.event.get()
        repeatchecker = []
        for event in events:
            if not (event in repeatchecker):
                repeatchecker.append(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_CAPSLOCK:
                        if self.capslock:
                            self.capslock = False
                        else:
                            self.capslock = True
                    elif event.key == pygame.K_ESCAPE and self.escapeback:
                        self.menuback()
                    elif event.key == pygame.K_F5:
                        thread = threading.Thread(target=self.refreshall)
                        thread.start()
                    elif event.key == pygame.K_F11 and self.fullscreenable and self.blockf11 < 0:
                        self.togglefullscreen(pygame.display.get_surface())
                    if event.key in self.buttonkeys:
                        for i in self.buttonkeys[event.key]:
                            if self.activemenu in i.menu:
                                i.press()
                                i.forceholding = True
                                self.holdingtracker.append([event.key, i])
                    if self.selectedtextbox != -1:
                        if not self.textboxes[self.selectedtextbox].selected:
                            self.selectedtextbox = -1
                        else:
                            self.textboxes[self.selectedtextbox].inputkey(self.capslock, event, self.kprs)
                elif event.type == pygame.VIDEORESIZE:
                    self.screenw = event.w
                    self.screenh = event.h
                    self.resetscreen(pygame.display.get_surface())
                elif event.type == pygame.MOUSEWHEEL:
                    moved = False
                    for a in self.textboxes:
                        if a.selected and self.activemenu == a.getmenu():
                            if a.scroll_input(event.y):
                                moved = True
                    if not moved:
                        scrollable = []
                        for a in self.scrollers:
                            if self.activemenu == a.getmenu() and type(a.master[0]) != Textbox:
                                if a.pageheight < (a.maxp - a.minp) and a.getenabled():
                                    scrollable.append(a)
                        for x in scrollable:
                            x.tempdistancetomouse = Collision.distancetorect(
                                [self.mpos[0] / x.dirscale[0], self.mpos[1] / x.dirscale[1]],
                                (x.x, x.y, x.width, x.height))
                            if type(x.master[0]) == ScrollerTable:
                                x.tempdistancetomouse = Collision.distancetorect(
                                    [self.mpos[0] / x.dirscale[0], self.mpos[1] / x.dirscale[1]],
                                    (x.master[0].x, x.master[0].y, x.master[0].width, x.master[0].height))
                        scrollable.sort(key=lambda x: x.tempdistancetomouse)
                        for a in scrollable:
                            a.scroll -= (event.y * min((a.maxp - a.minp) / 20, self.scrolllimit))
                            a.limitpos()
                            a.command()
                            break

        return repeatchecker

    def togglefullscreen(self, screen):
        if self.fullscreen:
            self.fullscreen = False
        else:
            self.fullscreen = True
        self.resetscreen(screen)

    def resetscreen(self, screen):
        if self.autoscale == 'width':
            self.__scaleset__(self.screenw / self.basescreensize[0])
        else:
            self.__scaleset__(self.screenh / self.basescreensize[1])
        if self.fullscreen:
            screen = pygame.display.set_mode((self.screenw, self.screenh), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((self.screenw, self.screenh), pygame.RESIZABLE)
        if self.PyUItitle:
            pygame.display.set_icon(self.logo)
        self.blockf11 = 10

    def write(self, screen, x, y, text, size, col=-1, center=True, font=-1, bold=False, antialiasing=True, scale=False,
              centery=-1):
        if font == -1: font = Style.defaults['font']
        if col == -1: col = Style.defaults['textcol']
        if size == -1: size = Style.defaults['textsize']
        if centery == -1: centery = center
        if scale:
            dirscale = self.dirscale
            scale = self.scale
        else:
            dirscale = [1, 1]
            scale = 1
        largetext = pygame.font.SysFont(font, int(size * scale), bold)
        textsurf = largetext.render(text, antialiasing, col)
        textrect = textsurf.get_rect()
        if center:
            textrect.center = (int(x) * dirscale[0], int(y) * dirscale[1])
            if not centery: textrect.y = y * dirscale[1]
        else:
            textrect.y = int(y) * dirscale[1]
            if centery: textrect.center = (int(x) * dirscale[0], int(y) * dirscale[1])
            textrect.x = int(x) * dirscale[0]
        screen.blit(textsurf, textrect)

    def rendertext(self, text, size, col=-1, font=-1, bold=False, antialiasing=True, backingcol=(150, 150, 150),
                   imgin=False, img=''):
        if font == -1: font = Style.defaults['font']
        if col == -1: col = Style.defaults['textcol']
        if size == -1: size = Style.defaults['textsize']
        if imgin:
            texts, imagenames = self.seperatestring(text)
        else:
            texts = [text]
            imagenames = ['']
        images = []
        textgen = pygame.font.SysFont(font, int(size), bold)
        for a in range(len(texts)):
            if texts[a] != '': images.append(textgen.render(texts[a], antialiasing, col))
            if imagenames[a] != '': images.append(self.rendershape(imagenames[a], size, col, False, backcol=backingcol))
        if len(images) == 0:
            return pygame.Surface((0, textgen.size('\n')[1]))
        else:
            textsurf = pygame.Surface((sum([a.get_width() for a in images]), max([a.get_height() for a in images])))

        textsurf.fill(backingcol)
        xpos = 0
        h = textsurf.get_height()
        for a in images:
            textsurf.blit(a, (xpos, (h - a.get_height()) / 2))
            xpos += a.get_width()
        textsurf.set_colorkey(backingcol)
        return textsurf

    def seperatestring(self, text):
        texts = ['']
        imagenames = ['']
        openn = 0
        for a in text:
            if a == '{':
                if openn == 0:
                    texts.append('')
                openn += 1
            if openn > 0:
                imagenames[-1] += a
            else:
                texts[-1] += a

            if a == '}':
                if openn == 1:
                    imagenames.append('')
                openn -= 1
                if openn < 0: openn = 0
        if len([i for i in imagenames[-1] if i == '{']) != len([i for i in imagenames[-1] if i == '}']):
            texts[-2] += imagenames.pop(-1)
            imagenames.append('')
            del texts[-1]
        for i, a in enumerate(imagenames):
            imagenames[i] = a.removeprefix('{').removesuffix('}')
        return texts, imagenames

    def rendershape(self, name, size, col='default', failmessage=True, backcol=(255, 255, 255)):
        name = name.strip()
        if col == 'default': col = Style.defaults['col']
        if col == backcol: backcol = (0, 0, 0)
        if 'col=' in name:
            try:
                c = name.split('col=')[1].split('(')[1].split(')')[0].split(',')
                col = (int(c[0]), int(c[1]), int(c[2]))
            except:
                pass
        if 'scale=' in name:
            size *= float(name.split('scale=')[1].split(' ')[0])

        if str([name, size, col, backcol]) in self.renderedshapes:
            return self.renderedshapes[str([name, size, col, backcol])]
        if len(name) > 0 and name[0] == '"':
            surf = self.rendershapetext(name, size, col, backcol)
        elif name.split(' ')[0] in self.rendershapefunctions:
            surf = self.rendershapefunctions[name.split(' ')[0]](name, size, col, backcol)
        else:
            surf, worked, backcol = self.rendershapebezier(name, size, col, backcol, failmessage)
            if not worked:
                surf = self.rendershapetext(name, size, col, backcol)
        keywords = name.split('"')[-1].split()
        if 'left' in keywords:
            surf = pygame.transform.flip(surf, True, False)
        elif 'up' in keywords:
            surf = pygame.transform.rotate(surf, 90)
        elif 'down' in keywords:
            surf = pygame.transform.rotate(surf, -90)
        surf.set_colorkey(backcol)
        self.renderedshapes[str([name, size, col, backcol])] = surf
        return surf

    def rendershapetick(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['thickness'], [0.2])
        basethickness = vals[0]
        tsize = size
        size = 1000
        surf = pygame.Surface((size, size))
        surf.fill(backcol)
        thickness = size * basethickness
        points = [[size * 0.12, size * 0.6], [size * 0.38, size * 0.9], [size * 0.88, size * 0.1]]
        sc = 1 - (thickness / size)
        for a in points:
            a[0] = (a[0] - size * 0.5) * sc + size * 0.5
            a[1] = (a[1] - size * 0.5) * sc + size * 0.5

        pygame.draw.lines(surf, col, False, points, int(thickness))
        thickness /= 2
        dirc = [-1, 1, -1]
        skew = [(-0.6, 0), (0, -0.4), (0.6, 0)]
        npoints = []
        detail = 100
        for i, a in enumerate(points):
            npoints.append([])
            for b in range(detail + 1):
                npoints[-1].append([a[0] + (
                            math.cos(b / detail * math.pi) + abs(math.sin(b / detail * math.pi)) * skew[i][
                        0]) * thickness, a[1] + (math.sin(b / detail * math.pi) + abs(math.sin(b / detail * math.pi)) *
                                                 skew[i][1]) * dirc[i] * thickness])
        for a in npoints[1]:
            a[1] -= size * 0.015
        for a in npoints:
            Draw.polygon(surf, col, a)
        surf = pygame.transform.scale(surf, (tsize, tsize))
        return surf

    def rendershapearrow(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['stick', 'point', 'smooth', 'width'], [0.95, 0.45, 0, 0.2])
        sticklen = vals[0]
        pointlen = vals[1]
        smooth = bool(vals[2])
        width = vals[3]
        surf = pygame.Surface((size * (sticklen + pointlen + 0.1), size * 0.7))
        surf.fill(backcol)
        if smooth:
            Draw.roundedline(surf, col, (size * (width + 0.05), size * 0.35),
                             (size * (sticklen + pointlen + 0.05 - width), size * 0.35), width * size)
            Draw.roundedline(surf, col, (size * (sticklen + 0.05), size * (0.05 + width)),
                             (size * (sticklen + pointlen + 0.05 - width), size * 0.35), width * size)
            Draw.roundedline(surf, col, (size * (sticklen + 0.05), size * (0.7 - 0.05 - width)),
                             (size * (sticklen + pointlen + 0.05 - width), size * 0.35), width * size)
        else:
            Draw.polygon(surf, col, ((size * 0.05, size * 0.25), (size * (sticklen + 0.05), size * 0.25),
                                     (size * (sticklen + 0.05), size * 0.05),
                                     (size * (sticklen + pointlen + 0.05), size * 0.35),
                                     (size * (sticklen + 0.05), size * 0.65), (size * (sticklen + 0.05), size * 0.45),
                                     (size * 0.05, size * 0.45)))
        return surf

    def rendershapecross(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['width'], [0.1])
        width = vals[0]
        surf = pygame.Surface((size + 1, size + 1))
        surf.fill(backcol)
        Draw.roundedline(surf, col, (size * width, size * width), (size * (1 - width), size * (1 - width)),
                         size * width)
        Draw.roundedline(surf, col, (size * (1 - width), size * width), (size * width, size * (1 - width)),
                         size * width)
        return surf

    def rendershapesettings(self, name, size, col, backcol, antialiasing=True):
        surf = pygame.Surface((size, size))
        surf.fill(backcol)
        vals = self.getshapedata(name, ['innercircle', 'outercircle', 'prongs', 'prongwidth', 'prongsteepness'],
                                 [0.15, 0.35, 6, 0.2, 1.1])
        innercircle = vals[0]
        outercircle = vals[1]
        prongs = int(vals[2])
        prongwidth = vals[3]
        prongsteepness = vals[4]
        if antialiasing:
            Draw.circle(surf, col, (size * 0.5, size * 0.5), size * outercircle)
        else:
            pygame.draw.circle(surf, col, (size * 0.5, size * 0.5), size * outercircle)
        width = prongwidth
        innerwidth = width + math.sin(width) * prongsteepness
        points = []
        outercircle -= 0.01
        for a in range(prongs):
            ang = (math.pi * 2) * a / prongs
            points.append(
                [((math.sin(ang - width) * 0.5 * 0.95 + 0.5) * size, (math.cos(ang - width) * 0.5 * 0.95 + 0.5) * size),
                 ((math.sin(ang + width) * 0.5 * 0.95 + 0.5) * size, (math.cos(ang + width) * 0.5 * 0.95 + 0.5) * size),
                 ((math.sin(ang + innerwidth) * 0.5 * (outercircle * 2) + 0.5) * size,
                  (math.cos(ang + innerwidth) * 0.5 * (outercircle * 2) + 0.5) * size), (
                 (math.sin(ang - innerwidth) * 0.5 * (outercircle * 2) + 0.5) * size,
                 (math.cos(ang - innerwidth) * 0.5 * (outercircle * 2) + 0.5) * size)])
        if antialiasing:
            for a in points:
                Draw.polygon(surf, col, a)
            Draw.circle(surf, backcol, (size * 0.5, size * 0.5), size * innercircle)
        else:
            for a in points:
                pygame.draw.polygon(surf, col, a)
            pygame.draw.circle(surf, backcol, (size * 0.5, size * 0.5), size * innercircle)
        return surf

    def rendershapelogo(self, name, size, col, backcol, antialiasing=True):
        surf = pygame.Surface((size, size))
        surf.fill(backcol)
        surf = self.rendershapesettings(name, size, (66, 129, 180), backcol, antialiasing)
        self.write(surf, size * 0.5, size * 0.5, 'PyUI', size * (360 / 600), (62, 63, 75), True,
                   antialiasing=antialiasing)
        self.write(surf, size * 0.5, size * 0.5, 'PyUI', size * (380 / 600), (253, 226, 93), True,
                   antialiasing=antialiasing)
        return surf

    def rendershapeplay(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['rounded'], [0.0])
        rounded = vals[0]
        points = [[size * rounded / 2, size * rounded / 2],
                  [size * rounded / 2 + size * (1 - rounded) * (3 ** 0.5) / 2, size * 0.5],
                  [size * rounded / 2, size - size * (rounded) / 2]]
        realign = ((((points[0][0] - points[-1][0]) ** 2 + (points[0][1] - points[-1][1]) ** 2) ** 0.5) * (
                    3 ** 0.5) / 3) - size / (2 * (3 ** 0.5))
        surf = pygame.Surface((size * (rounded + (1 - rounded) * (3 ** 0.5) / 2) + realign, size))
        surf.fill(backcol)
        for a in range(len(points)):
            points[a][0] += realign
        for a in range(len(points)):
            Draw.roundedline(surf, col, points[a], points[a - 1], size * rounded / 2)
        Draw.polygon(surf, col, points)
        return surf

    def rendershapepause(self, name, size, col, backcol):
        surf = pygame.Surface((size * 0.75, size))
        surf.fill(backcol)
        vals = self.getshapedata(name, ['rounded'], [0.0])
        rounded = vals[0]
        Draw.rect(surf, col, pygame.Rect(0, 0, size * 0.25, size), border_radius=int(size * rounded))
        Draw.rect(surf, col, pygame.Rect(size * 0.5, 0, size * 0.25, size), border_radius=int(size * rounded))
        return surf

    def rendershapeskip(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['rounded', 'thickness', 'offset'], [0, 0.25, -0.35])
        rounded = vals[0]
        thickness = vals[1]
        offset = vals[2]
        points = [[size * rounded / 2, size * rounded / 2], [size * rounded / 2, size - size * (rounded) / 2]]
        realign = ((((points[0][0] - points[-1][0]) ** 2 + (points[0][1] - points[-1][1]) ** 2) ** 0.5) * (
                    3 ** 0.5) / 3) - size / (2 * (3 ** 0.5))
        surf = pygame.Surface(
            (max([size * (rounded + (1 - rounded) * (3 ** 0.5) / 2), size + (offset + thickness) * size]), size))
        surf.fill(backcol)
        surf.blit(self.rendershapeplay(name, size, col, backcol), (-realign, 0))
        Draw.rect(surf, col, pygame.Rect(size + size * offset, 0, size * thickness, size),
                  border_radius=int(size * rounded))
        return surf

    def rendershapecircle(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['width'], [1])
        width = vals[0]
        surf = pygame.Surface((size * width, size))
        surf.fill(backcol)
        pygame.draw.ellipse(surf, col, pygame.Rect(0, 0, size * width, size))
        return surf

    def rendershaperect(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['rounded', 'width'], [0, size])
        rounded = vals[0]
        width = vals[1] * self.scale
        surf = pygame.Surface((width, size))
        surf.fill(backcol)
        Draw.rect(surf, col, pygame.Rect(0, 0, width, size), border_radius=int(size * rounded))
        return surf

    def rendershapeclock(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['hour', 'minute', 'minutehandwidth', 'hourhandwidth', 'circlewidth'],
                                 [0, 20, 0.05, 0.05, 0.05])
        hour = vals[0]
        minute = vals[1]
        minutehandwidth = vals[2]
        hourhandwidth = vals[3]
        circlewidth = vals[4]
        surf = pygame.Surface((size + 1, size + 1))
        surf.fill(backcol)
        Draw.circle(surf, col, (size / 2, size / 2), size / 2)
        Draw.circle(surf, backcol, (size / 2, size / 2), size / 2 - size * circlewidth)
        Draw.roundedline(surf, col, (size / 2, size / 2), (
        size / 2 + size * 0.4 * math.cos(math.pi * 2 * (minute / 60) - math.pi / 2),
        size / 2 + size * 0.4 * math.sin(math.pi * 2 * (minute / 60) - math.pi / 2)), size * minutehandwidth)
        Draw.roundedline(surf, col, (size / 2, size / 2), (
        size / 2 + size * 0.25 * math.cos(math.pi * 2 * (hour / 12) - math.pi / 2),
        size / 2 + size * 0.25 * math.sin(math.pi * 2 * (hour / 12) - math.pi / 2)), size * hourhandwidth)
        return surf

    def rendershapeloading(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['points', 'largest', 'traildrop', 'spotsize'], [12, 0, 0.015, 0.1])
        points = vals[0]
        largest = vals[1]
        traildrop = vals[2]
        spotsize = vals[3]
        surf = pygame.Surface((size + 2, size + 2))
        surf.fill(backcol)
        rad = (size / 2 - spotsize * size)
        for a in range(points):
            Draw.circle(surf, col, (size / 2 + rad * math.sin(math.pi * 2 * (a - largest) / points) + 1,
                                    size / 2 + rad * math.cos(math.pi * 2 * (a - largest) / points) + 1),
                        spotsize * size)
            spotsize -= traildrop
            if spotsize < 0:
                break
        return surf

    def rendershapedots(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['num', 'seperation', 'radius'], [3, 0.3, 0.1])
        dots = vals[0]
        seperation = vals[1]
        radius = vals[2]
        surf = pygame.Surface(((radius * 2 + seperation * (dots - 1)) * size + 2, size + 2))
        surf.fill(backcol)
        x = radius
        for a in range(dots):
            Draw.circle(surf, col, (x * size + 1, size / 2 + 1), radius * size)
            x += seperation
        return surf

    def rendershapetext(self, name, size, col, backcol):
        vals = self.getshapedata(name, ['font', 'bold', 'italic', 'strikethrough', 'underlined', 'antialias'],
                                 [Style.defaults['font'], False, False, False, False, True])
        font = vals[0]
        bold = vals[1]
        italic = vals[2]
        strikethrough = vals[3]
        underlined = vals[4]
        antialias = vals[5]
        textgen = pygame.font.SysFont(font, int(size), bold, italic)
        try:
            textgen.set_strikethrough(strikethrough)
            textgen.set_underline(underlined)
        except:
            pass
        text = name
        if len([i for i in text if i == '"']) == 2:
            text = name.split('"')[1]
        else:
            text = name.split(' ')[0]
        return textgen.render(text, antialias, col, backcol)

    def rendershapebezier(self, name, size, col, backcol, failmessage):
        data = [['test thing', [
            [[(200, 100), (490, 220), (300, 40), (850, 340)], [(850, 340), (300, 200), (450, 350), (340, 430)],
             [(340, 430), (310, 250), (200, 310), (200, 100)]],
            [[(380, 440), (540, 360), (330, 240), (850, 370)], [(850, 370), (380, 440)]]]],
                ['search', [
                    [[(300, 350), (150, 200), (350, 0), (500, 150)], [(500, 150), (560, 210), (520, 280), (485, 315)],
                     [(485, 315), (585, 415)], [(585, 415), (625, 455), (595, 485), (555, 445)],
                     [(555, 445), (455, 345)], [(455, 345), (420, 380), (350, 400), (300, 350)],
                     [(300, 350), (325, 325)], [(325, 325), (205, 205), (365, 65), (475, 175)],
                     [(475, 175), (555, 255), (395, 395), (325, 325)], [(325, 325), (300, 350)]]]],
                ['shuffle', [[[(275, 200), (450, 200), (450, 400), (600, 400)], [(600, 400), (600, 350)],
                              [(600, 350), (675, 425)], [(675, 425), (600, 500)], [(600, 500), (600, 450)],
                              [(600, 450), (425, 450), (425, 250), (275, 250)], [(275, 250), (275, 200)]],
                             [[(275, 400), (275, 450)], [(275, 450), (360, 450), (420, 390)], [(420, 390), (385, 345)],
                              [(385, 345), (350, 390), (275, 400)]],
                             [[(600, 250), (600, 300)], [(600, 300), (675, 225)], [(675, 225), (600, 150)],
                              [(600, 150), (600, 200)], [(600, 200), (500, 200), (455, 260)], [(455, 260), (490, 300)],
                              [(490, 300), (530, 255), (600, 250)]]]],
                ['pfp', [[[(340, 430), (710, 430)], [(710, 430), (650, 280), (380, 280), (340, 430)]],
                         [[(510, 280), (400, 280), (400, 50), (630, 50), (630, 280), (510, 280)]]]],
                ['smiley', [
                    [[(560, 460), (310, 460), (310, 40), (810, 40), (810, 460), (560, 460)], [(560, 460), (560, 430)],
                     [(560, 430), (380, 430), (380, 120), (740, 120), (740, 430), (560, 430)],
                     [(560, 430), (560, 460)]],
                    [[(630, 350), (560, 470), (500, 350)], [(500, 350), (560, 420), (630, 350)]],
                    [[(490, 290), (520, 340), (550, 290)], [(550, 290), (520, 280), (490, 290)]],
                    [[(570, 290), (600, 340), (630, 290)], [(630, 290), (600, 280), (570, 290)]]]],
                ['happy face', [
                    [[(560, 460), (310, 460), (310, 40), (810, 40), (810, 460), (560, 460)], [(560, 460), (560, 430)],
                     [(560, 430), (380, 430), (380, 120), (740, 120), (740, 430), (560, 430)],
                     [(560, 430), (560, 460)]],
                    [[(590, 350), (560, 470), (530, 350)], [(530, 350), (570, 360), (590, 350)]],
                    [[(490, 290), (520, 340), (550, 290)], [(550, 290), (520, 280), (490, 290)]],
                    [[(570, 290), (600, 340), (630, 290)], [(630, 290), (600, 280), (570, 290)]]]],
                ['heart', [
                    [[(549, 526), (528, 483), (444, 462), (444, 399)], [(444, 399), (444, 357), (486, 315), (549, 357)],
                     [(549, 357), (612, 315), (654, 357), (654, 399)],
                     [(654, 399), (654, 462), (570, 483), (549, 526)]]]],
                ['mute', [[[(325, 215), (325, 315)], [(325, 315), (325, 325), (335, 325)], [(335, 325), (435, 325)],
                           [(435, 325), (445, 325), (455, 335)], [(455, 335), (535, 415)],
                           [(535, 415), (565, 445), (565, 415)], [(565, 415), (565, 115)],
                           [(565, 115), (565, 85), (535, 115)], [(535, 115), (455, 195)],
                           [(455, 195), (445, 205), (435, 205)], [(435, 205), (335, 205)],
                           [(335, 205), (325, 205), (325, 215)]],
                          [[(705.0, 240.0), (735.0, 210.0), (715.0, 190.0), (685.0, 220.0)],
                           [(685.0, 220.0), (615.0, 290.0)],
                           [(615.0, 290.0), (585.0, 320.0), (605.0, 340.0), (635.0, 310.0)],
                           [(635.0, 310.0), (705.0, 240.0)]],
                          [[(615.0, 240.0), (585.0, 210.0), (605.0, 190.0), (635.0, 220.0)],
                           [(635.0, 220.0), (705.0, 290.0)],
                           [(705.0, 290.0), (735.0, 320.0), (715.0, 340.0), (685.0, 310.0)],
                           [(685.0, 310.0), (615.0, 240.0)]]]],
                ['speaker', [[[(325, 215), (325, 315)], [(325, 315), (325, 325), (335, 325)], [(335, 325), (435, 325)],
                              [(435, 325), (445, 325), (455, 335)], [(455, 335), (535, 415)],
                              [(535, 415), (565, 445), (565, 415)], [(565, 415), (565, 115)],
                              [(565, 115), (565, 85), (535, 115)], [(535, 115), (455, 195)],
                              [(455, 195), (445, 205), (435, 205)], [(435, 205), (335, 205)],
                              [(335, 205), (325, 205), (325, 215)]],
                             [[(665.0, 145.0), (655.0, 135.0), (635.0, 155.0), (645.0, 165.0)],
                              [(645.0, 165.0), (705.0, 235.0), (705.0, 285.0), (645.0, 365.0)],
                              [(645.0, 365.0), (635.0, 375.0), (655.0, 395.0), (665.0, 385.0)],
                              [(665.0, 385.0), (735.0, 305.0), (735.0, 215.0), (665.0, 145.0)]],
                             [[(605.0, 205.0), (595.0, 195.0), (615.0, 175.0), (625.0, 185.0)],
                              [(625.0, 185.0), (665.0, 225.0), (665.0, 305.0), (625.0, 345.0)],
                              [(625.0, 345.0), (615.0, 355.0), (595.0, 335.0), (605.0, 325.0)],
                              [(605.0, 325.0), (635.0, 285.0), (635.0, 245.0), (605.0, 205.0)]]]],
                ['3dots',
                 [[[(385.0, 325.0), (325.0, 325.0), (325.0, 205.0), (445.0, 205.0), (445.0, 325.0), (385.0, 325.0)]],
                  [[(505.0, 325.0), (445.0, 325.0), (445.0, 205.0), (565.0, 205.0), (565.0, 325.0), (505.0, 325.0)]],
                  [[(625.0, 325.0), (565.0, 325.0), (565.0, 205.0), (685.0, 205.0), (685.0, 325.0), (625.0, 325.0)]]]],
                ['pencil', [[[(325, 365), (345, 305)], [(345, 305), (515, 135)], [(515, 135), (555, 175)],
                             [(555, 175), (385, 345)], [(385, 345), (325, 365)], [(325, 365), (345, 345)],
                             [(345, 345), (355, 315)], [(355, 315), (515, 155)], [(515, 155), (535, 175)],
                             [(535, 175), (385, 325)], [(385, 325), (365, 305)], [(365, 305), (355, 315)],
                             [(355, 315), (375, 335)], [(375, 335), (345, 345)], [(345, 345), (325, 365)]]]],
                ['youtube', [
                    [[(295.0, 215.0), (295.0, 185.0), (305.0, 175.0), (345.0, 175.0)], [(345.0, 175.0), (445.0, 175.0)],
                     [(445.0, 175.0), (485.0, 175.0), (495.0, 185.0), (495.0, 215.0)], [(495.0, 215.0), (495.0, 255.0)],
                     [(495.0, 255.0), (495.0, 285.0), (485.0, 295.0), (445.0, 295.0)], [(445.0, 295.0), (345.0, 295.0)],
                     [(345.0, 295.0), (305.0, 295.0), (295.0, 285.0), (295.0, 255.0)], [(295.0, 255.0), (295.0, 235.0)],
                     [(295.0, 235.0), (375.0, 235.0)], [(375.0, 235.0), (375.0, 265.0)],
                     [(375.0, 265.0), (425.0, 235.0)], [(425.0, 235.0), (375.0, 205.0)],
                     [(375.0, 205.0), (375.0, 235.0)], [(375.0, 235.0), (295.0, 235.0)],
                     [(295.0, 235.0), (295.0, 215.0)]]]],
                ['queue', [
                    [[(295.0, 215.0), (295.0, 185.0), (305.0, 175.0), (345.0, 175.0)], [(345.0, 175.0), (445.0, 175.0)],
                     [(445.0, 175.0), (485.0, 175.0), (495.0, 185.0), (495.0, 215.0)], [(495.0, 215.0), (495.0, 255.0)],
                     [(495.0, 255.0), (495.0, 285.0), (485.0, 295.0), (445.0, 295.0)], [(445.0, 295.0), (345.0, 295.0)],
                     [(345.0, 295.0), (305.0, 295.0), (295.0, 285.0), (295.0, 255.0)], [(295.0, 255.0), (295.0, 235.0)],
                     [(295.0, 235.0), (375.0, 235.0)], [(375.0, 235.0), (375.0, 265.0)],
                     [(375.0, 265.0), (425.0, 235.0)], [(425.0, 235.0), (375.0, 205.0)],
                     [(375.0, 205.0), (375.0, 235.0)], [(375.0, 235.0), (295.0, 235.0)],
                     [(295.0, 235.0), (295.0, 215.0)]],
                    [[(345.0, 155.0), (475.0, 155.0)], [(475.0, 155.0), (505.0, 155.0), (515.0, 165.0), (515.0, 195.0)],
                     [(515.0, 195.0), (515.0, 245.0)], [(515.0, 245.0), (515.0, 275.0), (535.0, 275.0), (535.0, 245.0)],
                     [(535.0, 245.0), (535.0, 185.0)], [(535.0, 185.0), (535.0, 155.0), (515.0, 135.0), (485.0, 135.0)],
                     [(485.0, 135.0), (345.0, 135.0)],
                     [(345.0, 135.0), (315.0, 135.0), (315.0, 155.0), (345.0, 155.0)]],
                    [[(515.0, 115.0), (375.0, 115.0)], [(375.0, 115.0), (345.0, 115.0), (345.0, 95.0), (375.0, 95.0)],
                     [(375.0, 95.0), (525.0, 95.0)], [(525.0, 95.0), (555.0, 95.0), (575.0, 115.0), (575.0, 145.0)],
                     [(575.0, 145.0), (575.0, 215.0)], [(575.0, 215.0), (575.0, 245.0), (555.0, 245.0), (555.0, 215.0)],
                     [(555.0, 215.0), (555.0, 155.0)],
                     [(555.0, 155.0), (555.0, 135.0), (545.0, 115.0), (515.0, 115.0)]]]],
                ['star', [[[(425.0, 225.0), (705.0, 225.0)], [(705.0, 225.0), (565.0, 315.0)],
                           [(565.0, 315.0), (425.0, 225.0)]],
                          [[(565.0, 135.0), (475.0, 375.0)], [(475.0, 375.0), (565.0, 315.0)],
                           [(565.0, 315.0), (655.0, 375.0)], [(655.0, 375.0), (565.0, 135.0)]]]],
                ['on', [[[(485.0, 275.0), (445.0, 285.0), (425.0, 345.0), (425.0, 375.0)],
                         [(425.0, 375.0), (425.0, 435.0), (465.0, 485.0), (535.0, 485.0)],
                         [(535.0, 485.0), (605.0, 485.0), (645.0, 435.0), (645.0, 375.0)],
                         [(645.0, 375.0), (645.0, 345.0), (625.0, 285.0), (585.0, 275.0)],
                         [(585.0, 275.0), (565.0, 275.0), (575.0, 295.0)],
                         [(575.0, 295.0), (645.0, 375.0), (645.0, 505.0), (425.0, 505.0), (425.0, 375.0),
                          (495.0, 295.0)], [(495.0, 295.0), (505.0, 275.0), (485.0, 275.0)]],
                        [[(520.0, 315.0), (520.0, 355.0), (550.0, 355.0), (550.0, 315.0)],
                         [(550.0, 315.0), (550.0, 265.0)],
                         [(550.0, 265.0), (550.0, 225.0), (520.0, 225.0), (520.0, 265.0)],
                         [(520.0, 265.0), (520.0, 315.0)]]]],
                ['lock', [[[(285.0, 205.0), (285.0, 115.0), (385.0, 115.0), (385, 205)], [(385, 205), (365.0, 205.0)],
                           [(365.0, 205.0), (365.0, 145.0), (305, 145), (305.0, 205.0)],
                           [(305.0, 205.0), (285.0, 205.0)]],
                          [[(275.0, 205.0), (395, 205)], [(395, 205), (415, 205), (415, 225)], [(415, 225), (415, 305)],
                           [(415, 305), (415, 325), (395, 325)], [(395, 325), (275, 325)],
                           [(275, 325), (255, 325), (255, 305)], [(255, 305), (255, 225)],
                           [(255, 225), (255, 205), (275, 205)], [(275, 205), (335, 225)],
                           [(335, 225), (355, 225), (355, 245)], [(355, 245), (355, 265), (345, 265)],
                           [(345, 265), (355.0, 305.0)], [(355.0, 305.0), (315.0, 305.0)], [(315.0, 305.0), (325, 265)],
                           [(325, 265), (315, 265), (315.0, 245.0)], [(315.0, 245.0), (315.0, 225.0), (335.0, 225.0)],
                           [(335.0, 225.0), (275.0, 205.0)]]]],
                ['splat', [
                    [[[385.0, 265.0], [250.0, 85.0], [475.0, 145.0]], [[475.0, 145.0], [670.0, 115.0], [610.0, 190.0]],
                     [[610.0, 190.0], [730.0, 325.0], [580.0, 340.0]], [[580.0, 340.0], [505.0, 475.0], [475.0, 370.0]],
                     [[475.0, 370.0], [295.0, 490.0], [385.0, 265.0]]]]],
                ['more', [[[(225.0, 175.0), (355.0, 305.0)], [(355.0, 305.0), (415.0, 365.0), (475.0, 305.0)],
                           [(475.0, 305.0), (605.0, 175.0)], [(605.0, 175.0), (625.0, 155.0), (605.0, 135.0)],
                           [(605.0, 135.0), (585.0, 115.0), (565.0, 135.0)], [(565.0, 135.0), (445.0, 255.0)],
                           [(445.0, 255.0), (415.0, 285.0), (385.0, 255.0)], [(385.0, 255.0), (265.0, 135.0)],
                           [(265.0, 135.0), (245.0, 115.0), (225.0, 135.0)],
                           [(225.0, 135.0), (205.0, 155.0), (225.0, 175.0)]]]],
                ['dropdown', [[[(275.0, 125.0), (435.0, 285.0)], [(435.0, 285.0), (595.0, 125.0)],
                               [(595.0, 125.0), (565.0, 95.0)], [(565.0, 95.0), (435.0, 225.0)],
                               [(435.0, 225.0), (305.0, 95.0)], [(305.0, 95.0), (275.0, 125.0)]]]],
                ['blobby', [[[(445.0, 325.0), (585.0, 525.0), (725.0, 215.0), (665.0, 135.0)],
                             [(665.0, 135.0), (575.0, 85.0), (235.0, -5.0), (345.0, 215.0)],
                             [(345.0, 215.0), (515.0, 185.0), (745.0, 105.0), (445.0, 325.0)]]]],
                ]
        for a in self.images:
            data.append(a)
        names = [a[0] for a in data]
        splines = []
        for a in names:
            if len(name) > 0 and name.split()[0] == a:
                splines = data[names.index(a)][1]
        if splines == []:
            for a in list(self.inbuiltimages):
                if len(name) > 0 and name.split()[0] == a:
                    img = self.inbuiltimages[a]
                    sc = size / img.get_height()
                    return pygame.transform.scale(img, (img.get_width() * sc, size)), True, img.get_colorkey()
            return 0, False, backcol
        boundingbox = [1000, 1000, 0, 0]
        for a in splines:
            for b in a:
                for c in b:
                    if c[0] < boundingbox[0]: boundingbox[0] = c[0]
                    if c[1] < boundingbox[1]: boundingbox[1] = c[1]
                    if c[0] > boundingbox[2]: boundingbox[2] = c[0]
                    if c[1] > boundingbox[3]: boundingbox[3] = c[1]
        minus1 = [boundingbox[0], boundingbox[1]]

        mul1 = size / (boundingbox[3] - boundingbox[1])
        polys = []
        for b in splines:
            points = []
            for a in b:
                points += Draw.bezierdrawer(
                    [((a[c][0] - minus1[0]) * mul1, (a[c][1] - minus1[1]) * mul1) for c in range(len(a))], 0, False,
                    rounded=False)
            polys.append(points)
        boundingbox = [1000, 1000, 0, 0]
        for a in polys:
            for c in a:
                if c[0] < boundingbox[0]: boundingbox[0] = c[0]
                if c[1] < boundingbox[1]: boundingbox[1] = c[1]
                if c[0] > boundingbox[2]: boundingbox[2] = c[0]
                if c[1] > boundingbox[3]: boundingbox[3] = c[1]
        minus = [boundingbox[0], boundingbox[1]]
        mul = size / (boundingbox[3] - boundingbox[1])
        surf = pygame.Surface(
            (size * ((boundingbox[2] - boundingbox[0]) / (boundingbox[3] - boundingbox[1])) + 2, size + 2))
        surf.fill(backcol)
        for b in splines:
            points = []
            for a in b:
                if len(a) == 2:
                    detail = 1
                else:
                    detail = 200
                points += Draw.bezierdrawer([(((a[c][0] - minus1[0]) * mul1 - minus[0]) * mul + 1,
                                              ((a[c][1] - minus1[1]) * mul1 - minus[1]) * mul + 1) for c in
                                             range(len(a))], 0, False, detail=detail, rounded=self.roundedbezier)
            pygame.draw.polygon(surf, col, points)
        return surf, True, backcol

    def addinbuiltimage(self, name, surface):
        self.inbuiltimages[name] = surface

    def getshapedata(self, name, var, defaults):
        vals = defaults
        if sum([a in name for a in var]) > 0:
            namesplit = name.split()
            for a in namesplit:
                for i, b in enumerate(var):
                    if b == a.split('=')[0]:
                        try:
                            vals[i] = float(a.split('=')[1])
                        except:
                            if str(a.split('=')[1]).lower() == 'true':
                                vals[i] = True
                            elif str(a.split('=')[1]).lower() == 'false':
                                vals[i] = False
                            else:
                                vals[i] = str(a.split('=')[1])
        return vals

    def drawtosurf(self, screen, IDlist, surfcol, x, y, displayrect=None, displaymode='render', roundedcorners=0):
        surf = pygame.Surface((self.screenw, self.screenh))
        surf.fill(surfcol)
        surf.set_colorkey(surfcol)
        for a in IDlist:
            if a in self.IDs:
                if displaymode == 'render':
                    self.IDs[a].render(surf)
                else:
                    self.IDs[a].draw(surf)

        Draw.blitroundedcorners(surf, screen, x, y, roundedcorners, pygame.Rect(displayrect))

    def rendertextlined(self, text, size, col='default', backingcol=(150, 150, 150), font='default', width=-1,
                        bold=False, antialiasing=True, center=False, spacing=0, imgin=False, img='', scale='default',
                        linelimit=10000, getcords=False, cutstartspaces=False):
        if font == 'default': font = Style.defaults['font']
        if col == 'default': col = Style.defaults['textcol']
        if width == -1 and center: center = False
        if scale == 'default': scale = self.scale
        size *= scale
        if width != -1: width *= scale
        if text == '' and (img == '' or img == 'none'):
            if getcords:
                return pygame.Surface((0, 0)), []
            return pygame.Surface((0, 0))
        imgchr = 'ξ'
        imgtracker = 0
        if imgin:
            texts, imgnames = self.seperatestring(text)
        else:
            texts = [text]
            imgnames = ['']
        ntext = ''
        for i, a in enumerate(texts):
            ntext += a
            if imgnames[i] != '':
                ntext += imgchr

        imgsurfs = [self.rendershape(imgnames[i], size, col, backcol=backingcol) for i in range(len(imgnames))]

        linesimgchr = Utils.losslesssplit(ntext, '\n')
        linesimgchrstored = []
        linesrealtext = Utils.losslesssplit(text, '\n')
        linesrealtextstored = []
        textgen = pygame.font.SysFont(font, int(size), bold)

        textimages = []
        imagesize = [0, 0]
        addedlines = 0
        while len(linesimgchr) > 0 and addedlines < linelimit:
            newline = ''
            if width != -1:
                chrwidth = self.gettextsize(linesrealtext[0], font, size, bold, imgin)[0]
                imgtrackeroffset = 0
                while chrwidth > width:
                    split = linesimgchr[0].rsplit(' ', 1)
                    if len(split) > 1:
                        slide = split[1]
                        replace = split[0] + ' '
                        if split[1] == '':
                            slide = ' '
                            replace = split[0]
                    else:
                        replace = split[0][:len(split[0]) - 1]
                        if split[0] != '':
                            slide = split[0][-1]
                        else:
                            slide = ''
                    linesimgchr[0] = replace
                    replace, imgtrackeroffset = self.replaceimgchr(replace, imgchr, imgtracker, imgnames)
                    linesrealtext[0] = replace
                    newline = slide + newline
                    chrwidth = self.gettextsize(linesrealtext[0], font, size, bold, imgin)[0]
                imgtracker += imgtrackeroffset
            if linesimgchr[0] == '':
                linesimgchr[0] = newline
                newline, _ = self.replaceimgchr(newline, imgchr, imgtracker, imgnames)
                linesrealtext[0] = newline
                newline = ''
            if cutstartspaces and len(linesimgchr[0]) > 0 and linesimgchr[0][0] == ' ':
                linesimgchr[0] = linesimgchr[0].removeprefix(' ')
                linesrealtext[0] = linesrealtext[0].removeprefix(' ')
            textimages.append(
                self.rendertext(linesrealtext[0].replace('\n', ''), int(size), col, font, bold, antialiasing,
                                backingcol, imgin, img))
            tempsize = (textimages[-1].get_width(), textimages[-1].get_height())
            if tempsize[0] > imagesize[0]: imagesize[0] = tempsize[0]
            imagesize[1] += tempsize[1] + spacing
            linesimgchrstored.append(linesimgchr[0])
            del linesimgchr[0]
            linesrealtextstored.append(linesrealtext[0][:])
            del linesrealtext[0]
            if newline != '':
                linesimgchr.insert(0, newline)
                newline, _ = self.replaceimgchr(newline, imgchr, imgtracker, imgnames)
                linesrealtext.insert(0, newline)
            elif not ('\n' in text):
                break
            addedlines += 1
        surf = pygame.Surface(imagesize)
        surf.fill(backingcol)
        yinc = 0
        if not center:
            for a in textimages:
                surf.blit(a, (0, yinc))
                yinc += a.get_height() + spacing
        else:
            for a in textimages:
                surf.blit(a, (int(surf.get_width() / 2) - int(a.get_width() / 2), yinc))
                yinc += a.get_height() + spacing
        surf.set_colorkey(backingcol)
        if getcords:
            cords = self.textlinedcordgetter(center, imagesize, textimages, linesimgchrstored, textgen, spacing, width,
                                             imgsurfs, linesrealtextstored, imgchr, imgnames, size, font, bold)
            return surf, cords
        return surf

    def textlinedcordgetter(self, center, imagesize, textimages, linesimgchrstored, textgen, spacing, width, imgsurfs,
                            linesrealtextstored, imgchr, imgnames, size, font, bold):
        rowstart = []
        if center:
            for a in linesrealtextstored:
                rowstart.append(int(width / 2) - int(textgen.size(a)[0] / 2))
        else:
            rowstart = [0 for a in range(len(linesrealtextstored))]
        yinc = 0
        corddata = []
        noffset = 0
        nsize = textgen.size('\n')[0]
        imgtracker = 0
        for i, a in enumerate(linesimgchrstored):
            if a[:1] == '\n':
                noffset = nsize
            else:
                noffset = 0
            corddata.append([])
            inc = 0
            for b in range(len(a)):
                b += inc
                extend = False
                if a[b] == imgchr:
                    a = a.replace(imgchr, '{' + imgnames[imgtracker] + '}', 1)
                    inc += len(imgnames[imgtracker]) + 1
                    b += len(imgnames[imgtracker]) + 1
                    lettersize = imgsurfs[imgtracker].get_size()
                    imgtracker += 1
                    extend = True
                else:
                    lettersize = textgen.size(a[b])
                if inc == 0:
                    linesize = textgen.size(a[:b + 1])
                else:
                    swapped = a[:b + 1]
                    linesize = self.gettextsize(swapped, font, size, bold)
                corddata[-1].append(
                    [a[b], [rowstart[i] + linesize[0] - lettersize[0] / 2 - noffset, yinc + lettersize[1] / 2],
                     lettersize])
                if extend:
                    del corddata[-1][-1]
                    for c in range(len(imgnames[imgtracker - 1]) + 1, -1, -1):
                        corddata[-1].append([a[b - c], [rowstart[i] + linesize[0] - lettersize[0] / 2 - noffset,
                                                        yinc + lettersize[1] / 2], lettersize])
            if len(corddata[-1]) != 0:
                ypoint = max([c[1][1] for c in corddata[-1]])
                for c in corddata[-1]:
                    c[1][1] = ypoint

                yinc += linesize[1] + spacing
        return corddata

    def gettextsize(self, text, font, textsize, bold=False, imgin=True):
        textgen = pygame.font.SysFont(font, int(textsize), bold)
        if imgin:
            texts, imgnames = self.seperatestring(text)
        else:
            texts = [text]
            imgnames = ['']
        size = [0, 0]
        for a in range(len(texts)):
            if texts[a] != '':
                addon = textgen.size(texts[a])
                size[0] += addon[0]
                size[1] = max(size[1], addon[1])
            if imgnames[a] != '':
                addon = self.rendershape(imgnames[a], textsize, (150, 150, 150), False, (0, 0, 0)).get_size()
                size[0] += addon[0]
                size[1] = max(size[1], addon[1])

        return size

    def replaceimgchr(self, line, imgchr, imgtracker, imgnames):
        count = 0
        while line.count(imgchr) != 0:
            line = line.replace(imgchr, '{' + imgnames[imgtracker + count] + '}', 1)
            if imgtracker + count != len(imgnames) - 1:
                count += 1
        return line, count

    def addid(self, ID, obj, refitems=True):
        if ID in self.IDs:
            adder = 1
            ID += str(adder)
            while ID in self.IDs:
                ID = ID.removesuffix(str(adder))
                adder += 1
                ID += str(adder)
        if self.idmessages: print('adding:', ID)
        self.IDs[ID] = obj
        obj.ID = ID
        if type(obj) == Menu:
            self.automenus.append(obj)
        else:
            if type(obj) == Button:
                self.buttons.append(obj)
            elif type(obj) == Textbox:
                self.textboxes.append(obj)
            elif type(obj) in [Table, ScrollerTable]:
                self.tables.append(obj)
            elif type(obj) == DropDown:
                self.dropdowns.append(obj)
            elif type(obj) == Text:
                self.texts.append(obj)
            elif type(obj) == Scroller:
                self.scrollers.append(obj)
            elif type(obj) == Slider:
                self.sliders.append(obj)
            elif type(obj) == WindowedMenu:
                self.windowedmenus.append(obj)
            elif type(obj) == Window:
                self.windows.append(obj)
            elif type(obj) == Animation:
                self.animations.append(obj)
            elif type(obj) == Rectangle:
                self.rects.append(obj)
            self.refreshitems()
        if not type(obj) in [Animation, Menu] and Utils.menuin(obj.truemenu, self.windowedmenunames):
            for b in obj.truemenu:
                if b in self.windowedmenunames:
                    valid = True
                    for a in obj.master:
                        if type(a) in [Button, Textbox, Text, Table, ScrollerTable, Scroller, Slider, Rectangle]:
                            valid = False
                    if valid:
                        self.windowedmenus[self.windowedmenunames.index(b)].binditem(obj, False, False)

    def reID(self, ID, obj):
        newid = ID
        if ID in self.IDs:
            adder = 1
            ID += str(adder)
            while ID in self.IDs:
                ID = ID.removesuffix(str(adder))
                adder += 1
                ID += str(adder)
        self.IDs[newid] = self.IDs.pop(obj.ID)
        obj.ID = newid

    def refreshitems(self):
        self.items = self.buttons + self.textboxes + self.tables + self.texts + self.scrollers + self.sliders + self.windowedmenus + self.rects + self.dropdowns + self.windows
        for a in self.items:
            if len(a.master) < len(a.truemenu) or not a.onitem:
                menu = a.truemenu
                for m in menu:
                    if not (m in self.windowedmenunames):
                        if not ('auto_generate_menu:' + m in self.IDs):
                            obj = self.automakemenu(m)
                        else:
                            obj = self.IDs['auto_generate_menu:' + m]
                        obj.binditem(a, False, False)
        self.items += self.automenus
        self.items.sort(key=lambda x: x.layer, reverse=False)
        self.refreshbuttonkeys()

    def refreshbuttonkeys(self):
        self.buttonkeys = {}
        for a in self.items:
            for k in a.presskeys:
                if not k in self.buttonkeys: self.buttonkeys[k] = []
                self.buttonkeys[k].append(a)

    def refreshnoclickrects(self):
        self.noclickrects = []
        for a in self.items:
            a.noclickrectsapplied = []
            a.refreshnoclickrect()
            self.noclickrects += a.noclickrect
        # Rect,IDs,menu,whitelist (true=all objects in list blocked by noclickrect)
        for a in self.noclickrects:
            objs = self.onmenu(a[2])
            if a[3]:
                for b in objs:
                    if b.ID in a[1]:
                        b.noclickrectsapplied.append(a[0])
            else:
                for b in objs:
                    if not b.ID in a[1]:
                        b.noclickrectsapplied.append(a[0])

    def printtree(self, obj=False):
        if type(obj) == str: obj = self.IDs[obj]
        prefixes = ['<{-=-{=-[=]-=}-=-}>', '#@' * 5, '<=>' * 3, '+=' * 3, '--', '']
        if obj == False:
            depth = max([self.gettreedepth(a) for a in self.automenus + self.windowedmenus])
            prefixes = prefixes[(6 - depth):]
            for a in self.automenus + self.windowedmenus:
                self.printbound(a, prefixes)
        else:
            prefixes = prefixes[(6 - self.gettreedepth(obj)):]
            self.printbound(obj, prefixes)

    def printbound(self, obj, prefixes):
        if prefixes[0] == '':
            print(obj.ID)
        else:
            print(prefixes[0], obj.ID)
        for a in obj.bounditems:
            self.printbound(a, prefixes[1:])

    def gettreedepth(self, obj, depth=1):
        ndepths = [depth]
        if len(obj.bounditems) > 0:
            depth += 1
            ndepths = []
            for a in obj.bounditems:
                ndepths.append(self.gettreedepth(a, depth))
        return max(ndepths)

    def makebutton(self, x, y, text, textsize=-1, command=Utils.emptyFunction, menu='main', ID='button', layer=1,
                   roundedcorners=-1, bounditems=[], killtime=-1, width=-1, height=-1,
                   anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, img='none', font=-1, bold=-1,
                   antialiasing=-1, pregenerated=True, enabled=True,
                   border=-1, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                   scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                   runcommandat=0, col=-1, textcol=-1, backingcol=-1, bordercol=-1, hovercol=-1, clickdownsize=-1,
                   clicktype=-1, textoffsetx=-1, textoffsety=-1, maxwidth=-1,
                   dragable=False, colorkey=-1, toggle=True, toggleable=False, toggletext=-1, toggleimg='none',
                   togglecol=-1, togglehovercol=-1, bindtoggle=[], spacing=-1, verticalspacing=-1, horizontalspacing=-1,
                   clickablerect=-1, clickableborder=-1,
                   backingdraw=-1, borderdraw=-1, animationspeed=-1, linelimit=1000, refreshbind=[], presskeys=[]):
        if maxwidth == -1: maxwidth = width
        if backingcol == -1: backingcol = bordercol
        obj = Button(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                     roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                     anchor=anchor, objanchor=objanchor, center=center, centery=centery, text=str(text),
                     textsize=textsize, img=img, font=font, bold=bold, antialiasing=antialiasing,
                     pregenerated=pregenerated, enabled=enabled,
                     border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                     leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                     glow=glow, glowcol=glowcol,
                     command=command, runcommandat=runcommandat, col=col, textcol=textcol, backingcol=backingcol,
                     hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype, textoffsetx=textoffsetx,
                     textoffsety=textoffsety, maxwidth=maxwidth,
                     dragable=dragable, colorkey=colorkey, toggle=toggle, toggleable=toggleable, toggletext=toggletext,
                     toggleimg=toggleimg, togglecol=togglecol, togglehovercol=togglehovercol, bindtoggle=bindtoggle,
                     spacing=spacing, verticalspacing=verticalspacing, horizontalspacing=horizontalspacing,
                     clickablerect=clickablerect, clickableborder=clickableborder,
                     animationspeed=animationspeed, backingdraw=backingdraw, borderdraw=borderdraw, linelimit=linelimit,
                     refreshbind=refreshbind, presskeys=presskeys)
        return obj

    def makecheckbox(self, x, y, textsize=-1, command=Utils.emptyFunction, menu='main', ID='checkbox', text='{tick}', layer=1,
                     roundedcorners=0, bounditems=[], killtime=-1, width=-1, height=-1,
                     anchor=(0, 0), objanchor=(0, 0), center=False, centery=-1, img='none', font=-1, bold=-1,
                     antialiasing=-1, pregenerated=True, enabled=True,
                     border=4, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                     scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                     runcommandat=0, col=-1, textcol=-1, backingcol=-1, bordercol=-1, hovercol=-1, clickdownsize=-1,
                     clicktype=-1, textoffsetx=-1, textoffsety=-1, maxwidth=-1,
                     dragable=False, colorkey=-1, toggle=True, toggleable=True, toggletext='', toggleimg='none',
                     togglecol=-1, togglehovercol=-1, bindtoggle=[], spacing=-1, verticalspacing=-1,
                     horizontalspacing=-1, clickablerect=-1, clickableborder=10,
                     backingdraw=False, borderdraw=-1, animationspeed=-1, linelimit=1000, refreshbind=[], presskeys=[]):
        if textsize == -1: textsize = Style.defaults['textsize']
        if spacing == -1: spacing = -int(textsize / 5)
        if width == -1: width = textsize + spacing * 2
        if height == -1: height = textsize + spacing * 2
        obj = Button(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                     roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                     anchor=anchor, objanchor=objanchor, center=center, centery=centery, text=text, textsize=textsize,
                     img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                     enabled=enabled,
                     border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                     leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                     glow=glow, glowcol=glowcol,
                     command=command, runcommandat=runcommandat, col=col, textcol=textcol, backingcol=backingcol,
                     hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype, textoffsetx=textoffsetx,
                     textoffsety=textoffsety, maxwidth=maxwidth,
                     dragable=dragable, colorkey=colorkey, toggle=toggle, toggleable=toggleable, toggletext=toggletext,
                     toggleimg=toggleimg, togglecol=togglecol, togglehovercol=togglehovercol, bindtoggle=bindtoggle,
                     spacing=spacing, verticalspacing=verticalspacing, horizontalspacing=horizontalspacing,
                     clickablerect=clickablerect, clickableborder=clickableborder,
                     animationspeed=animationspeed, backingdraw=backingdraw, borderdraw=borderdraw, linelimit=linelimit,
                     refreshbind=refreshbind, presskeys=presskeys)
        return obj

    def maketextbox(self, x, y, text='', width=200, lines=-1, menu='main', command=Utils.emptyFunction, ID='textbox', layer=1,
                    roundedcorners=-1, bounditems=[], killtime=-1, height=-1,
                    anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, img='none', textsize=-1, font=-1, bold=-1,
                    antialiasing=-1, pregenerated=True, enabled=True,
                    border=3, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                    scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                    runcommandat=0, col=-1, textcol=-1, backingcol=-1, hovercol=-1, clickdownsize=4, clicktype=0,
                    textoffsetx=-1, textoffsety=-1,
                    colorkey=-1, spacing=-1, verticalspacing=-1, horizontalspacing=-1, clickablerect=-1,
                    attachscroller=True, intscroller=False, minint=-math.inf, maxint=math.inf, intwraparound=False,
                    linelimit=-1, selectcol=-1, selectbordersize=2, selectshrinksize=0, cursorsize=-1, textcenter=-1,
                    chrlimit=10000, numsonly=False, enterreturns=False, commandifenter=True, commandifkey=False,
                    imgdisplay=False, allowedcharacters='',
                    backingdraw=-1, borderdraw=-1, refreshbind=[]):

        if col == -1: col = Style.objectdefaults[Textbox]['col']
        if backingcol == -1: backingcol = ColEdit.autoshiftcol(Style.objectdefaults[Textbox]['backingcol'], col, -20)

        obj = Textbox(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                      roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                      anchor=anchor, objanchor=objanchor, center=center, centery=centery, text=text, textsize=textsize,
                      img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                      enabled=enabled,
                      border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                      leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                      glow=glow, glowcol=glowcol,
                      command=command, runcommandat=runcommandat, col=col, textcol=textcol, backingcol=backingcol,
                      hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype, textoffsetx=textoffsetx,
                      textoffsety=textoffsety,
                      colorkey=colorkey, spacing=spacing, verticalspacing=verticalspacing,
                      horizontalspacing=horizontalspacing, clickablerect=clickablerect, attachscroller=attachscroller,
                      intscroller=intscroller, minp=minint, maxp=maxint, intwraparound=intwraparound,
                      lines=lines, linelimit=linelimit, selectcol=selectcol, selectbordersize=selectbordersize,
                      selectshrinksize=selectshrinksize, cursorsize=cursorsize, textcenter=textcenter,
                      chrlimit=chrlimit, numsonly=numsonly, enterreturns=enterreturns, commandifenter=commandifenter,
                      commandifkey=commandifkey, imgdisplay=imgdisplay, allowedcharacters=allowedcharacters,
                      backingdraw=backingdraw, borderdraw=borderdraw, refreshbind=refreshbind)
        return obj

    ##    def maketable(self,x,y,data='empty',titles=[],menu='main',menuexceptions=[],edgebound=(1,0,0,1),rows=5,colomns=3,boxwidth=-1,boxheight=-1,spacing=10,col='default',boxtextcol='default',boxtextsize=40,boxcenter=True,font='default',bold=False,titlefont=-1,titlebold=-1,titleboxcol=-1,titletextcol='default',titletextsize=-1,titlecenter=True,linesize=2,linecol=-1,roundedcorners=0,layer=1,ID='default',returnobj=False):

    def maketable(self, x, y, data=[], titles=[], menu='main', ID='table', layer=1, roundedcorners=-1, bounditems=[],
                  killtime=-1, width=-1, height=-1,
                  anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, text='', textsize=-1, img='none', font=-1,
                  bold=-1, antialiasing=-1, pregenerated=True, enabled=True,
                  border=3, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                  scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                  command=Utils.emptyFunction, runcommandat=0, col=-1, textcol=-1, backingcol=-1, hovercol=-1,
                  clickdownsize=4, clicktype=0, textoffsetx=-1, textoffsety=-1,
                  dragable=False, colorkey=-1, spacing=-1, verticalspacing=-1, horizontalspacing=-1, clickablerect=-1,
                  boxwidth=-1, boxheight=-1, linesize=2, textcenter=-1, guesswidth=-1, guessheight=-1,
                  splitcellchar='M',
                  backingdraw=-1, borderdraw=-1, refreshbind=[]):

        if col == -1: col = Style.objectdefaults[Table]['col']
        if backingcol == -1: backingcol = ColEdit.autoshiftcol(Style.objectdefaults[Table]['backingcol'], col, -20)

        # obj = Table(x,y,rows,colomns,data,titles,boxwidth,boxheight,spacing,menu,menuexceptions,boxcol,boxtextcol,boxtextsize,boxcenter,font,bold,titlefont,titlebold,titleboxcol,titletextcol,titletextsize,titlecenter,linesize,linecol,roundedcorners,layer,ID,self)
        obj = Table(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                    roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                    anchor=anchor, objanchor=objanchor, center=center, centery=centery, text=text, textsize=textsize,
                    img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                    enabled=enabled,
                    border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                    leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                    glow=glow, glowcol=glowcol,
                    command=command, runcommandat=runcommandat, col=col, textcol=textcol, backingcol=backingcol,
                    hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype, textoffsetx=textoffsetx,
                    textoffsety=textoffsety,
                    colorkey=colorkey, spacing=spacing, verticalspacing=verticalspacing,
                    horizontalspacing=horizontalspacing, clickablerect=clickablerect,
                    data=data, titles=titles, boxwidth=boxwidth, boxheight=boxheight, linesize=linesize,
                    textcenter=textcenter, guesswidth=guesswidth, guessheight=guessheight, splitcellchar=splitcellchar,
                    backingdraw=backingdraw, borderdraw=borderdraw, refreshbind=refreshbind)
        return obj

    ##    def maketext(self,x,y,text,size,menu='main',menuexceptions=[],edgebound=(1,0,0,1),col='default',center=True,font='default',bold=False,maxwidth=-1,border=4,backingcol='default',backingdraw=0,backingwidth=-1,backingheight=-1,img='none',colorkey=(255,255,255),roundedcorners=0,layer=1,ID='default',antialiasing=True,pregenerated=True,returnobj=False):
    def maketext(self, x, y, text, textsize=-1, menu='main', ID='text', layer=1, roundedcorners=-1, bounditems=[],
                 killtime=-1, width=-1, height=-1,
                 anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, img='none', font=-1, bold=-1, antialiasing=-1,
                 pregenerated=True, enabled=True,
                 border=3, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                 scaley=-1, scaleby=-1, glow=0, glowcol=-1,
                 command=Utils.emptyFunction, runcommandat=0, col=-1, textcol=-1, clicktype=0, backingcol=-1, bordercol=-1,
                 textoffsetx=-1, textoffsety=-1,
                 dragable=False, colorkey=-1, spacing=-1, verticalspacing=-1, horizontalspacing=-1, maxwidth=-1,
                 animationspeed=-1, clickablerect=-1,
                 textcenter=-1, backingdraw=-1, borderdraw=-1, refreshbind=[]):
        if col == -1: col = backingcol
        if col == -1: col = Style.wallpapercol
        backingcol = bordercol

        obj = Text(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                   roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                   anchor=anchor, objanchor=objanchor, center=center, centery=centery, text=str(text),
                   textsize=textsize, img=img, font=font, bold=bold, antialiasing=antialiasing,
                   pregenerated=pregenerated, enabled=enabled,
                   border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                   leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby, glow=glow,
                   glowcol=glowcol,
                   command=command, runcommandat=runcommandat, col=col, textcol=textcol, backingcol=backingcol,
                   clicktype=clicktype, textoffsetx=textoffsetx, textoffsety=textoffsety, maxwidth=maxwidth,
                   dragable=dragable, colorkey=colorkey, spacing=spacing, verticalspacing=verticalspacing,
                   horizontalspacing=horizontalspacing, clickablerect=clickablerect,
                   textcenter=textcenter, backingdraw=backingdraw, borderdraw=borderdraw, animationspeed=animationspeed,
                   refreshbind=refreshbind)
        return obj

    ##    def makescroller(self,x,y,height,command=emptyfunction,width=15,minh=0,maxh=-1,pageh=100,starth=0,menu='main',menuexceptions=[],edgebound=(1,0,0,1),col='default',scrollercol=-1,hovercol=-1,clickcol=-1,scrollerwidth=11,runcommandat=1,clicktype=0,layer=1,ID='default',returnobj=False):
    def makescroller(self, x, y, height, command=Utils.emptyFunction, width=15, minp=0, maxp=100, pageheight=15, menu='main',
                     ID='scroller', layer=1, roundedcorners=-1, bounditems=[], killtime=-1,
                     anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, enabled=True,
                     border=3, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                     scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                     runcommandat=1, col=-1, backingcol=-1, clicktype=0, clickablerect=-1, scrollbind=[],
                     dragable=True, backingdraw=-1, borderdraw=-1, scrollercol=-1, increment=0, startp=0,
                     refreshbind=[], screencompressed=False):

        if maxp == -1: maxp = height

        obj = Scroller(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                       roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                       anchor=anchor, objanchor=objanchor, center=center, centery=centery, enabled=enabled,
                       border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                       leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                       glow=glow, glowcol=glowcol,
                       command=command, runcommandat=runcommandat, col=col, backingcol=backingcol, clicktype=clicktype,
                       dragable=dragable, backingdraw=backingdraw, borderdraw=borderdraw, clickablerect=clickablerect,
                       scrollbind=scrollbind,
                       increment=increment, minp=minp, maxp=maxp, startp=startp, pageheight=pageheight,
                       refreshbind=refreshbind, screencompressed=screencompressed)
        return obj

    ##    def makeslider(self,x,y,width,height,maxp=100,menu='main',command=emptyfunction,menuexceptions=[],edgebound=(1,0,0,1),col='default',slidercol=-1,sliderbordercol=-1,hovercol=-1,clickcol=-1,clickdownsize=2,bordercol=-1,border=2,slidersize=-1,increment=0,img='none',colorkey=(255,255,255),minp=0,startp=0,style='square',roundedcorners=0,barroundedcorners=-1,dragable=True,runcommandat=1,clicktype=0,layer=1,ID='default',returnobj=False):
    def makeslider(self, x, y, width, height, maxp=100, menu='main', command=Utils.emptyFunction, ID='slider', layer=1,
                   roundedcorners=-1, bounditems=[], boundtext=-1, killtime=-1,
                   anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, enabled=True,
                   border=3, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                   scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                   runcommandat=1, col=-1, backingcol=-1, button='default', clickablerect=-1,
                   dragable=True, colorkey=(255, 255, 255), backingdraw=-1, borderdraw=-1,
                   slidersize=-1, increment=0, sliderroundedcorners=-1, minp=0, startp=0, direction='horizontal',
                   containedslider=-1, movetoclick=-1, refreshbind=[]):
        if boundtext != -1:
            bounditems.append(boundtext)
        obj = Slider(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                     roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                     anchor=anchor, objanchor=objanchor, center=center, centery=centery, enabled=enabled,
                     border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                     leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                     glow=glow, glowcol=glowcol,
                     command=command, runcommandat=runcommandat, col=col, backingcol=backingcol,
                     clickablerect=clickablerect,
                     dragable=dragable, colorkey=colorkey, backingdraw=backingdraw, borderdraw=borderdraw,
                     slidersize=slidersize, increment=increment, sliderroundedcorners=sliderroundedcorners, minp=minp,
                     maxp=maxp, startp=startp, direction=direction, containedslider=containedslider, data=button,
                     movetoclick=movetoclick, refreshbind=refreshbind)
        obj.boundtext = boundtext
        if type(boundtext) == Textbox:
            boundtext.slider = obj
        obj.updatetext()
        return obj

    ##    def makewindowedmenu(self,x,y,width,height,menu,behindmenu,edgebound=(1,0,0,1),col='default',isolated=True,roundedcorners=0,darken=60,colourkey=(243,244,242),ID='default'):
    def makewindowedmenu(self, x, y, width, height, menu, behindmenu='main', col=-1, bounditems=[],
                         dragable=False, colorkey=(255, 255, 255), isolated=True, darken=-1, ID='windowedmenu', layer=1,
                         roundedcorners=-1,
                         anchor=(0, 0), objanchor=(0, 0), center=False, centery=-1, enabled=True, glow=-1, glowcol=-1,
                         scalesize=-1, scalex=-1, scaley=-1, scaleby=-1, command=Utils.emptyFunction, runcommandat=0,
                         refreshbind=[], presskeys=[]):

        if col == -1: col = ColEdit.shiftcolor(Style.objectdefaults[WindowedMenu]['col'], -35)

        self.windowedmenunames = [a.menu for a in self.windowedmenus]
        self.windowedmenunames.append(menu)

        obj = WindowedMenu(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                           roundedcorners=roundedcorners, bounditems=bounditems,
                           anchor=anchor, objanchor=objanchor, center=center, centery=centery,
                           scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                           command=Utils.emptyFunction, runcommandat=runcommandat, col=col,
                           dragable=dragable, colorkey=colorkey, border=0, enabled=enabled,
                           behindmenu=behindmenu, isolated=isolated, darken=darken, refreshbind=refreshbind,
                           presskeys=presskeys)
        return obj

    def makewindow(self, x, y, width, height, menu='main', col=-1, bounditems=[], colorkey=(255, 255, 255),
                   ID='window', layer=10, roundedcorners=-1, anchor=(0, 0), objanchor=(0, 0), isolated=False, darken=-1,
                   center=False, centery=-1, enabled=False, glow=-1, glowcol=-1, scalesize=-1, scalex=-1, scaley=-1,
                   scaleby=-1, backingdraw=-1,
                   refreshbind=[], clickablerect=(0, 0, 'w', 'h'), animationspeed=-1, animationtype='moveup',
                   autoshutwindows=[], presskeys=[]):

        if col == -1: col = ColEdit.shiftcolor(Style.objectdefaults[Window]['col'], -35)

        obj = Window(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                     roundedcorners=roundedcorners, bounditems=bounditems,
                     anchor=anchor, objanchor=objanchor, center=center, centery=centery, enabled=enabled,
                     scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby, col=col, colorkey=colorkey,
                     autoshutwindows=autoshutwindows, backingdraw=backingdraw,
                     refreshbind=refreshbind, isolated=isolated, darken=darken, clickablerect=clickablerect,
                     animationspeed=animationspeed, animationtype=animationtype, presskeys=presskeys)
        return obj

    def makerect(self, x, y, width, height, command=Utils.emptyFunction, menu='main', ID='button', layer=1, roundedcorners=-1,
                 bounditems=[], killtime=-1,
                 anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, enabled=True,
                 border=0, scalesize=-1, scalex=-1, scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                 runcommandat=0, col=-1, dragable=False, backingdraw=-1, refreshbind=[]):
        obj = Rectangle(ui=self, x=x, y=y, command=Utils.emptyFunction, menu=menu, ID=ID, layer=layer,
                   roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime, width=width, height=height,
                   anchor=anchor, objanchor=objanchor, center=center, centery=centery, enabled=enabled,
                   border=border, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby, glow=glow,
                   glowcol=glowcol,
                   runcommandat=runcommandat, col=col, dragable=dragable, backingdraw=backingdraw,
                   refreshbind=refreshbind)
        return obj

    def makecircle(self, x, y, radius, command=Utils.emptyFunction, menu='main', ID='button', layer=1, roundedcorners=-1,
                   bounditems=[], killtime=-1,
                   anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, enabled=True,
                   border=-1, scalesize=-1, scalex=-1, scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                   runcommandat=0, col=-1, dragable=False, backingdraw=-1, refreshbind=[]):
        if roundedcorners == -1: roundedcorners = radius
        obj = self.makerect(x=x, y=y, width=radius * 2, height=radius * 2, command=command, menu=menu, ID=ID,
                            layer=layer, roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                            anchor=anchor, objanchor=objanchor, center=center, centery=centery, enabled=enabled,
                            border=border, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                            glow=glow, glowcol=glowcol,
                            runcommandat=runcommandat, col=col, dragable=dragable, backingdraw=backingdraw,
                            refreshbind=refreshbind)
        return obj

    def makesearchbar(self, x, y, text='Search', width=400, lines=1, menu='main', command=Utils.emptyFunction, ID='searchbar',
                      layer=1, roundedcorners=-1, bounditems=[], killtime=-1, height=-1,
                      anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, img='none', textsize=-1, font=-1, bold=-1,
                      antialiasing=-1, pregenerated=True, enabled=True,
                      border=3, upperborder=-1, lowerborder=-1, scalesize=-1, scalex=-1, scaley=-1, scaleby=-1, glow=0,
                      glowcol=-1,
                      runcommandat=0, col=-1, textcol=-1, titletextcol=-1, backingcol=-1, hovercol=-1, clickdownsize=-1,
                      clicktype=0, textoffsetx=-1, textoffsety=-1,
                      colorkey=-1, spacing=-1, verticalspacing=2, horizontalspacing=4, clickablerect=-1,
                      attachscroller=True, intscroller=False, minint=-math.inf, maxint=math.inf, intwraparound=False,
                      linelimit=100, selectcol=-1, selectbordersize=2, selectshrinksize=0, cursorsize=-1, textcenter=-1,
                      chrlimit=10000, numsonly=False, enterreturns=False, commandifenter=True, commandifkey=False,
                      imgdisplay=-1, allowedcharacters='',
                      backingdraw=-1, borderdraw=-1, refreshbind=[]):

        if titletextcol == -1: titletextcol = textcol
        if upperborder == -1: upperborder = border
        if lowerborder == -1: lowerborder = border
        if textsize == -1: textsize = Style.defaults['textsize']
        if height == -1:
            heightgetter = self.rendertext('Tg', textsize, (255, 255, 255), font, bold)
            height = upperborder + lowerborder + heightgetter.get_height() * lines + verticalspacing * 2
        col = ColEdit.autoshiftcol(col, Style.defaults['col'])
        if backingcol == -1: backingcol = ColEdit.autoshiftcol(Style.defaults['backingcol'], col, 20)

        txt = self.maketext(int(border + horizontalspacing) / 2, 0, text, textsize, anchor=(0, 'h/2'),
                            objanchor=(0, 'h/2'), img=img, font=font, bold=bold, antialiasing=antialiasing,
                            pregenerated=pregenerated, enabled=enabled, textcol=titletextcol,
                            col=ColEdit.autoshiftcol(backingcol, col, -20), animationspeed=5)

        bsize = height - upperborder - lowerborder
        search = self.makebutton(-border * 2 - bsize, 0, '{search}', textsize * 0.55, command=command,
                                 roundedcorners=roundedcorners, width=bsize, height=bsize,
                                 anchor=('w', 'h/2'), objanchor=('w', 'h/2'), border=0, col=col, textcol=textcol,
                                 backingcol=backingcol, bordercol=col,
                                 clickdownsize=1, textoffsetx=0, textoffsety=0, spacing=2, clickablerect=clickablerect,
                                 hovercol=ColEdit.autoshiftcol(hovercol, col, -6), borderdraw=False)
        cross = self.makebutton(-border, 0, '{cross}', textsize * 0.5, command=Utils.emptyFunction,
                                roundedcorners=roundedcorners, width=bsize, height=bsize,
                                anchor=('w', 'h/2'), objanchor=('w', 'h/2'), border=0, col=col, textcol=textcol,
                                backingcol=backingcol, bordercol=col,
                                clickdownsize=1, textoffsetx=1, textoffsety=1, spacing=2, clickablerect=clickablerect,
                                hovercol=ColEdit.autoshiftcol(hovercol, col, -6), borderdraw=False)

        obj = self.maketextbox(x, y, '', width, lines, menu, command, ID, layer, roundedcorners,
                               bounditems + [txt, search, cross], killtime, height,
                               anchor, objanchor, center, centery, img, textsize, font, bold, antialiasing,
                               pregenerated, enabled,
                               border, upperborder, lowerborder, bsize * 2 + border * 3,
                               txt.textimage.get_width() + border + horizontalspacing * 2, scalesize, scalex, scaley,
                               scaleby, glow, glowcol,
                               runcommandat, col, textcol, backingcol, hovercol, clickdownsize, clicktype, textoffsetx,
                               textoffsety,
                               colorkey, spacing, verticalspacing, horizontalspacing, clickablerect, attachscroller,
                               intscroller, minint, maxint, intwraparound,
                               linelimit, selectcol, selectbordersize, selectshrinksize, cursorsize, textcenter,
                               chrlimit, numsonly, enterreturns, commandifenter, commandifkey, imgdisplay,
                               allowedcharacters,
                               backingdraw, borderdraw, refreshbind)

        cross.command = lambda: obj.settext('')
        return obj

    def makescrollertable(self, x, y, data=[], titles=[], menu='main', ID='scrollertable', layer=1, roundedcorners=-1,
                          bounditems=[], killtime=-1, width=-1, height=-1,
                          anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, text='', textsize=-1, img='none',
                          font=-1, bold=-1, antialiasing=-1, pregenerated=True, enabled=True,
                          border=3, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1,
                          scalex=-1, scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                          command=Utils.emptyFunction, runcommandat=0, col=-1, textcol=-1, backingcol=-1, hovercol=-1,
                          clickdownsize=4, clicktype=0, textoffsetx=-1, textoffsety=-1,
                          dragable=False, colorkey=-1, spacing=-1, verticalspacing=-1, horizontalspacing=-1,
                          clickablerect=(0, 0, 'w', 'h'),
                          boxwidth=-1, boxheight=-1, linesize=2, textcenter=-1, guesswidth=-1, guessheight=-1,
                          backingdraw=-1, borderdraw=-1, pageheight=-1, refreshbind=[], compress=True, scrollerwidth=15,
                          screencompressed=5):

        if col == -1: col = Style.objectdefaults[Table]['col']
        if backingcol == -1: backingcol = ColEdit.autoshiftcol(Style.objectdefaults[Table]['backingcol'], col, -20)

        obj = ScrollerTable(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                            roundedcorners=roundedcorners, bounditems=bounditems, killtime=killtime,
                            anchor=anchor, objanchor=objanchor, center=center, centery=centery, text=text,
                            textsize=textsize, img=img, font=font, bold=bold, antialiasing=antialiasing,
                            pregenerated=pregenerated, enabled=enabled,
                            border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                            leftborder=leftborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                            glow=glow, glowcol=glowcol,
                            command=command, runcommandat=runcommandat, col=col, textcol=textcol, backingcol=backingcol,
                            hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype,
                            textoffsetx=textoffsetx, textoffsety=textoffsety,
                            colorkey=colorkey, spacing=spacing, verticalspacing=verticalspacing,
                            horizontalspacing=horizontalspacing, clickablerect=clickablerect,
                            data=data, titles=titles, boxwidth=boxwidth, boxheight=boxheight, linesize=linesize,
                            textcenter=textcenter, guesswidth=guesswidth, guessheight=guessheight,
                            backingdraw=backingdraw, borderdraw=borderdraw, refreshbind=refreshbind,
                            scroller=Utils.EmptyObject(0, 0, 15, 15), compress=compress)
        if len(titles) != 0 and clickablerect == (0, 0, 'w', 'h'):
            obj.startclickablerect = (
            0, f'(ui.IDs["{obj.ID}"].boxheights[0]+ui.IDs["{obj.ID}"].linesize*2)*ui.IDs["{obj.ID}"].scale', 'w',
            f'h-(ui.IDs["{obj.ID}"].boxheights[0]-ui.IDs["{obj.ID}"].linesize*2)')
        if pageheight == -1:
            pageheight = self.IDs[obj.ID].height
        obj.startpageheight = pageheight
        obj.autoscale()
        scroller = self.makescroller(x=border, y=0, width=scrollerwidth, height=f'ui.IDs["{obj.ID}"].pageheight',
                                     menu=menu, ID=obj.ID + 'scroller', layer=layer, roundedcorners=roundedcorners,
                                     bounditems=bounditems, killtime=killtime,
                                     anchor=('w', 0), objanchor=(0, 0), enabled=enabled,
                                     border=border, upperborder=upperborder, lowerborder=lowerborder,
                                     rightborder=rightborder, leftborder=leftborder, scalesize=scalesize, scalex=scalex,
                                     scaley=scaley, scaleby=scaleby, glow=glow, glowcol=glowcol,
                                     col=col, backingcol=backingcol, clicktype=clicktype,
                                     backingdraw=backingdraw, borderdraw=borderdraw, clickablerect=-1, scrollbind=[],
                                     screencompressed=screencompressed,
                                     increment=0, minp=0, maxp=f"ui.IDs['{obj.ID}'].height", startp=0,
                                     pageheight=f'ui.IDs["{obj.ID}"].pageheight')
        scroller.command = lambda: obj.scrollerblocks(scroller)
        obj.refreshbind.append(scroller.ID)
        obj.binditem(scroller)
        obj.scroller = scroller
        scroller.resetcords()
        return obj

    def makedropdown(self, x, y, options: list, textsize=-1, command=Utils.emptyFunction, menu='main', ID='dropdown', layer=1,
                     roundedcorners=-1, bounditems=[], killtime=-1, width=-1, height=-1,
                     anchor=(0, 0), objanchor=(0, 0), center=-1, centery=-1, img='none', font=-1, bold=-1,
                     antialiasing=-1, pregenerated=True, enabled=True, pageheight=300,
                     border=3, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1, scalex=-1,
                     scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                     runcommandat=0, col=-1, textcol=-1, backingcol=-1, bordercol=-1, hovercol=-1, clickdownsize=-1,
                     clicktype=-1, textoffsetx=-1, textoffsety=-1, maxwidth=-1,
                     dragable=False, colorkey=-1, toggle=True, toggleable=False, toggletext=-1, toggleimg='none',
                     togglecol=-1, togglehovercol=-1, bindtoggle=[], spacing=-1, verticalspacing=1, horizontalspacing=4,
                     clickablerect=-1, clickableborder=-1,
                     backingdraw=-1, borderdraw=-1, linelimit=1000, refreshbind=[], animationspeed=15,
                     animationtype='compressleft', startoptionindex=0, dropsdown=True):

        if options == []: options = ['text']
        text = options[startoptionindex]
        if textsize == -1: textsize = Style.defaults['textsize']

        if upperborder == -1: upperborder = border
        if lowerborder == -1: lowerborder = border
        if leftborder == -1: leftborder = border
        if rightborder == -1: rightborder = border
        if height == -1:
            heightgetter = self.rendertext('Tg', textsize, (255, 255, 255), font, bold)
            height = upperborder + lowerborder + heightgetter.get_height()
        col = ColEdit.autoshiftcol(col, Style.defaults['col'])
        if dropsdown:
            txt = [self.maketext(int(border + horizontalspacing) / 2, 0, text, textsize, anchor=(0, 'h/2'),
                                 objanchor=(0, 'h/2'),
                                 img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                                 enabled=enabled, textcol=textcol, col=ColEdit.autoshiftcol(backingcol, col, 20),
                                 animationspeed=5, roundedcorners=roundedcorners)]
            text = '{more scale=0.3}'
            if width == -1:
                lborder = txt[0].textimage.get_width() + border + horizontalspacing * 2
                wid = -1
            else:
                lborder = width - textsize + border
        else:
            txt = []
            lborder = leftborder
            wid = width

        obj = DropDown(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                       roundedcorners=roundedcorners, bounditems=txt + bounditems, killtime=killtime,
                       anchor=anchor, objanchor=objanchor, center=center, centery=centery, text=text, textsize=textsize,
                       img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                       enabled=enabled,
                       border=border, upperborder=upperborder, lowerborder=lowerborder, rightborder=rightborder,
                       leftborder=lborder, scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                       glow=glow, glowcol=glowcol,
                       command=command, runcommandat=runcommandat, col=col, textcol=textcol, backingcol=backingcol,
                       hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype, textoffsetx=textoffsetx,
                       textoffsety=textoffsety, maxwidth=maxwidth,
                       dragable=dragable, colorkey=colorkey, toggle=toggle, toggleable=toggleable,
                       toggletext=toggletext, toggleimg=toggleimg, togglecol=togglecol, togglehovercol=togglehovercol,
                       bindtoggle=bindtoggle, spacing=spacing,
                       verticalspacing=verticalspacing, horizontalspacing=horizontalspacing,
                       clickablerect=clickablerect, clickableborder=clickableborder,
                       animationspeed=animationspeed, backingdraw=backingdraw, borderdraw=borderdraw,
                       linelimit=linelimit, refreshbind=refreshbind, options=options, startoptionindex=startoptionindex,
                       dropsdown=dropsdown)
        obj.init_height = height
        tablew = width
        if tablew != -1: tablew -= border * 2

        if dropsdown:

            table = self.makescrollertable(border, border, [], pageheight=pageheight, roundedcorners=roundedcorners,
                                           textsize=textsize, font=font, bold=bold, border=border, scalesize=scalesize,
                                           col=col, textcol=textcol, backingcol=backingcol, width=tablew)
            obj.table = table
            obj.refreshoptions()

            window = self.makewindow(0, obj.height, f'ui.IDs["{obj.ID}"].width',
                                     f'ui.IDs["{table.ID}"].getheight()+{border}*2', menu=menu, enabled=False,
                                     animationspeed=animationspeed, animationtype=animationtype)
            obj.binditem(window)
            window.binditem(table)
            if width == -1:
                nwidth = (max([a[0].textimage.get_width() for a in table.table]) + (
                            obj.width - obj.leftborder - obj.rightborder) + border * 5)
            else:
                nwidth = width
            obj.leftborder += nwidth - obj.width
            obj.refresh()
            obj.init_width = obj.width
            table.startwidth = nwidth - border * 2
            table.refresh()
            window.refresh()
            obj.window = window
            obj.titletext = txt[0]
        else:
            temp_texts = [self.rendertext(t, textsize, font=font, imgin=True) for t in options]
            if width == -1:
                nwidth = (max([t.get_width() for t in temp_texts]) + leftborder + rightborder + horizontalspacing * 2)
            else:
                nwidth = width
            obj.startwidth = nwidth
            obj.refresh()
            obj.init_width = nwidth

        obj.command = lambda: obj.mainbuttonclicked()
        obj.truecommand = command
        return obj

    def makelabeledcheckbox(self, x, y, text, textsize=-1, command=Utils.emptyFunction, menu='main', ID='checkbox',
                            textpos='left', layer=1, roundedcorners=0, bounditems=[], killtime=-1, width=-1, height=-1,
                            anchor=(0, 0), objanchor=(0, 0), center=False, centery=-1, img='none', font=-1, bold=-1,
                            antialiasing=-1, pregenerated=True, enabled=True,
                            border=4, upperborder=-1, lowerborder=-1, rightborder=-1, leftborder=-1, scalesize=-1,
                            scalex=-1, scaley=-1, scaleby=-1, glow=-1, glowcol=-1,
                            runcommandat=0, col=-1, textcol=-1, backingcol=-1, bordercol=-1, hovercol=-1,
                            clickdownsize=-1, clicktype=-1, textoffsetx=-1, textoffsety=-1, maxwidth=-1,
                            dragable=False, colorkey=-1, toggle=True, toggleable=True, toggleimg='none', togglecol=-1,
                            togglehovercol=-1, bindtoggle=[], spacing=-1, horizontalspacing=5, clickablerect=-1,
                            clickableborder=10,
                            backingdraw=False, borderdraw=-1, animationspeed=-1, linelimit=1000, refreshbind=[]):

        if textsize == -1: textsize = Style.defaults['textsize']

        if textpos == 'left':
            anch = (0, 'h/2')
            objanch = ('w', 'h/2')
            tx = -horizontalspacing
        else:
            anch = ('w', 'h/2')
            objanch = (0, 'h/2')
            tx = horizontalspacing
        text = self.maketext(tx, 0, text, textsize, menu, ID=ID + 'text',
                             anchor=anch, objanchor=objanch, font=font, bold=bold, antialiasing=antialiasing,
                             pregenerated=pregenerated, enabled=enabled,
                             scalesize=scalesize, scalex=scalex, scaley=scaley, scaleby=scaleby,
                             col=col, textcol=textcol, backingcol=backingcol, textoffsetx=textoffsetx,
                             textoffsety=textoffsety,
                             colorkey=colorkey, maxwidth=maxwidth, animationspeed=animationspeed)

        obj = self.makecheckbox(x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                                roundedcorners=roundedcorners, bounditems=bounditems + [text], killtime=killtime,
                                anchor=anchor, objanchor=objanchor, center=center, centery=centery, textsize=textsize,
                                img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                                enabled=enabled,
                                border=border, upperborder=upperborder, lowerborder=lowerborder,
                                rightborder=rightborder, leftborder=leftborder, scalesize=scalesize, scalex=scalex,
                                scaley=scaley, scaleby=scaleby, glow=glow, glowcol=glowcol,
                                command=command, runcommandat=runcommandat, col=col, textcol=textcol,
                                backingcol=bordercol, hovercol=hovercol, clickdownsize=clickdownsize,
                                clicktype=clicktype, textoffsetx=textoffsetx, textoffsety=textoffsety,
                                maxwidth=maxwidth,
                                dragable=dragable, colorkey=colorkey, toggle=toggle, toggleable=toggleable,
                                toggleimg=toggleimg, togglecol=togglecol, togglehovercol=togglehovercol,
                                bindtoggle=bindtoggle,
                                spacing=spacing, clickablerect=clickablerect, clickableborder=clickableborder,
                                animationspeed=animationspeed, backingdraw=backingdraw, borderdraw=borderdraw,
                                linelimit=linelimit, refreshbind=refreshbind)
        return obj

    def automakemenu(self, menu):
        obj = Menu(ui=self, x=0, y=0, width=self.screenw, height=self.screenh, menu=menu,
                   ID='auto_generate_menu:' + menu)
        return obj

    def animate(self):
        self.queuedmenumove[0] -= 1
        if self.queuedmenumove[0] < 0 and self.queuedmenumove[1] != []:
            if self.queuedmenumove[1][0] == 'move':
                self.movemenu(self.queuedmenumove[1][1], self.queuedmenumove[1][2], self.queuedmenumove[1][3])
            else:
                self.menuback(self.queuedmenumove[1][1], self.queuedmenumove[1][2])
            self.queuedmenumove[1] = []
        delete = []
        for a in self.animations:
            if a.animate():
                delete.append(a.ID)
        for a in delete:
            self.delete(a)

    def makeanimation(self, animateID, startpos, endpos, movetype='linear', length='default', command=Utils.emptyFunction,
                      runcommandat=-1, queued=True, menu=False, relativemove=False, skiptoscreen=False, acceleration=1,
                      permamove=True, ID='default'):
        if length == 'default':
            length = Style.defaults['animationspeed']
        if menu:
            for a in self.automenus:
                if (animateID in a.truemenu):
                    if not a.onitem:
                        self.makeanimation(a.ID, startpos, endpos, movetype, length, command, runcommandat, queued,
                                           False, relativemove, skiptoscreen, acceleration, permamove)
                        runcommandat = -2
        else:
            if ID == 'default':
                ID = 'animation ' + animateID
            wait = 1
            if not queued:
                tofinish = []
                for a in self.animations:
                    if a.animateID == animateID:
                        tofinish.append([a.ID, a.wait])
                tofinish.sort(key=lambda x: x[0], reverse=False)
                for a in tofinish:
                    self.IDs[a[0]].finish(True)
                    self.delete(a[0])
            else:
                for a in self.animations:
                    if a.animateID == animateID:
                        wait = max([a.wait + a.length, wait])
            obj = Animation(self, animateID, startpos, endpos, movetype, length, wait, relativemove, command,
                            runcommandat, skiptoscreen, acceleration, permamove, ID)
            self.addid(ID, obj)

    def movemenu(self, moveto, slide='none', length='default', backchainadd=True):
        if length == 'default':
            length = Style.defaults['animationspeed']
        if self.queuedmenumove[0] < 0 or slide == 'none':
            if (self.activemenu in self.windowedmenunames) and (moveto == self.activemenu) and (
                    self.queuedmenumove[0] < 0):
                if slide != 'none':
                    self.menuback(slide + ' flip', length)
                else:
                    self.menuback()
            else:
                if backchainadd:
                    self.backchain.append([self.activemenu, slide, length])
                if slide == 'none':
                    self.activemenu = moveto
                else:
                    self.slidemenu(self.activemenu, moveto, slide, length)
            for a in self.mouseheld:
                a[1] -= 1
        elif self.queuemenumove:
            if ['move', moveto, slide, length] != self.prevmenumove:
                self.queuedmenumove[1] = ['move', moveto, slide, length]
            self.prevmenumove = self.queuedmenumove[1]

    def menuback(self, slide='none', length='default'):
        if len(self.backchain) > 0:
            if slide == 'none' and self.backchain[-1][1] != 'none':
                if not (self.activemenu in self.windowedmenunames and self.backchain[-1][0] in self.windowedmenunames):
                    slide = self.backchain[-1][1] + ' flip'
                else:
                    slide = self.backchain[-1][1]
            length = self.backchain[-1][2]
        if length == 'default':
            length = Style.defaults['animationspeed']
        if self.queuedmenumove[0] < 0 or slide == 'none':
            if len(self.backchain) > 0:
                if slide == 'none':
                    self.activemenu = self.backchain[-1][0]
                else:
                    self.slidemenu(self.activemenu, self.backchain[-1][0], slide, length)
                del self.backchain[-1]
            elif self.backquits and self.queuedmenumove[0] < 0:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            for a in self.mouseheld:
                a[1] -= 1
        elif self.queuemenumove:
            if ['back', slide, length] != self.prevmenumove:
                self.queuedmenumove[1] = ['back', slide, length]
            self.prevmenumove = self.queuedmenumove[1]

    def slidemenu(self, menufrom, menuto, slide, length):
        self.queuedmenumove[0] = length * 30
        dirr = [0, 0]
        if 'left' in slide: dirr[0] -= self.screenw
        if 'right' in slide: dirr[0] += self.screenw
        if 'up' in slide: dirr[1] -= self.screenh
        if 'down' in slide: dirr[1] += self.screenh
        if 'flip' in slide: dirr = [dirr[0] * -1, dirr[1] * -1]

        if menufrom in self.windowedmenunames:
            if menuto == self.windowedmenus[self.windowedmenunames.index(menufrom)].behindmenu:
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID, 'current', dirr,
                                   'sinout', length, command=lambda: self.movemenu(menuto, backchainadd=False),
                                   runcommandat=length, queued=False, relativemove=True, skiptoscreen=True)
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID, 'current',
                                   [dirr[0] * -1, dirr[1] * -1], 'linear', 1, command=self.finishmenumove,
                                   runcommandat=1, queued=True, relativemove=True)
            else:
                if menuto in self.windowedmenunames:
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID, 'current', dirr,
                                       'sinout', length, command=lambda: self.slidemenuin(
                            self.windowedmenus[self.windowedmenunames.index(menuto)].ID, length,
                            [dirr[0] * -1, dirr[1] * -1], menuto, False), runcommandat=length, queued=False,
                                       relativemove=True, skiptoscreen=True)
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID, 'current',
                                       [dirr[0] * -1, dirr[1] * -1], 'linear', 1, relativemove=True)
                else:
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].behindmenu, 'current',
                                       dirr, 'sinout', length, command=lambda: self.slidemenuin(menuto, length, dirr),
                                       runcommandat=length, queued=False, menu=True, relativemove=True)
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].behindmenu, 'current',
                                       [dirr[0] * -1, dirr[1] * -1], 'linear', 1, menu=True, relativemove=True)
        elif menuto in self.windowedmenunames:
            if menufrom == self.windowedmenus[self.windowedmenunames.index(menuto)].behindmenu:
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menuto)].ID,
                                   [dirr[0] * -1, dirr[1] * -1], 'current', 'sinin', length,
                                   command=self.finishmenumove, runcommandat=length, queued=True, relativemove=True,
                                   skiptoscreen=True)
                self.movemenu(menuto, backchainadd=False)
            else:
                self.makeanimation(menufrom, 'current', dirr, 'sinout', length, command=lambda: self.slidemenuin(
                    self.windowedmenus[self.windowedmenunames.index(menuto)].behindmenu, length, dirr, menuto),
                                   runcommandat=length, queued=False, menu=True, relativemove=True)
                self.makeanimation(menufrom, 'current', [dirr[0] * -1, dirr[1] * -1], 'linear', 1, menu=True,
                                   relativemove=True)
        else:
            self.makeanimation(menufrom, 'current', dirr, 'sinout', length,
                               command=lambda: self.slidemenuin(menuto, length, dirr), runcommandat=length,
                               queued=False, menu=True, relativemove=True)
            self.makeanimation(menufrom, 'current', [dirr[0] * -1, dirr[1] * -1], 'linear', 1, menu=True,
                               relativemove=True)

    def slidemenuin(self, moveto, length, dirr, realmenuto=0, menu=True):
        self.makeanimation(moveto, [dirr[0] * -1, dirr[1] * -1], 'current', 'sinin', length,
                           command=self.finishmenumove, runcommandat=length, queued=True, menu=menu, relativemove=True)
        if realmenuto != 0: moveto = realmenuto
        self.movemenu(moveto, backchainadd=False)

    def finishmenumove(self):
        self.queuedmenumove[0] = -1

    def delete(self, ID, failmessage=True):
        try:
            if self.IDs[ID].onitem:
                self.IDs[ID].master[0].bounditems.remove(self.IDs[ID])
            delids = [a.ID for a in self.IDs[ID].bounditems]
            for a in delids:
                self.delete(a, failmessage)
            if type(self.IDs[ID]) == Button:
                self.buttons.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Textbox:
                selected = -1
                if self.selectedtextbox != -1:
                    selected = self.textboxes[self.selectedtextbox]
                self.textboxes.remove(self.IDs[ID])
                if selected in self.textboxes:
                    self.selectedtextbox = self.textboxes.index(selected)
                else:
                    self.selectedtextbox = -1
            elif type(self.IDs[ID]) in [Table, ScrollerTable]:
                self.tables.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == DropDown:
                self.dropdowns.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Text:
                self.texts.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Scroller:
                self.scrollers.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Slider:
                self.sliders.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Animation:
                self.animations.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Rectangle:
                self.rects.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Menu:
                self.automenus.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == Window:
                self.windows.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == WindowedMenu:
                self.windowedmenus.remove(self.IDs[ID])
            del self.IDs[ID]
            self.refreshitems()
            return True
        except Exception as e:
            if failmessage: print('Failed to delete object:', ID, 'Error:', e)
            return False

    def onmenu(self, menu):
        lis = []
        for b in self.items:
            if b.getmenu() == menu:
                lis.append(b)
        return lis
