import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(x, y):
    """示例二元函数：f(x,y) = x^2 + y^2 + 2xy"""
    return x**2 + y**2 + 2*x*y

def partial_x(x, y):
    """对x的偏导数"""
    return 2*x + 2*y

def partial_y(x, y):
    """对y的偏导数"""
    return 2*y + 2*x

def hessian(x, y):
    """计算Hessian矩阵"""
    return np.array([[2, 2],
                     [2, 2]])

def check_extremum(x, y):
    """判断极值类型"""
    H = hessian(x, y)
    det = np.linalg.det(H)
    trace = np.trace(H)
    
    if det > 0:
        if trace > 0:
            return "极小值点"
        else:
            return "极大值点"
    elif det < 0:
        return "鞍点"
    else:
        return "无法判断"

def plot_function():
    """绘制函数图像和极值点"""
    # 创建网格点
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    
    # 创建图形
    fig = plt.figure(figsize=(12, 5))
    
    # 3D表面图
    ax1 = fig.add_subplot(121, projection='3d')
    surf = ax1.plot_surface(X, Y, Z, cmap='viridis')
    ax1.set_title('二元函数f(x,y) = x² + y² + 2xy')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('f(x,y)')
    
    # 等高线图
    ax2 = fig.add_subplot(122)
    contour = ax2.contour(X, Y, Z, levels=20)
    ax2.clabel(contour, inline=True, fontsize=8)
    ax2.set_title('等高线图')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    
    # 添加极值点
    critical_points = [(0, 0)]
    for point in critical_points:
        x, y = point
        extremum_type = check_extremum(x, y)
        ax2.plot(x, y, 'r*', markersize=10, label=f'({x}, {y}): {extremum_type}')
    
    ax2.legend()
    plt.tight_layout()
    plt.show()

def print_analysis():
    """打印分析过程"""
    print("二元函数极值分析过程：")
    print("\n1. 计算偏导数：")
    print("∂f/∂x = 2x + 2y")
    print("∂f/∂y = 2y + 2x")
    
    print("\n2. 求临界点：")
    print("令 ∂f/∂x = 0 且 ∂f/∂y = 0")
    print("解得：x = 0, y = 0")
    
    print("\n3. 计算Hessian矩阵：")
    H = hessian(0, 0)
    print(f"H = \n{H}")
    
    print("\n4. 判断极值类型：")
    det = np.linalg.det(H)
    trace = np.trace(H)
    print(f"行列式 det(H) = {det}")
    print(f"迹 tr(H) = {trace}")
    print(f"结论：{check_extremum(0, 0)}")

if __name__ == "__main__":
    print_analysis()
    plot_function() 