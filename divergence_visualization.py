import numpy as np
import matplotlib.pyplot as plt

def create_vector_field(x, y):
    """创建一个示例矢量场"""
    u = x
    v = -y
    return u, v

def calculate_divergence(x, y):
    """计算矢量场的散度"""
    return np.ones_like(x) - np.ones_like(y)

def plot_divergence_field():
    # 创建网格点
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    
    # 计算矢量场和散度
    U, V = create_vector_field(X, Y)
    div = calculate_divergence(X, Y)
    
    # 创建图形
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # 绘制矢量场
    ax1.quiver(X, Y, U, V)
    ax1.set_title('矢量场')
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    
    # 绘制散度场
    div_plot = ax2.contourf(X, Y, div, cmap='RdBu')
    ax2.set_title('散度场')
    ax2.set_xlabel('X')
    ax2.set_ylabel('Y')
    
    plt.colorbar(div_plot, ax=ax2)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_divergence_field() 