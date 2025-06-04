import numpy as np
import matplotlib.pyplot as plt

# 载入npy文件
depthmap = np.load('result/mask/11m_damped_1/00302.npy')

# 显示图像
plt.imshow(depthmap)
plt.colorbar() # 添加colorbar
plt.show()