import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_scalar_field(x, y):
    """创建一个示例标量场 (例如高度场)"""
    return np.sin(x) * np.cos(y) + x**2 + y**2

def calculate_gradient(x, y):
    """计算标量场的梯度"""
    dx = 2*x + np.cos(x) * np.cos(y)
    dy = -np.sin(x) * np.sin(y) + 2*y
    return dx, dy

def plot_gradient_field():
    # 创建网格点
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    
    # 计算标量场和梯度
    Z = create_scalar_field(X, Y)
    dx, dy = calculate_gradient(X, Y)
    
    # 创建3D图
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # 绘制标量场表面
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    
    # 在选定点绘制梯度向量
    skip = 2
    ax.quiver(X[::skip, ::skip], 
              Y[::skip, ::skip], 
              Z[::skip, ::skip],
              dx[::skip, ::skip], 
              dy[::skip, ::skip], 
              np.zeros_like(X[::skip, ::skip]),
              color='r', length=0.3)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('标量场及其梯度向量')
    
    plt.colorbar(surf)
    plt.show()

if __name__ == "__main__":
    plot_gradient_field() 