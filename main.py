# main.py
import random
import math
from typing import List

# 從各個模組匯入所需的功能
import config
from component import Component
from rule_engine import RuleSelector
from visualization import visualize_placements

# 'SYMMETRIC_RULES', 'process_component_recursively', 'check_overlap' 函式維持不變...
SYMMETRIC_RULES = [
    "mirrored_vertical",
    "mirrored_horizontal",
    "common_centroid",
    "triplet_vertical",
    "triplet_horizontal",
]

def process_component_recursively(component: Component, rule_selector: RuleSelector, max_depth: int) -> List[Component]:
    """遞迴地對一個元件應用切割規則，直到達到最大深度。"""
    if component.level >= max_depth:
        return [component]
    available_rules = list(rule_selector.rules.keys())
    weights = [config.RULE_WEIGHTS.get(rule, 1) for rule in available_rules]
    rule_to_apply = random.choices(available_rules, weights=weights, k=1)[0]
    mode_to_apply = "keep_all"
    params = {"gap": config.COMPONENT_GAP}
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
        params["global_scale"] = random.uniform(0.75, 0.95)
        params["individual_scales"] = [random.uniform(0.8, 1.0) for _ in range(num_splits)]
    elif rule_to_apply == "mirrored_vertical":
        params["ratio_h"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "mirrored_horizontal":
        params["ratio_v"] = random.uniform(0.3, 0.7)
    elif rule_to_apply == "triplet_vertical":
        params["ratio_w"] = random.uniform(0.2, 0.45)
    elif rule_to_apply == "triplet_horizontal":
        params["ratio_h"] = random.uniform(0.2, 0.45)
    new_components = rule_selector.apply(component, rule_to_apply, mode_to_apply, **params)
    if rule_to_apply in SYMMETRIC_RULES:
        for comp in new_components:
            comp.symmetrical = True
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

def reduce_components_to_target(components: List[Component], target_count: int, gap: float) -> List[Component]:
    """
    透過合併相鄰的元件來減少元件總數，直到等於目標數量。
    優先合併總面積最小的一對元件。
    """
    while len(components) > target_count:
        best_pair_to_merge = None
        min_combined_area = float('inf')
        merged_props = {}
        TOLERANCE = 1e-5
        for i in range(len(components)):
            for j in range(i + 1, len(components)):
                comp1 = components[i]
                comp2 = components[j]

                # --- 主要修改處：跳過對稱元件 ---
                # 如果任一元件是對稱元件，則不考慮將它們合併
                if comp1.symmetrical or comp2.symmetrical:
                    continue

                if abs(comp1.x + comp1.width + gap - comp2.x) < TOLERANCE and \
                   abs(comp1.y - comp2.y) < TOLERANCE and \
                   abs(comp1.height - comp2.height) < TOLERANCE:
                    combined_area = (comp1.width * comp1.height) + (comp2.width * comp2.height)
                    if combined_area < min_combined_area:
                        min_combined_area = combined_area
                        best_pair_to_merge = (comp1, comp2)
                        merged_props = {'x': comp1.x, 'y': comp1.y, 'width': comp1.width + comp2.width + gap, 'height': comp1.height}
                elif abs(comp1.y + comp1.height + gap - comp2.y) < TOLERANCE and \
                     abs(comp1.x - comp2.x) < TOLERANCE and \
                     abs(comp1.width - comp2.width) < TOLERANCE:
                    combined_area = (comp1.width * comp1.height) + (comp2.width * comp2.height)
                    if combined_area < min_combined_area:
                        min_combined_area = combined_area
                        best_pair_to_merge = (comp1, comp2)
                        merged_props = {'x': comp1.x, 'y': comp1.y, 'width': comp1.width, 'height': comp1.height + comp2.height + gap}
        if best_pair_to_merge:
            comp_to_remove1, comp_to_remove2 = best_pair_to_merge
            new_component = Component(x=merged_props['x'], y=merged_props['y'], width=merged_props['width'], height=merged_props['height'], group_id=min(comp_to_remove1.group_id, comp_to_remove2.group_id), level=min(comp_to_remove1.level, comp_to_remove2.level))
            components.remove(comp_to_remove1)
            components.remove(comp_to_remove2)
            components.append(new_component)
            print(f"策略 [合併] 成功：2 個元件合併為 1 個。目前總數: {len(components)}")
        else:
            print("警告：策略 [合併] 失敗，找不到任何可合併的非對稱元件。無法精確達到目標數量。")
            break
    return components

def main():
    """主執行函式"""
    target_min, target_max = config.TOTAL_COMPONENT_COUNT_RANGE
    target_count = random.randint(target_min, target_max)
    target_area = random.uniform(config.MN_RECT_AREA_RANGE[0], config.MN_RECT_AREA_RANGE[1])
    aspect_ratio = random.uniform(config.MN_ASPECT_RATIO_RANGE[0], config.MN_ASPECT_RATIO_RANGE[1])
    mn_rect_height = math.sqrt(target_area / aspect_ratio)
    mn_rect_width = aspect_ratio * mn_rect_height
    if mn_rect_width >= config.CANVAS_WIDTH or mn_rect_height >= config.CANVAS_HEIGHT:
        print(f"警告：隨機生成的 m*n 尺寸 ({mn_rect_width:.2f}x{mn_rect_height:.2f}) 過大，將使用最小面積與正方形。")
        fallback_area = config.MN_RECT_AREA_RANGE[0]
        mn_rect_height = math.sqrt(fallback_area)
        mn_rect_width = mn_rect_height
    print(f"本次 m*n 矩形尺寸: {mn_rect_width:.2f} x {mn_rect_height:.2f} (長寬比: {aspect_ratio:.2f})")
    print(f"本次隨機目標元件總數: {target_count} (範圍: {config.TOTAL_COMPONENT_COUNT_RANGE})")
    rule_selector = RuleSelector()
    all_final_components = []
    mn_center_x = (config.CANVAS_WIDTH - mn_rect_width) / 2
    mn_center_y = (config.CANVAS_HEIGHT - mn_rect_height) / 2
    print(f"\n--- 步驟 1 & 2: 動態尋找中心區域切割深度 ---")
    center_components = []
    initial_component = Component(x=mn_center_x, y=mn_center_y, width=mn_rect_width, height=mn_rect_height, group_id=0, level=0)
    best_trial_components = [initial_component]
    min_diff = float('inf')
    for k in range(1, config.MAX_K_ITERATIONS + 2):
        trial_components = process_component_recursively(initial_component, rule_selector, k)
        print(f"嘗試深度 k={k}，生成 {len(trial_components)} 個元件...")
        if len(trial_components) > target_max * 1.5:
             print(f"已遠超出目標範圍，採用上一個最接近的結果。")
             break
        diff = abs(len(trial_components) - target_count)
        if diff < min_diff:
            min_diff = diff
            best_trial_components = trial_components
            if diff == 0:
                break
    center_components = best_trial_components
    all_final_components.extend(center_components)
    print(f"中心區域最終生成了 {len(center_components)} 個元件。")
    if len(all_final_components) < target_count:
        print(f"\n--- 步驟 3 & 4: 元件數量 ({len(all_final_components)}) 低於目標 {target_count}，開始精細調整 ---")
        filler_group_id_counter = 1
        while len(all_final_components) < target_count:
            placement_successful = False
            for _ in range(200):
                width = random.uniform(config.MIN_FILLER_SIZE, config.MAX_FILLER_SIZE)
                height = random.uniform(config.MIN_FILLER_SIZE, config.MAX_FILLER_SIZE)
                x = random.uniform(mn_center_x, mn_center_x + mn_rect_width - width)
                y = random.uniform(mn_center_y, mn_center_y + mn_rect_height - height)
                new_filler = Component(x, y, width, height, group_id=filler_group_id_counter)
                if not any(check_overlap(new_filler, comp) for comp in all_final_components):
                    all_final_components.append(new_filler)
                    print(f"策略 [填補] 成功：加入 1 個新元件。目前總數: {len(all_final_components)}")
                    filler_group_id_counter += 1
                    placement_successful = True
                    break
            if not placement_successful:
                print("策略 [填補] 失敗：找不到可用空間。改用策略 [切割]。")
                
                # --- 主要修改處：從候選清單中排除對稱元件 ---
                candidates = sorted([
                    c for c in all_final_components if 
                    not c.symmetrical and  # 保護條件：元件不能是對稱的
                    c.width > config.COMPONENT_GAP * 2 and 
                    c.height > config.COMPONENT_GAP * 2
                ], key=lambda c: c.width * c.height, reverse=True)

                if not candidates:
                    print("錯誤：策略 [切割] 失敗，已無任何足夠大的「非對稱」元件可供切割。")
                    break
                component_to_split = candidates[0]
                preferred_direction = 'vertical' if component_to_split.width > component_to_split.height else 'horizontal'
                fallback_direction = 'horizontal' if preferred_direction == 'vertical' else 'vertical'
                params = {"gap": config.COMPONENT_GAP, "ratio": random.uniform(0.3, 0.7)}
                new_components = rule_selector.apply(component_to_split, preferred_direction, "keep_all", **params)
                if len(new_components) <= 1:
                    new_components = rule_selector.apply(component_to_split, fallback_direction, "keep_all", **params)
                if len(new_components) > 1:
                    original_index = next((i for i, comp in enumerate(all_final_components) if comp is component_to_split), -1)
                    if original_index != -1:
                        all_final_components.pop(original_index)
                        all_final_components.extend(new_components)
                        print(f"策略 [切割] 成功：1 個元件變為 2 個。目前總數: {len(all_final_components)}")
                    else:
                        print("嚴重錯誤：在主列表中找不到要替換的元件，程式中止。")
                        break
                else:
                    print(f"錯誤：策略 [切割] 失敗，最大元件在兩個方向上都無法被切割。")
                    break
    elif len(all_final_components) > target_count:
        print(f"\n--- 步驟 5: 元件數量 ({len(all_final_components)}) 高於目標 {target_count}，開始合併 ---")
        all_final_components = reduce_components_to_target(all_final_components, target_count, config.COMPONENT_GAP)
    else:
        print(f"\n中心元件數量 ({len(all_final_components)}) 已精確滿足目標 {target_count}，無需調整。")
    print(f"\n--- 目標達成，總共生成 {len(all_final_components)} 個元件。開始繪圖... ---")
    visualize_placements(all_final_components, (config.CANVAS_WIDTH, config.CANVAS_HEIGHT), (mn_rect_width, mn_rect_height))
    print("圖檔已儲存為 synthetic_layout.png")

if __name__ == "__main__":
    main()