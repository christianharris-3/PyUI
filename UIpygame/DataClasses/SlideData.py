from dataclasses import dataclass


@dataclass
class SlideData:
    start_value: int | float = 0
    min_value: int | float = 0
    max_value: int | float = 100
