from abc import ABC, abstractmethod

import pygame.locals


class widget(ABC):
    def __init__(self,dataclassobject):
        print('widget made')
        # self.hi()




class style(widget):
    def __init__(self,dataclassobject):
        print("style started")
        super().__init__(dataclassobject)
        print("style finished")

class positional(widget):
    def __init__(self, dataclassobject):
        print('positional started')
        super().__init__(dataclassobject)
        print('positional finished')
    def funced(self):
        print("a")

class clickable(positional, widget):
    def __init__(self, dataclassobject):
        print('positional started')
        super().__init__(dataclassobject)
        print('positional finished')
    def funced(self):
        print("a")

class scrollable(positional, widget):
    def __init__(self, dataclassobject):
        print('positional started')
        super().__init__(dataclassobject)
        print('positional finished')

class button(positional, style):
    def __init__(self, dataclassobject):
        print('button started')
        super().__init__(dataclassobject)
        print('button finished')
        self.funced()

class scroller(scrollable, clickable, positional, style):
    def __init__(self, dataclassobject):
        print('button started')
        super().__init__(dataclassobject)
        print('button finished')
        self.funced()

# obj = button("kiouiojsiof")
# obj = widget("afasd")
# new = widget(2)
