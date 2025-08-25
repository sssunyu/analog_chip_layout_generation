# rules/__init__.py
from .split_basic import split_vertical, split_horizontal, split_quadrants
from .split_aligned import split_aligned
from .split_symmetric import (
    split_mirrored_vertical,
    split_mirrored_horizontal,
    split_common_centroid_quadrants,
    split_symmetric_triplet_vertical,
    split_symmetric_triplet_horizontal
)

# 這個字典會被 RuleSelector 使用，集中管理所有可用的規則
available_rules = {
    # --- Basic Rules ---
    "vertical": split_vertical,
    "horizontal": split_horizontal,
    "quadrants": split_quadrants,
    
    # --- Aligned Rule ---
    "aligned": split_aligned,
    
    # --- Symmetric Rules ---
    "mirrored_vertical": split_mirrored_vertical,
    "mirrored_horizontal": split_mirrored_horizontal,
    "common_centroid": split_common_centroid_quadrants,
    "triplet_vertical": split_symmetric_triplet_vertical,
    "triplet_horizontal": split_symmetric_triplet_horizontal,
}