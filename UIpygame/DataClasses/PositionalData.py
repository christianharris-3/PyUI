from dataclasses import dataclass

from UIpygame.Constants import ScaleBy


@dataclass
class PositionalData:
    """
    Dataclass containing data used by all children of GuiItem.
    """
    x: int|float|str = 0
    y: int|float|str = 0
    width: int|float|str = 0
    height: int|float|str = 0
    anchor: list[int|float|str] = None
    obj_anchor: list[int|float|str] = None
    center: bool = False
    scale_by: ScaleBy = ScaleBy.MIN
    do_dimensions_scaling: bool|list[bool,bool] = True
    do_pos_scaling: bool|list[bool,bool] = True
