import pygame

class ColEdit:

    @staticmethod
    def colav(col1, col2, weight):
        if len(col1) == 3:
            return (col1[0] + (col2[0] - col1[0]) * weight, col1[1] + (col2[1] - col1[1]) * weight,
                    col1[2] + (col2[2] - col1[2]) * weight)
        else:
            return (col1[0] + (col2[0] - col1[0]) * weight, col1[1] + (col2[1] - col1[1]) * weight,
                    col1[2] + (col2[2] - col1[2]) * weight, col1[3] + (col2[3] - col1[3]) * weight)

    @staticmethod
    def genfade(colourlist, sizeperfade):
        cols = []
        for a in range(len(colourlist) - 1):
            for b in range(sizeperfade):
                cols.append(ColEdit.colav(colourlist[a], colourlist[a + 1], b / sizeperfade))
        return cols

    @staticmethod
    def RGBtoHSV(rgb):
        rp = rgb[0] / 255
        gp = rgb[1] / 255
        bp = rgb[2] / 255
        cmax = max(rp, gp, bp)
        cmin = min(rp, gp, bp)
        delta = cmax - cmin
        H = 0
        if cmax - cmin != 0:
            if cmax == rp:
                H = (60 * (0 + (gp - bp) / (cmax - cmin))) % 360
            elif cmax == gp:
                H = (60 * (2 + (bp - rp) / (cmax - cmin))) % 360
            elif cmax == bp:
                H = (60 * (4 + (rp - gp) / (cmax - cmin))) % 360

        if cmax == 0:
            S = 0
        else:
            S = delta / cmax
        V = cmax
        return H, S, V

    @staticmethod
    def shiftcolor_hsva(col, shift):
        col = pygame.color.Color(col)
        col.hsva = (col.hsva[0], col.hsva[1], max([min([100, col.hsva[2] + shift / 2.55]), 0]), col.hsva[3])
        return col

    @staticmethod
    def shiftcolor_rgb(col, shift):
        return [max([min([255, a + shift]), 0]) for a in col]

    @staticmethod
    def shiftcolor(col, shift):
        # if Style.defaults['hsvashift']:
        #     return shiftcolor_hsva(col, shift)
        # else:
        return ColEdit.shiftcolor_rgb(col, shift)

    @staticmethod
    def autoshiftcol(col, default=(150, 150, 150), editamount=0):
        if type(col) == int:
            if col != -1:
                editamount = col
            col = default
            return ColEdit.shiftcolor(col, editamount)
        return col