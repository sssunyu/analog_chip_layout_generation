# rules/split_aligned.py
from typing import List
from component import Component
import config # 匯入 config

def is_aspect_ratio_valid(width: float, height: float) -> bool:
    """檢查元件長寬比是否在 config 設定的限制範圍內"""
    if width <= 0 or height <= 0:
        return False
    ratio = max(width / height, height / width)
    return ratio <= config.MAX_ASPECT_RATIO

def split_aligned(component: Component, orientation: str = 'vertical', num_splits: int = 3, alignment: str = 'center', global_scale: float = 1.0, individual_scales: list = None, gap: float = 0.01) -> List[Component]:
    if num_splits <= 1: return [component]
    if individual_scales is None: individual_scales = [1.0] * num_splits
    elif len(individual_scales) != num_splits: raise ValueError("individual_scales 的長度必須等於 num_splits")
    
    new_components = []
    
    # 在實際建立元件前，先檢查所有潛在子元件的長寬比
    if orientation == 'vertical':
        slot_width = (component.width - (num_splits - 1) * gap) / num_splits
        if slot_width <= 0: return [component]
        for i in range(num_splits):
            final_width = slot_width * global_scale * individual_scales[i]
            if not is_aspect_ratio_valid(final_width, component.height):
                return [component] # 若任一潛在元件不符規定，則取消整個切割
    elif orientation == 'horizontal':
        slot_height = (component.height - (num_splits - 1) * gap) / num_splits
        if slot_height <= 0: return [component]
        for i in range(num_splits):
            final_height = slot_height * global_scale * individual_scales[i]
            if not is_aspect_ratio_valid(component.width, final_height):
                return [component] # 若任一潛在元件不符規定，則取消整個切割

    # 如果所有檢查都通過，才開始建立元件
    if orientation == 'vertical':
        current_x = component.x
        slot_width = (component.width - (num_splits - 1) * gap) / num_splits
        for i in range(num_splits):
            final_width = slot_width * global_scale * individual_scales[i]
            offset = 0
            if alignment == 'center': offset = (slot_width - final_width) / 2
            elif alignment == 'right': offset = slot_width - final_width
            new_comp = Component(current_x + offset, component.y, final_width, component.height, component.group_id, component.level + 1)
            new_components.append(new_comp)
            current_x += slot_width + gap
    elif orientation == 'horizontal':
        current_y = component.y
        slot_height = (component.height - (num_splits - 1) * gap) / num_splits
        for i in range(num_splits):
            final_height = slot_height * global_scale * individual_scales[i]
            offset = 0
            if alignment == 'center': offset = (slot_height - final_height) / 2
            elif alignment == 'right' or alignment == 'top': offset = slot_height - final_height
            new_comp = Component(component.x, current_y + offset, component.width, final_height, component.group_id, component.level + 1)
            new_components.append(new_comp)
            current_y += slot_height + gap
            
    return new_components