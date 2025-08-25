# aclg/rules/split_ratio.py
from typing import List
from enum import Enum
from aclg.dataclass.component import Component

class SplitOrientation(str, Enum):
    """定義分割方向"""
    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

def split_by_ratio(
        component: Component,
        ratios: List[float],
        orientation: SplitOrientation = SplitOrientation.HORIZONTAL
) -> List[Component]:
    """
    根據指定的比例列表，將一個元件水平或垂直地分割成多個子元件。

    Args:
        component: 要被分割的父元件。
        ratios: 一個浮點數的列表，定義了每個子元件的相對尺寸。
        orientation: 分割的方向。

    Returns:
        一個包含所有已生成子元件的列表。
    """
    if not ratios:
        return []
    
    total_ratio = sum(ratios)
    if total_ratio <= 0:
        raise ValueError("比例總和必須大於 0。")

    parent = component
    new_components = []
    
    if orientation == SplitOrientation.HORIZONTAL:
        # 水平分割 (沿 Y 軸)
        parent_start_y = parent.y - parent.height / 2
        current_y = parent_start_y
        
        for ratio in ratios:
            sub_height = parent.height * (ratio / total_ratio)
            center_y = current_y + sub_height / 2
            
            sub_comp = Component(
                x=parent.x,
                y=center_y,
                width=parent.width,
                height=sub_height,
                generate_rule=f"split_ratio_{orientation.value}"
            )
            new_components.append(sub_comp)
            current_y += sub_height

    elif orientation == SplitOrientation.VERTICAL:
        # 垂直分割 (沿 X 軸)
        parent_start_x = parent.x - parent.width / 2
        current_x = parent_start_x

        for ratio in ratios:
            sub_width = parent.width * (ratio / total_ratio)
            center_x = current_x + sub_width / 2

            sub_comp = Component(
                x=center_x,
                y=parent.y,
                width=sub_width,
                height=parent.height,
                generate_rule=f"split_ratio_{orientation.value}"
            )
            new_components.append(sub_comp)
            current_x += sub_width
            
    return new_components

# --- 新增的強力分割工具 ---
def split_by_ratio_grid(
        component: Component,
        h_ratios: List[float],
        v_ratios: List[float]
) -> List[Component]:
    """
    根據指定的水平和垂直比例，將一個元件分割成一個比例網格。

    Args:
        component: 要被分割的父元件。
        h_ratios: 定義網格中每一「列」高度的比例列表。
        v_ratios: 定義網格中每一「行」寬度的比例列表。

    Returns:
        一個包含所有網格內子元件的列表。
    """
    final_components = []
    
    # 1. 首先，根據水平比例 (h_ratios) 將父元件切成多個水平長條 (rows)
    horizontal_strips = split_by_ratio(component, h_ratios, SplitOrientation.HORIZONTAL)
    
    # 2. 然後，對每一個水平長條，再進行垂直分割 (v_ratios)
    for strip in horizontal_strips:
        # 對這個長條進行垂直分割
        grid_cells = split_by_ratio(strip, v_ratios, SplitOrientation.VERTICAL)
        # 將分割出的網格元件加入最終列表
        final_components.extend(grid_cells)
        
    # 更新 generate_rule，使其能反映這是一個網格操作
    for comp in final_components:
        comp.generate_rule = "split_by_ratio_grid"
        
    return final_components