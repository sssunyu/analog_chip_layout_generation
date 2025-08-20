# visualization.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
from component import Component
import colorsys

def darken_color(color, factor=0.6):
    """
    將傳入的 RGBA 顏色變暗。
    :param color: 一個包含 (r, g, b, a) 的元組。
    :param factor: 變暗的程度，0 表示最暗 (黑色)，1 表示原色。
    :return: 一個變暗後的 (r, g, b, a) 元組。
    """
    # 將 RGB 值乘以 factor 來變暗，保持 alpha 值不變
    return (color[0] * factor, color[1] * factor, color[2] * factor, color[3])

def visualize_placements(components: List[Component], canvas_dims, mn_rect_dims, save_path="synthetic_layout.png"):
    """將元件佈局視覺化"""
    fig, ax = plt.subplots(1, figsize=(12, 12))
    
    # --- 畫布與 m*n 區域設定 (與原版相同) ---
    canvas_patch = patches.Rectangle((0, 0), canvas_dims[0], canvas_dims[1], linewidth=2, edgecolor='black', facecolor='#F8F8F8', label='Canvas')
    ax.add_patch(canvas_patch)

    mn_x = (canvas_dims[0] - mn_rect_dims[0]) / 2
    mn_y = (canvas_dims[1] - mn_rect_dims[1]) / 2
    mn_patch = patches.Rectangle((mn_x, mn_y), mn_rect_dims[0], mn_rect_dims[1], linewidth=1.5, edgecolor='r', linestyle='--', facecolor='none', label='m*n Area')
    ax.add_patch(mn_patch)

    # --- 核心修改：顏色與邊框 ---
    if components:
        unique_group_ids = sorted(list(set(c.group_id for c in components)))
        
        # 使用一個更柔和、更美觀的顏色對照表 (Pastel1)
        colors = plt.cm.get_cmap('Pastel1', len(unique_group_ids))
        color_map = {gid: colors(i) for i, gid in enumerate(unique_group_ids)}

        for comp in components:
            # 取得該群組的基礎顏色 (淺色)
            face_color = color_map.get(comp.group_id, 'gray')
            # 計算出對應的深色邊框
            edge_color = darken_color(face_color, factor=0.5)

            rect = patches.Rectangle(
                (comp.x, comp.y), comp.width, comp.height, 
                facecolor=face_color,
                edgecolor=edge_color, # 設定邊框顏色
                linewidth=1.0         # 設定邊框寬度
            )
            ax.add_patch(rect)

    # --- 圖表美化設定 ---
    ax.set_xlim(-0.05, canvas_dims[0] + 0.05)
    ax.set_ylim(-0.05, canvas_dims[1] + 0.05)
    ax.set_aspect('equal', adjustable='box')
    
    # 將圖例放在圖表外側，避免遮擋
    ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1.0))
    plt.title("Synthetic Analog Layout Generation", fontsize=16)
    plt.grid(True, linestyle=':', alpha=0.5, color='gray')
    
    # 儲存圖片，設定更高的解析度
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()