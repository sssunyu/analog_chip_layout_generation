# component.py
from dataclasses import dataclass

@dataclass
class Component:
    """
    用於表示電路中一個元件（或一個區域）的資料結構
    """
    x: float
    y: float
    width: float
    height: float
    group_id: int
    level: int = 0