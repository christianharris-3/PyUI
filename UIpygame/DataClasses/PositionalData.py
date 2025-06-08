from dataclasses import dataclass

@dataclass
class PositionalData:
    """
    Dataclass containing data used by all children of GuiItem.
    """
    x: int|float = 0
    y: int|float = 0
    width: int|float = 0
    height: int|float = 0
    anchor: list[list[int | float]] = None
    obj_anchor: list[list[int | float]] = None
    center: bool = False