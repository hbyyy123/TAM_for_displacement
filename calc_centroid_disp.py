import cv2
import numpy as np
import pandas as pd

# —— 配置区 ——
OVERLAY_VIDEO = "/home/edison/projects/Track-Anything/result/track/11m_damped_1.mp4"
OUT_CSV       = "displacement_centroid.csv"
# —— end 配置区 ——

def extract_binary_mask(frame_bgr):
    """从叠加帧中提取二值掩码（假设掩码是橙色）。"""
    hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    lower = np.array([5, 100, 100])
    upper = np.array([25, 255, 255])
    mask = cv2.inRange(hsv, lower, upper)
    return mask

def compute_centroid_y(mask):
    """计算二值 mask 的重心 y，如果前景像素为空则返回 np.nan。"""
    M = cv2.moments(mask)
    if M["m00"] == 0:
        return np.nan
    return M["m01"] / M["m00"]

def main():
    cap = cv2.VideoCapture(OVERLAY_VIDEO)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30

    # 读第一帧，计算初始重心 y0
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError(f"无法读取视频 {OVERLAY_VIDEO}")
    mask0 = extract_binary_mask(frame)
    y0 = compute_centroid_y(mask0)

    times, disps = [0.0], [0.0]  # 第0帧位移 0
    idx = 1

    # 遍历其余帧
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        mask = extract_binary_mask(frame)
        y  = compute_centroid_y(mask)
        disp = (y0 - y) if not np.isnan(y) else np.nan
        times.append(idx / fps)
        disps.append(disp)
        idx += 1

    cap.release()

    # 输出 CSV
    df = pd.DataFrame({"time_s": times, "disp_px": disps})
    df.to_csv(OUT_CSV, index=False)
    print(f"已保存: {OUT_CSV}")

if __name__ == "__main__":
    main()
