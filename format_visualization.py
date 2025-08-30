# -*- coding: utf-8 -*-
"""
此腳本用於視覺化 `format_for_ml.py` 產生的 ML-ready JSON 檔案，
以驗證資料轉換的正確性。
(新版：增加了對稱群組的視覺化功能，以不同顏色標示)
"""

import os
import json
import glob
import yaml
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Tuple

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

def plot_formatted_layout(data: Dict[str, Any], output_path: str, canvas_size: Tuple[int, int] = (1000, 1000)):
    """
    根據單一 formatted JSON 檔案的資料繪製佈局圖。
    """
    canvas_w, canvas_h = canvas_size
    nodes = data.get("node", [])
    targets = data.get("target", [])
    edges = data.get("edges", {}).get("basic_component_edge", [])
    # --- [新增] 讀取對稱群組資訊 ---
    symmetry_groups = data.get("symmetry_groups", [])

    if not nodes or not targets:
        print(f"⚠️ 警告：檔案缺少 'node' 或 'target' 資料，無法繪圖。")
        return

    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_facecolor('#f0f0f0')

    # --- [新增] 為對稱群組準備顏色 ---
    SYMMETRY_COLORS = ['#ff796c', '#6cff79', '#796cff', '#ffc56c', '#6cffc5', '#c56cff']
    component_colors = {}
    for i, pair in enumerate(symmetry_groups):
        color = SYMMETRY_COLORS[i % len(SYMMETRY_COLORS)]
        if len(pair) == 2:
            component_colors[pair[0]] = color
            component_colors[pair[1]] = color

    # 1. 繪製元件 (Nodes)
    components = []
    for i in range(len(nodes)):
        norm_w, norm_h = nodes[i]
        norm_x, norm_y = targets[i]
        
        abs_w = norm_w * canvas_w
        abs_h = norm_h * canvas_h
        abs_x = norm_x * (canvas_w / 2)
        abs_y = norm_y * (canvas_h / 2)
        
        top_left_x = abs_x - abs_w / 2
        top_left_y = abs_y - abs_h / 2
        
        components.append({'x': abs_x, 'y': abs_y, 'w': abs_w, 'h': abs_h})

        # --- [修改] 根據是否為對稱元件，決定顏色 ---
        face_color = component_colors.get(i, 'skyblue') # 預設為 skyblue，對稱則使用指定顏色

        rect = plt.Rectangle(
            (top_left_x, top_left_y), abs_w, abs_h,
            linewidth=1, edgecolor='black', facecolor=face_color, alpha=0.7
        )
        ax.add_patch(rect)
        ax.text(abs_x, abs_y, str(i), ha='center', va='center', fontsize=8, color='black')

    # 2. 繪製網路線 (Edges)
    all_pins = set()
    for edge_info in edges:
        indices, offsets = edge_info
        src_idx, dest_idx = indices
        src_off_x, src_off_y, dest_off_x, dest_off_y = offsets

        if src_idx < len(components) and dest_idx < len(components):
            src_comp = components[src_idx]
            dest_comp = components[dest_idx]

            src_pin_x = src_comp['x'] + src_off_x * (canvas_w / 2)
            src_pin_y = src_comp['y'] + src_off_y * (canvas_h / 2)
            dest_pin_x = dest_comp['x'] + dest_off_x * (canvas_w / 2)
            dest_pin_y = dest_comp['y'] + dest_off_y * (canvas_h / 2)

            ax.plot([src_pin_x, dest_pin_x], [src_pin_y, dest_pin_y], color='#555555', linestyle='-', linewidth=0.8, alpha=0.7)
            all_pins.add((src_pin_x, src_pin_y))
            all_pins.add((dest_pin_x, dest_pin_y))

    # 3. 繪製 Pin 點
    for px, py in all_pins:
        ax.plot(px, py, 'o', color='black', markersize=3)
    
    # 設定圖表外觀
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlim(-canvas_w/2 - 50, canvas_w/2 + 50)
    ax.set_ylim(-canvas_h/2 - 50, canvas_h/2 + 50)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.title(f"視覺化: {os.path.basename(output_path)}", fontsize=16)
    plt.xlabel("X 座標")
    plt.ylabel("Y 座標")
    
    # 儲存圖片
    try:
        plt.savefig(output_path, dpi=150)
        print(f"🖼️  視覺化圖片已儲存至: {os.path.basename(output_path)}")
    except Exception as e:
        print(f"❌ 寫入圖片 {output_path} 時發生錯誤: {e}")
    finally:
        plt.close(fig)

def main():
    """主執行函式"""
    print("--- 開始執行 ML-ready 資料視覺化任務 ---")
    config = load_config()
    if not config:
        return

    path_cfg = config.get('path_settings', {})
    ml_dir = path_cfg.get('ml_ready_output_directory')
    viz_dir = path_cfg.get('visualization_output_directory')

    if not ml_dir or not viz_dir:
        print("❌ 錯誤：config.yaml 中缺少 'ml_ready_output_directory' 或 'visualization_output_directory' 設定。")
        return
        
    os.makedirs(viz_dir, exist_ok=True)
    
    input_files = glob.glob(os.path.join(ml_dir, 'formatted_*.json'))

    if not input_files:
        print(f"⚠️ 在 '{ml_dir}' 中找不到任何 'formatted_*.json' 檔案。")
        return
        
    print(f"🔍 發現 {len(input_files)} 個已格式化的 JSON 檔案，準備進行視覺化...")
    print("-" * 40)
    
    for input_file in input_files:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = json.load(f)
            
            base_name = os.path.basename(input_file).replace('.json', '')
            output_image_path = os.path.join(viz_dir, f"{base_name}_visualization.png")
            
            plot_formatted_layout(content, output_image_path)
            
        except json.JSONDecodeError:
            print(f"⚠️ 警告：無法解析 {os.path.basename(input_file)}，檔案可能已損壞。")
        except Exception as e:
            print(f"處理 {os.path.basename(input_file)} 時發生未知錯誤: {e}")
        finally:
            print("-" * 20)

    print("✨ 所有視覺化任務執行完畢！ ✨")

if __name__ == "__main__":
    main()