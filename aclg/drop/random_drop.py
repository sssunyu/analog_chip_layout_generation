# aclg/drop/random_drop.py
import random
from typing import List
from aclg.dataclass.component import Component

def drop_by_ratio(
        components: List[Component], 
        drop_ratio: float
) -> List[Component]:
    """
    從一個元件列表中，根據指定的比例隨機捨棄一部分元件。

    Args:
        components: 包含 Component 物件的原始列表。
        drop_ratio: 要捨棄的元件比例，值應介于 0.0 (不捨棄) 到 1.0 (全部捨棄) 之間。

    Returns:
        一個新的 Component 列表，其中已隨機移除了指定比例的元件。
    """
    if not 0.0 <= drop_ratio <= 1.0:
        raise ValueError("drop_ratio 必須介于 0.0 和 1.0 之間。")

    # 計算要保留的元件數量
    num_to_keep = round(len(components) * (1 - drop_ratio))
    
    # 使用 random.sample 隨機選出要保留的元件，它會回傳一個新的列表
    kept_components = random.sample(components, num_to_keep)
    
    return kept_components