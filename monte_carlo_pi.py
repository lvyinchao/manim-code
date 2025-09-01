import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 参数设置
num_samples = 2000    # 总样本数
batch_size = 20      # 每次动画更新添加的点数
radius = 1.0         # 圆半径

# 创建图形和轴
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
fig.suptitle('蒙特卡洛方法估算π值', fontsize=14)

# 初始化数据存储
x_points = []
y_points = []
pi_estimates = []
frame_numbers = []

# 设置坐标轴
ax1.set_xlim(0, radius)
ax1.set_ylim(0, radius)
ax1.set_aspect('equal')
ax1.set_xlabel('x')
ax1.set_ylabel('y')
ax1.grid(True)

# 绘制1/4圆弧
theta = np.linspace(0, np.pi/2, 100)
ax1.plot(radius * np.cos(theta), radius * np.sin(theta), 'k-')

# 设置π值估计图
ax2.set_xlim(0, num_samples)
ax2.set_ylim(2.8, 3.4)
ax2.set_xlabel('采样点数')
ax2.set_ylabel('π值估计')
ax2.grid(True)
ax2.axhline(y=np.pi, color='r', linestyle='--', label='实际π值')
ax2.legend()

# 散点和线的初始化
scatter_inside = ax1.scatter([], [], c='blue', s=2, label='圆内')
scatter_outside = ax1.scatter([], [], c='red', s=2, label='圆外')
line, = ax2.plot([], [], 'g-', label='估计值')
ax1.legend()

def init():
    """初始化动画"""
    return scatter_inside, scatter_outside, line

def update(frame):
    """更新动画帧"""
    # 生成新的随机点
    new_x = np.random.uniform(0, radius, batch_size)
    new_y = np.random.uniform(0, radius, batch_size)
    
    # 添加新点到列表
    x_points.extend(new_x)
    y_points.extend(new_y)
    
    # 计算点到原点的距离
    distances = np.sqrt(np.array(x_points)**2 + np.array(y_points)**2)
    inside = distances <= radius
    
    # 更新散点图
    scatter_inside.set_offsets(np.c_[np.array(x_points)[inside], 
                                   np.array(y_points)[inside]])
    scatter_outside.set_offsets(np.c_[np.array(x_points)[~inside], 
                                    np.array(y_points)[~inside]])
    
    # 计算并存储π值估计
    pi_estimate = 4 * np.sum(inside) / len(x_points)
    pi_estimates.append(pi_estimate)
    frame_numbers.append(len(x_points))
    
    # 更新π值估计图
    line.set_data(frame_numbers, pi_estimates)
    
    # 更新标题
    ax1.set_title(f'采样点数: {len(x_points)}')
    ax2.set_title(f'π估计值: {pi_estimate:.4f}')
    
    return scatter_inside, scatter_outside, line

# 创建动画
anim = FuncAnimation(fig, update, frames=num_samples//batch_size,
                    init_func=init, blit=True, interval=1)

plt.tight_layout()
plt.show() 