from aclg.dataclass.component import Component
from aclg.rules.spacing import spacing_horizontal, spacing_vertical
from typing import List
from enum import Enum

class AlignmentMode(str, Enum):
    """定義對齊模式的列舉，增加程式碼的穩健性和可讀性。"""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    CENTER_H = "center_horizontal" # 水平置中
    CENTER_V = "center_vertical"   # 垂直置中

# --- 新增的高階函式 ---
def create_aligned_components(
        component: Component,
        scale_factors: List[float],
        mode: AlignmentMode
) -> List[Component]:
    """
    一步到位地生成一排對齊的子元件。
    此函式會先根據對齊模式自動決定水平或垂直分割，然後應用縮放與對齊。

    Args:
        parent_component: 要在其內部生成子元件的父元件。
        scale_factors: 一個浮點數比例的列表，決定了每個子元件的縮放比例。
                       列表的長度也決定了要生成的子元件數量。
        mode: 對齊模式，同時也決定了元件是水平還是垂直排列。

    Returns:
        一個包含所有已生成並對齊的子元件的列表。
    """
    num_components = len(scale_factors)
    if num_components == 0:
        return []

    # 1. 根據對齊模式，自動呼叫 spacing_horizontal 或 spacing_vertical
    if mode in [AlignmentMode.TOP, AlignmentMode.BOTTOM, AlignmentMode.CENTER_H]:
        # 這些模式適用於水平排列
        initial_components = spacing_horizontal(component, num_components=num_components)
    elif mode in [AlignmentMode.LEFT, AlignmentMode.RIGHT, AlignmentMode.CENTER_V]:
        # 這些模式適用於垂直排列
        initial_components = spacing_vertical(component, num_components=num_components)
    else:
        raise ValueError(f"不支援的對齊模式: {mode}")

    # 2. 呼叫底層的對齊函式來修改尺寸和位置
    aligned_components = _align_and_scale_components(initial_components, scale_factors, mode)
    
    return aligned_components

# --- 底層的輔助函式 (原 align_components，加上您的修改並重新命名) ---
def _align_and_scale_components(
        components: List[Component],
        scale_factors: List[float],
        mode: AlignmentMode
) -> List[Component]:
    """
    (輔助函式) 對已存在的一組元件應用縮放與對齊。
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
        
        # 更新 generate_rule (根據您的要求)
        comp.generate_rule = f"align_{mode.value}"

    return components