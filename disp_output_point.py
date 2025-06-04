
import pandas as pd
import os
import cv2, numpy as np

# ========= 配 置 =========
# 掩码视频（纯黑白或叠加也行，只要能二值化）
MASK_VIDEO = "/home/edison/projects/Track-Anything/result/track/11m_free_1.mp4"
OUT_VIDEO  = "annotated_mask_center_11m_free_1.mp4"
OUT_CSV    = "displacement_bbox_center_11m_damped_1.csv"

# 如果是“叠加”视频，需要先提取前景颜色；若已是二值掩码则设为 None
HSV_RANGE = (np.array([  5, 100, 100]),  # lower H,S,V  (橙红色)
            np.array([ 25, 255, 255]))  # upper H,S,V
# ========= END =========


def binarize(frame_bgr):
    gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
    # Otsu 自动分出“亮的叠加区” vs “暗的背景”
    _, mask = cv2.threshold(gray, 0, 255,
                            cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 可选闭运算填洞
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    return mask


def largest_component_bbox(mask):
    """
    返回面积最大的连通域的外接矩形中心 (cx, cy)。
    若无前景返回 None。
    """
    num, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    if num <= 1:               # 只有背景
        return None
    # stats[1:] 排除第 0 行背景，取面积最大行
    largest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    x, y, w, h, _ = stats[largest]
    cx, cy = x + w / 2, y + h / 2
    return int(cx), int(cy)


def main():
    cap = cv2.VideoCapture(MASK_VIDEO)
    if not cap.isOpened():
        raise RuntimeError(f"无法打开视频 {MASK_VIDEO}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out_v  = cv2.VideoWriter(OUT_VIDEO, fourcc, fps, (W, H))

    times, disps = [], []

    frame_idx = 0
    cy0 = None  # 初始中心 y

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mask = binarize(frame)
        center = largest_component_bbox(mask)
        if center is not None:
            cx, cy = center
            if cy0 is None:
                cy0 = cy  # 第一帧记录基准
            disp = cy0 - cy
            # 画标记
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1, cv2.LINE_AA)
            cv2.putText(frame,
                        f"disp: {disp:.1f}px",
                        (10, H - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (255, 255, 255), 2, cv2.LINE_AA)
        else:
            disp = np.nan
            cv2.putText(frame,
                        "disp: --",
                        (10, H - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                        (255, 255, 255), 2, cv2.LINE_AA)

        out_v.write(frame)

        times.append(frame_idx / fps)
        disps.append(disp)
        frame_idx += 1

    cap.release()
    out_v.release()

    # 保存 CSV
    df = pd.DataFrame({"time_s": times, "disp_px": disps})
    df.to_csv(OUT_CSV, index=False)

    print("✅ 已生成:")
    print("   • 标注视频 :", os.path.abspath(OUT_VIDEO))
    print("   • 位移数据 :", os.path.abspath(OUT_CSV))


if __name__ == "__main__":
    main()
