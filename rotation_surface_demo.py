import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm

def generate_curve_points(t):
    """生成初始曲线的点"""
    # 这里我们使用一个简单的抛物线作为示例
    x = t
    y = t**2
    return x, y

def create_rotation_surface(t, theta):
    """生成旋转曲面上的点"""
    x, y = generate_curve_points(t)
    # 绕 y 轴旋转
    X = x * np.cos(theta)
    Z = x * np.sin(theta)
    Y = y
    return X, Y, Z

def update(frame):
    """更新动画帧"""
    ax.cla()
    
    # 设置视角
    ax.view_init(elev=30, azim=frame)
    
    # 生成网格点
    t = np.linspace(-2, 2, 100)
    theta = np.linspace(0, 2*np.pi, 100)
    T, Theta = np.meshgrid(t, theta)
    
    # 计算曲面上的点
    X, Y, Z = create_rotation_surface(T.flatten(), Theta.flatten())
    X = X.reshape(T.shape)
    Y = Y.reshape(T.shape)
    Z = Z.reshape(T.shape)
    
    # 绘制曲面
    surf = ax.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8)
    
    # 绘制初始曲线
    t_curve = np.linspace(-2, 2, 100)
    x_curve, y_curve = generate_curve_points(t_curve)
    ax.plot(x_curve, y_curve, np.zeros_like(x_curve), 'r-', linewidth=2, label='初始曲线')
    
    # 设置坐标轴标签
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('旋转曲面构成过程演示')
    
    # 设置坐标轴范围
    ax.set_xlim(-2, 2)
    ax.set_ylim(0, 4)
    ax.set_zlim(-2, 2)
    
    return surf,

# 创建图形和3D坐标轴
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 创建动画
ani = FuncAnimation(fig, update, frames=np.linspace(0, 360, 180),
                   interval=50, blit=False)

# 显示动画
plt.show() 