import pygame
import math
from UIpygame.Utils.Utils import Utils
from UIpygame.Utils.ColEdit import ColEdit
import pygame.gfxdraw

class Draw:
    @staticmethod
    def bezierpoints(roots, progress, detail):
        # print(roots)
        npoints = []
        for a in range(len(roots) - 1):
            npoints.append((roots[a][0] + (roots[a + 1][0] - roots[a][0]) * (progress / detail),
                            roots[a][1] + (roots[a + 1][1] - roots[a][1]) * (progress / detail)))
        if len(npoints) > 0:
            point = Draw.bezierpoints(npoints, progress, detail)
        else:
            point = roots[0]
        return point

    @staticmethod
    def bezierdrawer(points, width, commandpoints=True, detail=200, rounded=True):
        curvepoints = []
        for a in range(detail):
            curvepoints.append(Draw.bezierpoints(points, a, detail))
        curvepoints.append(points[-1])
        # if commandpoints:
        #     pygame.draw.aalines(screen, (0, 0, 0), False, curvepoints)
        #     if len(points) == 4:
        #         pygame.draw.line(screen, (100, 100, 100), points[0], points[1])
        #         pygame.draw.line(screen, (100, 100, 100), points[2], points[3])
        #     else:
        #         pygame.draw.lines(screen, (100, 100, 100), False, points)
        if rounded:
            final = []
            prev = 0
            for a in curvepoints:
                if (round(a[0]), round(a[1])) != prev:
                    final.append((round(a[0]), round(a[1])))
                    prev = (round(a[0]), round(a[1]))
            return final
        return curvepoints

    @staticmethod
    def roundedline(surf, col, point1, point2, width, circles=True):
        if point1[0] - point2[0] != 0:
            grad = (point1[1] - point2[1]) / (point1[0] - point2[0])
            if grad != 0:
                invgrad = -1 / grad
            else:
                invgrad = 100000
        else:
            invgrad = 0
        ang = math.atan(invgrad)
        points = [(point1[0] + math.cos(ang) * width, point1[1] + math.sin(ang) * width),
                  (point1[0] - math.cos(ang) * width, point1[1] - math.sin(ang) * width),
                  (point2[0] - math.cos(ang) * width, point2[1] - math.sin(ang) * width),
                  (point2[0] + math.cos(ang) * width, point2[1] + math.sin(ang) * width)]
        pygame.gfxdraw.aapolygon(surf, points, col)
        pygame.gfxdraw.filled_polygon(surf, points, col)
        if circles:
            Draw.circle(surf, col, point1, width)
            Draw.circle(surf, col, point2, width)

    @staticmethod
    def rect(surf, col, rect, width=0, border_radius=0):
        x, y, w, h = rect
        radius = abs(int(min([border_radius, rect[2] / 2, rect[3] / 2])))
        if border_radius != 0 and (radius * (1 + (2 ** 0.5) / 2) < width or width == 0) and width>0:
            try:
                pygame.gfxdraw.aacircle(surf, x + radius, y + radius, radius, col)
                pygame.gfxdraw.aacircle(surf, x + w - radius - 1, y + radius, radius, col)
                pygame.gfxdraw.aacircle(surf, x + w - radius - 1, y + h - radius - 1, radius, col)
                pygame.gfxdraw.aacircle(surf, x + radius, y + h - radius - 1, radius, col)
            except:
                ## catches error with integer overflow when drawn at large coordinates
                pass
        pygame.draw.rect(surf, col, Utils.roundRect(x, y, w, h), int(width), int(border_radius))

    @staticmethod
    def circle(surf, col, center, radius, width=0):
        try:
            pygame.gfxdraw.aacircle(surf, int(center[0]), int(center[1]), int(radius), col)
            if width == 0:
                pygame.gfxdraw.filled_circle(surf, int(center[0]), int(center[1]), int(radius), col)
            else:
                pygame.draw.circle(surf, col, center, radius, width)
                pygame.gfxdraw.aacircle(surf, int(center[0]), int(center[1]), int(radius - width), col)

        except:
            ## catches error with integer overflow when drawn at large coordinates
            pass

    @staticmethod
    def polygon(surf, col, points):
        pygame.gfxdraw.aapolygon(surf, points, col)
        pygame.gfxdraw.filled_polygon(surf, points, col)

    @staticmethod
    def glow(surf, rect, distances, col, scale=1, detail=-1, shade=100, roundedcorners=-1):
        if distances != 0:
            if type(distances) == int: distances = [distances for a in range(4)]
            if roundedcorners == -1: roundedcorners = max(distances)
            colorkey = (255, 255, 255)
            if col == colorkey: colorkey = (0, 0, 0)

            if len(col) == 3:
                col = [col[0], col[1], col[2], 1]
            else:
                shade = col[3]
            shade = round(shade)

            if detail == -1:
                detail = int(shade)
                col = list(col)
                col[3] = 1
            count = detail

            a = detail
            for r in range(shade):
                while a > (1 - r / shade) * detail:
                    a -= 1
                w = rect.width + (a / detail) * (distances[1] + distances[3])
                h = rect.height + (a / detail) * (distances[0] + distances[2])
                rec = pygame.Surface((w, h), pygame.SRCALPHA)
                pygame.draw.rect(rec, col, pygame.Rect(0, 0, w, h), 0,
                                 int(roundedcorners - (1 - a / detail) * distances[0]))
                ##                print(rec,(rect.x-(a/detail)*distances[3],rect.y-(a/detail)*distances[0]))
                surf.blit(rec, (rect.x - (a / detail) * distances[3], rect.y - (a / detail) * distances[0]))

    @staticmethod
    def pichart(surf, center, radius, col, ang1, ang2=0, innercol=-1, border_size=2):
        Draw.circle(surf, col, [center[0], center[1]], radius)
        if ang1 != ang2:
            innercol = ColEdit.autoShiftCol(innercol, col, -20)
            rad = radius - border_size
            Draw.circle(surf, innercol, [center[0], center[1]], rad)
            temp = ang1
            ang1 = ang2
            ang2 = temp
            diff = (ang1 - ang2) % (math.pi * 2)
            poly = [[center[0], center[1]]]
            segments = max(int(radius * diff), 1)
            rad += 1
            for a in range(segments + 1):
                poly.append([center[0] - rad * math.sin(ang2 + diff * a / segments),
                             center[1] - rad * math.cos(ang2 + diff * a / segments)])
            Draw.polygon(surf, col, poly)

    @staticmethod
    def blitroundedcorners(surf, surfto, x, y, roundedcorners, area=None):
        if area == None:
            area = surf.get_rect()
        area.normalize()
        mask = pygame.Surface(area.size, pygame.SRCALPHA)
        Draw.rect(mask, (255, 255, 255), (0, 0, area.width, area.height), border_radius=roundedcorners)
        nsurf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        nsurf.blit(surf, (0, 0))
        nsurf.blit(mask, (area.x, area.y), special_flags=pygame.BLEND_RGBA_MIN)
        surfto.blit(nsurf, (x, y), area)

