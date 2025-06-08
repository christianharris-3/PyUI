from dataclasses import dataclass

import UIpygame


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
    scale_by: UIpygame.ScaleBy = UIpygame.ScaleBy.MIN
    do_dimension_scale: bool = True
    do_pos_scale: bool = True
    do_scale_x: bool = True
    do_scale_y: bool = True