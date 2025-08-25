from aclg.rules.split_basic import split_vertical, split_horizontal
from aclg.dataclass.component import Component

"""
symmetric_1 refer to cutting at the center of the component
"""

def split_symmetric_1_vertical(
        component_to_split: Component
) -> list[Component]:

    components = split_vertical(component_to_split, ratio=0.5)

    for comp in components:
        comp.generate_rule = "split_symmetric_1"

    return components


def split_symmetric_1_horizontal(
        component_to_split: Component
) -> list[Component]:

    components = split_horizontal(component_to_split, ratio=0.5)

    for comp in components:
        comp.generate_rule = "split_symmetric_1"

    return components