import copy

class Style:
    universaldefaults = {'roundedcorners': 0, 'anchor': (0, 0), 'objanchor': (0, 0), 'center': False, 'centery': -1,
                         'textsize': 50, 'font': 'calibre', 'bold': True,
                         'antialiasing': True, 'border': 3, 'upperborder': -1, 'lowerborder': -1, 'rightborder': -1,
                         'leftborder': -1, 'scalesize': True,
                         'scalex': -1, 'scaley': -1, 'glow': 0, 'glowcol': -1, 'col': -1, 'textcol': -1,
                         'backingcol': -1, 'hovercol': -1, 'clickdownsize': 4,
                         'clicktype': 0, 'textoffsetx': 0, 'textoffsety': 0, 'maxwidth': -1, 'colorkey': -1,
                         'togglecol': -1, 'togglehovercol': -1, 'spacing': -1,
                         'verticalspacing': -1, 'horizontalspacing': -1, 'clickableborder': 0, 'lines': 1,
                         'selectcol': -1, 'selectbordersize': 2,
                         'selectshrinksize': 0, 'cursorsize': -1, 'textcenter': True, 'linesize': 2,
                         'backingdraw': True, 'borderdraw': True, 'animationspeed': 5,
                         'scrollercol': -1, 'slidercol': -1, 'sliderbordercol': -1, 'slidersize': -1, 'increment': 0,
                         'guesswidth': 100, 'guessheight': 100,
                         'sliderroundedcorners': -1, 'containedslider': True, 'movetoclick': True, 'isolated': True,
                         'darken': 60, 'hsvashift': False}

    replace = {'roundedcorners': -1, 'center': -1, 'textsize': -1, 'font': -1, 'bold': -1, 'antialiasing': -1,
               'border': -1, 'scalesize': -1, 'glow': -1, 'col': -1, 'clickdownsize': -1, 'clicktype': -1,
               'guesswidth': -1, 'guessheight': -1,
               'textoffsetx': -1, 'textoffsety': -1, 'clickableborder': -1, 'textcenter': -1, 'lines': -1,
               'linesize': -1, 'backingdraw': -1, 'borderdraw': -1, 'animationspeed': -1, 'containedslider': -1,
               'movetoclick': -1, 'darken': -1}
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
