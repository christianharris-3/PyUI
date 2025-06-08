from dataclasses import dataclass
from UIpygame.Utils.Utils import Utils
import pygame

@dataclass
class ClickableData:
    """
    Dataclass containing data used by all children of GuiItem.
    """
    clickable: bool = True
    clickable_rect: pygame.Rect | tuple[float, float, float, float] = None
    command: callable = Utils.emptyFunction
    run_command_at: int = 0

