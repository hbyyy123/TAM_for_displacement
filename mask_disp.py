import numpy as np
import pandas as pd
import os
import cv2

# ——— 配置 ———
# 掩码 NPY 文件夹
MASK_DIR = "/home/edison/projects/Track-Anything/result/mask/17m_180kg_free"
# 输出 CSV 路径
OUT_CSV   = "displacement_from_npy_17m_180kg_free.csv"
# 原始视频（可选，用来获取 fps；如果知道帧率，也可以直接写一个常数）
ORIG_VIDEO = "/home/edison/projects/Track-Anything/result/track/17m_180kg_free.mp4"
# ——————————

# 1) 读帧率
cap = cv2.VideoCapture(ORIG_VIDEO)
fps = cap.get(cv2.CAP_PROP_FPS) or 30
cap.release()

# 2) 列出并排序所有 npy
files = sorted([f for f in os.listdir(MASK_DIR) if f.endswith(".npy")])
times, disps = [], []

y0 = None
for idx, fn in enumerate(files):
    mask = np.load(os.path.join(MASK_DIR, fn))  # 0/1 或 0/255
    # 如果是 0/255，先归一到 0/1
    if mask.max() > 1:
        mask = (mask > 0).astype(np.uint8)
    # 计算质心（所有前景像素的平均位置）
    ys, xs = np.nonzero(mask)      # ys: 所有行索引
    if len(ys)==0:
        cy = np.nan
    else:
        cy = ys.mean()
    if y0 is None:
        y0 = cy                      # 第一帧基准
    disp = (y0 - cy) if not np.isnan(cy) else np.nan

    times.append(idx / fps)
    disps.append(disp)

# 3) 存成 CSV
df = pd.DataFrame({"time_s": times, "disp_px": disps})
df.to_csv(OUT_CSV, index=False)
print(f"Done → {OUT_CSV}")
