from UIpygame.Widgets.GuiItem import GuiItem
from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.Draw import Draw
import random
import threading
import copy
import pygame

class Table(GuiItem):
    def reset(self):
        self.startboxwidth = self.boxwidth
        self.startboxheight = self.boxheight
        self.tableitemID = str(random.randint(1000000, 10000000))
        self.threadactive = False
        self.table = 0
        self.refreshScale()
        self.autoScale()
        self.resetCords()
        self.refreshScale()
        self.preprocess()
        self.initheightwidth()
        self.estimatewidths()
        self.genText()
        self.gettablewidths()
        self.gettableheights()
        self.refreshCords()
        self.resetCords()
        self.enable()

    def refresh(self):
        self.refreshScale()
        self.autoScale()
        self.preprocess()
        self.initheightwidth()
        self.estimatewidths()
        self.genText()
        self.gettablewidths()
        self.gettableheights()
        self.refreshCords()
        self.refreshGlow()
        self.refreshClickableRect()
        self.enable()
        self.threadactive = False

    def threadrefresh(self):
        if not self.threadactive:
            self.threadactive = True
            thread = threading.Thread(target=lambda: self.refresh())
            thread.start()

    def disable(self):
        self.enabled = False
        if self.table != 0:
            for a in self.table:
                for b in a:
                    b.enabled = False
        else:
            for a in self.data:
                for b in a:
                    if not (type(b) in [str, int, float, list]):
                        b.enabled = False

    def enable(self):
        self.enabled = True
        if self.table != 0:
            for a in self.table:
                for b in a:
                    b.enabled = True

    def setWidth(self, width):
        self.startwidth = width
        self.refresh()
        self.resetCords()

    def setHeight(self, height):
        self.startheight = height
        self.refresh()
        self.resetCords()

    def preprocess(self):
        self.preprocessed = []

        def seperate(lis, targetlen, insert=''):
            if len(lis) == 0: return [copy.deepcopy(insert) for a in range(targetlen)]
            width_per = targetlen / len(lis)
            pos = 0
            section = width_per
            for i in range(targetlen - len(lis)):
                pos += 1
                section -= 1
                while section < 1:
                    section += width_per - 1
                    pos += 1
                lis.insert(pos, copy.deepcopy(insert))
            return lis

        for a in self.data:
            self.preprocessed.append(list(a))
        if len(self.titles) != 0:
            self.preprocessed.insert(0, copy.copy(list(self.titles)))
        self.rows = len(self.preprocessed)
        if self.rows == 0:
            self.columns = 0
        else:
            self.columns = max([len(a) for a in self.preprocessed])
            if type(self.startboxwidth) == list:
                self.columns = max(self.columns, len(self.startboxwidth))

        self.preprocessed = seperate(self.preprocessed, self.rows, [])
        for a in range(self.rows):
            self.preprocessed[a] = seperate(self.preprocessed[a], self.columns, self.split_cell_char)

        if len(self.preprocessed) > 0 and len(self.preprocessed[0]) > 0:
            grabber = self.preprocessed[0][0]
            pos = [0, 0]
            while grabber == self.split_cell_char:
                prev = pos[:]
                pos[0] = (pos[0] + 1)
                pos[1] += pos[0] // len(self.preprocessed[0])
                pos[0] %= len(self.preprocessed[0])
                if pos[1] < len(self.preprocessed) and pos[0] < len(self.preprocessed[pos[1]]):
                    grabber = self.preprocessed[pos[1]][pos[0]]
                else:
                    grabber = ''
                    pos = prev[:]
            self.preprocessed[pos[1]][pos[0]] = self.split_cell_char
            self.preprocessed[0][0] = grabber
        ##        except Exception as e:
        ##            return

        self.cellreferencemap = [
            [-1 if self.preprocessed[y][x] == self.split_cell_char else (x, y) for x in range(self.columns)] for y in
            range(self.rows)]

        for y in range(self.rows):
            current = self.cellreferencemap[y][0]
            pull_left = current != -1

            for x in range(self.columns):
                if self.cellreferencemap[y][x] == -1:
                    if pull_left:
                        self.cellreferencemap[y][x] = current
                    elif y != 0:
                        self.cellreferencemap[y][x] = self.cellreferencemap[y - 1][x]
                else:
                    pull_left = True
                    current = self.cellreferencemap[y][x]
                if y != 0 and x != 0 and self.cellreferencemap[y][x - 1] == self.cellreferencemap[y - 1][x]:
                    if self.cellreferencemap[y][x - 1] != self.cellreferencemap[y][x]:
                        raise Exception(f"Invalid Table, ID:{self.ID}, Segment Rectangles Overlap")

    def genText(self):
        self.enabled = True
        stillactive = []
        for a in self.preprocessed: stillactive += a
        copy = [a.ID for a in self.bound_items][:]
        for a in copy:
            if self.ui.IDs[a].table_object and not (self.ui.IDs[a] in stillactive):
                self.ui.delete(a)
        self.table = []
        for a in range(len(self.preprocessed)):
            self.table.append(self.row_gentext(a))

    def row_gentext(self, index):
        row = []
        a = index
        for i, b in enumerate(self.preprocessed[a]):
            refrence = self.cellreferencemap[a][i]
            if refrence != (i, a):
                if refrence[1] != a:
                    row.append(self.table[refrence[1]][refrence[0]])
                else:
                    row.append(row[refrence[0]])
            else:
                ref = False
                if type(b) in [Button, Textbox, Text, Table, ScrollerTable, Slider, DropDown]:
                    b.enabled = self.enabled
                    ref = True
                    obj = b
                elif type(b) == pygame.Surface:
                    self.ui.delete('tabletext' + self.tableitemID + self.ID + str(a) + '-' + str(i), False)
                    obj = self.ui.maketext(0, 0, '', self.text_size, self.menu,
                                           'tabletext' + self.tableitemID + self.ID + str(a) + '-' + str(i),
                                           self.layer + 0.01, self.rounded_corners, textcenter=self.text_center, img=b,
                                           maxwidth=self.boxwidth[i],
                                           scalesize=self.scale_size, scale_by=self.scale_by,
                                           horizontalspacing=self.horizontal_spacing,
                                           verticalspacing=self.vertical_spacing, colorkey=self.colorkey, enabled=False)
                else:
                    b = str(b)
                    self.ui.delete('tabletext' + self.tableitemID + self.ID + str(a) + '-' + str(i), False)
                    obj = self.ui.maketext(0, 0, b, self.text_size, self.menu,
                                           'tabletext' + self.tableitemID + self.ID + str(a) + '-' + str(i), self.layer,
                                           self.rounded_corners, textcenter=self.text_center, text_col=self.text_col,
                                           font=self.font, bold=self.bold, antialiasing=self.antialiasing,
                                           pregenerated=self.pre_generate_text,
                                           maxwidth=max([self.boxwidth[i] - self.horizontal_spacing * 2, -1]),
                                           scalesize=self.scale_size, scale_by=self.scale_by,
                                           horizontalspacing=self.horizontal_spacing,
                                           verticalspacing=self.vertical_spacing, backing_col=self.col, enabled=False)
                row.append(obj)
                self.itemintotable(obj, i, a)
                if ref:
                    obj.refresh()
        return row

    def childRefreshCords(self):
        if self.table != 0:
            repeats = []
            for a in range(len(self.table)):
                for i, b in enumerate(self.table[a]):
                    if not self.cellreferencemap[a][i] in repeats:
                        self.itemrefreshcords(b, i, a)
                        repeats.append(self.cellreferencemap[a][i])
            alltable = self.getalltableitems()
            for a in self.bound_items:
                if not a.ID in alltable:
                    a.resetCords()

    def itemintotable(self, obj, x, y):
        self.bindItem(obj)
        self.itemrefreshcords(obj, x, y)
        obj.enabled = True

    def itemrefreshcords(self, obj, x, y):
        obj.start_x = (self.line_size * (x + 1) + self.boxwidthsinc[x])
        obj.start_y = (self.line_size * (y + 1) + self.boxheightsinc[y])

        bwidth = self.boxwidths[x]
        rectsize = x + 1
        while rectsize < len(self.boxwidths) and self.cellreferencemap[y][rectsize] == (x, y):
            bwidth += self.line_size + self.boxwidths[rectsize]
            rectsize += 1
        obj.ontable_tilewidth = rectsize - x
        bheight = self.boxheights[y]
        rectsize = y + 1
        while rectsize < len(self.boxheights) and self.cellreferencemap[rectsize][x] == (x, y):
            bheight += self.line_size + self.boxheights[rectsize]
            rectsize += 1
        obj.ontable_tileheight = rectsize - y

        if not (type(obj) in [Slider, Table, ScrollerTable]):
            obj.width = bwidth
            obj.height = bheight
            obj.start_width = bwidth
            obj.start_height = bheight
        elif type(obj) in [Table, ScrollerTable]:
            if obj.width < bwidth:
                obj.width = bwidth
                obj.start_width = bwidth
            elif obj.height < bheight:
                obj.height = bheight
                obj.start_height = bheight
        obj.backing_draw = self.backing_draw
        obj.scale_x = self.scale_size
        obj.scale_y = self.scale_size
        obj.scale_size = self.scale_size
        obj.scale_by = self.scale_by
        obj.table_object = True
        obj.layer = self.rows - y
        if type(self) == ScrollerTable:
            if y != 0 or len(self.titles) == 0:
                obj.start_clickable_rect = self.start_clickable_rect
                obj.clickable_rect = self.clickable_rect
        obj.refreshScale()
        obj.resetCords(False)

    def getalltableitems(self):
        if len(self.titles) != 0:
            titlerem = 1
        else:
            titlerem = 0
        lis = self.table[titlerem:]
        alltable = []
        for y in lis:
            alltable += [a.ID for a in y]
        return alltable

    def initheightwidth(self):
        w = self.getMasterWidth()
        h = self.getMasterHeight()
        ##
        ratiowidth = False
        if self.startwidth != -1: ratiowidth = True
        if type(self.startboxwidth) == int:
            if self.columns == 0:
                tempboxwidth = []
            else:
                tempboxwidth = [self.startboxwidth for a in range(self.columns)]
        else:
            tempboxwidth = self.startboxwidth[:]
            while len(tempboxwidth) < self.columns:
                tempboxwidth.append(-1)
        if ratiowidth:
            splitwidth = self.width - self.line_size * (self.columns + 1)
            count = 0
            for a in tempboxwidth:
                if a == -1:
                    count += 1
                elif type(a) == int:
                    splitwidth -= a
                elif type(a) == str:
                    splitwidth -= Utils.relativeToValue(a, w, h, self.ui)
            for i, a in enumerate(tempboxwidth):
                if a == -1: tempboxwidth[i] = splitwidth / count

        if not (not self.compress_table and type(self.compress_table) == bool):
            if type(self.compress_table) == bool:
                compress = Utils.normalizelist([1 for a in tempboxwidth])
                for i in range(len(compress)):
                    if tempboxwidth[i] == -1:
                        compress[i] = 0
            elif type(self.compress_table) == int:
                compress = [0 for a in tempboxwidth]
                compress[self.compress_table] = 1
            else:
                compress = Utils.normalizelist(self.compress_table[:])
                if len(compress) != len(tempboxwidth):
                    raise Exception(f'Wrong length of variable "compress" in object {self.ID}')
            for i in range(len(tempboxwidth)):
                if compress[i] != 0:
                    tempboxwidth[i] = str(tempboxwidth[
                                              i]) + f'-(ui.IDs["{self.ID}"].scroller.width+ui.IDs["{self.ID}"].border)*ui.IDs["{self.ID}"].scroller.active*{compress[i]}'
        self.boxwidth = []
        for a in tempboxwidth:
            self.boxwidth.append(max(Utils.relativeToValue(a, w, h, self.ui), -1))
        ##
        if self.startboxheight == -1 and self.startheight != -1:
            tempboxheight = [(self.height - self.line_size * (self.rows + 1)) / self.rows for a in range(self.rows)]
        elif type(self.startboxheight) == int:
            if self.rows == 0:
                tempboxheight = []
            else:
                tempboxheight = [self.startboxheight for a in range(self.rows)]
        else:
            tempboxheight = self.startboxheight[:]
            while len(tempboxheight) < self.rows:
                tempboxheight.append(-1)
            while len(tempboxheight) > self.rows and len(tempboxheight) > 0 and tempboxheight[-1] == -1:
                del tempboxheight[-1]
        self.boxheight = []
        for a in tempboxheight:
            self.boxheight.append(Utils.relativeToValue(a, w, h, self.ui))

    def gettablewidths(self):
        self.boxwidthsinc = []
        self.boxwidths = []

        def factor_tilewidth(w, obj):
            return (w - (obj.ontable_tilewidth - 1) * self.line_size) / obj.ontable_tilewidth

        for a in range(len(self.boxwidth)):
            if self.boxwidth[a] == -1:
                minn = 0
                for b in [self.table[c][a] for c in range(len(self.table))]:
                    if type(b) in [Button, Text]:
                        if minn < factor_tilewidth(b.textimage.get_width() + b.horizontal_spacing * 2 * self.scale, b):
                            minn = factor_tilewidth(b.textimage.get_width() + b.horizontal_spacing * 2 * self.scale, b)
                    elif type(b) in [Table, ScrollerTable, Slider]:
                        if minn < factor_tilewidth(b.width * b.scale, b):
                            minn = factor_tilewidth(b.width * b.scale, b)
                    elif type(b) in [DropDown]:
                        if minn < factor_tilewidth(b.init_width * b.scale, b):
                            minn = factor_tilewidth(b.init_width * b.scale, b)
                self.boxwidthsinc.append(sum(self.boxwidths))
                self.boxwidths.append(minn / self.scale)
            else:
                self.boxwidthsinc.append(sum(self.boxwidths))
                self.boxwidths.append(self.boxwidth[a])
        self.boxwidthtotal = sum(self.boxwidths)
        self.width = self.boxwidthtotal + self.line_size * (self.columns + 1)

    def gettableheights(self):
        self.boxheightsinc = []
        self.boxheights = []

        def factor_tileheight(w, obj):
            return (w - (obj.ontable_tileheight - 1) * self.line_size) / obj.ontable_tileheight

        for a in range(len(self.boxheight)):
            if self.boxheight[a] == -1:
                minn = 0
                for b in [self.table[a][c] for c in range(len(self.table[0]))]:
                    if type(b) in [Button, Text]:
                        if minn < factor_tileheight(b.textimage.get_height() + b.vertical_spacing * 2 * self.scale, b):
                            minn = factor_tileheight(b.textimage.get_height() + b.vertical_spacing * 2 * self.scale, b)
                    elif type(b) in [Table, ScrollerTable, Slider]:
                        if minn < factor_tileheight(b.height * b.scale, b):
                            minn = factor_tileheight(b.height * b.scale, b)
                    elif type(b) in [Textbox, DropDown]:
                        if minn < factor_tileheight(b.init_height * b.scale, b):
                            minn = factor_tileheight(b.init_height * b.scale, b)
                self.boxheightsinc.append(sum(self.boxheights))
                self.boxheights.append(minn / self.scale)
            else:
                self.boxheightsinc.append(sum(self.boxheights))
                self.boxheights.append(self.boxheight[a])
        self.boxheighttotal = sum(self.boxheights)
        self.height = self.boxheighttotal + self.line_size * (self.rows + 1)

    def estimatewidths(self):
        self.boxheightsinc = []
        self.boxheights = []
        for a in self.boxheight:
            self.boxheightsinc.append(sum(self.boxheights))
            if a == -1:
                self.boxheights.append(self.box_guess_height)
            else:
                self.boxheights.append(a)
        self.boxwidthsinc = []
        self.boxwidths = []
        for a in self.boxwidth:
            self.boxwidthsinc.append(sum(self.boxwidths))
            if a == -1:
                self.boxwidths.append(self.box_guess_width)
            else:
                self.boxwidths.append(a)

    def wipe(self, titles=True):
        for i, a in enumerate(self.table):
            if titles or i > 0:
                for b in a:
                    self.ui.delete(b.ID, False)
        self.data = []
        if titles:
            self.titles = []

    def child_render(self, screen):
        self.draw(screen)

    def draw(self, screen):
        if self.enabled:
            if self.glow != 0:
                screen.blit(self.glow_image, (
                    self.x * self.dir_scale[0] - self.glow * self.scale, self.y * self.dir_scale[1] - self.glow * self.scale))
            if self.border_draw:
                if type(self) == ScrollerTable:
                    h = min(self.height, self.scroller.page_height)
                else:
                    h = self.height
                Draw.rect(screen, self.border_col,
                          Utils.roundRect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                                          (h) * self.scale), border_radius=int(self.rounded_corners * self.scale))

    def getat(self, row, column):
        return self.table[row + 1][column]

    def row_append(self, row):
        self.rows += 1
        self.data.append(row)
        pre = self.columns
        self.preprocess()
        if pre != self.columns:
            self.refresh()
            self.small_refresh()
        else:
            self.boxheight.append(-1)
            self.__row_init__(len(self.preprocessed) - 1)

    def row_insert(self, row, index):
        if index < len(self.table):
            self.rows += 1
            self.data.insert(index, row)
            if len(self.titles) != 0: index += 1
            pre = self.columns
            self.preprocess()
            if pre != self.columns:
                self.refresh()
                self.small_refresh()
            else:
                self.boxheight.insert(index, -1)
                self.__row_init__(index)
            return True
        else:
            return False

    def row_remove(self, index):
        if index < len(self.table) - 1:
            self.rows -= 1
            if index == -1:
                self.titles = []
                index = 0
            else:
                del self.data[index]
                if len(self.titles) != 0: index += 1
            pre = self.columns
            self.preprocess()
            if pre != self.columns:
                self.refresh()
            else:
                for a in self.table[index]:
                    self.ui.delete(a.ID)
                del self.boxheight[index]
                del self.table[index]
                self.gettableheights()
                for a in range(index, len(self.table)):
                    for i, b in enumerate(self.table[a]):
                        self.ui.setObjectID('tabletext' + self.tableitemID + self.ID + str(a) + '-' + str(i), b)
                        self.itemrefreshcords(b, i, a)
            self.small_refresh()
            return True
        else:
            return False

    def row_replace(self, row, index):
        self.row_remove(index)
        return self.row_insert(row, index)

    def __row_init__(self, index):
        self.initheightwidth()
        self.estimatewidths()
        for a in range(len(self.table) - 1, index - 1, -1):
            for i, b in enumerate(self.table[a]):
                self.ui.setObjectID('tabletext' + self.tableitemID + self.ID + str(a + 1) + '-' + str(i), b)
        self.table.insert(index, self.row_gentext(index))
        self.gettableheights()
        for a in range(index, len(self.table)):
            for i, b in enumerate(self.table[a]):
                self.itemrefreshcords(b, i, a)
        self.small_refresh()

    def small_refresh(self):
        self.autoScale()
        self.initheightwidth()
        self.refreshGlow()
        self.gettablewidths()
        self.gettableheights()
        self.refreshClickableRect()
        self.refreshCords()
        self.refreshBound()
