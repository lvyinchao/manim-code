import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# 创建一个二次函数作为示例
def f(x, y):
    return 2*x**2 + 3*y**2 + 2*x*y

# 计算Hessian矩阵
def hessian(x, y):
    return np.array([[4, 2],
                    [2, 6]])

# 创建网格点
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# 设置图形
fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(121, projection='3d')
ax2 = fig.add_subplot(122)

# 绘制3D曲面
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
ax1.set_title('3D曲面和Hessian特征向量')

# 绘制等高线
contour = ax2.contour(X, Y, Z, levels=20, cmap='viridis')
ax2.set_title('等高线图和Hessian特征向量')
plt.colorbar(contour)

# 计算特征值和特征向量
H = hessian(0, 0)
eigvals, eigvecs = np.linalg.eig(H)

# 动画函数
def update(frame):
    ax1.clear()
    ax2.clear()
    
    # 重新绘制3D曲面
    surf = ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax1.set_title('3D曲面和Hessian特征向量')
    
    # 重新绘制等高线
    contour = ax2.contour(X, Y, Z, levels=20, cmap='viridis')
    ax2.set_title('等高线图和Hessian特征向量')
    
    # 计算当前角度
    angle = frame * 2 * np.pi / 100
    
    # 绘制特征向量
    for i in range(2):
        # 3D图
        vec = eigvecs[:, i] * np.cos(angle) + np.roll(eigvecs[:, i], 1) * np.sin(angle)
        ax1.quiver(0, 0, f(0, 0), vec[0], vec[1], 0, 
                  color='red', alpha=0.6, length=2)
        
        # 等高线图
        ax2.quiver(0, 0, vec[0], vec[1], 
                  color='red', alpha=0.6, scale=2)
    
    # 设置坐标轴范围
    ax1.set_xlim([-3, 3])
    ax1.set_ylim([-3, 3])
    ax1.set_zlim([0, 30])
    
    ax2.set_xlim([-3, 3])
    ax2.set_ylim([-3, 3])
    
    return surf, contour

# 创建动画
anim = FuncAnimation(fig, update, frames=100, interval=50, blit=True)
plt.tight_layout()
plt.show() 