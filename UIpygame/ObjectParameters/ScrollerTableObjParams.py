from dataclasses import dataclass

from UIpygame.ObjectParameters.TableObjParams import TableObjParams

@dataclass
class ScrollerTableObjParams(TableObjParams):
    page_height: int = None
    compress_width: bool | list[int] = True
    scroller_width: int = 15
    screen_cut_off: bool | int = 5
