# main.py
import random
from typing import List

# 從各個模組匯入所需的功能
import config
from component import Component
from rule_engine import RuleSelector
from visualization import visualize_placements

def process_component_recursively(component: Component, rule_selector: RuleSelector, max_depth: int) -> List[Component]:
    """遞迴地對一個元件應用切割規則，直到達到最大深度。"""
    if component.level >= max_depth:
        return [component]

    rule_to_apply = random.choice(list(rule_selector.rules.keys()))
    mode_to_apply = "keep_all" 

    params = {"gap": config.COMPONENT_GAP}
    # 根據選擇的規則，準備對應的隨機參數
    if rule_to_apply in ["vertical", "horizontal"]:
        params["ratio"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "quadrants":
        params["ratio_v"] = random.uniform(0.3, 0.7)
        params["ratio_h"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "aligned":
        num_splits = random.randint(2, 4)
        params["num_splits"] = num_splits
        params["orientation"] = random.choice(['vertical', 'horizontal'])
        params["alignment"] = random.choice(['left', 'center', 'right'])
        params["global_scale"] = random.uniform(0.7, 0.95)
        params["individual_scales"] = [random.uniform(0.8, 1.0) for _ in range(num_splits)]
    # --- 為新的對稱規則新增參數 ---
    elif rule_to_apply == "mirrored_vertical":
        params["ratio_h"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "mirrored_horizontal":
        params["ratio_v"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "triplet_vertical":
        # 側邊元件的比例，必須小於 0.5
        params["ratio_w"] = random.uniform(0.2, 0.45)
    elif rule_to_apply == "triplet_horizontal":
        # 側邊元件的比例，必須小於 0.5
        params["ratio_h"] = random.uniform(0.2, 0.45)
    # common_centroid 不需要額外參數

    new_components = rule_selector.apply(component, rule_to_apply, mode_to_apply, **params)
    
    final_components = []
    for comp in new_components:
        final_components.extend(process_component_recursively(comp, rule_selector, max_depth))
    
    return final_components

def check_overlap(comp1: Component, comp2: Component) -> bool:
    """檢查兩個元件是否重疊"""
    return not (comp1.x + comp1.width < comp2.x or
                comp2.x + comp2.width < comp1.x or
                comp1.y + comp1.height < comp2.y or
                comp2.y + comp2.height < comp1.y)

def main():
    """主執行函式"""
    rule_selector = RuleSelector()
    all_final_components = []
    
    mn_center_x = (config.CANVAS_WIDTH - config.MN_RECT_WIDTH) / 2
    mn_center_y = (config.CANVAS_HEIGHT - config.MN_RECT_HEIGHT) / 2
    
    print(f"--- 步驟 1 & 2: 處理中心區域 (切割 {config.K_ITERATIONS} 次) ---")
    initial_component = Component(
        x=mn_center_x, y=mn_center_y,
        width=config.MN_RECT_WIDTH, height=config.MN_RECT_HEIGHT,
        group_id=0, level=0
    )
    center_components = process_component_recursively(initial_component, rule_selector, config.K_ITERATIONS)
    all_final_components.extend(center_components)
    print(f"中心區域生成了 {len(center_components)} 個元件。")

    print(f"\n--- 步驟 3 & 4: 在 m*n 區域內填補 (生成 {config.NUM_FILLER_COMPONENTS} 組，每組切割 {config.J_ITERATIONS} 次) ---")
    for i in range(config.NUM_FILLER_COMPONENTS):
        attempts = 0
        while attempts < 200:
            width = random.uniform(config.MIN_FILLER_SIZE, config.MAX_FILLER_SIZE)
            height = random.uniform(config.MIN_FILLER_SIZE, config.MAX_FILLER_SIZE)
            x = random.uniform(mn_center_x, mn_center_x + config.MN_RECT_WIDTH - width)
            y = random.uniform(mn_center_y, mn_center_y + config.MN_RECT_HEIGHT - height)
            
            new_filler = Component(x, y, width, height, group_id=i + 1)
            
            is_valid = True
            for existing_comp in all_final_components:
                if check_overlap(new_filler, existing_comp):
                    is_valid = False
                    break
            
            if is_valid:
                filler_components = process_component_recursively(new_filler, rule_selector, config.J_ITERATIONS)
                all_final_components.extend(filler_components)
                print(f"成功生成第 {i+1} 組填補元件 ({len(filler_components)} 個)。")
                break
            attempts += 1
        if attempts >= 200:
            print(f"警告：無法為第 {i+1} 組填補元件找到合適的位置。")

    print(f"\n--- 總共生成 {len(all_final_components)} 個元件。開始繪圖... ---")
    visualize_placements(
        all_final_components,
        (config.CANVAS_WIDTH, config.CANVAS_HEIGHT),
        (config.MN_RECT_WIDTH, config.MN_RECT_HEIGHT)
    )
    print("圖檔已儲存為 synthetic_layout.png")

if __name__ == "__main__":
    main()