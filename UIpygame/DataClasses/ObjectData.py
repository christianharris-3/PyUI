from dataclasses import dataclass


@dataclass
class ObjectData:
    """
    Dataclass containing data used by all children of GuiItem.
    """
    ID: str = "Object"
    layer: int = None
    bound_items: list = None
    kill_time: int | float = None
    enabled: bool = True
    refresh_bind: list[str] = None