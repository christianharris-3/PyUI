from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from UIpygame.UI import UI

@dataclass
class ObjectData:
    """
    Dataclass containing data used by all children of GuiItem.
    """
    ID: str = "Object"
    ui: 'UI' = None
    layer: int = None
    bound_items: list = None
    kill_time: int | float = None
    enabled: bool = True
    refresh_bind: list[str] = None