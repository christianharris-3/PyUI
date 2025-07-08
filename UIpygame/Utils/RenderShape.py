import pygame
import re
import math
from UIpygame.Utils.Draw import Draw

class RenderShape:
    def __init__(self):
        self.rounded_bezier = True
        self.render_shape_functions = {
            'tick': RenderShape.renderShapeTick,
            'cross': RenderShape.renderShapeCross,
            'arrow': RenderShape.renderShapeArrow,
            'settings': RenderShape.renderShapeSettings,
            'play': RenderShape.renderShapePlay,
            'pause': RenderShape.renderShapePause,
            'skip': RenderShape.renderShapeSkip,
            'circle': RenderShape.renderShapeCircle,
            'rect': RenderShape.renderShapeRect,
            'clock': RenderShape.renderShapeClock,
            'loading': RenderShape.renderShapeLoading,
            'dots': RenderShape.renderShapeDots,
            'logo': RenderShape.renderShapeLogo
        }
        self.rendered_shapes = {}
        
    def renderShape(self, name, size, col=None, failmessage=True, backcol=(255, 255, 255)):
        name = name.strip()
        col = col or self.styleGet("text_col")
        if col == backcol: backcol = (0, 0, 0)

        # if 'col=' in name:
        #     try:
        #         c = name.split('col=')[1].split('(')[1].split(')')[0].split(',')
        #         col = (int(c[0]), int(c[1]), int(c[2]))
        #     except:
        #         pass
        # if 'scale=' in name:
        #     size *= float(name.split('scale=')[1].split(' ')[0])

        if str([name, size, col, backcol]) in self.rendered_shapes:
            return self.rendered_shapes[str([name, size, col, backcol])]
        if len(name) > 0 and name[0] == '"':
            surf = self.renderShapetext(name, size, col, backcol)
        elif name.split(' ')[0] in self.render_shape_functions:
            surf = self.render_shape_functions[name.split(' ')[0]](name, size, col, backcol)
        else:
            surf, worked, backcol = self.renderShapebezier(name, size, col, backcol, failmessage)
            if not worked:
                surf = self.renderShapetext(name, size, col, backcol)
                
        keywords = name.split('"')[-1].split()
        if 'left' in keywords:
            surf = pygame.transform.flip(surf, True, False)
        elif 'up' in keywords:
            surf = pygame.transform.rotate(surf, 90)
        elif 'down' in keywords:
            surf = pygame.transform.rotate(surf, -90)
        surf.set_colorkey(backcol)
        self.rendered_shapes[str([name, size, col, backcol])] = surf
        return surf

    @staticmethod
    def renderShapeTick(name, size, col, backcol):
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

    @staticmethod
    def renderShapeArrow(name, size, col, backcol):
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

    @staticmethod
    def renderShapeCross(name, size, col, backcol):
        vals = self.getshapedata(name, ['width'], [0.1])
        width = vals[0]
        surf = pygame.Surface((size + 1, size + 1))
        surf.fill(backcol)
        Draw.roundedline(surf, col, (size * width, size * width), (size * (1 - width), size * (1 - width)),
                         size * width)
        Draw.roundedline(surf, col, (size * (1 - width), size * width), (size * width, size * (1 - width)),
                         size * width)
        return surf

    @staticmethod
    def renderShapeSettings(name, size, col, backcol, antialiasing=True):
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

    @staticmethod
    def renderShapeLogo(name, size, col, backcol, antialiasing=True):
        surf = pygame.Surface((size, size))
        surf.fill(backcol)
        surf = self.renderShapesettings(name, size, (66, 129, 180), backcol, antialiasing)
        self.write(surf, size * 0.5, size * 0.5, 'PyUI', size * (360 / 600), (62, 63, 75), True,
                   antialiasing=antialiasing)
        self.write(surf, size * 0.5, size * 0.5, 'PyUI', size * (380 / 600), (253, 226, 93), True,
                   antialiasing=antialiasing)
        return surf

    @staticmethod
    def renderShapePlay(name, size, col, backcol):
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

    @staticmethod
    def renderShapePause(name, size, col, backcol):
        surf = pygame.Surface((size * 0.75, size))
        surf.fill(backcol)
        vals = self.getshapedata(name, ['rounded'], [0.0])
        rounded = vals[0]
        Draw.rect(surf, col, pygame.Rect(0, 0, size * 0.25, size), border_radius=int(size * rounded))
        Draw.rect(surf, col, pygame.Rect(size * 0.5, 0, size * 0.25, size), border_radius=int(size * rounded))
        return surf

    @staticmethod
    def renderShapeSkip(name, size, col, backcol):
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
        surf.blit(self.renderShapeplay(name, size, col, backcol), (-realign, 0))
        Draw.rect(surf, col, pygame.Rect(size + size * offset, 0, size * thickness, size),
                  border_radius=int(size * rounded))
        return surf

    @staticmethod
    def renderShapeCircle(name, size, col, backcol):
        vals = self.getshapedata(name, ['width'], [1])
        width = vals[0]
        surf = pygame.Surface((size * width, size))
        surf.fill(backcol)
        pygame.draw.ellipse(surf, col, pygame.Rect(0, 0, size * width, size))
        return surf

    @staticmethod
    def renderShapeRect(name, size, col, backcol):
        vals = self.getshapedata(name, ['rounded', 'width'], [0, size])
        rounded = vals[0]
        width = vals[1] * self.scale
        surf = pygame.Surface((width, size))
        surf.fill(backcol)
        Draw.rect(surf, col, pygame.Rect(0, 0, width, size), border_radius=int(size * rounded))
        return surf

    @staticmethod
    def renderShapeClock(name, size, col, backcol):
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

    @staticmethod
    def renderShapeLoading(name, size, col, backcol):
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

    @staticmethod
    def renderShapeDots(name, size, col, backcol):
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

    @staticmethod
    def renderShapeText(name, size, col, backcol):
        vals = self.getshapedata(name, ['font', 'bold', 'italic', 'strikethrough', 'underlined', 'antialias'],
                                 [self.styleGet('font'), False, False, False, False, True])
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

    @staticmethod
    def renderShapeBezier(name, size, col, backcol, failmessage):
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
            for a in list(self.in_built_images):
                if len(name) > 0 and name.split()[0] == a:
                    img = self.in_built_images[a]
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
                                             range(len(a))], 0, False, detail=detail, rounded=self.rounded_bezier)
            pygame.draw.polygon(surf, col, points)
        return surf, True, backcol

    def extractShapeDataFromName(self, name, variables, defaults):
        vals = defaults
        if sum([a in name for a in variables]) > 0:
            namesplit = name.split()
            for a in namesplit:
                for i, b in enumerate(variables):
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

    @staticmethod
    def parseName(name: str) -> tuple(str, dict, bool):
        if len(name) == 0:
            return "", {}, False

        is_text = False

        start_char = name[0]
        if start_char == "'" or start_char == '"':
            segments = name.split(start_char)
            if len(segments) != 3:
                raise Exception(f"Invalid renderShape name \"{name}\": Wrong string syntax for renderShapeText")

            is_text = True
            shape_name = segments[1]
            shape_args = RenderShape.parseArguments(segments[2])
        else:
            segments = name.split(" ",1)
            shape_name = segments[0]
            if len(segments) == 2:
                shape_args = RenderShape.parseArguments(segments[1])
            else:
                shape_args = {}

        return shape_name, shape_args, is_text


    @staticmethod
    def parseArguments(args_string: str) -> dict:
        split_arg_strings = args_string.split(" ")
        args = {}

        for arg_string in split_arg_strings:
            key_value_pair = arg_string.split("=")

            if len(key_value_pair) == 1:
                key = key_value_pair[0]
                value = True
            else:
                key, value_str = key_value_pair

                try:
                    value = float(value_str)
                except ValueError:
                    if value_str.lower() == 'true':
                        value = True
                    elif value_str.lower() == 'false':
                        value = False
                    else:
                        value = value_str

            args[key] = value

        return args

    @staticmethod
    def parseColor(col_string: str) -> pygame.Color:
        # matches all nums 0-255
        num_parse = r"1\d\d|2[0-4]\d|25[0-5]|\d{1,2}"

        rgb_values = re.findall(num_parse, col_string)

        if len(rgb_values) < 3 or len(rgb_values) > 4:
            raise Exception(f"Invalid Color string {col_string}")

        return pygame.Color(rgb_values)


