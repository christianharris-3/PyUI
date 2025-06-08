from dataclasses import dataclass, field, replace,fields

import dataclasses

@dataclass
class PositionalData:
    """
    Dataclass containing data used by all children of GuiItem.
    """
    x: int|float = 0
    y: int|float = 0
    width: int|float = 0
    height: int|float = 0
    ID: str = None
    layer: int = None
    bound_items: list = None
    kill_time: int|float= None
    anchor: list[list[int|float]] = None
    obj_anchor: list[list[int|float]] = None
    enabled_bool: bool = True
    center: bool = False





