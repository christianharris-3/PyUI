from dataclasses import dataclass

from UIpygame.ObjectParameters.ButtonObjParams import ButtonObjParams


@dataclass
class DropDownObjParams(ButtonObjParams):
    ID = "Dropdown"
    options: list[str] = None
    drops_down = False # TODO separate into different object