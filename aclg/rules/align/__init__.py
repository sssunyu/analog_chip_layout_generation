# aclg/rules/align/__init__.py (修改後)
from aclg.dataclass.component import Component
from typing import List
from enum import Enum

class AlignmentMode(str, Enum):
    """定義對齊模式的列舉"""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER_H = "center_horizontal" # 水平置中
    CENTER_V = "center_vertical"   # 垂直置中

def align_components(
        components: List[Component],
        scale_factors: List[float],
        mode: AlignmentMode
) -> List[Component]:
    """
    對已存在的一組元件應用縮放與對齊。

    Args:
        components: 要進行對齊與縮放的元件列表。
        scale_factors: 一個浮點數比例的列表，決定了每個子元件的縮放比例。
        mode: 對齊模式。
    
    Returns:
        回傳修改後的元件列表。
    """
    if len(components) != len(scale_factors):
        raise ValueError(f"元件數量 ({len(components)}) 與比例因子數量 ({len(scale_factors)}) 必須相同。")

    for comp, factor in zip(components, scale_factors):
        if mode in [AlignmentMode.TOP, AlignmentMode.BOTTOM, AlignmentMode.CENTER_H]:
            original_height = comp.height
            new_height = original_height * factor
            if new_height < 0:
                raise ValueError("計算出的新高度不能為負數。")
            comp.height = new_height

            if mode == AlignmentMode.TOP:
                top_edge_y = comp.y - original_height / 2
                comp.y = top_edge_y + comp.height / 2
            elif mode == AlignmentMode.BOTTOM:
                bottom_edge_y = comp.y + original_height / 2
                comp.y = bottom_edge_y - comp.height / 2

        elif mode in [AlignmentMode.LEFT, AlignmentMode.RIGHT, AlignmentMode.CENTER_V]:
            original_width = comp.width
            new_width = original_width * factor
            if new_width < 0:
                raise ValueError("計算出的新寬度不能為負數。")
            comp.width = new_width
            
            if mode == AlignmentMode.LEFT:
                left_edge_x = comp.x - original_width / 2
                comp.x = left_edge_x + comp.width / 2
            elif mode == AlignmentMode.RIGHT:
                right_edge_x = comp.x + original_width / 2
                comp.x = right_edge_x - comp.width / 2
        
        comp.generate_rule = f"align_{mode.value}"

    return components