# format_for_ml.py

# -*- coding: utf-8 -*-
"""
此腳本用於將 `production.ipynb` 產生的佈局 JSON 資料，
轉換為機器學習模型所需的格式。

1. 將所有元件內容的中心點對齊到一個固定的 1000x1000 畫布的中心。
2. 節點特徵 ('node') 使用元件的 [寬, 高] 尺寸，並基於 1000x1000 畫布進行正規化 。
3. 座標 ('target') 和邊偏移 ('edge' offset) 也基於這個 1000x1000 的畫布進行正規化。
"""

import os
import json
import glob
import yaml
from typing import List, Dict, Any, Tuple
from collections import defaultdict

# 遵循論文方法，我們需要一個固定的基準畫布尺寸來進行正規化
TARGET_CANVAS_DIM = 1000.0

def load_config(config_path: str = 'config.yaml') -> Dict[str, Any]:
    """從指定的路徑載入 YAML 設定檔。"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ 錯誤：找不到設定檔 '{config_path}'。")
        return None
    except yaml.YAMLError as e:
        print(f"❌ 錯誤：解析 YAML 檔案 '{config_path}' 失敗: {e}")
        return None

def find_parent_component_index(pin_coords: Tuple[float, float], components: List[Dict[str, Any]]) -> int:
    """
    根據 pin 的絕對座標，在元件列表中找到其所屬的父元件索引。
    """
    px, py = pin_coords
    for i, comp in enumerate(components):
        left = comp['x'] - comp['width'] / 2
        right = comp['x'] + comp['width'] / 2
        top = comp['y'] - comp['height'] / 2
        bottom = comp['y'] + comp['height'] / 2
        if (left - 1e-6) <= px <= (right + 1e-6) and (top - 1e-6) <= py <= (bottom + 1e-6):
            return i
    return None

def format_single_layout(input_path: str, output_path: str):
    """
    將單一的 layout.json 檔案轉換為 ML-ready 格式。
    """
    print(f"🔄 正在處理: {os.path.basename(input_path)}")
    
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    leaf_components = data.get("final_leaf_components", [])
    if not leaf_components:
        print(f"⚠️ 警告：找不到 'final_leaf_components'，跳過此檔案。")
        return
        
    netlist_edges = data.get("netlist_edges", [])

    # --- [功能1] 計算所有元件的內容邊界與中心 (使用原始座標) ---
    min_x = min(comp['x'] - comp['width'] / 2 for comp in leaf_components)
    max_x = max(comp['x'] + comp['width'] / 2 for comp in leaf_components)
    min_y = min(comp['y'] - comp['height'] / 2 for comp in leaf_components)
    max_y = max(comp['y'] + comp['height'] / 2 for comp in leaf_components)
    content_center_x = (min_x + max_x) / 2
    content_center_y = (min_y + max_y) / 2
    
    ml_nodes = []
    ml_targets = []
    ml_sub_components = []
    
    # 遍歷所有元件
    for comp in leaf_components:
        # ✨ [修改] 遵循論文，對元件尺寸進行正規化 
        # 使用 TARGET_CANVAS_DIM 作為正規化的基準
        norm_w = comp['width'] / (TARGET_CANVAS_DIM / 2)
        norm_h = comp['height'] / (TARGET_CANVAS_DIM / 2)
        ml_nodes.append([norm_w, norm_h])

        # --- 座標處理 ---
        # 1. 計算元件相對於內容中心的偏移
        shifted_x = comp['x'] - content_center_x
        shifted_y = comp['y'] - content_center_y
        
        # 2. 遵循論文，使用 TARGET_CANVAS_DIM 來正規化座標 
        norm_x = shifted_x / (TARGET_CANVAS_DIM / 2)
        norm_y = shifted_y / (TARGET_CANVAS_DIM / 2)
        ml_targets.append([norm_x, norm_y])
        
        # sub_components 依然儲存原始絕對尺寸，供未來視覺化或還原使用
        ml_sub_components.append([
            {
                "offset": [0.0, 0.0],
                "dims": [comp['width'], comp['height']]
            }
        ])

    # 處理 edges
    basic_component_edges = []
    for edge in netlist_edges:
        src_pin_abs, dest_pin_abs = tuple(edge[0]), tuple(edge[1])
        src_comp_idx = find_parent_component_index(src_pin_abs, leaf_components)
        dest_comp_idx = find_parent_component_index(dest_pin_abs, leaf_components)
        
        if src_comp_idx is not None and dest_comp_idx is not None:
            src_comp = leaf_components[src_comp_idx]
            dest_comp = leaf_components[dest_comp_idx]
            
            # Pin的偏移量也必須基於新的目標畫布尺寸進行正規化，以保持座標系一致 
            src_offset_x = (src_pin_abs[0] - src_comp['x']) / (TARGET_CANVAS_DIM / 2)
            src_offset_y = (src_pin_abs[1] - src_comp['y']) / (TARGET_CANVAS_DIM / 2)
            dest_offset_x = (dest_pin_abs[0] - dest_comp['x']) / (TARGET_CANVAS_DIM / 2)
            dest_offset_y = (dest_pin_abs[1] - dest_comp['y']) / (TARGET_CANVAS_DIM / 2)
            
            basic_component_edges.append([
                [src_comp_idx, dest_comp_idx],
                [src_offset_x, src_offset_y, dest_offset_x, dest_offset_y]
            ])

    # 處理對稱群組資訊
    symmetry_groups_map = defaultdict(list)
    for i, comp in enumerate(leaf_components):
        group_id = comp.get("symmetric_group_id", -1)
        if group_id != -1:
            symmetry_groups_map[group_id].append(i)
    ml_symmetry_groups = [indices for indices in symmetry_groups_map.values() if len(indices) == 2]

    # 組合最終的 ML-ready JSON 物件
    ml_data = {
        "node": ml_nodes,
        "target": ml_targets,
        "edges": { "basic_component_edge": basic_component_edges, "align_edge": [], "group_edge": [] },
        "sub_components": ml_sub_components,
        "symmetry_groups": ml_symmetry_groups
    }

    # 寫入檔案
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(ml_data, f, indent=2)
        print(f"✅ 成功轉換並儲存至: {os.path.basename(output_path)}")
    except Exception as e:
        print(f"❌ 寫入 {output_path} 時發生錯誤: {e}")

def main():
    """主執行函式"""
    print("--- 開始執行佈局資料轉換任務 (遵循論文方法) ---")
    path_cfg = load_config().get('path_settings', {})
    raw_dir, ml_dir = path_cfg.get('raw_output_directory'), path_cfg.get('ml_ready_output_directory')
    
    if not raw_dir or not ml_dir:
        print("❌ 錯誤：config.yaml 中缺少路徑設定。")
        return

    input_folder = os.path.join(raw_dir, path_cfg.get('json_subdirectory', 'json_data'))
    os.makedirs(ml_dir, exist_ok=True)
    input_files = glob.glob(os.path.join(input_folder, '*.json'))

    if not input_files:
        print(f"⚠️ 在 '{input_folder}' 中找不到任何 .json 檔案。")
        return
        
    print(f"🔍 發現 {len(input_files)} 個檔案。")
    print(f"🎨 將使用目標畫布尺寸: {TARGET_CANVAS_DIM}x{TARGET_CANVAS_DIM} 進行正規化。")
    print("-" * 40)

    for input_file_path in input_files:
        basename = os.path.basename(input_file_path).replace('.json', '')
        output_filename = f"formatted_{basename.split('_')[-1]}.json"
        output_file_path = os.path.join(ml_dir, output_filename)
        format_single_layout(input_file_path, output_file_path)
        print("-" * 20)

    print("✨ 所有檔案轉換完畢！ ✨")

if __name__ == "__main__":
    main()