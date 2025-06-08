import pygame, sys, os

class Utils:

    @staticmethod
    def resourcepath(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @staticmethod
    def loadinganimation(points=12):
        img = []
        for a in range(points):
            img.append('{loading largest=' + str(a) + '}')
        return img

    @staticmethod
    def rectscaler(rect, scale, offset=(0, 0)):
        if not type(scale) in [float, int]:
            return pygame.Rect((rect.x - offset[0]) * scale.dir_scale[0], (rect.y - offset[1]) * scale.dir_scale[1],
                               rect.w * scale.scale, rect.h * scale.scale)
        else:
            return pygame.Rect((rect.x - offset[0]) * scale, (rect.y - offset[1]) * scale, rect.w * scale, rect.h * scale)

    @staticmethod
    def roundRect(x, y, width, height):
        return pygame.Rect(round(x), round(y), round(width), round(height))

    @staticmethod
    def normalizelist(lis, sumto=1):
        total = sum(lis)
        if total > 0:
            newlis = []
            for a in lis:
                newlis.append(a * (sumto / total))
            return newlis
        else:
            return lis

    @staticmethod
    def menuin(objmenu, menulist):
        for a in objmenu:
            if a in menulist:
                return True
        return False

    @staticmethod
    def relativeToValue(st, w, h, ui):
        global returnedexecvalue
        if type(st) == str:
            st = Utils.smartreplace(Utils.smartreplace(st, 'w', w), 'h', h)
            tlocals = {'ui': ui}
            execstring = 'returnedexecvalue=' + st
            exec(execstring, tlocals, globals())
            return returnedexecvalue
        else:
            return st

    @staticmethod
    def smartreplace(st, char, replace):
        # Only replaces when no characters on either side
        lis = list(st)
        alphabet = [chr(a) for a in range(97, 123)]
        nstring = ''
        for i, a in enumerate(lis):
            if a == char and (i == 0 or not (lis[i - 1] in alphabet)) and (
                    i == len(lis) - 1 or not (lis[i + 1] in alphabet)):
                nstring += str(replace)
            else:
                nstring += a
        return nstring

    @staticmethod
    def losslesssplit(text, splitter):
        splitted = text.split(splitter)
        for a in range(len(splitted) - 1):
            splitted[a + 1] = splitter + splitted[a + 1]
        if text[-2:] == splitter:
            splitted.append(splitter)
        return splitted

    @staticmethod
    def emptyFunction():
        pass

    class EmptyObject:
        def __init__(self, x, y, w, h):
            self.x = x
            self.y = y
            self.width = w
            self.height = h
            self.scale = 1
            self.dirscale = [1, 1]
            self.empty = True
            self.active = False
            self.scroll = 0

        def getEnabled(self):
            return True

        def getMenu(self):
            return 'EMPTY_OBJECT'

    class Funcer:
        def __init__(self, func, **args):
            self.func = lambda: func(**args)

