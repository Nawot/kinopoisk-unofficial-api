from dataclasses import dataclass


@dataclass
class BaseFilter:
    id : int = None
    name : str = None
