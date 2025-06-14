import numpy as np
import pygame, sys, os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UIpygame.UI import UI

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
    def initialPosToValuePos(
            pos: list[int|float|str, int|float|str],
            parent_dimensions: list[int|float, int|float],
            ui: UI,
    ) -> np.array:
        """
        Converts a list of 2 pos strings into real positions.
        :param pos: The position, list of 2 items each of which can be ints or pos strings
        :param parent_dimensions: a list of 2 items, storing the width and height of the parent pos
        :param ui: The main instances of the ui object
        :return: np.array storing the true int/float x and y pos
        """
        return np.array([
            Utils.relativeToValue(pos[0], parent_dimensions[0], parent_dimensions[1], ui),
            Utils.relativeToValue(pos[1], parent_dimensions[0], parent_dimensions[1], ui)
        ])

    @staticmethod
    def getBaseDirScaleValue(
            dir_scale: list[float, float] ,
            do_scaling: bool|list[bool, bool]
    ) -> list[float, float]:
        """
        Converts a do_scaling var and a base dir_scale var into an output dir_scale value
        e.g. dir_scale = [1.5, 2.0], do_scale=[False,True], return = [1.0, 2.0]
        :param dir_scale: the base dir_scale value
        :param do_scaling: a bool or 2 bools that controls if scaling will be applied
        :return: the output 2 item list, the new dir_scale
        """
        if isinstance(do_scaling, bool):
            do_scaling = [do_scaling, do_scaling]

        output_dir_scale = [1, 1]

        if do_scaling[0]:
            output_dir_scale[0] = dir_scale[0]
        if do_scaling[1]:
            output_dir_scale[1] = dir_scale[1]

        return output_dir_scale


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

