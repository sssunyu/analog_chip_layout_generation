# aclg/rules/spacing_grid.py
from aclg.dataclass.component import Component

def spacing_grid(
        component: Component,
        rows: int = 1,
        cols: int = 1
) -> list[Component]:
    """
    將一個元件分割成指定行列數的均等網格。

    Args:
        component: 要被分割的父元件。
        rows: 網格的行數。
        cols: 網格的列數。

    Returns:
        一個包含所有網格內子元件的列表。
    """
    if rows <= 0 or cols <= 0:
        raise ValueError("行數和列數必須是大於 0 的整數。")

    parent = component
    new_components = []

    sub_width = parent.width / cols
    sub_height = parent.height / rows

    start_x, start_y = parent.get_topleft()

    for r in range(rows):
        for c in range(cols):
            center_x = start_x + (c * sub_width) + (sub_width / 2)
            center_y = start_y + (r * sub_height) + (sub_height / 2)

            grid_component = Component(
                x=center_x,
                y=center_y,
                width=sub_width,
                height=sub_height,
                generate_rule=f"spacing_grid"
            )
            new_components.append(grid_component)

    return new_components

def spacing_horizontal(
        component: Component,
        num_components: int
) -> list[Component]:
    """
    將元件水平分割成多個等寬的子元件 (單一行)。

    Args:
        component: 要被分割的父元件。
        num_components: 要分割出的子元件數量。

    Returns:
        一個包含所有水平排列子元件的列表。
    """
    components = spacing_grid(component, rows=1, cols=num_components)
    
    for comp in components:
        comp.generate_rule = "spacing_horizontal"
        
    return components

def spacing_vertical(
        component: Component,
        num_components: int
) -> list[Component]:
    """
    將元件垂直分割成多個等高的子元件 (單一列)。

    Args:
        component: 要被分割的父元件。
        num_components: 要分割出的子元件數量。

    Returns:
        一個包含所有垂直排列子元件的列表。
    """
    components = spacing_grid(component, rows=num_components, cols=1)

    for comp in components:
        comp.generate_rule = "spacing_vertical"
        
    return components