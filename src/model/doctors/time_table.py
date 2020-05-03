from dataclasses import dataclass
from typing import List


@dataclass
class Interval:
    from_time: str
    to_time: str


@dataclass
class TimeTable:
    day: str
    intervals: List[Interval]
