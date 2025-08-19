# visualization.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
from component import Component

def visualize_placements(components: List[Component], canvas_dims, mn_rect_dims, save_path="synthetic_layout.png"):
    """將元件佈局視覺化"""
    fig, ax = plt.subplots(1, figsize=(8, 8))
    
    canvas_patch = patches.Rectangle((0, 0), canvas_dims[0], canvas_dims[1], linewidth=2, edgecolor='black', facecolor='none', label='Canvas')
    ax.add_patch(canvas_patch)

    mn_x = (canvas_dims[0] - mn_rect_dims[0]) / 2
    mn_y = (canvas_dims[1] - mn_rect_dims[1]) / 2
    mn_patch = patches.Rectangle((mn_x, mn_y), mn_rect_dims[0], mn_rect_dims[1], linewidth=1.5, edgecolor='r', linestyle='--', facecolor='none', label='m*n Area')
    ax.add_patch(mn_patch)

    if components:
        unique_group_ids = sorted(list(set(c.group_id for c in components)))
        colors = plt.cm.get_cmap('tab20', len(unique_group_ids))
        color_map = {gid: colors(i) for i, gid in enumerate(unique_group_ids)}

        for comp in components:
            rect = patches.Rectangle(
                (comp.x, comp.y), comp.width, comp.height, 
                facecolor=color_map.get(comp.group_id, 'gray')
            )
            ax.add_patch(rect)

    ax.set_xlim(0, canvas_dims[0])
    ax.set_ylim(0, canvas_dims[1])
    ax.set_aspect('equal', adjustable='box')
    plt.legend()
    plt.title("Synthetic Analog Layout Generation")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.savefig(save_path)
    plt.show()