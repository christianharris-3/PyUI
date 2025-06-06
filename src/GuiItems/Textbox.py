import pygame
from src.GuiItems.GuiItem import GuiItem
from src.Utils.Utils import Utils
from src.Utils.Draw import Draw


class Textbox(GuiItem):
    def reset(self):
        self.setvars()
        self.autoscale()
        self.resetcords()
        self.resetscroller()
        self.refreshscale()
        self.gentext(False)
        self.refreshcursor()
        self.refreshscroller()
        self.refreshcords()
        self.refreshglow()
        self.resetcords()

    def setvars(self):
        self.scroller = 0
        self.selected = False
        self.textselected = [False, 0, 0]
        self.clickstartedinbound = False
        self.typingcursor = 0
        self.typeline = 0
        self.scrolleron = False
        self.slider = -1
        self.previntscrollerhoff = 0
        self.undochain = [(self.text, self.typingcursor)]

    def child_autoscale(self):
        heightgetter = self.ui.rendertext('Tg', self.textsize, self.textcol, self.font, self.bold)
        if self.height == -1:
            self.startheight = self.upperborder + self.lowerborder + heightgetter.get_height() * self.lines + self.verticalspacing * 2
            self.init_height = self.startheight
            self.height = self.startheight
        if self.cursorsize == -1:
            self.cursorsize = self.ui.gettextsize('Tg', self.font, self.textsize, self.bold)[1] - 2

    def select(self):
        for a in self.ui.textboxes:
            a.selected = False
        self.ui.selectedtextbox = self.ui.textboxes.index(self)
        self.selected = True

    def undo(self, refresh=True):
        while self.undochain[-1][0] == self.text:
            del self.undochain[-1]
        self.text = self.undochain[-1][0]
        self.typingcursor = self.undochain[-1][1]
        if refresh:
            self.refresh()

    def scroll_input(self, scroll_size):
        if self.scrolleron and self.attachscroller:
            if self.pageheight < (self.maxp - self.minp):
                self.scroller.scroll -= (
                            scroll_size * min((self.scroller.maxp - self.scroller.minp) / 20, self.ui.scrolllimit))
                self.scroller.limitpos()
                self.scroller.command()
                return True
        elif self.intscroller:
            return self.change_textnum(scroll_size)
        return False

    def change_textnum(self, change, refresh=True, wraparound=True):
        try:
            if '.' in self.text:
                val = float(self.text)
            else:
                val = int(self.text)
        except Exception as e:
            return False
        val += change
        if self.intwraparound and wraparound:
            val = (val - self.minp) % (self.maxp - self.minp + 1) + self.minp
        else:
            if val < self.minp:
                val = self.minp
            elif val > self.maxp:
                val = self.maxp

        self.text = str(round(val, 14))
        if refresh: self.refresh()
        return True

    def settext(self, text=''):
        self.text = text
        self.refresh()

    def inputkey(self, caps, event, kprs):
        starttext = self.text
        if kprs[pygame.K_LSHIFT] or kprs[pygame.K_RSHIFT]:
            if caps:
                caps = False
            else:
                caps = True
        if kprs[pygame.K_LCTRL] or kprs[pygame.K_RCTRL]:
            ctrl = True
        else:
            ctrl = False
        if self.textselected[1] > self.textselected[2]:
            temp = self.textselected[1]
            self.textselected[1] = self.textselected[2]
            self.textselected[2] = temp
        item = ''
        backspace = False
        delete = False
        esc = False
        enter = False
        unicodechrs = '''#',-./0123456789;=[\\]`'''
        shiftunicodechrs = '''~@<_>?)!"£$%^&*(:+{|}¬'''
        if event.key > 32 and event.key < 127:
            if ctrl:
                if chr(event.key) == 'a':
                    self.textselected = [True, 0, len(self.chrcorddata)]
                elif chr(event.key) == 'x':
                    delete = True
                elif chr(event.key) == 'z':
                    if len(self.undochain) > 1:
                        self.undo(False)
                        del self.undochain[-1]
                elif chr(event.key) == 'c':
                    pygame.scrap.put('text/plain;charset=utf-8', self.text.encode())
                elif chr(event.key) == 'v':
                    clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if clipboard == None:
                        clipboard = pygame.scrap.get(pygame.scrap.get_types()[0])
                    clipboard = clipboard.decode().strip('\x00')
                    item = clipboard
            else:
                if (event.key > 96 and event.key < 123):
                    if caps:
                        item = chr(event.key - 32)
                    else:
                        item = chr(event.key)
                elif chr(event.key) in unicodechrs:
                    if not (kprs[pygame.K_LSHIFT] or kprs[pygame.K_RSHIFT]):
                        item = chr(event.key)
                    else:
                        item = shiftunicodechrs[list(unicodechrs).index(chr(event.key))]
        elif event.key == pygame.K_BACKSPACE:
            backspace = True
        elif event.key == pygame.K_DELETE:
            delete = True
        elif event.key == pygame.K_ESCAPE:
            self.selected = False
        elif event.key == pygame.K_RETURN:
            if self.enterreturns: item = '\n'
            if self.commandifenter: self.command()
        elif event.key == pygame.K_SPACE:
            item = ' '
        elif event.key == pygame.K_LEFT:
            if self.typingcursor > -1:
                prev = self.chrcorddata[self.typingcursor][1]
                while self.chrcorddata[self.typingcursor][1] == prev:
                    if self.typingcursor > -1:
                        self.typingcursor -= 1
                    else:
                        break
        elif event.key == pygame.K_RIGHT:
            if len(self.chrcorddata) > 0:
                if self.typingcursor < len(self.chrcorddata) - 1:
                    prev = self.chrcorddata[self.typingcursor + 1][1]
                    start = self.typingcursor
                    while self.chrcorddata[self.typingcursor + 1][1] == prev:
                        if self.typingcursor < len(self.chrcorddata) - 1:
                            self.typingcursor += 1
                        else:
                            break
                        if self.typingcursor > len(self.chrcorddata) - 3:
                            break
                    if self.typingcursor - start > 1: self.typingcursor += 1
        elif event.key == pygame.K_UP:
            self.typingcursor = self.findclickloc(
                relativempos=[self.linecenter[0], self.linecenter[1] - self.cursorsize])
        elif event.key == pygame.K_DOWN:
            self.typingcursor = self.findclickloc(
                relativempos=[self.linecenter[0], self.linecenter[1] + self.cursorsize])

        if not (self.textselected[0] and self.textselected[1] != self.textselected[2]):
            if item != '':
                if self.allowedcharacters != '':
                    newitem = ''
                    for i in item:
                        if i in self.allowedcharacters:
                            newitem += i
                    item = newitem
                try:
                    temp = float(self.text[:self.typingcursor + 1] + item + self.text[self.typingcursor + 1:])
                    num = True
                except:
                    num = False
                if (not (self.numsonly) or num):
                    self.text = self.text[:self.typingcursor + 1] + item + self.text[self.typingcursor + 1:]
                    self.typingcursor += len(item)
                    self.change_textnum(0, False, False)
            if backspace:
                if self.typingcursor > -1:
                    self.typingcursor -= 1
                if self.text[self.typingcursor:self.typingcursor + 2] == '\n':
                    self.text = self.text[:self.typingcursor] + self.text[self.typingcursor + 2:]
                    self.typingcursor -= 1
                else:
                    self.text = self.text[:self.typingcursor + 1] + self.text[self.typingcursor + 2:]
            elif delete:
                if self.text[self.typingcursor:self.typingcursor + 2] == '\n':
                    self.text = self.text[:self.typingcursor] + self.text[self.typingcursor + 2:]
                else:
                    self.text = self.text[:self.typingcursor + 1] + self.text[self.typingcursor + 2:]
            if self.commandifkey and (item != '' or backspace or delete):
                self.command()
        else:
            if backspace or delete or item != '':
                self.text = self.text[:self.textselected[1]] + item + self.text[self.textselected[2]:]
                self.typingcursor = self.textselected[1] - 1 + len(item)
                self.textselected = [False, 0, 0]
        if self.text[self.chrlimit - 1:self.chrlimit + 1] == '\n':
            self.text = self.text[:self.chrlimit - 1]
        else:
            self.text = self.text[:self.chrlimit]
        if self.text != starttext:
            self.refresh()
            self.updateslider()
        else:
            self.refreshcursor()
        self.undochain.append((self.text, self.typingcursor))

    def resetscroller(self):
        self.scroll = 0
        if self.attachscroller:
            if self.scroller != 0:
                self.bounditems.remove(self.scroller)
                self.ui.delete(self.scroller.ID, False)

            self.scroller = self.ui.makescroller(-self.rightborder - 15 + self.border / 2, self.upperborder,
                                                 self.height - self.upperborder - self.lowerborder, Utils.emptyFunction, 15,
                                                 0, self.height - self.upperborder - self.lowerborder, self.height,
                                                 anchor=('w', 0),
                                                 menu=self.menu, roundedcorners=self.roundedcorners, col=self.col,
                                                 scalesize=self.scalesize, scaley=self.scalesize, scalex=self.scalesize,
                                                 scaleby=self.scaleby)
            self.binditem(self.scroller)
        else:
            self.scroller = Utils.EmptyObject(0, 0, 0, 0)

    def updateslider(self):
        if self.slider != -1:
            try:
                self.slider.slider = int(self.text)
                self.slider.limitpos()
                self.slider.updatetext()
            except:
                pass

    def refresh(self):
        self.refreshscale()
        self.gentext()
        self.refreshcursor()

        if self.attachscroller:
            self.refreshscroller()
            self.scroller.setmaxp((self.textimage.get_height()) / self.scale + self.verticalspacing * 2 - 1)
            self.scroller.setheight(self.height - self.upperborder - self.lowerborder)
            self.scroller.setpageheight(self.height - self.upperborder - self.lowerborder)
            self.scroller.menu = self.menu
            self.scroller.scalesize = self.scalesize
            self.scroller.scalex = self.scalesize
            self.scroller.scaley = self.scalesize
            self.scroller.refresh()
            if (self.scroller.maxp - self.scroller.minp) > self.scroller.pageheight:
                self.scrolleron = True
                if self.scroller.scroll > self.scroller.maxp - self.scroller.pageheight:
                    self.scroller.scroll = self.scroller.maxp - self.scroller.pageheight
            else:
                self.scrolleron = False
            self.scroller.refresh()

        self.resetcords()
        self.refreshglow()
        self.refreshbound()

    def gentext(self, refcurse=True):
        self.textimage, self.chrcorddatalined = self.ui.rendertextlined(self.text, self.textsize, self.textcol,
                                                                        self.col, self.font,
                                                                        self.width - self.horizontalspacing * 2 - self.leftborder - self.rightborder - self.scrolleron * self.scroller.width,
                                                                        self.bold, center=self.textcenter,
                                                                        scale=self.scale, linelimit=self.linelimit,
                                                                        getcords=True, imgin=self.imgdisplay)
        for l in self.chrcorddatalined:
            for a in l:
                a[1] = (a[1][0] / self.scale, a[1][1] / self.scale)
                a[2] = (a[2][0] / self.scale, a[2][1] / self.scale)
        self.chrcorddata = []
        for a in self.chrcorddatalined:
            self.chrcorddata += a
        self.textimagerect = self.textimage.get_rect()
        self.textimagerect.width /= self.ui.scale
        self.textimagerect.height /= self.ui.scale
        if refcurse: self.refreshcursor()

        if len(self.chrcorddata) < len(self.text):
            self.undo()

    def refreshcursor(self):
        if self.typingcursor > len(self.chrcorddata) - 1:
            self.typingcursor = len(self.chrcorddata) - 1
        elif self.typingcursor < -1:
            self.typingcursor = -1
        if self.typingcursor != -1:
            self.linecenter = [self.chrcorddata[self.typingcursor][1][0] + self.chrcorddata[self.typingcursor][2][
                0] / 2 + self.horizontalspacing, self.chrcorddata[self.typingcursor][1][1]]
        elif len(self.chrcorddata) > 0:
            self.linecenter = [
                self.chrcorddata[self.typingcursor + 1][1][0] - self.chrcorddata[self.typingcursor + 1][2][
                    0] / 2 + self.horizontalspacing, self.chrcorddata[self.typingcursor + 1][1][1]]
        else:
            if self.textcenter:
                self.linecenter = [self.width / 2 - self.leftborder, self.textsize * 0.3]
            else:
                self.linecenter = [self.horizontalspacing, self.textsize * 0.3]
        if self.textselected[1] > len(self.chrcorddata):
            self.textselected[1] = len(self.chrcorddata)
        elif self.textselected[1] < 0:
            self.textselected[1] = 0
        if self.textselected[2] > len(self.chrcorddata):
            self.textselected[2] = len(self.chrcorddata)
        elif self.textselected[2] < 0:
            self.textselected[2] = 0

    def refreshscroller(self):
        if self.attachscroller:
            self.scroller.setheight(self.height - self.upperborder - self.lowerborder)
            self.scroller.setpageheight(self.height - self.upperborder - self.lowerborder)
            self.scroller.refresh()
            inc = 0
            if self.linecenter[1] - self.scroller.scroll > self.scroller.height:
                inc = self.textsize
            if self.linecenter[1] - self.scroller.scroll < 0:
                inc = -self.textsize
            count = 0
            while inc != 0:
                self.scroller.scroll += inc
                count += 1
                if not (self.linecenter[1] - self.scroller.scroll < 0 or self.linecenter[
                    1] - self.scroller.scroll > self.height - self.upperborder - self.lowerborder):
                    inc = 0
                if count > 20:
                    break
            if self.scrolleron:
                self.scroller.limitpos()
            else:
                self.scroller.scroll = self.scroller.minp

    def child_refreshcords(self):
        if self.scroller != 0:
            self.refreshscroller()
            self.rect = Utils.roundrect(self.x, self.y, self.width, self.height)
            self.innerrect = Utils.roundrect(self.x + self.leftborder, self.y + self.upperborder,
                                       self.width - self.rightborder - self.leftborder - self.scrolleron * self.scroller.width,
                                       self.height - self.upperborder - self.lowerborder)
            self.textimagerect = self.textimage.get_rect()
            if self.textcenter:
                self.textimagerect.x = (
                                                   self.width - self.horizontalspacing * 2 - self.scrolleron * self.scroller.width - self.leftborder - self.rightborder) / 2 + self.textoffsetx + self.horizontalspacing - self.textimagerect.width / 2 / self.scale
                self.textimagerect.y = self.verticalspacing + self.textimagerect.height / 2 + self.textoffsety - self.textimagerect.height / 2
            else:
                self.textimagerect.x = self.textoffsetx + self.horizontalspacing
                self.textimagerect.y = self.textoffsety + self.verticalspacing

    def child_render(self, screen):
        self.typeline += 1
        self.selectrect = Utils.roundrect(self.x * self.dirscale[0] + (self.leftborder - self.selectbordersize) * self.scale,
                                    self.y * self.dirscale[1] + (self.upperborder - self.selectbordersize) * self.scale,
                                    (self.width - (
                                                self.leftborder + self.rightborder) + self.selectbordersize * 2 - self.scrolleron * self.scroller.width) * self.scale,
                                    (self.height - (
                                                self.upperborder + self.lowerborder) + self.selectbordersize * 2) * self.scale)
        if self.typeline == 80:
            self.typeline = 0
        self.getclickedon(self.selectrect, False, False)
        self.draw(screen)
        mpos = self.ui.mpos
        if self.clickedon == 0:
            self.typingcursor = min([max([self.findclickloc(mpos) + 1, 0]), len(self.chrcorddata)]) - 1
            self.textselected[2] = self.typingcursor + 1
            if len(self.chrcorddata) != 0: self.textselected[0] = True
            self.textselected[1] = self.typingcursor + 1
            self.refreshcursor()
            self.select()
            self.clickstartedinbound = True
        elif self.selected:
            if self.ui.mprs[self.clicktype] and self.ui.mouseheld[self.clicktype][1] == self.ui.buttondowntimer:
                self.clickstartedinbound = False
                self.selected = False
            if not self.selectrect.collidepoint(mpos) and self.ui.mprs[self.clicktype] and not self.ui.mouseheld[
                self.clicktype]:
                self.selected = False
                self.textselected = [False, 0, 0]

        if self.ui.mprs[self.clicktype] and self.ui.mouseheld[self.clicktype][
            1] != self.ui.buttondowntimer and self.clickstartedinbound:
            self.textselected[2] = min([max([self.findclickloc(mpos) + 1, 0]), len(self.chrcorddata)])
            hoff = 0
            if mpos[1] < self.y * self.dirscale[1] + self.upperborder * self.scale:
                hoff = (mpos[1] - (self.y * self.dirscale[1] + self.upperborder * self.scale))
            elif mpos[1] > self.y * self.dirscale[1] + (self.height - self.lowerborder) * self.scale:
                hoff = (mpos[1] - (self.y * self.dirscale[1] + (self.height - self.lowerborder) * self.scale))
            if hoff != 0:
                if self.scrolleron:
                    self.scroller.scroll += hoff / 10
                    self.scroller.limitpos()

            hoff = int((self.ui.mpos[1] - self.selectrect.y - self.holdingcords[1]) / 10)
            if self.intscroller:
                self.change_textnum(self.previntscrollerhoff - hoff)
            self.previntscrollerhoff = hoff
        else:
            self.previntscrollerhoff = 0
        if not self.ui.mprs[self.clicktype]:
            self.clickstartedinbound = False
        return False

    def findclickloc(self, mpos=-1, relativempos=-1):
        if len(self.chrcorddata) == 0:
            return -1
        else:
            if relativempos == -1:
                self.relativempos = ((mpos[0] - (self.x * self.dirscale[0] + (
                            self.leftborder + self.horizontalspacing) * self.scale)) / self.scale, (mpos[1] - (
                            self.y * self.dirscale[1] + (
                                self.upperborder + self.verticalspacing - self.scroller.scroll) * self.scale)) / self.scale)
            else:
                self.relativempos = relativempos
            dis = [0, 10000]
            for i, a in enumerate(self.chrcorddatalined):
                if len(a) != 0 and abs(a[0][1][1] - self.relativempos[1]) < dis[1]:
                    dis[1] = abs(a[0][1][1] - self.relativempos[1])
                    dis[0] = i
            hdis = [0, 10000]
            for i, a in enumerate(self.chrcorddatalined[dis[0]]):
                if abs(a[1][0] - self.relativempos[0]) < hdis[1]:
                    hdis[1] = abs(a[1][0] - self.relativempos[0])
                    hdis[0] = i
            if hdis[0] > len(self.chrcorddatalined[dis[0]]) - 1:
                hdis[0] = len(self.chrcorddatalined[dis[0]]) - 1

            strpos = hdis[0] + sum([len(a) for a in self.chrcorddatalined[:max([dis[0], 0])]])
            if self.relativempos[0] < self.chrcorddatalined[dis[0]][hdis[0]][1][0]:
                strpos -= 1
            return strpos

    def draw(self, screen):
        if self.enabled:
            ui = self.ui
            if self.glow != 0:
                screen.blit(self.glowimage, (
                self.x * self.dirscale[0] - self.glow * self.scale, self.y * self.dirscale[1] - self.glow * self.scale))
            if self.borderdraw:
                Draw.rect(screen, self.backingcol,
                          Utils.roundrect(self.x * self.dirscale[0], self.y * self.dirscale[1], self.width * self.scale,
                                    self.height * self.scale), border_radius=int(self.roundedcorners * self.scale))
            if self.selected and self.selectbordersize != 0:
                Draw.rect(screen, self.selectcol,
                          pygame.Rect(self.selectrect.x + self.holding * self.selectshrinksize * self.scale,
                                      self.selectrect.y + self.holding * self.selectshrinksize * self.scale,
                                      self.selectrect.width - self.holding * self.selectshrinksize * self.scale * 2,
                                      self.selectrect.height - self.holding * self.selectshrinksize * self.scale * 2),
                          int(self.selectbordersize * self.scale),
                          border_radius=int((self.roundedcorners + self.selectbordersize) * self.scale))
            surf = pygame.Surface(((
                                               self.width - self.leftborder - self.rightborder - self.scrolleron * self.scroller.width) * self.scale,
                                   (self.height - self.upperborder - self.lowerborder) * self.scale))
            surf.fill(self.backingcol)
            if self.backingdraw: Draw.rect(surf, self.col, (0, 0, surf.get_width(), surf.get_height()),
                                           border_radius=int(self.roundedcorners * self.scale))
            surf.set_colorkey(self.backingcol)

            offset = (0, self.scroller.scroll)
            surf.blit(self.textimage,
                      (self.textimagerect.x * self.scale, (self.textimagerect.y - self.scroller.scroll) * self.scale))
            if self.typeline > 20 and self.selected:
                pygame.draw.line(surf, self.textcol, ((self.linecenter[0]) * self.scale, (self.linecenter[
                                                                                              1] - self.cursorsize / 2 + self.verticalspacing - self.scroller.scroll) * self.scale),
                                 ((self.linecenter[0]) * self.scale, (self.linecenter[
                                                                          1] + self.cursorsize / 2 + self.verticalspacing - self.scroller.scroll) * self.scale),
                                 2)
            if self.textselected[0] and self.textselected[1] != self.textselected[2]:
                trect = [1000000, 0, 0, 0]
                prev = [0, 0]
                for a in range(min([self.textselected[1], self.textselected[2]]),
                               max([self.textselected[1], self.textselected[2]])):
                    if prev != self.chrcorddata[a][1]:
                        if self.chrcorddata[a][0] != '\n':
                            trect[0] = (self.horizontalspacing + self.chrcorddata[a][1][0] - self.chrcorddata[a][2][
                                0] / 2) * self.scale
                            trect[1] = (self.verticalspacing + self.chrcorddata[a][1][1] - self.chrcorddata[a][2][
                                1] / 2 - self.scroller.scroll) * self.scale
                            trect[2] = self.chrcorddata[a][2][0] * self.scale
                            trect[3] = self.chrcorddata[a][2][1] * self.scale
                        highlight = pygame.Surface((trect[2], trect[3]))
                        highlight.set_alpha(180)
                        highlight.fill((51, 144, 255))
                        surf.blit(highlight, (trect[0], trect[1]))

                    prev = self.chrcorddata[a][1]

            screen.blit(surf, (self.x * self.dirscale[0] + (self.leftborder) * self.scale,
                               self.y * self.dirscale[1] + (self.upperborder) * self.scale))