import pygame, math

class Collision:

    @staticmethod
    def collidepointrects(point, rects):
        for a in rects:
            if a.collidepoint(point):
                return True
        return False

    @staticmethod
    def distance(point1, point2):
        return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5

    @staticmethod
    def distancetorect(point, rect):
        x, y, w, h = rect
        if pygame.Rect(x, y, w, h).collidepoint(point): return 0
        if point[0] < x:
            if point[1] > y:
                if point[1] < y + h:
                    return x - point[0]
                else:
                    return Collision.distance(point, (x, y + h))
            else:
                return Collision.distance(point, (x, y))
        elif point[0] > x + w:
            if point[1] > y:
                if point[1] < y + h:
                    return point[0] - (x + w)
                else:
                    return Collision.distance(point, (x + w, y + h))
            else:
                return Collision.distance(point, (x + w, y))
        else:
            if point[1] > y:
                return y - point[1]
            else:
                return point[1] - (y - h)

    @staticmethod
    def pointdis(point1, point2):
        tot = 0
        for a in range(len(point1)):
            tot += (point1[a] - point2[a]) ** 2
        return tot ** 0.5

    @staticmethod
    def trianglearea(points):
        a = Collision.pointdis(points[2], points[0])
        b = Collision.pointdis(points[1], points[0])
        c = Collision.pointdis(points[2], points[1])
        if b == 0 or c == 0: return 0
        return 0.5 * c * b * math.sin(math.acos(max([min([(b ** 2 + c ** 2 - a ** 2) / (2 * b * c), 1]), -1])))

    @staticmethod
    def trianglecollide(point, poly):
        mainA = Collision.trianglearea(poly)
        A1 = Collision.trianglearea([poly[0], poly[1], point])
        A2 = Collision.trianglearea([poly[0], point, poly[2]])
        A3 = Collision.trianglearea([point, poly[1], poly[2]])
        if A1 + A2 + A3 - 0.000001 > mainA: return False
        return True

    @staticmethod
    def polycollide(point, poly, angle=0.5):
        center = point
        crosses = 0
        dis = 100000
        for a in range(len(poly)):
            awayline = [center, [center[0] + (dis * math.cos(angle / 180 * math.pi)),
                                 center[1] + (dis * math.sin(angle / 180 * math.pi))]]
            collide = Collision.linecross(awayline, [poly[a], poly[a - 1]])
            if collide[0]:
                crosses += 1
        if crosses % 2:
            return True
        return False

    @staticmethod
    def linecross(L1, L2):
        # print(L1,L2)
        ##    x1,x2,x3,x4,y1,y2,y3 ,y4 = L1[0][0],L1[1][0],L2[0][0],L2[1][0],L1[0][1],L1[1][1],L2[0][1],L2[1][1]
        ##    xcross = (x1*(x3*(-2*y1+y2+2*y3-y4)+x4*(2*y1-y2-y3))+x2*(x3*(y1-2*y3+y4)+x4*(y3-y1)))/(y3*(x1-x2)+y4*(x2-x1)+y1*(x4-x3)+y2*(x3-x4))
        a, b, c, d, e, f, g, h = L1[0][0], L1[1][0], L2[0][0], L2[1][0], L1[0][1], L1[1][1], L2[0][1], L2[1][1]
        try:
            xcross = (a * (c * (h - f) + d * (f - g)) + b * (c * (e - h) + d * (g - e))) / (
            (g * (b - a) + h * (a - b) + e * (c - d) + f * (d - c)))
            if abs(a - b) < 0.001:
                ycross = (xcross - c) * ((g - h) / (c - d)) + g
            else:
                ycross = ((e - f) * (xcross - a)) / (a - b) + e

            ##        if xcross<min([a,b]) or xcross>max([a,b]) or ycross<min([e,f]) or ycross>max([e,f]) or xcross<min([c,d]) or xcross>max([c,d]) or ycross<min([g,h]) or ycross>max([g,h]):
            ##            return False,1

            dis = 0.1
            if a < b:
                if xcross < a - dis or xcross > b + dis: return False, 1
            else:
                if xcross < b - dis or xcross > a + dis: return False, 2
            if c < d:
                if xcross < c - dis or xcross > d + dis: return False, 3
            else:
                if xcross < d - dis or xcross > c + dis: return False, 4
            if e < f:
                if ycross < e - dis or ycross > f + dis: return False, 5
            else:
                if ycross < f - dis or ycross > e + dis: return False, 6
            if g < h:
                if ycross < g - dis or ycross > h + dis: return False, 7
            else:
                if ycross < h - dis or ycross > g + dis: return False, 8

            return True, xcross, ycross
        except:
            return False, 9

    @staticmethod
    def linecirclecross(L1, L2):
        # print(L1,L2)
        a, b, c, d = -L1[0][0], -L1[1][0], -L1[0][1], -L1[1][1]
        p, q, r = L2[0][0], L2[0][1], L2[1]
        if c - d == 0:
            m = 0
            i = m * a - c
            A = (m ** 2 + 1)
            B = 2 * (m * i - m * q - p)
        elif a - b == 0:
            m = 1000000000
            i = a
            A = 1
            B = 2 * p
        else:
            m = (c - d) / (a - b)
            i = m * a - c
            A = (m ** 2 + 1)
            B = 2 * (m * i - m * q - p)
        C = (q ** 2 - r ** 2 + p ** 2 - 2 * i * q + i ** 2)
        if B ** 2 - 4 * A * C < 0:
            return False, 2
        ##    ycross1 = (m*(((-B)+math.sqrt(B**2-4*A*C))/(2*A))+i)
        ##    ycross2 = (m*(((-B)-math.sqrt(B**2-4*A*C))/(2*A))+i)
        xcross1 = (((-B) + math.sqrt(B ** 2 - 4 * A * C)) / (2 * A))
        xcross2 = (((-B) - math.sqrt(B ** 2 - 4 * A * C)) / (2 * A))
        ycross1 = (m * xcross1 + i)
        ycross2 = (m * xcross2 + i)
        dis = 0
        passed = [True, True]
        a, b, c, d = -a, -b, -c, -d
        if a < b:
            if xcross1 < a - dis or xcross1 > b + dis:
                passed[0] = False
        elif b < a:
            if xcross1 < b - dis or xcross1 > a + dis:
                passed[0] = False
        if c < d:
            if ycross1 < c - dis or ycross1 > d + dis:
                passed[0] = False
        elif d < c:
            if ycross1 < d - dis or ycross1 > c + dis:
                passed[0] = False
        if a < b:
            if xcross2 < a - dis or xcross2 > b + dis:
                passed[1] = False
        elif b < a:
            if xcross2 < b - dis or xcross2 > a + dis:
                passed[1] = False
        if c < d:
            if ycross2 < c - dis or ycross2 > d + dis:
                passed[1] = False
        elif d < c:
            if ycross2 < d - dis or ycross2 > c + dis:
                passed[1] = False
        if passed[0]:
            return True, [xcross1, ycross1]
        if passed[1]:
            return True, [xcross2, ycross2]
        return False, 0