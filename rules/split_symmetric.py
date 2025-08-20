# rules/split_symmetric.py
from typing import List
from component import Component
from .split_basic import split_vertical, split_horizontal, split_quadrants
import config # 匯入 config

def is_aspect_ratio_valid(width: float, height: float) -> bool:
    """檢查元件長寬比是否在 config 設定的限制範圍內"""
    if width <= 0 or height <= 0:
        return False
    ratio = max(width / height, height / width)
    return ratio <= config.MAX_ASPECT_RATIO

# split_mirrored_vertical, split_mirrored_horizontal, split_common_centroid_quadrants
# 這三個函式不需修改，它們依賴的基礎函式已經被修改了

def split_mirrored_vertical(component: Component, ratio_h: float = 0.5, gap: float = 0.01) -> List[Component]:
    if component.width <= gap or component.height <= 2 * gap:
        return [component]
    halves = split_vertical(component, ratio=0.5, gap=gap)
    if len(halves) < 2:
        return [component]
    left_splits = split_horizontal(halves[0], ratio=ratio_h, gap=gap)
    right_splits = split_horizontal(halves[1], ratio=1 - ratio_h, gap=gap)
    if len(left_splits) < 2 or len(right_splits) < 2:
        return [component]
    return [left_splits[1], left_splits[0], right_splits[0], right_splits[1]]

def split_mirrored_horizontal(component: Component, ratio_v: float = 0.5, gap: float = 0.01) -> List[Component]:
    if component.height <= gap or component.width <= 2 * gap:
        return [component]
    halves = split_horizontal(component, ratio=0.5, gap=gap)
    if len(halves) < 2:
        return [component]
    top_splits = split_vertical(halves[1], ratio=ratio_v, gap=gap)
    bottom_splits = split_vertical(halves[0], ratio=1 - ratio_v, gap=gap)
    if len(top_splits) < 2 or len(bottom_splits) < 2:
        return [component]
    return [top_splits[0], top_splits[1], bottom_splits[0], bottom_splits[1]]

def split_common_centroid_quadrants(component: Component, gap: float = 0.01) -> List[Component]:
    return split_quadrants(component, ratio_v=0.5, ratio_h=0.5, gap=gap)

def split_symmetric_triplet_vertical(component: Component, ratio_w: float = 0.25, gap: float = 0.01) -> List[Component]:
    if ratio_w <= 0 or ratio_w >= 0.5: return [component]
    total_gap = 2 * gap
    if component.width <= total_gap: return [component]
    w_side = (component.width - total_gap) * ratio_w
    w_center = (component.width - total_gap) * (1 - 2 * ratio_w)
    if w_side <= 0 or w_center <= 0: return [component]

    # --- 新增長寬比檢查 ---
    if not is_aspect_ratio_valid(w_side, component.height) or \
       not is_aspect_ratio_valid(w_center, component.height):
        return [component]

    comp_left = Component(component.x, component.y, w_side, component.height, component.group_id, component.level + 1)
    center_x = component.x + w_side + gap
    comp_center = Component(center_x, component.y, w_center, component.height, component.group_id, component.level + 1)
    right_x = center_x + w_center + gap
    comp_right = Component(right_x, component.y, w_side, component.height, component.group_id, component.level + 1)
    return [comp_left, comp_center, comp_right]

def split_symmetric_triplet_horizontal(component: Component, ratio_h: float = 0.25, gap: float = 0.01) -> List[Component]:
    if ratio_h <= 0 or ratio_h >= 0.5: return [component]
    total_gap = 2 * gap
    if component.height <= total_gap: return [component]
    h_side = (component.height - total_gap) * ratio_h
    h_center = (component.height - total_gap) * (1 - 2 * ratio_h)
    if h_side <= 0 or h_center <= 0: return [component]

    # --- 新增長寬比檢查 ---
    if not is_aspect_ratio_valid(component.width, h_side) or \
       not is_aspect_ratio_valid(component.width, h_center):
        return [component]

    comp_bottom = Component(component.x, component.y, component.width, h_side, component.group_id, component.level + 1)
    center_y = component.y + h_side + gap
    comp_center = Component(component.x, center_y, component.width, h_center, component.group_id, component.level + 1)
    top_y = center_y + h_center + gap
    comp_top = Component(component.x, top_y, component.width, h_side, component.group_id, component.level + 1)
    return [comp_bottom, comp_center, comp_top]