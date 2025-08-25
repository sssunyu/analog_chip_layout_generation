# aclg/post_processing/padding.py

from aclg.dataclass.component import Component
from typing import List

def add_padding(
        components: List[Component], 
        padding: float
) -> List[Component]:
    """
    對一個或多個元件應用邊距（Padding），使其尺寸縮小。
    這個函式會直接修改傳入的元件物件。

    Args:
        components: 一個包含 Component 物件的列表。
        padding: 要在元件四周留下的邊界寬度。

    Returns:
        回傳修改後的元件列表。
    """
    if padding < 0:
        raise ValueError("Padding 值不能為負數。")

    for comp in components:
        # 檢查 padding 是否會導致尺寸變為負數
        if (comp.width - 2 * padding) < 0 or (comp.height - 2 * padding) < 0:
            raise ValueError(f"Padding ({padding}) 對於元件尺寸 ({comp.width}x{comp.height}) 而言太大了。")

        # 中心點 (x, y) 保持不變
        # generate_rule 保持不變

        # 寬度和高度各自減去兩倍的 padding
        comp.width -= 2 * padding
        comp.height -= 2 * padding

    return components