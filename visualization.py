# visualization.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List
from component import Component
import colorsys

def darken_color(color, factor=0.6):
    """將傳入的 RGBA 顏色變暗。"""
    return (color[0] * factor, color[1] * factor, color[2] * factor, color[3])

def visualize_placements(components: List[Component], canvas_dims, mn_rect_dims, save_path="synthetic_layout.png"):
    """將元件佈局視覺化"""
    fig, ax = plt.subplots(1, figsize=(12, 12))
    
    # 畫布與 m*n 區域設定
    canvas_patch = patches.Rectangle((0, 0), canvas_dims[0], canvas_dims[1], linewidth=2, edgecolor='black', facecolor='#F8F8F8', label='Canvas')
    ax.add_patch(canvas_patch)
    mn_x = (canvas_dims[0] - mn_rect_dims[0]) / 2
    mn_y = (canvas_dims[1] - mn_rect_dims[1]) / 2
    mn_patch = patches.Rectangle((mn_x, mn_y), mn_rect_dims[0], mn_rect_dims[1], linewidth=1.5, edgecolor='r', linestyle='--', facecolor='none', label='m*n Area')
    ax.add_patch(mn_patch)

    if components:
        unique_group_ids = sorted(list(set(c.group_id for c in components)))
        colors = plt.cm.get_cmap('Pastel1', len(unique_group_ids))
        color_map = {gid: colors(i) for i, gid in enumerate(unique_group_ids)}

        SYMMETRIC_FACE_COLOR = "#DAEFE1"  # 淡綠色
        SYMMETRIC_EDGE_COLOR = "#4EA052"  # 深綠色
        
        found_symmetric = False # 用於追蹤是否畫了任何對稱元件

        for comp in components:
            if comp.symmetrical:
                face_color = SYMMETRIC_FACE_COLOR
                edge_color = SYMMETRIC_EDGE_COLOR
                found_symmetric = True # 標記已找到
            else:
                face_color = color_map.get(comp.group_id, 'gray')
                edge_color = darken_color(face_color, factor=0.5)

            rect = patches.Rectangle(
                (comp.x, comp.y), comp.width, comp.height, 
                facecolor=face_color,
                edgecolor=edge_color,
                linewidth=1.0
            )
            ax.add_patch(rect)

    # 圖表美化設定
    ax.set_xlim(-0.05, canvas_dims[0] + 0.05)
    ax.set_ylim(-0.05, canvas_dims[1] + 0.05)
    ax.set_aspect('equal', adjustable='box')
    
    # --- 主要修改處：動態新增圖例 ---
    # 獲取現有的圖例控制代碼和標籤
    handles, labels = ax.get_legend_handles_labels()
    
    # 如果在繪圖過程中發現了對稱元件，就為其建立一個圖例補丁
    if found_symmetric:
        symmetric_patch = patches.Patch(
            facecolor=SYMMETRIC_FACE_COLOR, 
            edgecolor=SYMMETRIC_EDGE_COLOR, 
            label='Symmetric Group'
        )
        handles.append(symmetric_patch)

    # 使用更新後的控制代碼重新繪製圖例
    ax.legend(handles=handles, loc='upper right', bbox_to_anchor=(1.15, 1.0))
    
    plt.title("Synthetic Analog Layout Generation", fontsize=16)
    plt.grid(True, linestyle=':', alpha=0.5, color='gray')
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()