import copy

class Style:
    universaldefaults = {'rounded_corners': 0, 'anchor': (0, 0), 'obj_anchor': (0, 0), 'center': False, 'center_y': -1,
                         'text_size': 50, 'font': 'calibre', 'bold': True,
                         'antialiasing': True, 'border_size': 3, 'top_border_size': -1, 'bottom_border_size': -1, 'right_border_size': -1,
                         'left_border_size': -1, 'scale_size': True,
                         'scale_x': -1, 'scale_y': -1, 'glow': 0, 'glow_col': -1, 'col': -1, 'text_col': -1,
                         'backing_col': -1, 'hover_col': -1, 'click_down_size': 4,
                         'click_type': 0, 'text_offset_x': 0, 'text_offset_y': 0, 'max_width': -1, 'colorkey': -1,
                         'toggled_col': -1, 'toggled_hover_col': -1, 'spacing': -1,
                         'vertical_spacing': -1, 'horizontal_spacing': -1, 'clickable_border': 0, 'lines': 1,
                         'selected_col': -1, 'selected_border_size': 2,
                         'selected_border_shrink_size': 0, 'cursor_size': -1, 'text_center': True, 'line_size': 2,
                         'backing_draw': True, 'border_draw': True, 'animation_speed': 5,
                         'scroller_col': -1, 'slider_col': -1, 'slider_border_col': -1, 'slider_size': -1, 'increment': 0,
                         'box_guess_width': 100, 'box_guess_height': 100,
                         'slider_rounded_corners': -1, 'contained_slider': True, 'move_to_click': True, 'isolated': True,
                         'darken': 60, 'hsvashift': False}

    replace = {'rounded_corners': -1, 'center': -1, 'text_size': -1, 'font': -1, 'bold': -1, 'antialiasing': -1,
               'border_size': -1, 'scale_size': -1, 'glow': -1, 'col': -1, 'click_down_size': -1, 'click_type': -1,
               'box_guess_width': -1, 'box_guess_height': -1,
               'text_offset_x': -1, 'text_offset_y': -1, 'clickable_border': -1, 'text_center': -1, 'lines': -1,
               'line_size': -1, 'backing_draw': -1, 'border_draw': -1, 'animation_speed': -1, 'contained_slider': -1,
               'move_to_click': -1, 'darken': -1}
    for var in list(replace):
        universaldefaults[var] = replace[var]

    defaults = copy.deepcopy(universaldefaults)

    wallpapercol = (255, 255, 255)

    # UI.objectkey = {'button': Button, 'text': Text, 'textbox': Textbox, 'table': Table, 'scrollertable': ScrollerTable,
    #                 'dropdown': DropDown, 'slider': Slider, 'scroller': Scroller, 'menu': MENU,
    #                 'windowedmenu': WindowedMenu, 'window': Window, 'rect': Rectangle}

    objectdefaults = {}
    # for a in [UI.objectkey[o] for o in UI.objectkey]:
    #     objectdefaults[a] = copy.deepcopy(defaults)
