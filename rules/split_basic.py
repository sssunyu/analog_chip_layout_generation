# rules/split_basic.py
from typing import List
from component import Component
import config  # 匯入 config

def is_aspect_ratio_valid(width: float, height: float) -> bool:
    """檢查元件長寬比是否在 config 設定的限制範圍內"""
    if width <= 0 or height <= 0:
        return False
    # 計算寬/高和高/寬中的較大值，與最大限制比較
    ratio = max(width / height, height / width)
    return ratio <= config.MAX_ASPECT_RATIO

def split_vertical(component: Component, ratio: float = 0.5, gap: float = 0.01) -> List[Component]:
    if component.width <= gap: return [component]
    w1 = component.width * ratio - gap / 2
    w2 = component.width * (1 - ratio) - gap / 2
    if w1 <= 0 or w2 <= 0: return [component]

    # --- 新增長寬比檢查 ---
    if not is_aspect_ratio_valid(w1, component.height) or \
       not is_aspect_ratio_valid(w2, component.height):
        return [component] # 如果任一子元件不符規定，則取消切割

    comp1 = Component(component.x, component.y, w1, component.height, component.group_id, component.level + 1)
    comp2 = Component(component.x + w1 + gap, component.y, w2, component.height, component.group_id, component.level + 1)
    return [comp1, comp2]

def split_horizontal(component: Component, ratio: float = 0.5, gap: float = 0.01) -> List[Component]:
    if component.height <= gap: return [component]
    h1 = component.height * ratio - gap / 2
    h2 = component.height * (1 - ratio) - gap / 2
    if h1 <= 0 or h2 <= 0: return [component]

    # --- 新增長寬比檢查 ---
    if not is_aspect_ratio_valid(component.width, h1) or \
       not is_aspect_ratio_valid(component.width, h2):
        return [component] # 如果任一子元件不符規定，則取消切割

    comp1 = Component(component.x, component.y, component.width, h1, component.group_id, component.level + 1)
    comp2 = Component(component.x, component.y + h1 + gap, component.width, h2, component.group_id, component.level + 1)
    return [comp1, comp2]

def split_quadrants(component: Component, ratio_v: float = 0.5, ratio_h: float = 0.5, gap: float = 0.01) -> List[Component]:
    # 這個函式不需修改，它會自動呼叫上面已修改過的 split_vertical 和 split_horizontal
    vertical_splits = split_vertical(component, ratio=ratio_v, gap=gap)
    if len(vertical_splits) < 2: return vertical_splits
    final_components = []
    for comp in vertical_splits:
        horizontal_splits = split_horizontal(comp, ratio=ratio_h, gap=gap)
        final_components.extend(horizontal_splits)
    return final_components