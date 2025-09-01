import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 设置图形和坐标轴
fig, ax = plt.subplots(figsize=(10, 6))
plt.style.use('seaborn-v0_8')

# 定义函数 f(x) = x^3 - 2x^2 + 2
def f(x):
    return x**3 - 2*x**2 + 2

# 定义函数的导数 f'(x)
def df(x):
    return 3*x**2 - 4*x

# 设置 x 的范围和函数图像
a, b = 0, 2  # 区间 [a, b]
x = np.linspace(-0.5, 2.5, 1000)
y = f(x)

# 计算割线斜率
secant_slope = (f(b) - f(a)) / (b - a)

# 绘制函数图像
ax.plot(x, y, 'b-', linewidth=2, label=r'$f(x) = x^3 - 2x^2 + 2$')

# 标记区间端点
ax.plot(a, f(a), 'ro', markersize=8)
ax.plot(b, f(b), 'ro', markersize=8)

# 绘制割线
x_secant = np.array([a, b])
y_secant = np.array([f(a), f(b)])
secant_line, = ax.plot(x_secant, y_secant, 'r-', linewidth=2, 
                      label=f'割线 (斜率: {secant_slope:.2f})')

# 初始化切线
tangent_point, = ax.plot([], [], 'go', markersize=8)
tangent_line, = ax.plot([], [], 'g-', linewidth=2)
tangent_text = ax.text(1.5, 0, '', fontsize=12)

# 找到使 f'(c) = secant_slope 的点 c
# 对于我们的函数，可以解方程 3c^2 - 4c = secant_slope
# 这里我们使用数值方法找近似解
x_vals = np.linspace(a, b, 1000)
slopes = df(x_vals)
c_index = np.argmin(np.abs(slopes - secant_slope))
c = x_vals[c_index]

# 动画更新函数
def update(frame):
    t = frame / 100  # 从0到1的参数
    
    # 在动画开始时只显示函数和区间端点
    if t < 0.2:
        tangent_point.set_data([], [])
        tangent_line.set_data([], [])
        tangent_text.set_text('')
        return tangent_point, tangent_line, tangent_text
    
    # 显示割线
    if t < 0.4:
        tangent_point.set_data([], [])
        tangent_line.set_data([], [])
        tangent_text.set_text('割线斜率 = {:.2f}'.format(secant_slope))
        return tangent_point, tangent_line, tangent_text
    
    # 移动切点并显示切线
    if t < 1:
        # 从 a 移动到 c
        current_x = a + (c - a) * ((t - 0.4) / 0.6)
        current_y = f(current_x)
        current_slope = df(current_x)
        
        # 在当前点绘制切线
        x_tangent = np.array([current_x - 0.5, current_x + 0.5])
        y_tangent = current_y + current_slope * (x_tangent - current_x)
        
        tangent_point.set_data([current_x], [current_y])
        tangent_line.set_data(x_tangent, y_tangent)
        tangent_text.set_text('切线斜率 = {:.2f}'.format(current_slope))
        
        return tangent_point, tangent_line, tangent_text
    
    # 显示最终结果（c点处的切线）
    current_x = c
    current_y = f(c)
    current_slope = df(c)
    
    x_tangent = np.array([current_x - 0.5, current_x + 0.5])
    y_tangent = current_y + current_slope * (x_tangent - current_x)
    
    tangent_point.set_data([current_x], [current_y])
    tangent_line.set_data(x_tangent, y_tangent)
    tangent_text.set_text('在 x = {:.2f} 处的切线斜率 = {:.2f}'.format(c, current_slope))
    
    return tangent_point, tangent_line, tangent_text

# 设置图例和标签
ax.legend(loc='upper left')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('微分中值定理动画演示')
ax.grid(True)

# 创建动画
ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)

# 保存动画（可选）
# ani.save('mean_value_theorem.gif', writer='pillow', fps=20)

plt.tight_layout()
plt.show() 