from abc import ABC
import time
import pygame
from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.ColEdit import ColEdit
from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.Collision import Collision
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Scroller import Scroller


class GuiItem(ABC):
    def __init__(self, **args):
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
        if args['center_y'] == -1:
            self.center_y = self.center
        else:
            self.center_y = args['center_y']
        self.x = args['x']
        self.y = args['y']
        self.startx = args['x']
        self.starty = args['y']
        self.start_anchor = list(args['anchor'])
        self.start_obj_anchor = list(args['obj_anchor'])
        if self.center and self.start_obj_anchor[0] == 0: self.start_obj_anchor[0] = 'w/2'
        if self.center_y and self.start_obj_anchor[1] == 0: self.start_obj_anchor[1] = 'h/2'
        self.scroll_cords = args['scroll_cords']
        self.refresh_bind = list(args['refresh_bind'])[:]
        if type(args['press_keys']) == list:
            self.press_keys = args['press_keys'][:]
        else:
            self.press_keys = [args['press_keys']]

        self.start_width = args['width']
        self.start_height = args['height']
        self.width = Utils.relativeToValue(args['width'], ui.screenw, ui.screenh, ui)
        self.height = Utils.relativeToValue(args['height'], ui.screenw, ui.screenh, ui)
        self.rounded_corners = args['rounded_corners']
        self.scale_size = args['scale_size']
        if args['scale_x'] == -1:
            self.scale_x = self.scale_size
        else:
            self.scale_x = args['scale_x']
        if args['scale_y'] == -1:
            self.scale_y = self.scale_size
        else:
            self.scale_y = args['scale_y']
        self.scale_by = args['scale_by']
        self.glow = args['glow']
        self.refreshScale()
        self.border_size = args['border_size']
        if args['top_border_size'] == -1:
            self.top_border_size = self.border_size
        else:
            self.top_border_size = args['top_border_size']
        if args['bottom_border_size'] == -1:
            self.bottom_border_size = self.border_size
        else:
            self.bottom_border_size = args['bottom_border_size']
        if args['left_border_size'] == -1:
            self.left_border_size = self.border_size
        else:
            self.left_border_size = args['left_border_size']
        if args['right_border_size'] == -1:
            self.right_border_size = self.border_size
        else:
            self.right_border_size = args['right_border_size']

        self.menu = args['menu']
        self.true_menu = self.menu
        if type(self.true_menu) == str: self.true_menu = [self.true_menu]
        self.behind_menu = args['behind_menu']
        if args['kill_time'] == -1:
            self.kill_time = -1
        else:
            self.kill_time = time.time() + args['kill_time']
        self.layer = args['layer']
        if args['ID'] == '': args['ID'] = args['text']

        self.text = str(args['text'])
        self.text_size = args['text_size']
        self.img = args['img']
        self.font = args['font']
        self.bold = args['bold']
        self.antialiasing = args['antialiasing']
        self.pre_generate_text = args['pre_generate_text']
        self.text_center = args['text_center']
        self.start_max_width = args['max_width']
        self.max_width = args['max_width']
        self.text_images = []
        self.toggle_text_images = []

        self.col = args['col']
        self.text_col = args['text_col']
        self.backing_col = ColEdit.autoShiftCol(args['backing_col'], self.col, 20)
        self.border_col = self.backing_col
        self.glow_col = ColEdit.autoShiftCol(args['glow_col'], self.col, -20)
        self.hover_col = ColEdit.autoShiftCol(args['hover_col'], self.col, -20)
        self.toggled_col = ColEdit.autoShiftCol(args['toggled_col'], self.col, -50)
        self.toggled_hover_col = ColEdit.autoShiftCol(args['toggled_hover_col'], self.toggled_col, -20)
        self.selected_col = ColEdit.autoShiftCol(args['selected_col'], self.col, 20)
        self.scroller_col = ColEdit.autoShiftCol(args['scroller_col'], self.col, -30)
        self.slider_col = ColEdit.autoShiftCol(args['slider_col'], self.col, -30)
        self.slider_border_col = ColEdit.autoShiftCol(args['slider_border_col'], self.col, -10)
        self.colorkey = args['colorkey']

        self.click_down_size = args['click_down_size']
        self.text_offset_x = args['text_offset_x']
        self.text_offset_y = args['text_offset_y']
        self.dragable = args['dragable']
        self.spacing = args['spacing']
        self.vertical_spacing = args['vertical_spacing']
        self.horizontal_spacing = args['horizontal_spacing']
        if args['spacing'] != -1:
            self.vertical_spacing = self.spacing
            self.horizontal_spacing = self.spacing

        self.toggle = args['toggle']
        self.toggleable = args['toggleable']
        if args['toggle_text'] == -1:
            self.toggle_text = args['text']
        else:
            self.toggle_text = args['toggle_text']
        if args['toggle_img'] == -1:
            self.toggle_img = args['img']
        else:
            self.toggle_img = args['toggle_img']
        self.bind_toggle = args['bind_toggle']

        self.click_type = args['click_type']

        self.start_clickable_rect = args['clickable_rect']
        self.clickable_rect = args['clickable_rect']
        self.no_click_rect = []
        self.no_click_rects_applied = []
        self.clickable_border = args['clickable_border']
        self.clicked_on = -1
        self.holding = False
        self.force_holding = False
        self.hovering = False
        self.animating = False
        self.animation_speed = args['animation_speed']
        self.animate = 0
        self.current_frame = 0
        self.command = args['command']
        self.run_command_at = args['run_command_at']

        self.lines = args['lines']
        self.line_limit = args['line_limit']
        self.attach_scroller = args['attach_scroller']
        if self.line_limit == -1:
            if self.attach_scroller:
                self.line_limit = 100
            else:
                self.line_limit = self.lines
        self.int_scroller = args['int_scroller']
        self.int_wrap_around = args['int_wrap_around']
        self.selected_border_size = args['selected_border_size']
        self.selected_border_shrink_size = args['selected_border_shrink_size']
        self.cursor_size = args['cursor_size']
        self.char_limit = args['char_limit']
        self.nums_only = args['nums_only']
        self.allowed_characters = args['allowed_characters']
        self.enter_returns = args['enter_returns']
        self.command_if_enter = args['command_if_enter']
        self.command_if_key = args['command_if_key']
        self.img_display = args['img_display']

        self.table_object = False
        self.data = args['data']
        self.titles = args['titles']
        self.split_cell_char = args['split_cell_char']
        self.table = 0
        self.line_size = args['line_size']
        self.box_width = args['box_width']
        self.box_height = args['box_height']
        self.box_guess_height = args['box_guess_height']
        self.box_guess_width = args['box_guess_width']
        self.scroller = args['scroller']
        self.compress_table = args['compress_table']

        self.animation_type = args['animation_type']
        self.options = args['options']
        self.drops_down = args['drops_down']
        if len(self.options) > 0: self.active = self.options[args['startoptionindex']]

        self.backing_draw = args['backing_draw']
        self.border_draw = args['border_draw']
        self.start_page_height = args['page_height']
        self.page_height = Utils.relativeToValue(args['page_height'], ui.screenw, ui.screenh, ui)

        self.start_min_p = args['min_value']
        self.min_value = Utils.relativeToValue(args['min_value'], ui.screenw, ui.screenh, ui)
        self.start_max_value = args['max_value']
        self.max_value = Utils.relativeToValue(args['max_value'], ui.screenw, ui.screenh, ui)
        self.startp = args['startp']
        self.increment = args['increment']
        self.contained_slider = args['contained_slider']
        if args['slider_size'] == -1:
            self.slider_size = self.height * 2
            if self.contained_slider: self.slider_size = self.height - self.top_border_size - self.bottom_border_size
            if args['direction'] == 'vertical':
                self.slider_size = self.width * 2
                if self.contained_slider: self.slider_size = self.width - self.left_border_size - self.right_border_size
        else:
            self.slider_size = args['slider_size']
        if args['slider_rounded_corners'] == -1:
            self.slider_rounded_corners = args['rounded_corners']
        else:
            self.slider_rounded_corners = args['slider_rounded_corners']
        self.direction = args['direction']
        self.contained_slider = args['contained_slider']
        self.move_to_click = args['move_to_click']
        self.scroll_bind = args['scroll_bind']
        self.screen_compressed = args['screen_compressed']

        self.onitem = False
        self.master = [Utils.EmptyObject(0, 0, ui.screenw, ui.screenh)]
        self.bound_items = args['bound_items'][:]
        ui.addid(args['ID'], self)
        for a in self.bound_items:
            self.binditem(a)
        self.empty = False

        self.isolated = args['isolated']
        self.darken = args['darken']
        self.auto_shut_windows = args['auto_shut_windows']
        for a in self.bound_items:
            self.binditem(a)
        self.reset()
        pygame.event.pump()

    def __str__(self):
        return '<' + str(type(self)).split("'")[1] + f' ID:{self.ID}>'

    def __repr__(self):
        return '<' + str(type(self)).split("'")[1] + f' ID:{self.ID}>'

    def reset(self):
        self.autoScale()
        self.refreshScale()
        self.genText()
        self.autoScale()
        self.refreshCords()
        self.resetCords()
        self.refresh()

    def refresh(self):
        self.refreshScale()
        self.genText()
        self.autoScale()
        self.resetCords()
        self.refreshGlow()
        self.refreshBound()
        self.refreshClickableRect()

    def genText(self):
        ui = self.ui
        self.current_frame = 0
        if type(self.img) != list:
            imgs = [self.img]
        else:
            imgs = self.img
            if len(imgs) < 1: imgs.append('')

        self.text_images = []
        for img in imgs:
            if type(img) == str:
                if len(imgs) != 1:
                    txt = img
                else:
                    txt = self.text
                self.text_images.append(
                    ui.rendertextlined(txt, self.text_size, self.text_col, self.col, self.font, self.max_width, self.bold,
                                       self.antialiasing, self.text_center, imgin=True, img=img, scale=self.scale,
                                       linelimit=self.line_limit, cutstartspaces=True))
            else:
                self.text_images.append(pygame.transform.scale(img, (
                img.get_width() * (self.text_size / img.get_height()) * self.scale,
                img.get_height() * (self.text_size / img.get_height()) * self.scale)))
            if self.colorkey != -1: self.text_images[-1].set_colorkey(self.colorkey)
        self.textimage = self.text_images[0]
        if len(self.text_images) != 1:
            self.animating = True
        self.child_gentext()

    def refreshGlow(self):
        if self.glow != 0:
            self.glow_image = pygame.Surface(
                ((self.glow * 2 + self.width) * self.scale, (self.glow * 2 + self.height) * self.scale),
                pygame.SRCALPHA)
            Draw.glow(self.glow_image, Utils.roundRect(self.glow * self.scale, self.glow * self.scale, self.width * self.scale,
                                                       self.height * self.scale), int(self.glow * self.scale), self.glow_col)

    def refreshBound(self):
        for a in self.refresh_bind:
            if a in self.ui.IDs:
                self.ui.IDs[a].refresh()

    def animatetext(self):
        if self.animating:
            self.animate += 1
            if self.animate % self.animation_speed == 0:
                self.current_frame += 1
                if self.current_frame == len(self.text_images):
                    self.current_frame = 0
                self.textimage = self.text_images[self.current_frame]

    def resetCords(self, scalereset=True):
        ui = self.ui
        if scalereset: self.refreshScale()
        self.anchor = self.start_anchor[:]

        master = self.master[0]
        if len(self.master) > 1:
            if 'animate' in self.true_menu:
                for a in self.master:
                    if ui.activemenu in a.truemenu:
                        master = a
            else:
                for a in self.master:
                    if not (ui.activemenu in a.truemenu):
                        master = a
                        break

        w = self.getMasterWidth()
        h = self.getMasterHeight()

        self.anchor[0] = Utils.relativeToValue(self.anchor[0], w, h, ui)
        self.anchor[1] = Utils.relativeToValue(self.anchor[1], w, h, ui)

        self.obj_anchor = self.start_obj_anchor[:]
        self.obj_anchor[0] = Utils.relativeToValue(self.obj_anchor[0], self.width, self.height, ui)
        self.obj_anchor[1] = Utils.relativeToValue(self.obj_anchor[1], self.width, self.height, ui)

        self.x = int(master.x * master.dirscale[0] + self.anchor[0] + (
                    self.startx - self.obj_anchor[0] - self.scroll_cords[0]) * self.scale) / self.dir_scale[0]
        self.y = int(master.y * master.dirscale[1] + self.anchor[1] + (
                    self.starty - self.obj_anchor[1] - self.scroll_cords[1]) * self.scale) / self.dir_scale[1]

        self.refreshCords()
        for a in self.bound_items:
            a.resetCords()
        self.refreshClickableRect()

    def refreshCords(self):
        self.refreshScale()
        self.child_refreshcords()

    def refreshScale(self):
        if self.scale_by == -1:
            self.scale = self.ui.scale
        elif self.scale_by == 'vertical':
            self.scale = self.ui.dir_scale[1]
        else:
            self.scale = self.ui.dir_scale[0]

        self.dir_scale = self.ui.dir_scale[:]
        if not self.scale_size: self.scale = 1
        if not self.scale_x: self.dir_scale[0] = 1
        if not self.scale_y: self.dir_scale[1] = 1

    def autoScale(self):
        w = self.getMasterWidth() / self.scale
        h = self.getMasterHeight() / self.scale
        if self.start_width != -1: self.width = Utils.relativeToValue(self.start_width, w, h, self.ui)
        if self.start_max_width != -1: self.max_width = Utils.relativeToValue(self.start_max_width, w, h, self.ui)
        if self.start_height != -1: self.height = Utils.relativeToValue(self.start_height, w, h, self.ui)
        self.refreshClickableRect()
        self.child_autoscale()

    def refreshClickableRect(self):
        w = self.getMasterWidth() / self.scale
        h = self.getMasterHeight() / self.scale
        if self.start_clickable_rect != -1:
            rx, ry, rw, rh = self.start_clickable_rect
            xstart = self.master[0].x * self.master[0].dirscale[0]
            ystart = self.master[0].y * self.master[0].dirscale[1]
            ow = self.getMasterWidth() / self.scale
            oh = self.getMasterHeight() / self.scale
            if type(self) == ScrollerTable:
                self.page_height = Utils.relativeToValue(self.start_page_height, w, h, self.ui)
                oh = self.page_height
            if type(self) in [ScrollerTable, Table]:
                xstart = self.x * self.dir_scale[0]
                ystart = self.y * self.dir_scale[1]
                ow = self.width
                oh = self.height
            self.clickable_rect = pygame.Rect(xstart + Utils.relativeToValue(rx, w, h, self.ui),
                                              ystart + Utils.relativeToValue(ry, w, h, self.ui),
                                              Utils.relativeToValue(rw, ow, oh, self.ui) * self.scale,
                                              Utils.relativeToValue(rh, ow, oh, self.ui) * self.scale)
        else:
            self.clickable_rect = self.start_clickable_rect

    def render(self, screen):
        if self.kill_time != -1 and self.kill_time < self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            self.child_render(screen)
            for a in [i.ID for i in self.bound_items][:]:
                if a in self.ui.IDs:
                    self.ui.IDs[a].render(screen)

    def smartcords(self, x=None, y=None, startset=True, accountscroll=False):
        scr = [0, 0]
        if accountscroll:
            scr = self.scroll_cords[:]

        if x is not None:
            self.x = x
            if startset: self.startx = ((self.x + scr[0]) * self.dir_scale[0] + self.obj_anchor[0] * self.scale -
                                        self.anchor[0]) / self.scale - self.master[0].x
        if y is not None:
            self.y = y
            if startset: self.starty = ((self.y + scr[1]) * self.dir_scale[1] + self.obj_anchor[1] * self.scale -
                                        self.anchor[1]) / self.scale - self.master[0].y

    def binditem(self, item, replace=True, resetcords=True):
        if item != self:
            for a in item.master:
                if type(a) == Utils.EmptyObject:
                    item.master.remove(a)
            if item.onitem and replace:
                for a in item.master:
                    if type(a) != Utils.EmptyObject:
                        if item in a.bound_items:
                            a.bound_items.remove(item)
            if not (item in self.bound_items):
                self.bound_items.append(item)
            item.onitem = True
            if replace:
                item.master = [self]
            else:
                item.master.append(self)
            self.bound_items.sort(key=lambda x: x.layer, reverse=False)
            if resetcords: item.resetCords()

    def setmenu(self, menu):
        self.menu = menu
        self.true_menu = self.menu
        if type(self.true_menu) == str: self.true_menu = [self.true_menu]

        for a in self.master:
            if type(a) in [WindowedMenu, Menu]:
                a.bound_items.remove(self)
        self.master = []
        for a in self.true_menu:
            if a in self.ui.windowedmenunames:
                self.ui.windowedmenus[self.ui.windowedmenunames.index(a)].binditem(self, False, False)
        self.ui.refreshitems()
        self.resetCords()

    def getmenu(self):
        if type(self.master[0]) in [WindowedMenu, Menu]:
            return self.master[0].menu
        else:
            return self.master[0].getmenu()

    def getMasterWidth(self):
        w = self.ui.screenw
        if self.onitem:
            w = self.master[0].width * self.master[0].scale
        return w

    def getMasterHeight(self):
        h = self.ui.screenh
        if self.onitem:
            h = self.master[0].height * self.master[0].scale
        return h

    def getchildIDs(self):
        lis = [self.ID]
        lis += sum([a.getchildIDs() for a in self.bound_items], [])
        return lis

    def getenabled(self):
        if not self.enabled:
            return False
        else:
            return self.master[0].getenabled()

    def settext(self, text):
        self.text = str(text)
        self.refresh()

    def settext_size(self, text_size):
        self.text_size = text_size
        self.refresh()

    def setwidth(self, width):
        self.start_width = width
        self.autoScale()

    def setheight(self, height):
        self.start_height = height
        self.autoScale()

    def settext_col(self, col):
        self.text_col = col
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
        for a in self.bind_toggle:
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

    def getClickedOn(self, rect='default', runcom=True, drag=True, smartdrag=True):
        ui = self.ui
        if rect == 'default':
            rect = pygame.Rect(self.x * self.dir_scale[0], self.y * self.dir_scale[1], self.width * self.scale,
                               self.height * self.scale)
        self.clicked_on = -1
        self.hovering = False
        mpos = ui.mpos
        if self.force_holding:
            if not self.holding:
                self.clicked_on = 0
            else:
                self.clicked_on = 1
            self.holding = True
            return False
        if rect.collidepoint(mpos) and (self.clickable_rect == -1 or self.clickable_rect.collidepoint(mpos)) and not (
        Collision.collidepointrects(mpos, self.no_click_rects_applied)):
            if ui.mprs[self.click_type] and (ui.mouseheld[self.click_type][1] > 0 or self.holding):
                if ui.mouseheld[self.click_type][1] == ui.buttondowntimer:
                    self.clicked_on = 0
                    self.holding = True
                    self.holding_cords = [(mpos[0]) - rect.x, (mpos[1]) - rect.y]
                    if self.run_command_at < 2 and runcom:
                        self.press()
            else:
                self.hovering = True
        if ui.mprs[self.click_type] and self.holding:
            if self.clicked_on != 0:
                self.clicked_on = 1
            if self.dragable and drag:
                if type(self) == Scroller:
                    account = [0, -self.border]
                else:
                    account = [-rect.x + self.x * self.dir_scale[0], -rect.y + self.y * self.dir_scale[1]]
                if smartdrag:
                    self.smartcords((mpos[0] - self.holding_cords[0] + account[0]) / self.dir_scale[0],
                                    (mpos[1] - self.holding_cords[1] + account[1]) / self.dir_scale[1])
                else:
                    self.x = (mpos[0] - self.holding_cords[0] + account[0]) / self.dir_scale[0]
                    self.y = (mpos[1] - self.holding_cords[1] + account[1]) / self.dir_scale[1]
                self.centerx = self.x + self.width / 2
                self.center_y = self.y + self.height / 2
                for a in self.bound_items:
                    a.resetCords(ui)
            if self.run_command_at == 1 and runcom:
                self.command()
        elif not ui.mprs[self.click_type]:
            if self.holding:
                self.clicked_on = 2
                if rect.collidepoint(mpos) and self.run_command_at > 0 and runcom:
                    self.press()
            self.holding = False
        return False