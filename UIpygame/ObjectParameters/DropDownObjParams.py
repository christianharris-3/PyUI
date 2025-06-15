from dataclasses import dataclass

from UIpygame.ObjectParameters.ButtonObjParams import ButtonObjParams


@dataclass
class DropDownObjParams(ButtonObjParams):
    ID: str = "Dropdown"
    options: list[str] = None
    animation_speed: int = 15
    drops_down: bool = False # TODO separate into different object