import pygame
import time
import math
import ctypes
import threading
import dataclasses

from UIpygame.ObjectParameters.AllObjParams import AllObjParams
from UIpygame.ObjectParameters.ButtonObjParams import ButtonObjParams
from UIpygame.ObjectParameters.DropDownObjParams import DropDownObjParams
from UIpygame.ObjectParameters.RectangleObjParams import RectangleObjParams
from UIpygame.ObjectParameters.ScrollerObjParams import ScrollerObjParams
from UIpygame.ObjectParameters.ScrollerTableObjParams import ScrollerTableObjParams
from UIpygame.ObjectParameters.SliderObjParams import SliderObjParams
from UIpygame.ObjectParameters.TableObjParams import TableObjParams
from UIpygame.ObjectParameters.TextboxObjParams import TextboxObjParams
from UIpygame.ObjectParameters.TextObjParams import TextObjParams
from UIpygame.ObjectParameters.WindowObjParams import WindowObjParams


from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.ColEdit import ColEdit
from UIpygame.Utils.Collision import Collision

from UIpygame.Widgets.Button import Button
from UIpygame.Widgets.DropDown import DropDown
from UIpygame.Widgets.Table import Table
from UIpygame.Widgets.Textbox import Textbox
from UIpygame.Widgets.Text import Text
from UIpygame.Widgets.Scroller import Scroller
from UIpygame.Widgets.Slider import Slider
from UIpygame.Widgets.Menu import Menu
from UIpygame.Widgets.Window import Window
from UIpygame.Widgets.Rectangle import Rectangle
from UIpygame.Widgets.WindowedMenu import WindowedMenu
from UIpygame.Widgets.ScrollerTable import ScrollerTable
from UIpygame.Animation import Animation

from UIpygame.Constants import ClickType


class UI:
    def __init__(self, scale=1, PyUItitle=True):
        pygame.key.set_repeat(350, 31)
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
        self.scale = scale
        self.dirscale = [1, 1]
        self.mouseheld = [[0, 0], [0, 0], [0, 0]]

        self.defaults = {
            'Text': TextObjParams(),
            'Button': ButtonObjParams(),
            'Textbox': TextboxObjParams(),
            'Table': TableObjParams(),
            'ScrollerTable': ScrollerTableObjParams(),
            'Rectangle': RectangleObjParams(),
            'DropDown': DropDownObjParams(),
            'Slider': SliderObjParams(),
            'Scroller': ScrollerObjParams(),
            'Window': WindowObjParams(),
            'All': AllObjParams()
        }

        # self.buttons = []
        # self.tables = []
        # self.textboxes = []
        # self.texts = []
        # self.scrollers = []
        # self.sliders = []
        self.animations = []
        # self.rects = []
        # self.dropdowns = []
        # self.windows = []
        self.no_click_rects = []
        self.selectedtextbox = -1
        self.IDs = {}
        self.items = []
        self.buttonkeys = {}
        self.holdingtracker = []

        self.images = []
        self.getScreen()
        self.in_built_images = {}

        self.active_menu = 'main'
        self.frame_menu = 'main'
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

        self.time_tracker = time.perf_counter()

        self.scroll_limit = 100
        self.escape_back = True
        self.back_quits = True
        self.scroll_wheel_scrolls = True
        self.id_messages = False
        self.queue_menu_move = True

        self.resizable = True
        self.fullscreenable = True
        self.auto_scale = 'width'
        temp_screen = pygame.display.get_surface()
        self.base_screen_size = [temp_screen.get_width(), temp_screen.get_height()]
        self.checkCaps()
        if self.scale != 1: self.setscale(self.scale)
        self.styleload_default()

        self.PyUItitle = PyUItitle
        if PyUItitle:
            self.logo = self.rendershapelogo('logo', 50, (0, 0, 0), (255, 255, 255), False)
            self.logo.set_colorkey((255, 255, 255))
            pygame.display.set_icon(self.logo)
            pygame.display.set_caption('PyUI Application')
        self.loadtickdata()

    def checkCaps(self):
        try:
            hllDll = ctypes.WinDLL("User32.dll")
            self.capslock = bool(hllDll.GetKeyState(0x14))
        except:
            self.capslock = False

    def __splitDefaultParameterName(self, parameterName: str):
        """
        Used exclusively by UI.styleSet and UI.styleGet to separate a given parameter name
        :param parameterName: string representing the name of the param
        :return: Object name e.g. Text, or All for no specific object
        :return: Attribute name e.g. border_size
        """
        split_arg = parameterName.split("_",1)
        if len(split_arg) == 1 or (split_arg[0] not in self.defaults):
            return "All", parameterName
        return split_arg[0], split_arg[1]

    def styleSet(self, **kwargs):
        for arg in kwargs:
            # args can be in form "Button_border_size", which would set the border_size for only text
            object_type, parameter = self.__splitDefaultParameterName(arg)
            if object_type == "All":
                # No specific object given (border_size)
                for object_type_iterated in self.defaults:
                    if parameter in self.defaults[object_type_iterated].__dict__:
                        self.defaults[object_type_iterated].__setattr__(parameter, kwargs[arg])
            else:
                # Specific object given (Button_border_size)
                if parameter not in self.defaults[object_type].__dict__:
                    print(self.defaults[object_type].__dict__)
                    raise Exception(f"invalid variable name {arg}")
                self.defaults[object_type].__setattr__(parameter, kwargs[arg])

    def styleGet(self, parameterName):
        object_type, parameter = self.__splitDefaultParameterName(parameterName)
        return self.defaults[object_type].__dict__[parameter]


    def styleload_soundium(self):
        self.styleSet(col=(16, 163, 127), text_col=(255, 255, 255), wallpaper_col=(62, 63, 75), text_size=24,
                      rounded_corners=5, spacing=5, clickdownsize=2, scalesize=False)

    def styleload_default(self):
        self.styleSet(rounded_corners=0, center=False, text_size=50, font='calibri', bold=False, antialiasing=True,
                      border_size=3, scalesize=True, glow=0, backing_col=(150, 150, 150),
                      clickdownsize=4, clicktype=0, textoffsetx=0, textoffsety=0, clickableborder=0, lines=1,
                      textcenter=False, linesize=2, backing_draw=True, borderdraw=True,
                      animationspeed=30, containedslider=False, movetoclick=True, isolated=True, darken=60,
                      window_darken=0, text_col=(0, 0, 0), verticalspacing=2, horizontalspacing=8,
                      text_animation_speed=5, Text_backing_draw=False, Text_border_draw=False, Text_spacing=3,
                      DropDown_animation_speed=15, Textbox_spacing=(4, 2),
                      Table_text_center=True, Button_text_center=True, guess_width=100, guess_height=100)

    def styleload_black(self):
        self.styleSet(text_col=(0, 0, 0), backing_col=(0, 0, 0), hovercol=(255, 255, 255), border_col=(0, 0, 0),
                      verticalspacing=3, text_size=30, col=(255, 255, 255), clickdownsize=1)

    def styleload_blue(self):
        self.styleSet(col=(35, 0, 156), text_col=(230, 246, 219), wallpaper_col=(0, 39, 254), text_size=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, rounded_corners=4)

    def styleload_green(self):
        self.styleSet(col=(87, 112, 86), text_col=(240, 239, 174), wallpaper_col=(59, 80, 61), text_size=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, rounded_corners=4)

    def styleload_lightblue(self):
        self.styleSet(col=(82, 121, 214), text_col=(56, 1, 103), wallpaper_col=(228, 242, 253), text_size=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, rounded_corners=4)

    def styleload_teal(self):
        self.styleSet(col=(109, 123, 152), text_col=(176, 243, 174), wallpaper_col=(69, 65, 88), text_size=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, rounded_corners=4)

    def styleload_brown(self):
        self.styleSet(col=(39, 75, 91), text_col=(235, 217, 115), wallpaper_col=(40, 41, 35), text_size=30,
                      verticalspacing=2, horizontalspacing=5, clickdownsize=2, rounded_corners=4)

    def styleload_red(self):
        self.styleSet(col=(152, 18, 20), text_col=(234, 230, 133), wallpaper_col=(171, 19, 18), spacing=3,
                      clickdownsize=2, text_size=40, horizontalspacing=8, rounded_corners=5)

    def __scaleset__(self, scale):
        self.scale = scale
        self.dirscale = [self.screenw / self.base_screen_size[0], self.screenh / self.base_screen_size[1]]
        ##        for a in self.automenus+self.windowedmenus:
        ##            a.refresh()
        ##            a.resetcords()
        self.refreshall()
        for a in self.items:
            checker = (a.width, a.height)
            a.autoScale()
            if type(a) in [Table, ScrollerTable]:
                a.small_refresh()
            if (a.width, a.height) != checker or a.scale_size:
                a.refresh()
            if a.clickable_rect != -1:
                a.refreshClickableRect()

    def setscale(self, scale):
        pygame.event.post(
            pygame.event.Event(pygame.VIDEORESIZE, w=self.base_screen_size[0] * scale, h=self.base_screen_size[1] * scale))

    def quit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def refreshall(self):
        for a in self.automenus + self.windowedmenus:
            self.refreshbound(a)

    def refreshbound(self, obj):
        pre = obj.enabled
        obj.enabled = False
        obj.refresh()
        obj.resetCords()
        obj.enabled = pre
        for b in obj.bound_items:
            self.refreshbound(b)

    def getScreen(self):
        sc = pygame.display.get_surface()
        self.screenw = sc.get_width()
        self.screenh = sc.get_height()

    def rendergui(self, screen):
        windowedmenubackings = [a.behind_menu for a in self.windowedmenus]
        self.breakrenderloop = False
        self.animate()
        self.frame_menu = self.active_menu
        for i, a in enumerate(self.automenus):
            if self.frame_menu in a.true_menu:
                a.render(screen)
        for a in self.windowedmenus:
            if self.frame_menu in a.true_menu:
                if pygame.Rect(a.x * a.dir_scale[0], a.y * a.dir_scale[1], a.width * a.scale,
                               a.height * a.scale).collidepoint(self.mpos):
                    self.drawmenu(a.behind_menu, screen)
                else:
                    if a.isolated:
                        self.drawmenu(a.behind_menu, screen)
                        if self.mprs[0] and self.mouseheld[0][1] == self.buttondowntimer:
                            self.menuback()
                    else:
                        self.rendermenu(a.behind_menu, screen)
                a.render(screen)

    def rendermenu(self, menu, screen):
        if f'auto_generate_menu:{menu}' in self.IDs:
            self.IDs[f'auto_generate_menu:{menu}'].render(screen)

    def drawmenu(self, menu, screen):
        if f'auto_generate_menu:{menu}' in self.IDs:
            self.IDs[f'auto_generate_menu:{menu}'].drawallmenu(screen)

    def loadtickdata(self):
        t = time.perf_counter()
        self.deltatime = 60 * (t - self.time_tracker)
        self.time_tracker = t
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
            b[1].force_holding = False

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
                    elif event.key == pygame.K_ESCAPE and self.escape_back:
                        self.menuback()
                    elif event.key == pygame.K_F5:
                        thread = threading.Thread(target=self.refreshall)
                        thread.start()
                    elif event.key == pygame.K_F11 and self.fullscreenable and self.blockf11 < 0:
                        self.togglefullscreen(pygame.display.get_surface())
                    if event.key in self.buttonkeys:
                        for i in self.buttonkeys[event.key]:
                            if self.active_menu in i.menu:
                                i.press()
                                i.force_holding = True
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
                        if a.selected and self.active_menu == a.getMenu():
                            if a.scroll_input(event.y):
                                moved = True
                    if not moved:
                        scrollable = []
                        for a in self.scrollers:
                            if self.active_menu == a.getMenu() and type(a.master[0]) != Textbox:
                                if a.page_height < (a.max_value - a.min_value) and a.getEnabled():
                                    scrollable.append(a)
                        for x in scrollable:
                            x.tempdistancetomouse = Collision.distancetorect(
                                [self.mpos[0] / x.dir_scale[0], self.mpos[1] / x.dir_scale[1]],
                                (x.x, x.y, x.width, x.height))
                            if type(x.master[0]) == ScrollerTable:
                                x.tempdistancetomouse = Collision.distancetorect(
                                    [self.mpos[0] / x.dir_scale[0], self.mpos[1] / x.dir_scale[1]],
                                    (x.master[0].x, x.master[0].y, x.master[0].width, x.master[0].height))
                        scrollable.sort(key=lambda x: x.tempdistancetomouse)
                        for a in scrollable:
                            a.value -= (event.y * min((a.max_value - a.min_value) / 20, self.scroll_limit))
                            a.limitPos()
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
        if self.auto_scale == 'width':
            self.__scaleset__(self.screenw / self.base_screen_size[0])
        else:
            self.__scaleset__(self.screenh / self.base_screen_size[1])
        if self.fullscreen:
            screen = pygame.display.set_mode((self.screenw, self.screenh), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((self.screenw, self.screenh), pygame.RESIZABLE)
        if self.PyUItitle:
            pygame.display.set_icon(self.logo)
        self.blockf11 = 10

    def write(self, screen, x, y, text, size=None, col=None, center=True, font=None,
              bold=False, antialiasing=True, scale=False, centery=-1):

        font = font or self.styleGet("font")
        col = col or self.styleGet("text_col")
        size = size or self.styleGet("text_size")

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

    def rendertext(self, text, size=None, col=None, font=None, bold=False, antialiasing=True, backing_col=(150, 150, 150),
                   imgin=False):
        font = font or self.styleGet("font")
        col = col or self.styleGet("text_col")
        size = size or self.styleGet("text_size")
        if imgin:
            texts, imagenames = self.seperatestring(text)
        else:
            texts = [text]
            imagenames = ['']
        images = []
        textgen = pygame.font.SysFont(font, int(size), bold)
        for a in range(len(texts)):
            if texts[a] != '': images.append(textgen.render(texts[a], antialiasing, col))
            if imagenames[a] != '': images.append(self.rendershape(imagenames[a], size, col, False, backcol=backing_col))
        if len(images) == 0:
            return pygame.Surface((0, textgen.size('\n')[1]))
        else:
            textsurf = pygame.Surface((sum([a.get_width() for a in images]), max([a.get_height() for a in images])))

        textsurf.fill(backing_col)
        xpos = 0
        h = textsurf.get_height()
        for a in images:
            textsurf.blit(a, (xpos, (h - a.get_height()) / 2))
            xpos += a.get_width()
        textsurf.set_colorkey(backing_col)
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

    def addinbuiltimage(self, name, surface):
        self.in_built_images[name] = surface

    def drawtosurf(self, screen, IDlist, surfcol, x, y, displayrect=None, displaymode='render', rounded_corners=0):
        surf = pygame.Surface((self.screenw, self.screenh))
        surf.fill(surfcol)
        surf.set_colorkey(surfcol)
        for a in IDlist:
            if a in self.IDs:
                if displaymode == 'render':
                    self.IDs[a].render(surf)
                else:
                    self.IDs[a].draw(surf)

        Draw.blitrounded_corners(surf, screen, x, y, rounded_corners, pygame.Rect(displayrect))

    def rendertextlined(self, text, size, col=None, backing_col=(150, 150, 150), font=None, width=-1,
                        bold=False, antialiasing=True, center=False, spacing=0, imgin=False, img='', scale='default',
                        linelimit=10000, getcords=False, cutstartspaces=False):
        font = font or self.styleGet('font')
        col = col or self.styleGet('text_col')
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

        imgsurfs = [self.rendershape(imgnames[i], size, col, backcol=backing_col) for i in range(len(imgnames))]

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
                chrwidth = self.gettext_size(linesrealtext[0], font, size, bold, imgin)[0]
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
                    chrwidth = self.gettext_size(linesrealtext[0], font, size, bold, imgin)[0]
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
                                backing_col, imgin, img))
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
        surf.fill(backing_col)
        yinc = 0
        if not center:
            for a in textimages:
                surf.blit(a, (0, yinc))
                yinc += a.get_height() + spacing
        else:
            for a in textimages:
                surf.blit(a, (int(surf.get_width() / 2) - int(a.get_width() / 2), yinc))
                yinc += a.get_height() + spacing
        surf.set_colorkey(backing_col)
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
                    linesize = self.gettext_size(swapped, font, size, bold)
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

    def gettext_size(self, text, font, text_size, bold=False, imgin=True):
        textgen = pygame.font.SysFont(font, int(text_size), bold)
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
                addon = self.rendershape(imgnames[a], text_size, (150, 150, 150), False, (0, 0, 0)).get_size()
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
        if self.id_messages: print('adding:', ID)
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
            self.refreshItems()
        if not type(obj) in [Animation, Menu] and Utils.menuin(obj.true_menu, self.windowedmenunames):
            for b in obj.true_menu:
                if b in self.windowedmenunames:
                    valid = True
                    for a in obj.master:
                        if type(a) in [Button, Textbox, Text, Table, ScrollerTable, Scroller, Slider, Rectangle]:
                            valid = False
                    if valid:
                        self.windowedmenus[self.windowedmenunames.index(b)].bindItem(obj, False, False)

    def setObjectID(self, ID, obj):
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

    def refreshItems(self):
        self.items = self.buttons + self.textboxes + self.tables + self.texts + self.scrollers + self.sliders + self.windowedmenus + self.rects + self.dropdowns + self.windows
        for a in self.items:
            if len(a.master) < len(a.true_menu) or not a.onitem:
                menu = a.true_menu
                for m in menu:
                    if not (m in self.windowedmenunames):
                        if not ('auto_generate_menu:' + m in self.IDs):
                            obj = self.automakemenu(m)
                        else:
                            obj = self.IDs['auto_generate_menu:' + m]
                        obj.bindItem(a, False, False)
        self.items += self.automenus
        self.items.sort(key=lambda x: x.layer, reverse=False)
        self.refreshButtonKeys()

    def refreshButtonKeys(self):
        self.buttonkeys = {}
        for a in self.items:
            for k in a.press_keys:
                if not k in self.buttonkeys: self.buttonkeys[k] = []
                self.buttonkeys[k].append(a)

    def refreshNoClickRects(self):
        self.no_click_rects = []
        for a in self.items:
            a.no_click_rects_applied = []
            a.refreshNoClickRect()
            self.no_click_rects += a.no_click_rect
        # Rect,IDs,menu,whitelist (true=all objects in list blocked by no_click_rect)
        for a in self.no_click_rects:
            objs = self.onmenu(a[2])
            if a[3]:
                for b in objs:
                    if b.ID in a[1]:
                        b.no_click_rects_applied.append(a[0])
            else:
                for b in objs:
                    if not b.ID in a[1]:
                        b.no_click_rects_applied.append(a[0])

    def printTree(self, obj=False):
        if type(obj) == str: obj = self.IDs[obj]
        prefixes = ['<{-=-{=-[=]-=}-=-}>', '#@' * 5, '<=>' * 3, '+=' * 3, '--', '']
        if obj == False:
            depth = max([self.getTreeDepth(a) for a in self.automenus + self.windowedmenus])
            prefixes = prefixes[(6 - depth):]
            for a in self.automenus + self.windowedmenus:
                self.printBound(a, prefixes)
        else:
            prefixes = prefixes[(6 - self.getTreeDepth(obj)):]
            self.printBound(obj, prefixes)

    def printBound(self, obj, prefixes):
        if prefixes[0] == '':
            print(obj.ID)
        else:
            print(prefixes[0], obj.ID)
        for a in obj.bound_items:
            self.printBound(a, prefixes[1:])

    def getTreeDepth(self, obj, depth=1):
        ndepths = [depth]
        if len(obj.bound_items) > 0:
            depth += 1
            ndepths = []
            for a in obj.bound_items:
                ndepths.append(self.getTreeDepth(a, depth))
        return max(ndepths)

    def addObject(self, obj):
        pass

    def makeButton(self, button_obj_params=None, **kwargs):
        obj = Button(
            Utils.generateParamObject(self, ButtonObjParams, button_obj_params, kwargs)
        )
        return obj

    def makeCheckbox(self, x, y, text_size=None, command=Utils.emptyFunction, menu='main', ID='checkbox', text='{tick}', layer=1,
                     rounded_corners=0, bound_items=[], kill_time=-1, width=-1, height=-1,
                     anchor=(0, 0), obj_anchor=(0, 0), center=False, centery=-1, img='none', font=-1, bold=-1,
                     antialiasing=-1, pregenerated=True, enabled=True,
                     border=4, top_border_size=-1, bottom_border_size=-1, right_border_size=-1, left_border_size=-1, scalesize=-1, scale_x=-1,
                     scale_y=-1, scale_by=-1, glow=-1, glow_col=-1,
                     runcommandat=0, col=-1, text_col=-1, backing_col=-1, border_col=-1, hovercol=-1, clickdownsize=-1,
                     clicktype=-1, textoffsetx=-1, textoffsety=-1, maxwidth=-1,
                     dragable=False, colorkey=-1, toggle=True, toggleable=True, toggletext='', toggleimg='none',
                     togglecol=-1, togglehovercol=-1, bindtoggle=[], spacing=-1, verticalspacing=-1,
                     horizontalspacing=-1, clickablerect=-1, clickableborder=10,
                     backing_draw=False, borderdraw=-1, animationspeed=-1, linelimit=1000, refreshbind=[], presskeys=[]):
        text_size = text_size or self.styleGet('text_size')
        if spacing == -1: spacing = -int(text_size / 5)
        if width == -1: width = text_size + spacing * 2
        if height == -1: height = text_size + spacing * 2
        obj = Button(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                     rounded_corners=rounded_corners, bound_items=bound_items, kill_time=kill_time,
                     anchor=anchor, obj_anchor=obj_anchor, center=center, centery=centery, text=text, text_size=text_size,
                     img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                     enabled=enabled,
                     border=border, top_border_size=top_border_size, bottom_border_size=bottom_border_size, right_border_size=right_border_size,
                     left_border_size=left_border_size, scalesize=scalesize, scale_x=scale_x, scale_y=scale_y, scale_by=scale_by,
                     glow=glow, glow_col=glow_col,
                     command=command, runcommandat=runcommandat, col=col, text_col=text_col, backing_col=backing_col,
                     hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype, textoffsetx=textoffsetx,
                     textoffsety=textoffsety, maxwidth=maxwidth,
                     dragable=dragable, colorkey=colorkey, toggle=toggle, toggleable=toggleable, toggletext=toggletext,
                     toggleimg=toggleimg, togglecol=togglecol, togglehovercol=togglehovercol, bindtoggle=bindtoggle,
                     spacing=spacing, verticalspacing=verticalspacing, horizontalspacing=horizontalspacing,
                     clickablerect=clickablerect, clickableborder=clickableborder,
                     animationspeed=animationspeed, backing_draw=backing_draw, borderdraw=borderdraw, linelimit=linelimit,
                     refreshbind=refreshbind, presskeys=presskeys)
        return obj

    def makeTextbox(self, textbox_obj_params: TextboxObjParams = None, **kwargs):
        obj = Textbox(
            Utils.generateParamObject(self, TextboxObjParams, textbox_obj_params, kwargs)
        )
        return obj

    def makeTable(self, table_obj_params: TableObjParams = None, **kwargs):
        obj = Table(
            Utils.generateParamObject(self, TableObjParams, table_obj_params, kwargs)
        )
        return obj

    def makeText(self, text_obj_params: TextObjParams = None, **kwargs):
        obj = Text(
            Utils.generateParamObject(self, TextObjParams, text_obj_params, kwargs)
        )
        return obj

    def makeScroller(self, scroller_obj_params: ScrollerObjParams = None, **kwargs):
        obj = Scroller(
            Utils.generateParamObject(self, ScrollerObjParams, scroller_obj_params, kwargs)
        )
        return obj

    def makeSlider(self, slider_obj_params: SliderObjParams = None, **kwargs):
        obj = Slider(
            Utils.generateParamObject(self, SliderObjParams, slider_obj_params, kwargs)
        )
        return obj

    def makeWindow(self, window_obj_params: WindowObjParams = None, **kwargs):
        obj = Window(
            Utils.generateParamObject(self, WindowObjParams, window_obj_params, kwargs)
        )
        return obj

    def makeRect(self, rect_obj_params: RectangleObjParams = None, **kwargs):
        obj = Rectangle(
            Utils.generateParamObject(self, RectangleObjParams, rect_obj_params, kwargs)
        )
        return obj

    def makecircle(self, x, y, radius, command=Utils.emptyFunction, menu='main', ID='button', layer=1, rounded_corners=-1,
                   bound_items=[], kill_time=-1,
                   anchor=(0, 0), obj_anchor=(0, 0), center=-1, centery=-1, enabled=True,
                   border=-1, scalesize=-1, scale_x=-1, scale_y=-1, scale_by=-1, glow=-1, glow_col=-1,
                   runcommandat=0, col=-1, dragable=False, backing_draw=-1, refreshbind=[]):
        if rounded_corners == -1: rounded_corners = radius
        obj = self.makerect(x=x, y=y, width=radius * 2, height=radius * 2, command=command, menu=menu, ID=ID,
                            layer=layer, rounded_corners=rounded_corners, bound_items=bound_items, kill_time=kill_time,
                            anchor=anchor, obj_anchor=obj_anchor, center=center, centery=centery, enabled=enabled,
                            border=border, scalesize=scalesize, scale_x=scale_x, scale_y=scale_y, scale_by=scale_by,
                            glow=glow, glow_col=glow_col,
                            runcommandat=runcommandat, col=col, dragable=dragable, backing_draw=backing_draw,
                            refreshbind=refreshbind)
        return obj

    def makesearchbar(self, x, y, text='Search', width=400, lines=1, menu='main', command=Utils.emptyFunction, ID='searchbar',
                      layer=1, rounded_corners=-1, bound_items=[], kill_time=-1, height=-1,
                      anchor=(0, 0), obj_anchor=(0, 0), center=-1, centery=-1, img='none', text_size=-1, font=-1, bold=-1,
                      antialiasing=-1, pregenerated=True, enabled=True,
                      border=3, top_border_size=-1, bottom_border_size=-1, scalesize=-1, scale_x=-1, scale_y=-1, scale_by=-1, glow=0,
                      glow_col=-1,
                      runcommandat=0, col=-1, text_col=-1, titletext_col=-1, backing_col=-1, hovercol=-1, clickdownsize=-1,
                      clicktype=0, textoffsetx=-1, textoffsety=-1,
                      colorkey=-1, spacing=-1, verticalspacing=2, horizontalspacing=4, clickablerect=-1,
                      attachscroller=True, intscroller=False, minint=-math.inf, maxint=math.inf, intwraparound=False,
                      linelimit=100, selectcol=-1, selectbordersize=2, selectshrinksize=0, cursorsize=-1, textcenter=-1,
                      chrlimit=10000, numsonly=False, enterreturns=False, commandifenter=True, commandifkey=False,
                      imgdisplay=-1, allowedcharacters='',
                      backing_draw=-1, borderdraw=-1, refreshbind=[]):

        if titletext_col == -1: titletext_col = text_col
        if top_border_size == -1: top_border_size = border
        if bottom_border_size == -1: bottom_border_size = border
        if text_size == -1: text_size = self.styleGet("text_size")
        if height == -1:
            heightgetter = self.rendertext('Tg', text_size, (255, 255, 255), font, bold)
            height = top_border_size + bottom_border_size + heightgetter.get_height() * lines + verticalspacing * 2
        col = ColEdit.autoShiftCol(col, self.styleGet("backing_col"))
        if backing_col == -1: backing_col = ColEdit.autoShiftCol(self.styleGet("backing_col"), col, 20)

        txt = self.maketext(int(border + horizontalspacing) / 2, 0, text, text_size, anchor=(0, 'h/2'),
                            obj_anchor=(0, 'h/2'), img=img, font=font, bold=bold, antialiasing=antialiasing,
                            pregenerated=pregenerated, enabled=enabled, text_col=titletext_col,
                            col=ColEdit.autoShiftCol(backing_col, col, -20), animationspeed=5)

        bsize = height - top_border_size - bottom_border_size
        search = self.makeButton(-border * 2 - bsize, 0, '{search}', text_size * 0.55, command=command,
                                 rounded_corners=rounded_corners, width=bsize, height=bsize,
                                 anchor=('w', 'h/2'), obj_anchor=('w', 'h/2'), border=0, col=col, text_col=text_col,
                                 backing_col=backing_col, border_col=col,
                                 clickdownsize=1, textoffsetx=0, textoffsety=0, spacing=2, clickablerect=clickablerect,
                                 hovercol=ColEdit.autoShiftCol(hovercol, col, -6), borderdraw=False)
        cross = self.makeButton(-border, 0, '{cross}', text_size * 0.5, command=Utils.emptyFunction,
                                rounded_corners=rounded_corners, width=bsize, height=bsize,
                                anchor=('w', 'h/2'), obj_anchor=('w', 'h/2'), border=0, col=col, text_col=text_col,
                                backing_col=backing_col, border_col=col,
                                clickdownsize=1, textoffsetx=1, textoffsety=1, spacing=2, clickablerect=clickablerect,
                                hovercol=ColEdit.autoShiftCol(hovercol, col, -6), borderdraw=False)

        obj = self.makeTextbox(x, y, '', width, lines, menu, command, ID, layer, rounded_corners,
                               bound_items + [txt, search, cross], kill_time, height,
                               anchor, obj_anchor, center, centery, img, text_size, font, bold, antialiasing,
                               pregenerated, enabled,
                               border, top_border_size, bottom_border_size, bsize * 2 + border * 3,
                               txt.textimage.get_width() + border + horizontalspacing * 2, scalesize, scale_x, scale_y,
                               scale_by, glow, glow_col,
                               runcommandat, col, text_col, backing_col, hovercol, clickdownsize, clicktype, textoffsetx,
                               textoffsety,
                               colorkey, spacing, verticalspacing, horizontalspacing, clickablerect, attachscroller,
                               intscroller, minint, maxint, intwraparound,
                               linelimit, selectcol, selectbordersize, selectshrinksize, cursorsize, textcenter,
                               chrlimit, numsonly, enterreturns, commandifenter, commandifkey, imgdisplay,
                               allowedcharacters,
                               backing_draw, borderdraw, refreshbind)

        cross.command = lambda: obj.setText('')
        return obj

    def makescrollertable(self, x, y, data=[], titles=[], menu='main', ID='scrollertable', layer=1, rounded_corners=-1,
                          bound_items=[], kill_time=-1, width=-1, height=-1,
                          anchor=(0, 0), obj_anchor=(0, 0), center=-1, centery=-1, text='', text_size=-1, img='none',
                          font=-1, bold=-1, antialiasing=-1, pregenerated=True, enabled=True,
                          border=3, top_border_size=-1, bottom_border_size=-1, right_border_size=-1, left_border_size=-1, scalesize=-1,
                          scale_x=-1, scale_y=-1, scale_by=-1, glow=-1, glow_col=-1,
                          command=Utils.emptyFunction, runcommandat=0, col=-1, text_col=-1, backing_col=-1, hovercol=-1,
                          clickdownsize=4, clicktype=0, textoffsetx=-1, textoffsety=-1,
                          dragable=False, colorkey=-1, spacing=-1, verticalspacing=-1, horizontalspacing=-1,
                          clickablerect=(0, 0, 'w', 'h'),
                          boxwidth=-1, boxheight=-1, linesize=2, textcenter=-1, guesswidth=-1, guessheight=-1,
                          backing_draw=-1, borderdraw=-1, pageheight=-1, refreshbind=[], compress=True, scrollerwidth=15,
                          screencompressed=5):

        if col == -1: col = self.styleGet("Table_backing_col")
        if backing_col == -1: backing_col = ColEdit.autoShiftCol(self.styleGet("Table_backing_col"), col, -20)

        obj = ScrollerTable(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                            rounded_corners=rounded_corners, bound_items=bound_items, kill_time=kill_time,
                            anchor=anchor, obj_anchor=obj_anchor, center=center, centery=centery, text=text,
                            text_size=text_size, img=img, font=font, bold=bold, antialiasing=antialiasing,
                            pregenerated=pregenerated, enabled=enabled,
                            border=border, top_border_size=top_border_size, bottom_border_size=bottom_border_size, right_border_size=right_border_size,
                            left_border_size=left_border_size, scalesize=scalesize, scale_x=scale_x, scale_y=scale_y, scale_by=scale_by,
                            glow=glow, glow_col=glow_col,
                            command=command, runcommandat=runcommandat, col=col, text_col=text_col, backing_col=backing_col,
                            hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype,
                            textoffsetx=textoffsetx, textoffsety=textoffsety,
                            colorkey=colorkey, spacing=spacing, verticalspacing=verticalspacing,
                            horizontalspacing=horizontalspacing, clickablerect=clickablerect,
                            data=data, titles=titles, boxwidth=boxwidth, boxheight=boxheight, linesize=linesize,
                            textcenter=textcenter, guesswidth=guesswidth, guessheight=guessheight,
                            backing_draw=backing_draw, borderdraw=borderdraw, refreshbind=refreshbind,
                            scroller=Utils.EmptyObject(0, 0, 15, 15), compress=compress)
        if len(titles) != 0 and clickablerect == (0, 0, 'w', 'h'):
            obj.start_clickable_rect = (
            0, f'(ui.IDs["{obj.ID}"].boxheights[0]+ui.IDs["{obj.ID}"].linesize*2)*ui.IDs["{obj.ID}"].scale', 'w',
            f'h-(ui.IDs["{obj.ID}"].boxheights[0]-ui.IDs["{obj.ID}"].linesize*2)')
        if pageheight == -1:
            pageheight = self.IDs[obj.ID].height
        obj.start_page_height = pageheight
        obj.autoScale()
        scroller = self.makescroller(x=border, y=0, width=scrollerwidth, height=f'ui.IDs["{obj.ID}"].pageheight',
                                     menu=menu, ID=obj.ID + 'scroller', layer=layer, rounded_corners=rounded_corners,
                                     bound_items=bound_items, kill_time=kill_time,
                                     anchor=('w', 0), obj_anchor=(0, 0), enabled=enabled,
                                     border=border, top_border_size=top_border_size, bottom_border_size=bottom_border_size,
                                     right_border_size=right_border_size, left_border_size=left_border_size, scalesize=scalesize, scale_x=scale_x,
                                     scale_y=scale_y, scale_by=scale_by, glow=glow, glow_col=glow_col,
                                     col=col, backing_col=backing_col, clicktype=clicktype,
                                     backing_draw=backing_draw, borderdraw=borderdraw, clickablerect=-1, scrollbind=[],
                                     screencompressed=screencompressed,
                                     increment=0, minp=0, maxp=f"ui.IDs['{obj.ID}'].height", startp=0,
                                     pageheight=f'ui.IDs["{obj.ID}"].pageheight')
        scroller.command = lambda: obj.scrollerblocks(scroller)
        obj.refresh_bind.append(scroller.ID)
        obj.bindItem(scroller)
        obj.scroller = scroller
        scroller.resetCords()
        return obj

    def makedropdown(self, x, y, options: list, text_size=-1, command=Utils.emptyFunction, menu='main', ID='dropdown', layer=1,
                     rounded_corners=-1, bound_items=[], kill_time=-1, width=-1, height=-1,
                     anchor=(0, 0), obj_anchor=(0, 0), center=-1, centery=-1, img='none', font=-1, bold=-1,
                     antialiasing=-1, pregenerated=True, enabled=True, pageheight=300,
                     border=3, top_border_size=-1, bottom_border_size=-1, right_border_size=-1, left_border_size=-1, scalesize=-1, scale_x=-1,
                     scale_y=-1, scale_by=-1, glow=-1, glow_col=-1,
                     runcommandat=0, col=-1, text_col=-1, backing_col=-1, border_col=-1, hovercol=-1, clickdownsize=-1,
                     clicktype=-1, textoffsetx=-1, textoffsety=-1, maxwidth=-1,
                     dragable=False, colorkey=-1, toggle=True, toggleable=False, toggletext=-1, toggleimg='none',
                     togglecol=-1, togglehovercol=-1, bindtoggle=[], spacing=-1, verticalspacing=1, horizontalspacing=4,
                     clickablerect=-1, clickableborder=-1,
                     backing_draw=-1, borderdraw=-1, linelimit=1000, refreshbind=[], animationspeed=15,
                     animationtype='compressleft', startoptionindex=0, dropsdown=True):

        if options == []: options = ['text']
        text = options[startoptionindex]
        if text_size == -1: text_size = self.styleGet("text_size")

        if top_border_size == -1: top_border_size = border
        if bottom_border_size == -1: bottom_border_size = border
        if left_border_size == -1: left_border_size = border
        if right_border_size == -1: right_border_size = border
        if height == -1:
            heightgetter = self.rendertext('Tg', text_size, (255, 255, 255), font, bold)
            height = top_border_size + bottom_border_size + heightgetter.get_height()
        col = ColEdit.autoShiftCol(col, self.styleGet(""))
        if dropsdown:
            txt = [self.maketext(int(border + horizontalspacing) / 2, 0, text, text_size, anchor=(0, 'h/2'),
                                 obj_anchor=(0, 'h/2'),
                                 img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                                 enabled=enabled, text_col=text_col, col=ColEdit.autoShiftCol(backing_col, col, 20),
                                 animationspeed=5, rounded_corners=rounded_corners)]
            text = '{more scale=0.3}'
            if width == -1:
                lborder = txt[0].textimage.get_width() + border + horizontalspacing * 2
                wid = -1
            else:
                lborder = width - text_size + border
        else:
            txt = []
            lborder = left_border_size
            wid = width

        obj = DropDown(ui=self, x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                       rounded_corners=rounded_corners, bound_items=txt + bound_items, kill_time=kill_time,
                       anchor=anchor, obj_anchor=obj_anchor, center=center, centery=centery, text=text, text_size=text_size,
                       img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                       enabled=enabled,
                       border=border, top_border_size=top_border_size, bottom_border_size=bottom_border_size, right_border_size=right_border_size,
                       left_border_size=lborder, scalesize=scalesize, scale_x=scale_x, scale_y=scale_y, scale_by=scale_by,
                       glow=glow, glow_col=glow_col,
                       command=command, runcommandat=runcommandat, col=col, text_col=text_col, backing_col=backing_col,
                       hovercol=hovercol, clickdownsize=clickdownsize, clicktype=clicktype, textoffsetx=textoffsetx,
                       textoffsety=textoffsety, maxwidth=maxwidth,
                       dragable=dragable, colorkey=colorkey, toggle=toggle, toggleable=toggleable,
                       toggletext=toggletext, toggleimg=toggleimg, togglecol=togglecol, togglehovercol=togglehovercol,
                       bindtoggle=bindtoggle, spacing=spacing,
                       verticalspacing=verticalspacing, horizontalspacing=horizontalspacing,
                       clickablerect=clickablerect, clickableborder=clickableborder,
                       animationspeed=animationspeed, backing_draw=backing_draw, borderdraw=borderdraw,
                       linelimit=linelimit, refreshbind=refreshbind, options=options, startoptionindex=startoptionindex,
                       dropsdown=dropsdown)
        obj.init_height = height
        tablew = width
        if tablew != -1: tablew -= border * 2

        if dropsdown:

            table = self.makescrollertable(border, border, [], pageheight=pageheight, rounded_corners=rounded_corners,
                                           text_size=text_size, font=font, bold=bold, border=border, scalesize=scalesize,
                                           col=col, text_col=text_col, backing_col=backing_col, width=tablew)
            obj.table = table
            obj.refreshoptions()

            window = self.makewindow(0, obj.height, f'ui.IDs["{obj.ID}"].width',
                                     f'ui.IDs["{table.ID}"].getheight()+{border}*2', menu=menu, enabled=False,
                                     animationspeed=animationspeed, animationtype=animationtype)
            obj.bindItem(window)
            window.bindItem(table)
            if width == -1:
                nwidth = (max([a[0].textimage.get_width() for a in table.table]) + (
                            obj.width - obj.left_border_size - obj.right_border_size) + border * 5)
            else:
                nwidth = width
            obj.left_border_size += nwidth - obj.width
            obj.refresh()
            obj.init_width = obj.width
            table.startwidth = nwidth - border * 2
            table.refresh()
            window.refresh()
            obj.window = window
            obj.titletext = txt[0]
        else:
            temp_texts = [self.rendertext(t, text_size, font=font, imgin=True) for t in options]
            if width == -1:
                nwidth = (max([t.get_width() for t in temp_texts]) + left_border_size + right_border_size + horizontalspacing * 2)
            else:
                nwidth = width
            obj.start_width = nwidth
            obj.refresh()
            obj.init_width = nwidth

        obj.command = lambda: obj.mainbuttonclicked()
        obj.truecommand = command
        return obj

    def makelabeledcheckbox(self, x, y, text, text_size=-1, command=Utils.emptyFunction, menu='main', ID='checkbox',
                            textpos='left', layer=1, rounded_corners=0, bound_items=[], kill_time=-1, width=-1, height=-1,
                            anchor=(0, 0), obj_anchor=(0, 0), center=False, centery=-1, img='none', font=-1, bold=-1,
                            antialiasing=-1, pregenerated=True, enabled=True,
                            border=4, top_border_size=-1, bottom_border_size=-1, right_border_size=-1, left_border_size=-1, scalesize=-1,
                            scale_x=-1, scale_y=-1, scale_by=-1, glow=-1, glow_col=-1,
                            runcommandat=0, col=-1, text_col=-1, backing_col=-1, border_col=-1, hovercol=-1,
                            clickdownsize=-1, clicktype=-1, textoffsetx=-1, textoffsety=-1, maxwidth=-1,
                            dragable=False, colorkey=-1, toggle=True, toggleable=True, toggleimg='none', togglecol=-1,
                            togglehovercol=-1, bindtoggle=[], spacing=-1, horizontalspacing=5, clickablerect=-1,
                            clickableborder=10,
                            backing_draw=False, borderdraw=-1, animationspeed=-1, linelimit=1000, refreshbind=[]):

        if text_size == -1: text_size = self.styleGet("text_size")

        if textpos == 'left':
            anch = (0, 'h/2')
            objanch = ('w', 'h/2')
            tx = -horizontalspacing
        else:
            anch = ('w', 'h/2')
            objanch = (0, 'h/2')
            tx = horizontalspacing
        text = self.maketext(tx, 0, text, text_size, menu, ID=ID + 'text',
                             anchor=anch, obj_anchor=objanch, font=font, bold=bold, antialiasing=antialiasing,
                             pregenerated=pregenerated, enabled=enabled,
                             scalesize=scalesize, scale_x=scale_x, scale_y=scale_y, scale_by=scale_by,
                             col=col, text_col=text_col, backing_col=backing_col, textoffsetx=textoffsetx,
                             textoffsety=textoffsety,
                             colorkey=colorkey, maxwidth=maxwidth, animationspeed=animationspeed)

        obj = self.makeCheckbox(x=x, y=y, width=width, height=height, menu=menu, ID=ID, layer=layer,
                                rounded_corners=rounded_corners, bound_items=bound_items + [text], kill_time=kill_time,
                                anchor=anchor, obj_anchor=obj_anchor, center=center, centery=centery, text_size=text_size,
                                img=img, font=font, bold=bold, antialiasing=antialiasing, pregenerated=pregenerated,
                                enabled=enabled,
                                border=border, top_border_size=top_border_size, bottom_border_size=bottom_border_size,
                                right_border_size=right_border_size, left_border_size=left_border_size, scalesize=scalesize, scale_x=scale_x,
                                scale_y=scale_y, scale_by=scale_by, glow=glow, glow_col=glow_col,
                                command=command, runcommandat=runcommandat, col=col, text_col=text_col,
                                backing_col=border_col, hovercol=hovercol, clickdownsize=clickdownsize,
                                clicktype=clicktype, textoffsetx=textoffsetx, textoffsety=textoffsety,
                                maxwidth=maxwidth,
                                dragable=dragable, colorkey=colorkey, toggle=toggle, toggleable=toggleable,
                                toggleimg=toggleimg, togglecol=togglecol, togglehovercol=togglehovercol,
                                bindtoggle=bindtoggle,
                                spacing=spacing, clickablerect=clickablerect, clickableborder=clickableborder,
                                animationspeed=animationspeed, backing_draw=backing_draw, borderdraw=borderdraw,
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
            length = self.styleGet("animation_speed")
        if menu:
            for a in self.automenus:
                if (animateID in a.true_menu):
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
            length = self.styleGet("animation_speed")
        if self.queuedmenumove[0] < 0 or slide == 'none':
            if (self.active_menu in self.windowedmenunames) and (moveto == self.active_menu) and (
                    self.queuedmenumove[0] < 0):
                if slide != 'none':
                    self.menuback(slide + ' flip', length)
                else:
                    self.menuback()
            else:
                if backchainadd:
                    self.backchain.append([self.active_menu, slide, length])
                if slide == 'none':
                    self.active_menu = moveto
                else:
                    self.slidemenu(self.active_menu, moveto, slide, length)
            for a in self.mouseheld:
                a[1] -= 1
        elif self.queue_menu_move:
            if ['move', moveto, slide, length] != self.prevmenumove:
                self.queuedmenumove[1] = ['move', moveto, slide, length]
            self.prevmenumove = self.queuedmenumove[1]

    def menuback(self, slide='none', length='default'):
        if len(self.backchain) > 0:
            if slide == 'none' and self.backchain[-1][1] != 'none':
                if not (self.active_menu in self.windowedmenunames and self.backchain[-1][0] in self.windowedmenunames):
                    slide = self.backchain[-1][1] + ' flip'
                else:
                    slide = self.backchain[-1][1]
            length = self.backchain[-1][2]
        if length == 'default':
            length = self.styleGet("animation_speed")
        if self.queuedmenumove[0] < 0 or slide == 'none':
            if len(self.backchain) > 0:
                if slide == 'none':
                    self.active_menu = self.backchain[-1][0]
                else:
                    self.slidemenu(self.active_menu, self.backchain[-1][0], slide, length)
                del self.backchain[-1]
            elif self.back_quits and self.queuedmenumove[0] < 0:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            for a in self.mouseheld:
                a[1] -= 1
        elif self.queue_menu_move:
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
            if menuto == self.windowedmenus[self.windowedmenunames.index(menufrom)].behind_menu:
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
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].behind_menu, 'current',
                                       dirr, 'sinout', length, command=lambda: self.slidemenuin(menuto, length, dirr),
                                       runcommandat=length, queued=False, menu=True, relativemove=True)
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].behind_menu, 'current',
                                       [dirr[0] * -1, dirr[1] * -1], 'linear', 1, menu=True, relativemove=True)
        elif menuto in self.windowedmenunames:
            if menufrom == self.windowedmenus[self.windowedmenunames.index(menuto)].behind_menu:
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menuto)].ID,
                                   [dirr[0] * -1, dirr[1] * -1], 'current', 'sinin', length,
                                   command=self.finishmenumove, runcommandat=length, queued=True, relativemove=True,
                                   skiptoscreen=True)
                self.movemenu(menuto, backchainadd=False)
            else:
                self.makeanimation(menufrom, 'current', dirr, 'sinout', length, command=lambda: self.slidemenuin(
                    self.windowedmenus[self.windowedmenunames.index(menuto)].behind_menu, length, dirr, menuto),
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
                self.IDs[ID].master[0].bound_items.remove(self.IDs[ID])
            delids = [a.ID for a in self.IDs[ID].bound_items]
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
            self.refreshItems()
            return True
        except Exception as e:
            if failmessage: print('Failed to delete object:', ID, 'Error:', e)
            return False

    def onmenu(self, menu):
        lis = []
        for b in self.items:
            if b.getMenu() == menu:
                lis.append(b)
        return lis
