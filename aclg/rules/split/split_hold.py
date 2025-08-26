from aclg.dataclass.component import Component
import copy

def split_hold(component: Component)-> list["Component"]:
    hold_comp = copy.deepcopy(component)
    hold_comp.generate_rule = 'hold'
    return [hold_comp]