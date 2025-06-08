from abc import ABC
import time

import numpy as np
import pygame
from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.ColEdit import ColEdit
from UIpygame.Utils.Draw import Draw
from UIpygame.Utils.Collision import Collision
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Scroller import Scroller


class GuiItem(ABC):
    def __init__(self, dataClass):

        return


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
        self.start_x = args['x']
        self.start_y = args['y']
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
            self.bindItem(a)
        self.empty = False

        self.isolated = args['isolated']
        self.darken = args['darken']
        self.auto_shut_windows = args['auto_shut_windows']
        for a in self.bound_items:
            self.bindItem(a)
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

    def refreshBound(self):
        for a in self.refresh_bind:
            if a in self.ui.IDs:
                self.ui.IDs[a].refresh()

    def refreshCords(self):
        self.refreshScale()
        self.childRefreshCords()

    def render(self, screen):
        if self.kill_time != -1 and self.kill_time < self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            self.child_render(screen)
            for a in [i.ID for i in self.bound_items][:]:
                if a in self.ui.IDs:
                    self.ui.IDs[a].render(screen)

    def bindItem(self, item, replace=True, resetcords=True):
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

    def getParentWidth(self):
        w = self.ui.screenw
        if self.onitem:
            w = self.master.getWidth()
        return w

    def getParentHeight(self):
        h = self.ui.screenh
        if self.onitem:
            h = self.master.getHeight()
        return h

    def getParentDimensions(self):
        if self.onitem:
            return self.master.getDimensions()
        return np.array([self.ui.screenw, self.ui.screenh])

    def getChildIDs(self):
        lis = [self.ID]
        lis += sum([a.getChildIDs() for a in self.bound_items], [])
        return lis

    def getChildren(self):
        return self.bound_items

    def getEnabled(self):
        if not self.enabled:
            return False
        else:
            return self.master[0].getEnabled()

    def setWidth(self, width):
        self.start_width = width
        self.autoScale()

    def setHeight(self, height):
        self.start_height = height
        self.autoScale()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def toggleEnabled(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def childGenText(self):
        pass

    def childRefreshCords(self):
        pass

    def childAutoScale(self):
        pass

    def refreshNoClickRect(self):
        pass

    ##        prevmenu = self.ui.active_menu
    ##        if prevmenu!=self.ui.active_menu:
    ##            temp = self.ui.mprs,self.ui.mpos
    ##            self.ui.mprs = [0,0,0]
    ##            self.ui.mpos = [-100000,-100000]
    ##            self.render(pygame.Surface((10,10)))
    ##            self.ui.mprs,self.ui.mpos = temp