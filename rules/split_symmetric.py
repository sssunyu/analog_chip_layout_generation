# rules/split_symmetric.py
from typing import List
from component import Component
from .split_basic import split_vertical, split_horizontal, split_quadrants

def split_mirrored_vertical(component: Component, ratio_h: float = 0.5, gap: float = 0.01) -> List[Component]:
    """
    先垂直對半切，然後對左半邊和右半邊進行水平切割，但使用相反的比例，形成鏡像對稱。
    - comp -> | | -> |-| + |-| (mirrored)
    """
    if component.width <= gap or component.height <= 2 * gap:
        return [component]

    # 1. 垂直對半切
    halves = split_vertical(component, ratio=0.5, gap=gap)
    if len(halves) < 2:
        return [component]

    # 2. 對左半邊和右半邊使用相反的比例進行水平切割
    left_splits = split_horizontal(halves[0], ratio=ratio_h, gap=gap)
    right_splits = split_horizontal(halves[1], ratio=1 - ratio_h, gap=gap) # 鏡像比例

    # 確保切割成功
    if len(left_splits) < 2 or len(right_splits) < 2:
        return [component]
        
    # 重新排序，讓視覺上更容易理解
    # [top-left, bottom-left, top-right, bottom-right]
    return [left_splits[1], left_splits[0], right_splits[0], right_splits[1]]

def split_mirrored_horizontal(component: Component, ratio_v: float = 0.5, gap: float = 0.01) -> List[Component]:
    """
    先水平對半切，然後對上半邊和下半邊進行垂直切割，但使用相反的比例，形成鏡像對稱。
    - comp -> - -> = + = (mirrored)
    """
    if component.height <= gap or component.width <= 2 * gap:
        return [component]

    # 1. 水平對半切
    halves = split_horizontal(component, ratio=0.5, gap=gap)
    if len(halves) < 2:
        return [component]
        
    # 2. 對上半邊和下半邊使用相反的比例進行垂直切割
    top_splits = split_vertical(halves[1], ratio=ratio_v, gap=gap)
    bottom_splits = split_vertical(halves[0], ratio=1 - ratio_v, gap=gap) # 鏡像比例

    if len(top_splits) < 2 or len(bottom_splits) < 2:
        return [component]

    # [top-left, top-right, bottom-left, bottom-right]
    return [top_splits[0], top_splits[1], bottom_splits[0], bottom_splits[1]]

def split_common_centroid_quadrants(component: Component, gap: float = 0.01) -> List[Component]:
    """
    切割成四個完全相同的象限，形成共質心(Point Symmetry)結構。
    這是 split_quadrants 的一個特例，強制使用 0.5 的比例。
    """
    return split_quadrants(component, ratio_v=0.5, ratio_h=0.5, gap=gap)

def split_symmetric_triplet_vertical(component: Component, ratio_w: float = 0.25, gap: float = 0.01) -> List[Component]:
    """
    垂直切割成三個元件，其中左右兩個元件的寬度相同。
    ratio_w 代表側邊元件佔總寬度的比例。
    """
    if ratio_w <= 0 or ratio_w >= 0.5: return [component] # 比例必須合理
    total_gap = 2 * gap
    if component.width <= total_gap: return [component]

    w_side = (component.width - total_gap) * ratio_w
    w_center = (component.width - total_gap) * (1 - 2 * ratio_w)

    if w_side <= 0 or w_center <= 0: return [component]

    comp_left = Component(component.x, component.y, w_side, component.height, component.group_id, component.level + 1)
    
    center_x = component.x + w_side + gap
    comp_center = Component(center_x, component.y, w_center, component.height, component.group_id, component.level + 1)
    
    right_x = center_x + w_center + gap
    comp_right = Component(right_x, component.y, w_side, component.height, component.group_id, component.level + 1)
    
    return [comp_left, comp_center, comp_right]

def split_symmetric_triplet_horizontal(component: Component, ratio_h: float = 0.25, gap: float = 0.01) -> List[Component]:
    """
    水平切割成三個元件，其中上下兩個元件的高度相同。
    ratio_h 代表側邊元件佔總高度的比例。
    """
    if ratio_h <= 0 or ratio_h >= 0.5: return [component] # 比例必須合理
    total_gap = 2 * gap
    if component.height <= total_gap: return [component]

    h_side = (component.height - total_gap) * ratio_h
    h_center = (component.height - total_gap) * (1 - 2 * ratio_h)
    
    if h_side <= 0 or h_center <= 0: return [component]

    comp_bottom = Component(component.x, component.y, component.width, h_side, component.group_id, component.level + 1)
    
    center_y = component.y + h_side + gap
    comp_center = Component(component.x, center_y, component.width, h_center, component.group_id, component.level + 1)
    
    top_y = center_y + h_center + gap
    comp_top = Component(component.x, top_y, component.width, h_side, component.group_id, component.level + 1)

    return [comp_bottom, comp_center, comp_top]