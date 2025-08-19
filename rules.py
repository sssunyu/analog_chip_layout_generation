# rules.py
import random
from typing import List, Dict, Callable
from component import Component

# --- 定義各種切割規則的函式 ---
# 每個規則函式都接收一個元件和一些參數，返回一個切割後的新元件列表

def split_vertical(component: Component, ratio: float = 0.5, gap: float = 0.01) -> List[Component]:
    """垂直切割元件，可指定比例和間隙"""
    if component.width <= gap:
        return [component]
    
    w1 = component.width * ratio - gap / 2
    w2 = component.width * (1 - ratio) - gap / 2
    
    if w1 <= 0 or w2 <= 0:
        return [component] # 如果切割後尺寸無效，則不切割

    comp1 = Component(
        x=component.x,
        y=component.y,
        width=w1,
        height=component.height,
        group_id=component.group_id,
        level=component.level + 1
    )
    comp2 = Component(
        x=component.x + w1 + gap,
        y=component.y,
        width=w2,
        height=component.height,
        group_id=component.group_id,
        level=component.level + 1
    )
    return [comp1, comp2]

def split_horizontal(component: Component, ratio: float = 0.5, gap: float = 0.01) -> List[Component]:
    """水平切割元件，可指定比例和間隙"""
    if component.height <= gap:
        return [component]
        
    h1 = component.height * ratio - gap / 2
    h2 = component.height * (1 - ratio) - gap / 2

    if h1 <= 0 or h2 <= 0:
        return [component]

    comp1 = Component(
        x=component.x,
        y=component.y,
        width=component.width,
        height=h1,
        group_id=component.group_id,
        level=component.level + 1
    )
    comp2 = Component(
        x=component.x,
        y=component.y + h1 + gap,
        width=component.width,
        height=h2,
        group_id=component.group_id,
        level=component.level + 1
    )
    return [comp1, comp2]

def split_quadrants(component: Component, ratio_v: float = 0.5, ratio_h: float = 0.5, gap: float = 0.01) -> List[Component]:
    """將元件切割成四個象限"""
    # 先垂直切
    vertical_splits = split_vertical(component, ratio=ratio_v, gap=gap)
    if len(vertical_splits) < 2:
        return vertical_splits

    # 再對切出來的兩個分別水平切
    final_components = []
    for comp in vertical_splits:
        horizontal_splits = split_horizontal(comp, ratio=ratio_h, gap=gap)
        final_components.extend(horizontal_splits)
        
    return final_components

def split_aligned(
    component: Component, 
    orientation: str = 'vertical',
    num_splits: int = 3,
    alignment: str = 'center',
    global_scale: float = 1.0,
    individual_scales: list = None,
    gap: float = 0.01
) -> List[Component]:
    """
    執行對齊切割，並在切割後對元件進行縮放。
    - orientation: 'vertical' 或 'horizontal'
    - num_splits: 切割數量
    - alignment: 'left', 'center', 'right' (對應垂直) 或 'bottom', 'center', 'top' (對應水平)
    - global_scale: 整體縮放
    - individual_scales: 個別縮放列表，長度需等於 num_splits
    """
    if num_splits <= 1:
        return [component]
        
    if individual_scales is None:
        individual_scales = [1.0] * num_splits
    elif len(individual_scales) != num_splits:
        raise ValueError("individual_scales 的長度必須等於 num_splits")

    new_components = []
    
    if orientation == 'vertical':
        # 1. 計算每個元件未縮放前的"插槽"寬度
        slot_width = (component.width - (num_splits - 1) * gap) / num_splits
        if slot_width <= 0: return [component]
        
        current_x = component.x
        for i in range(num_splits):
            # 2. 計算縮放後的最終寬度
            final_width = slot_width * global_scale * individual_scales[i]
            
            # 3. 根據對齊模式，計算元件的 x 座標
            offset = 0
            if alignment == 'center':
                offset = (slot_width - final_width) / 2
            elif alignment == 'right':
                offset = slot_width - final_width
            # 'left' alignment has offset = 0

            new_comp = Component(
                x=current_x + offset,
                y=component.y,
                width=final_width,
                height=component.height, # 垂直切割，高度不變
                group_id=component.group_id,
                level=component.level + 1
            )
            new_components.append(new_comp)
            
            # 更新下一個"插槽"的起始位置
            current_x += slot_width + gap

    elif orientation == 'horizontal':
        # 邏輯與垂直切割相同，只是將 x/width 換成 y/height
        slot_height = (component.height - (num_splits - 1) * gap) / num_splits
        if slot_height <= 0: return [component]

        current_y = component.y
        for i in range(num_splits):
            final_height = slot_height * global_scale * individual_scales[i]
            
            offset = 0
            # 為了清晰，水平的對齊也可用 left/right/center，對應 bottom/top/center
            if alignment == 'center':
                offset = (slot_height - final_height) / 2
            elif alignment == 'right' or alignment == 'top': # 'right' and 'top' are equivalent here
                offset = slot_height - final_height
            # 'left' or 'bottom' alignment has offset = 0

            new_comp = Component(
                x=component.x,
                y=current_y + offset,
                width=component.width, # 水平切割，寬度不變
                height=final_height,
                group_id=component.group_id,
                level=component.level + 1
            )
            new_components.append(new_comp)
            
            current_y += slot_height + gap
            
    return new_components

# --- 規則選擇與應用 ---

class RuleSelector:
    def __init__(self):
        self.rules: Dict[str, Callable] = {
            "vertical": split_vertical,
            "horizontal": split_horizontal,
            "quadrants": split_quadrants,
            "aligned": split_aligned  # <-- 在此註冊新規則
        }
        self.modes: List[str] = ["keep_all", "keep_first", "keep_second", "keep_random"]

    def apply(self, component: Component, rule_name: str, mode: str, **kwargs) -> List[Component]:
        """
        應用指定的規則和模式
        
        :param component: 要處理的元件
        :param rule_name: 規則名稱 (e.g., "vertical")
        :param mode: 切割後保留的模式 (e.g., "keep_all")
        :param kwargs: 傳遞給規則函式的額外參數 (e.g., ratio=0.3)
        :return: 處理後留下的元件列表
        """
        if rule_name not in self.rules:
            raise ValueError(f"規則 '{rule_name}' 不存在.")
        if mode not in self.modes:
            raise ValueError(f"模式 '{mode}' 不存在.")
            
        rule_func = self.rules[rule_name]
        new_components = rule_func(component, **kwargs)

        if len(new_components) <= 1:
            return new_components
            
        if mode == "keep_all":
            return new_components
        elif mode == "keep_first":
            return [new_components[0]]
        elif mode == "keep_second":
            return [new_components[1]]
        elif mode == "keep_random":
            return [random.choice(new_components)]
        
        return [] # 預設情況