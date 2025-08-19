# rules/split_basic.py
from typing import List
from component import Component

def split_vertical(component: Component, ratio: float = 0.5, gap: float = 0.01) -> List[Component]:
    # ... (此處程式碼與舊 rules.py 中的完全相同) ...
    if component.width <= gap: return [component]
    w1 = component.width * ratio - gap / 2
    w2 = component.width * (1 - ratio) - gap / 2
    if w1 <= 0 or w2 <= 0: return [component]
    comp1 = Component(component.x, component.y, w1, component.height, component.group_id, component.level + 1)
    comp2 = Component(component.x + w1 + gap, component.y, w2, component.height, component.group_id, component.level + 1)
    return [comp1, comp2]

def split_horizontal(component: Component, ratio: float = 0.5, gap: float = 0.01) -> List[Component]:
    # ... (此處程式碼與舊 rules.py 中的完全相同) ...
    if component.height <= gap: return [component]
    h1 = component.height * ratio - gap / 2
    h2 = component.height * (1 - ratio) - gap / 2
    if h1 <= 0 or h2 <= 0: return [component]
    comp1 = Component(component.x, component.y, component.width, h1, component.group_id, component.level + 1)
    comp2 = Component(component.x, component.y + h1 + gap, component.width, h2, component.group_id, component.level + 1)
    return [comp1, comp2]

def split_quadrants(component: Component, ratio_v: float = 0.5, ratio_h: float = 0.5, gap: float = 0.01) -> List[Component]:
    # ... (此處程式碼與舊 rules.py 中的完全相同) ...
    vertical_splits = split_vertical(component, ratio=ratio_v, gap=gap)
    if len(vertical_splits) < 2: return vertical_splits
    final_components = []
    for comp in vertical_splits:
        horizontal_splits = split_horizontal(comp, ratio=ratio_h, gap=gap)
        final_components.extend(horizontal_splits)
    return final_components