# rules/split_aligned.py
from typing import List
from component import Component

def split_aligned(component: Component, orientation: str = 'vertical', num_splits: int = 3, alignment: str = 'center', global_scale: float = 1.0, individual_scales: list = None, gap: float = 0.01) -> List[Component]:
    # ... (此處程式碼與舊 rules.py 中的完全相同) ...
    if num_splits <= 1: return [component]
    if individual_scales is None: individual_scales = [1.0] * num_splits
    elif len(individual_scales) != num_splits: raise ValueError("individual_scales 的長度必須等於 num_splits")
    new_components = []
    if orientation == 'vertical':
        slot_width = (component.width - (num_splits - 1) * gap) / num_splits
        if slot_width <= 0: return [component]
        current_x = component.x
        for i in range(num_splits):
            final_width = slot_width * global_scale * individual_scales[i]
            offset = 0
            if alignment == 'center': offset = (slot_width - final_width) / 2
            elif alignment == 'right': offset = slot_width - final_width
            new_comp = Component(current_x + offset, component.y, final_width, component.height, component.group_id, component.level + 1)
            new_components.append(new_comp)
            current_x += slot_width + gap
    elif orientation == 'horizontal':
        slot_height = (component.height - (num_splits - 1) * gap) / num_splits
        if slot_height <= 0: return [component]
        current_y = component.y
        for i in range(num_splits):
            final_height = slot_height * global_scale * individual_scales[i]
            offset = 0
            if alignment == 'center': offset = (slot_height - final_height) / 2
            elif alignment == 'right' or alignment == 'top': offset = slot_height - final_height
            new_comp = Component(component.x, current_y + offset, component.width, final_height, component.group_id, component.level + 1)
            new_components.append(new_comp)
            current_y += slot_height + gap
    return new_components