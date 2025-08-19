# component.py
from dataclasses import dataclass

@dataclass
class Component:
    """
    用於表示電路中一個元件（或一個區域）的資料結構
    """
    x: float          # 左下角的 x 座標
    y: float          # 左下角的 y 座標
    width: float      # 寬度
    height: float     # 高度
    group_id: int     # 用於表示關聯性，來自同一個初始元件的 group_id 相同
    level: int = 0    # 用於追蹤切割的遞迴深度