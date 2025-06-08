import pygame
from UIpygame.Widgets.GuiItem import GuiItem
from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.Draw import Draw


class Textbox(GuiItem):
    def reset(self):
        self.setvars()
        self.autoScale()
        self.resetCords()
        self.resetscroller()
        self.refreshScale()
        self.genText(False)
        self.refreshcursor()
        self.refreshscroller()
        self.refreshCords()
        self.refreshGlow()
        self.resetCords()

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

    def childAutoScale(self):
        heightgetter = self.ui.rendertext('Tg', self.text_size, self.text_col, self.font, self.bold)
        if self.height == -1:
            self.startheight = self.top_border_size + self.bottom_border_size + heightgetter.get_height() * self.lines + self.vertical_spacing * 2
            self.init_height = self.startheight
            self.height = self.startheight
        if self.cursor_size == -1:
            self.cursorsize = self.ui.gettext_size('Tg', self.font, self.text_size, self.bold)[1] - 2

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
        if self.scrolleron and self.attach_scroller:
            if self.page_height < (self.max_value - self.min_value):
                self.scroller.scroll -= (
                            scroll_size * min((self.scroller.maxp - self.scroller.minp) / 20, self.ui.scroll_limit))
                self.scroller.limitpos()
                self.scroller.command()
                return True
        elif self.int_scroller:
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
        if self.int_wrap_around and wraparound:
            val = (val - self.min_value) % (self.max_value - self.min_value + 1) + self.min_value
        else:
            if val < self.min_value:
                val = self.min_value
            elif val > self.max_value:
                val = self.max_value

        self.text = str(round(val, 14))
        if refresh: self.refresh()
        return True

    def setText(self, text=''):
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
            if self.enter_returns: item = '\n'
            if self.command_if_enter: self.command()
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
                if self.allowed_characters != '':
                    newitem = ''
                    for i in item:
                        if i in self.allowed_characters:
                            newitem += i
                    item = newitem
                try:
                    temp = float(self.text[:self.typingcursor + 1] + item + self.text[self.typingcursor + 1:])
                    num = True
                except:
                    num = False
                if (not (self.nums_only) or num):
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
            if self.command_if_key and (item != '' or backspace or delete):
                self.command()
        else:
            if backspace or delete or item != '':
                self.text = self.text[:self.textselected[1]] + item + self.text[self.textselected[2]:]
                self.typingcursor = self.textselected[1] - 1 + len(item)
                self.textselected = [False, 0, 0]
        if self.text[self.char_limit - 1:self.char_limit + 1] == '\n':
            self.text = self.text[:self.char_limit - 1]
        else:
            self.text = self.text[:self.char_limit]
        if self.text != starttext:
            self.refresh()
            self.updateslider()
        else:
            self.refreshcursor()
        self.undochain.append((self.text, self.typingcursor))

    def resetscroller(self):
        self.scroll = 0
        if self.attach_scroller:
            if self.scroller != 0:
                self.bound_items.remove(self.scroller)
                self.ui.delete(self.scroller.ID, False)

            self.scroller = self.ui.makescroller(-self.right_border_size - 15 + self.border / 2, self.top_border_size,
                                                 self.height - self.top_border_size - self.bottom_border_size, Utils.emptyFunction, 15,
                                                 0, self.height - self.top_border_size - self.bottom_border_size, self.height,
                                                 anchor=('w', 0),
                                                 menu=self.menu, rounded_corners=self.rounded_corners, col=self.col,
                                                 scalesize=self.scale_size, scale_y=self.scale_size, scale_x=self.scale_size,
                                                 scale_by=self.scale_by)
            self.bindItem(self.scroller)
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
        self.refreshScale()
        self.genText()
        self.refreshcursor()

        if self.attach_scroller:
            self.refreshscroller()
            self.scroller.setmaxp((self.textimage.get_height()) / self.scale + self.vertical_spacing * 2 - 1)
            self.scroller.setheight(self.height - self.top_border_size - self.bottom_border_size)
            self.scroller.setpageheight(self.height - self.top_border_size - self.bottom_border_size)
            self.scroller.menu = self.menu
            self.scroller.scalesize = self.scale_size
            self.scroller.scale_x = self.scale_size
            self.scroller.scale_y = self.scale_size
            self.scroller.refresh()
            if (self.scroller.maxp - self.scroller.minp) > self.scroller.pageheight:
                self.scrolleron = True
                if self.scroller.scroll > self.scroller.maxp - self.scroller.pageheight:
                    self.scroller.scroll = self.scroller.maxp - self.scroller.pageheight
            else:
                self.scrolleron = False
            self.scroller.refresh()

        self.resetCords()
        self.refreshGlow()
        self.refreshBound()

    def genText(self, refcurse=True):
        self.textimage, self.chrcorddatalined = self.ui.rendertextlined(self.text, self.text_size, self.text_col,
                                                                        self.col, self.font,
                                                                        self.width - self.horizontal_spacing * 2 - self.left_border_size - self.right_border_size - self.scrolleron * self.scroller.width,
                                                                        self.bold, center=self.text_center,
                                                                        scale=self.scale, linelimit=self.line_limit,
                                                                        getcords=True, imgin=self.img_display)
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
                0] / 2 + self.horizontal_spacing, self.chrcorddata[self.typingcursor][1][1]]
        elif len(self.chrcorddata) > 0:
            self.linecenter = [
                self.chrcorddata[self.typingcursor + 1][1][0] - self.chrcorddata[self.typingcursor + 1][2][
                    0] / 2 + self.horizontal_spacing, self.chrcorddata[self.typingcursor + 1][1][1]]
        else:
            if self.text_center:
                self.linecenter = [self.width / 2 - self.left_border_size, self.text_size * 0.3]
            else:
                self.linecenter = [self.horizontal_spacing, self.text_size * 0.3]
        if self.textselected[1] > len(self.chrcorddata):
            self.textselected[1] = len(self.chrcorddata)
        elif self.textselected[1] < 0:
            self.textselected[1] = 0
        if self.textselected[2] > len(self.chrcorddata):
            self.textselected[2] = len(self.chrcorddata)
        elif self.textselected[2] < 0:
            self.textselected[2] = 0

    def refreshscroller(self):
        if self.attach_scroller:
            self.scroller.setheight(self.height - self.top_border_size - self.bottom_border_size)
            self.scroller.setpageheight(self.height - self.top_border_size - self.bottom_border_size)
            self.scroller.refresh()
            inc = 0
            if self.linecenter[1] - self.scroller.scroll > self.scroller.height:
                inc = self.text_size
            if self.linecenter[1] - self.scroller.scroll < 0:
                inc = -self.text_size
            count = 0
            while inc != 0:
                self.scroller.scroll += inc
                count += 1
                if not (self.linecenter[1] - self.scroller.scroll < 0 or self.linecenter[
                    1] - self.scroller.scroll > self.height - self.top_border_size - self.bottom_border_size):
                    inc = 0
                if count > 20:
                    break
            if self.scrolleron:
                self.scroller.limitpos()
            else:
                self.scroller.scroll = self.scroller.minp

    def childRefreshCords(self):
        if self.scroller != 0:
            self.refreshscroller()
            self.rect = Utils.roundRect(self.x, self.y, self.width, self.height)
            self.innerrect = Utils.roundRect(self.x + self.left_border_size, self.y + self.top_border_size,
                                             self.width - self.right_border_size - self.left_border_size - self.scrolleron * self.scroller.width,
                                             self.height - self.top_border_size - self.bottom_border_size)
            self.textimagerect = self.textimage.get_rect()
            if self.text_center:
                self.textimagerect.x = (
                                               self.width - self.horizontal_spacing * 2 - self.scrolleron * self.scroller.width - self.left_border_size - self.right_border_size) / 2 + self.text_offset_x + self.horizontal_spacing - self.textimagerect.width / 2 / self.scale
                self.textimagerect.y = self.vertical_spacing + self.textimagerect.height / 2 + self.text_offset_y - self.textimagerect.height / 2
            else:
                self.textimagerect.x = self.text_offset_x + self.horizontal_spacing
                self.textimagerect.y = self.text_offset_y + self.vertical_spacing

    def child_render(self, screen):
        self.typeline += 1
        self.selectrect = Utils.roundRect(self.x * self.dir_scale[0] + (self.left_border_size - self.selected_border_size) * self.scale,
                                          self.y * self.dir_scale[1] + (self.top_border_size - self.selected_border_size) * self.scale,
                                          (self.width - (
                                                self.left_border_size + self.right_border_size) + self.selected_border_size * 2 - self.scrolleron * self.scroller.width) * self.scale,
                                          (self.height - (
                                                self.top_border_size + self.bottom_border_size) + self.selected_border_size * 2) * self.scale)
        if self.typeline == 80:
            self.typeline = 0
        self.getClickedOn(self.selectrect, False, False)
        self.draw(screen)
        mpos = self.ui.mpos
        if self.clicked_on == 0:
            self.typingcursor = min([max([self.findclickloc(mpos) + 1, 0]), len(self.chrcorddata)]) - 1
            self.textselected[2] = self.typingcursor + 1
            if len(self.chrcorddata) != 0: self.textselected[0] = True
            self.textselected[1] = self.typingcursor + 1
            self.refreshcursor()
            self.select()
            self.clickstartedinbound = True
        elif self.selected:
            if self.ui.mprs[self.click_type] and self.ui.mouseheld[self.click_type][1] == self.ui.buttondowntimer:
                self.clickstartedinbound = False
                self.selected = False
            if not self.selectrect.collidepoint(mpos) and self.ui.mprs[self.click_type] and not self.ui.mouseheld[
                self.click_type]:
                self.selected = False
                self.textselected = [False, 0, 0]

        if self.ui.mprs[self.click_type] and self.ui.mouseheld[self.click_type][
            1] != self.ui.buttondowntimer and self.clickstartedinbound:
            self.textselected[2] = min([max([self.findclickloc(mpos) + 1, 0]), len(self.chrcorddata)])
            hoff = 0
            if mpos[1] < self.y * self.dir_scale[1] + self.top_border_size * self.scale:
                hoff = (mpos[1] - (self.y * self.dir_scale[1] + self.top_border_size * self.scale))
            elif mpos[1] > self.y * self.dir_scale[1] + (self.height - self.bottom_border_size) * self.scale:
                hoff = (mpos[1] - (self.y * self.dir_scale[1] + (self.height - self.bottom_border_size) * self.scale))
            if hoff != 0:
                if self.scrolleron:
                    self.scroller.scroll += hoff / 10
                    self.scroller.limitpos()

            hoff = int((self.ui.mpos[1] - self.selectrect.y - self.holding_cords[1]) / 10)
            if self.int_scroller:
                self.change_textnum(self.previntscrollerhoff - hoff)
            self.previntscrollerhoff = hoff
        else:
            self.previntscrollerhoff = 0
        if not self.ui.mprs[self.click_type]:
            self.clickstartedinbound = False
        return False

    def findclickloc(self, mpos=-1, relativempos=-1):
        if len(self.chrcorddata) == 0:
            return -1
        else:
            if relativempos == -1:
                self.relativempos = ((mpos[0] - (self.x * self.dir_scale[0] + (
                            self.left_border_size + self.horizontal_spacing) * self.scale)) / self.scale, (mpos[1] - (
                        self.y * self.dir_scale[1] + (
                        self.top_border_size + self.vertical_spacing - self.scroller.scroll) * self.scale)) / self.scale)
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
                screen.blit(self.glow_image, (
                    self.x * self.dir_scale[0] - self.glow * self.scale, self.y * self.dir_scale[1] - self.glow * self.scale))
            if self.border_draw:
                Draw.rect(screen, self.backing_col,
                          Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                          self.height * self.scale), border_radius=int(self.rounded_corners * self.scale))
            if self.selected and self.selected_border_size != 0:
                Draw.rect(screen, self.selected_col,
                          pygame.Rect(self.selectrect.x + self.holding * self.selected_border_shrink_size * self.scale,
                                      self.selectrect.y + self.holding * self.selected_border_shrink_size * self.scale,
                                      self.selectrect.width - self.holding * self.selected_border_shrink_size * self.scale * 2,
                                      self.selectrect.height - self.holding * self.selected_border_shrink_size * self.scale * 2),
                          int(self.selected_border_size * self.scale),
                          border_radius=int((self.rounded_corners + self.selected_border_size) * self.scale))
            surf = pygame.Surface(((
                                               self.width - self.left_border_size - self.right_border_size - self.scrolleron * self.scroller.width) * self.scale,
                                   (self.height - self.top_border_size - self.bottom_border_size) * self.scale))
            surf.fill(self.backing_col)
            if self.backing_draw: Draw.rect(surf, self.col, (0, 0, surf.get_width(), surf.get_height()),
                                            border_radius=int(self.rounded_corners * self.scale))
            surf.set_colorkey(self.backing_col)

            offset = (0, self.scroller.scroll)
            surf.blit(self.textimage,
                      (self.textimagerect.x * self.scale, (self.textimagerect.y - self.scroller.scroll) * self.scale))
            if self.typeline > 20 and self.selected:
                pygame.draw.line(surf, self.text_col, ((self.linecenter[0]) * self.scale, (self.linecenter[
                                                                                              1] - self.cursorsize / 2 + self.vertical_spacing - self.scroller.scroll) * self.scale),
                                 ((self.linecenter[0]) * self.scale, (self.linecenter[
                                                                          1] + self.cursorsize / 2 + self.vertical_spacing - self.scroller.scroll) * self.scale),
                                 2)
            if self.textselected[0] and self.textselected[1] != self.textselected[2]:
                trect = [1000000, 0, 0, 0]
                prev = [0, 0]
                for a in range(min([self.textselected[1], self.textselected[2]]),
                               max([self.textselected[1], self.textselected[2]])):
                    if prev != self.chrcorddata[a][1]:
                        if self.chrcorddata[a][0] != '\n':
                            trect[0] = (self.horizontal_spacing + self.chrcorddata[a][1][0] - self.chrcorddata[a][2][
                                0] / 2) * self.scale
                            trect[1] = (self.vertical_spacing + self.chrcorddata[a][1][1] - self.chrcorddata[a][2][
                                1] / 2 - self.scroller.scroll) * self.scale
                            trect[2] = self.chrcorddata[a][2][0] * self.scale
                            trect[3] = self.chrcorddata[a][2][1] * self.scale
                        highlight = pygame.Surface((trect[2], trect[3]))
                        highlight.set_alpha(180)
                        highlight.fill((51, 144, 255))
                        surf.blit(highlight, (trect[0], trect[1]))

                    prev = self.chrcorddata[a][1]

            screen.blit(surf, (self.x * self.dir_scale[0] + (self.left_border_size) * self.scale,
                               self.y * self.dir_scale[1] + (self.top_border_size) * self.scale))