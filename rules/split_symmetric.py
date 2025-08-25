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

def split_mirrored_vertical(component: Component, ratio_h: float = 0.5, gap: float = 0.01) -> List[Component]:
    """
    【已修正】先垂直對半切，然後對左右兩半進行水平切割，形成真正的鏡像對稱。
    左上元件的高度會等於右下元件的高度。
    """
    # 基本的尺寸有效性檢查
    if component.width <= gap or component.height <= gap:
        return [component]

    w_half = (component.width - gap) / 2
    h1 = (component.height - gap) * ratio_h
    h2 = (component.height - gap) * (1 - ratio_h)

    if w_half <= 0 or h1 <= 0 or h2 <= 0:
        return [component]

    # 檢查所有潛在子元件的長寬比
    if not is_aspect_ratio_valid(w_half, h1) or not is_aspect_ratio_valid(w_half, h2):
        return [component]

    # 直接計算四個象限的座標和尺寸
    x_left = component.x
    x_right = component.x + w_half + gap
    y_bottom = component.y
    
    # 建立四個子元件
    # 左半邊
    comp_bl = Component(x_left, y_bottom, w_half, h1, component.group_id, component.level + 1)
    comp_tl = Component(x_left, y_bottom + h1 + gap, w_half, h2, component.group_id, component.level + 1)
    
    # 右半邊 (高度反轉以形成鏡像)
    comp_br = Component(x_right, y_bottom, w_half, h2, component.group_id, component.level + 1)
    comp_tr = Component(x_right, y_bottom + h2 + gap, w_half, h1, component.group_id, component.level + 1)
    
    return [comp_bl, comp_tl, comp_br, comp_tr]


def split_mirrored_horizontal(component: Component, ratio_v: float = 0.5, gap: float = 0.01) -> List[Component]:
    """
    【已修正】先水平對半切，然後對上下兩半進行垂直切割，形成真正的鏡像對稱。
    左上元件的寬度會等於右下元件的寬度。
    """
    if component.height <= gap or component.width <= gap:
        return [component]

    h_half = (component.height - gap) / 2
    w1 = (component.width - gap) * ratio_v
    w2 = (component.width - gap) * (1 - ratio_v)

    if h_half <= 0 or w1 <= 0 or w2 <= 0:
        return [component]

    if not is_aspect_ratio_valid(w1, h_half) or not is_aspect_ratio_valid(w2, h_half):
        return [component]

    y_bottom = component.y
    y_top = component.y + h_half + gap
    x_left = component.x

    # 下半邊
    comp_bl = Component(x_left, y_bottom, w1, h_half, component.group_id, component.level + 1)
    comp_br = Component(x_left + w1 + gap, y_bottom, w2, h_half, component.group_id, component.level + 1)

    # 上半邊 (寬度反轉以形成鏡像)
    comp_tl = Component(x_left, y_top, w2, h_half, component.group_id, component.level + 1)
    comp_tr = Component(x_left + w2 + gap, y_top, w1, h_half, component.group_id, component.level + 1)
    
    return [comp_bl, comp_br, comp_tl, comp_tr]


def split_common_centroid_quadrants(component: Component, gap: float = 0.01) -> List[Component]:
    # This rule is correct, no changes needed.
    return split_quadrants(component, ratio_v=0.5, ratio_h=0.5, gap=gap)

def split_symmetric_triplet_vertical(component: Component, ratio_w: float = 0.25, gap: float = 0.01) -> List[Component]:
    # This rule is correct, no changes needed.
    if ratio_w <= 0 or ratio_w >= 0.5: return [component]
    total_gap = 2 * gap
    if component.width <= total_gap: return [component]
    w_side = (component.width - total_gap) * ratio_w
    w_center = (component.width - total_gap) * (1 - 2 * ratio_w)
    if w_side <= 0 or w_center <= 0: return [component]

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
    # This rule is correct, no changes needed.
    if ratio_h <= 0 or ratio_h >= 0.5: return [component]
    total_gap = 2 * gap
    if component.height <= total_gap: return [component]
    h_side = (component.height - total_gap) * ratio_h
    h_center = (component.height - total_gap) * (1 - 2 * ratio_h)
    if h_side <= 0 or h_center <= 0: return [component]

    if not is_aspect_ratio_valid(component.width, h_side) or \
       not is_aspect_ratio_valid(component.width, h_center):
        return [component]

    comp_bottom = Component(component.x, component.y, component.width, h_side, component.group_id, component.level + 1)
    center_y = component.y + h_side + gap
    comp_center = Component(component.x, center_y, component.width, h_center, component.group_id, component.level + 1)
    top_y = center_y + h_center + gap
    comp_top = Component(component.x, top_y, component.width, h_side, component.group_id, component.level + 1)
    return [comp_bottom, comp_center, comp_top]