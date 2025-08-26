# D:\Projects\analog_chip_layout_generation\rules\split_basic.py

from aclg.dataclass.component import Component

def split_horizontal(
        component: Component, 
        ratio: float = 0.5
        ) -> list[Component]:
    
    parent = component

    width1 = parent.width * ratio
    width2 = parent.width * (1 - ratio)


    x1 = parent.x - parent.width / 2 + width1 / 2
    x2 = parent.x + parent.width / 2 - width2 / 2

    left_component = Component(
        x=x1,
        y=parent.y,
        width=width1,
        height=parent.height,
        generate_rule="split_basic"
    )

    right_component = Component(
        x=x2,
        y=parent.y,
        width=width2,
        height=parent.height,
        generate_rule="split_basic"
    )
    
    return [left_component, right_component]

def split_vertical(
        component: Component, 
        ratio: float = 0.5
        ) -> list[Component]:
    
    parent = component
    
    height1 = parent.height * ratio
    height2 = parent.height * (1 - ratio)

    y1 = parent.y - parent.height / 2 + height1 / 2
    y2 = parent.y + parent.height / 2 - height2 / 2

    top_component = Component(
        x=parent.x,
        y=y1,
        width=parent.width,
        height=height1,
        generate_rule="split_basic"
    )

    # 建立右邊的子元件
    buttom_component = Component(
        x=parent.x,
        y=y2,
        width=parent.width,
        height=height2,
        generate_rule="split_basic"
    )
    
    return [top_component, buttom_component]