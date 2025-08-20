# config.py

# --- 畫布設定 ---
CANVAS_WIDTH = 2.0
CANVAS_HEIGHT = 2.0

# --- 初始 m*n 矩形設定 ---
MN_RECT_AREA_RANGE = (1.8, 2.5)      # 設定 m*n 矩形的隨機面積範圍
MN_ASPECT_RATIO_RANGE = (0.7, 1.4)   # 設定 m*n 矩形的長寬比 (寬/高) 隨機範圍

# --- 流程控制參數 ---
K_ITERATIONS = 5          # 中心區域初始切割遞迴深度
# J_ITERATIONS = 2        <- 舊設定
MAX_J_ITERATIONS = 2      # 填補元件切割遞迴深度的「最大值」
NUM_FILLER_COMPONENTS = 10 # 填補元件的數量

# --- 元件尺寸與間隙 ---
MIN_FILLER_SIZE = 0.05
MAX_FILLER_SIZE = 0.2
COMPONENT_GAP = 0.01      # 元件間的最小間隙

# --- 元件幾何限制 ---
MAX_ASPECT_RATIO = 6.0    # 元件的寬高比或高寬比最大值