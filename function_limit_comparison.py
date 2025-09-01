#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个程序用动画对比一元函数和二元函数的概念及其极限
作者: Claude
日期: 2023-07-10
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.rcParams['axes.unicode_minus'] = False    # 正常显示负号

def create_animation():
    """创建动画对比一元函数和二元函数的概念和极限"""
    
    # 创建图形和子图布局
    fig = plt.figure(figsize=(16, 8))
    
    # 添加一元函数子图
    ax1 = fig.add_subplot(121)
    ax1.set_xlim(-5, 5)
    ax1.set_ylim(-3, 3)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title('一元函数 f(x) = sin(x)/x 的极限')
    ax1.grid(True)
    ax1.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    
    # 添加二元函数子图
    ax2 = fig.add_subplot(122, projection='3d')
    ax2.set_xlim(-5, 5)
    ax2.set_ylim(-5, 5)
    ax2.set_zlim(-1, 1)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_zlabel('f(x,y)')
    ax2.set_title('二元函数 f(x,y) = sin(√(x²+y²))/√(x²+y²) 的极限')
    
    # 一元函数 f(x) = sin(x)/x
    def f1(x):
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.sin(x) / x
        return result
    
    # 二元函数 f(x,y) = sin(√(x²+y²))/√(x²+y²)
    def f2(x, y):
        r = np.sqrt(x**2 + y**2)
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.sin(r) / r
        # 处理原点的情况
        if isinstance(r, np.ndarray):
            result[r == 0] = 1
        elif r == 0:
            result = 1
        return result
    
    # 绘制初始状态
    x = np.linspace(-5, 5, 1000)
    x = x[x != 0]  # 移除0以避免除以零的错误
    line1, = ax1.plot(x, f1(x), 'b-', lw=2)
    point1, = ax1.plot([], [], 'ro', ms=8)
    
    # 文本注释
    limit_text1 = ax1.text(0.05, 0.95, '', transform=ax1.transAxes, 
                          fontsize=10, verticalalignment='top')
    
    # 二元函数表面
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros_like(X)
    
    for i in range(len(x)):
        for j in range(len(y)):
            Z[i, j] = f2(X[i, j], Y[i, j])
    
    surface = ax2.plot_surface(X, Y, Z, cmap=cm.viridis, alpha=0.8, 
                              rstride=1, cstride=1, linewidth=0)
    
    # 添加一个点来演示函数值
    point2, = ax2.plot([], [], [], 'ro', ms=8)
    
    # 文本注释
    limit_text2 = ax2.text2D(0.05, 0.95, '', transform=ax2.transAxes, 
                            fontsize=10, verticalalignment='top')
    
    # 更新函数 - 用于动画
    def update(frame):
        t = frame / 100  # 动画参数
        
        # 更新一元函数部分
        delta = 5 - 4.9 * t  # 逐渐接近零点
        x_point = delta if frame % 2 == 0 else -delta
        
        if x_point != 0:
            y_point = f1(x_point)
            point1.set_data([x_point], [y_point])
            limit_text1.set_text(f'x = {x_point:.5f}\nf(x) = {y_point:.5f}\n\n当 x → 0 时\nlim f(x) = 1')
        else:
            point1.set_data([], [])
            limit_text1.set_text('x = 0 时函数无定义\n但极限存在: lim f(x) = 1')
        
        # 更新二元函数部分
        angle = frame * 2 * np.pi / 100  # 圆周运动
        r = delta  # 与一元函数使用相同的delta值
        x_point = r * np.cos(angle)
        y_point = r * np.sin(angle)
        
        if r != 0:
            z_point = f2(x_point, y_point)
            point2.set_data([x_point], [y_point])
            point2.set_3d_properties([z_point])
            limit_text2.set_text(f'x = {x_point:.5f}, y = {y_point:.5f}\nf(x,y) = {z_point:.5f}\n\n当 (x,y) → (0,0) 时\nlim f(x,y) = 1')
        else:
            point2.set_data([], [])
            point2.set_3d_properties([])
            limit_text2.set_text('(x,y) = (0,0) 时函数无定义\n但极限存在: lim f(x,y) = 1')
        
        # 调整视角使二元函数图表旋转
        ax2.view_init(elev=30, azim=frame)
        
        return line1, point1, limit_text1, surface, point2, limit_text2
    
    # 创建动画
    ani = FuncAnimation(fig, update, frames=np.arange(0, 100), 
                       interval=100, blit=False)
    
    # 调整布局
    plt.tight_layout()
    
    return fig, ani

def main():
    """主函数"""
    fig, ani = create_animation()
    
    # 显示图形和动画
    plt.show()
    
    # 保存动画（可选）
    # ani.save('function_limit_comparison.gif', writer='pillow', fps=10)
    
    print("动画展示完成！")

if __name__ == "__main__":
    main() 