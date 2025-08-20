# config.py

# --- 畫布設定 ---
CANVAS_WIDTH = 2.0
CANVAS_HEIGHT = 2.0

# --- 初始 m*n 矩形設定 ---
MN_RECT_AREA_RANGE = (1.8, 2.5)      # 設定 m*n 矩形的隨機面積範圍
MN_ASPECT_RATIO_RANGE = (0.7, 1.4)   # 設定 m*n 矩形的長寬比 (寬/高) 隨機範圍

# --- 流程控制參數 ---
# K_ITERATIONS = 5                 <- 舊設定，已移除
MAX_K_ITERATIONS = 5             # 動態尋找合適深度時的最大嘗試深度
MAX_J_ITERATIONS = 2             # 填補元件切割遞迴深度的「最大值」

# --- 總元件數量控制 ---
TOTAL_COMPONENT_COUNT_RANGE = (10, 50) # 期望產生的總元件數量隨機範圍
MAX_FILLER_GROUPS = 50                  # 安全機制：最多嘗試生成 50 組填補元件，避免無限迴圈

# --- 元件尺寸與間隙 ---
MIN_FILLER_SIZE = 0.05
MAX_FILLER_SIZE = 0.2
COMPONENT_GAP = 0.01      # 元件間的最小間隙

# --- 元件幾何限制 ---
MAX_ASPECT_RATIO = 6.0    # 元件的寬高比或高寬比最大值

# --- 新增：規則選擇權重 ---
# 數值越大，該規則被選中的機率越高。
# 您可以根據需求調整這些權重。
RULE_WEIGHTS = {
    # --- 基本不對稱規則 ---
    "vertical": 8,
    "horizontal": 8,
    "quadrants": 6,
    "aligned": 4,
    
    # --- 對稱規則 (依照您的要求調整) ---
    # 1. 水平/垂直鏡像對稱 (最高機率)
    "mirrored_vertical": 12,
    "mirrored_horizontal": 12,
    
    # 2. 共質心對稱 (中等機率)
    "common_centroid": 7,
    
    # 3. 三元件對稱 (最低機率)
    "triplet_vertical": 2,
    "triplet_horizontal": 2,
}