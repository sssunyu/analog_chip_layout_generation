# main_generator.py
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List

from component import Component
from rules import RuleSelector

# --- 參數設定 ---
# 畫布
CANVAS_WIDTH = 2.0
CANVAS_HEIGHT = 2.0
# 初始 m*n 矩形
MN_RECT_WIDTH = 1.5
MN_RECT_HEIGHT = 1.5
# 流程控制
K_ITERATIONS = 5  # 中心矩形初始切割次數
J_ITERATIONS = 2  # 填補元件切割次數
NUM_FILLER_COMPONENTS = 10 # 填補元件的數量
MIN_FILLER_SIZE = 0.05
MAX_FILLER_SIZE = 0.2
# 其他
COMPONENT_GAP = 0.01 # 用於切割時的間隙

def process_component_recursively(
    component: Component, 
    rule_selector: RuleSelector, 
    max_depth: int
) -> List[Component]:
    """
    遞迴地對一個元件應用切割規則，直到達到最大深度。
    """
    if component.level >= max_depth:
        return [component]

    rule_to_apply = random.choice(list(rule_selector.rules.keys()))
    
    # 將模式固定為 "keep_all"，以保留所有切割後的元件
    mode_to_apply = "keep_all" 

    # -------------------【修改部分】-------------------
    # 根據選擇的規則準備對應的參數
    params = {"gap": COMPONENT_GAP}
    if rule_to_apply in ["vertical", "horizontal"]:
        params["ratio"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "quadrants":
        params["ratio_v"] = random.uniform(0.3, 0.7)
        params["ratio_h"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "aligned":
        # 為 "aligned" 規則準備專屬參數
        num_splits = random.randint(2, 4)  # 隨機切成 2, 3 或 4 份
        params["num_splits"] = num_splits
        params["orientation"] = random.choice(['vertical', 'horizontal'])
        params["alignment"] = random.choice(['left', 'center', 'right'])
        params["global_scale"] = random.uniform(0.7, 0.95)
        # 為每個切出的元件準備一個隨機的獨立縮放參數
        params["individual_scales"] = [random.uniform(0.8, 1.0) for _ in range(num_splits)]
    # ----------------------------------------------------

    # 應用規則
    new_components = rule_selector.apply(component, rule_to_apply, mode_to_apply, **params)
    
    # 對所有新生成的元件進行遞迴處理
    final_components = []
    for comp in new_components:
        final_components.extend(
            process_component_recursively(comp, rule_selector, max_depth)
        )
    
    return final_components

def check_overlap(comp1: Component, comp2: Component) -> bool:
    """檢查兩個元件是否重疊"""
    return not (comp1.x + comp1.width < comp2.x or
                comp2.x + comp2.width < comp1.x or
                comp1.y + comp1.height < comp2.y or
                comp2.y + comp2.height < comp1.y)

def visualize_placements(components: List[Component], canvas_dims, mn_rect_dims):
    """將元件佈局視覺化"""
    fig, ax = plt.subplots(1, figsize=(8, 8))
    
    canvas_patch = patches.Rectangle((0, 0), canvas_dims[0], canvas_dims[1], linewidth=2, edgecolor='black', facecolor='none', label='Canvas')
    ax.add_patch(canvas_patch)

    mn_x = (canvas_dims[0] - mn_rect_dims[0]) / 2
    mn_y = (canvas_dims[1] - mn_rect_dims[1]) / 2
    mn_patch = patches.Rectangle((mn_x, mn_y), mn_rect_dims[0], mn_rect_dims[1], linewidth=1.5, edgecolor='r', linestyle='--', facecolor='none', label='m*n Area')
    ax.add_patch(mn_patch)

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
    plt.savefig("synthetic_layout.png")
    plt.show()

def main():
    rule_selector = RuleSelector()
    all_final_components = []
    
    mn_center_x = (CANVAS_WIDTH - MN_RECT_WIDTH) / 2
    mn_center_y = (CANVAS_HEIGHT - MN_RECT_HEIGHT) / 2
    
    # 步驟 1 & 2: 產生並切割中心 m*n 矩形內的初始元件
    print(f"--- 步驟 1 & 2: 處理中心區域 (切割 {K_ITERATIONS} 次) ---")
    
    initial_component = Component(
        x=mn_center_x, y=mn_center_y,
        width=MN_RECT_WIDTH, height=MN_RECT_HEIGHT,
        group_id=0, level=0
    )
    
    center_components = process_component_recursively(initial_component, rule_selector, K_ITERATIONS)
    all_final_components.extend(center_components)
    print(f"中心區域生成了 {len(center_components)} 個元件。")

    # -------------------【修改 2: 在 m*n 範圍內填補】-------------------
    # 步驟 3 & 4: 在 m*n 矩形的空白處補上元件並進行切割
    print(f"\n--- 步驟 3 & 4: 在 m*n 區域內填補 (生成 {NUM_FILLER_COMPONENTS} 組，每組切割 {J_ITERATIONS} 次) ---")
    
    for i in range(NUM_FILLER_COMPONENTS):
        attempts = 0
        while attempts < 200: # 增加嘗試次數以找到不重疊的位置
            # 隨機生成尺寸
            width = random.uniform(MIN_FILLER_SIZE, MAX_FILLER_SIZE)
            height = random.uniform(MIN_FILLER_SIZE, MAX_FILLER_SIZE)
            
            # 在 m*n 矩形範圍內隨機生成位置
            x = random.uniform(mn_center_x, mn_center_x + MN_RECT_WIDTH - width)
            y = random.uniform(mn_center_y, mn_center_y + MN_RECT_HEIGHT - height)
            
            new_filler = Component(x, y, width, height, group_id=i + 1)
            
            # 檢查是否與其他已存在元件重疊
            is_valid = True
            for existing_comp in all_final_components:
                if check_overlap(new_filler, existing_comp):
                    is_valid = False
                    break
            
            if is_valid:
                filler_components = process_component_recursively(new_filler, rule_selector, J_ITERATIONS)
                all_final_components.extend(filler_components)
                print(f"成功生成第 {i+1} 組填補元件 ({len(filler_components)} 個)。")
                break
            attempts += 1
        if attempts >= 200:
            print(f"警告：無法為第 {i+1} 組填補元件找到合適的位置。")

    # 視覺化最終結果
    print(f"\n--- 總共生成 {len(all_final_components)} 個元件。開始繪圖... ---")
    visualize_placements(
        all_final_components,
        (CANVAS_WIDTH, CANVAS_HEIGHT),
        (MN_RECT_WIDTH, MN_RECT_HEIGHT)
    )
    print("圖檔已儲存為 synthetic_layout.png")

if __name__ == "__main__":
    main()