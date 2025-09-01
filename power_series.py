# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class PowerSeriesConvergence(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("幂级数的收敛性").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # 展示幂级数
        series = MathTex(
            r"\sum_{n=0}^{\infty} x^n = 1 + x + x^2 + x^3 + \cdots"
        ).scale(0.8)
        series.next_to(title, DOWN, buff=0.5)
        self.play(Write(series))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 4, 1],
            axis_config={"include_tip": True},
            x_length=8,
            y_length=6
        ).scale(0.8)
        axes.shift(DOWN * 0.5)
        
        # 添加坐标轴标签
        x_label = Text("x").scale(0.6)
        y_label = Text("y").scale(0.6)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label.next_to(axes.y_axis, UP)
        
        axes_group = VGroup(axes, x_label, y_label)
        self.play(Create(axes_group))

        # 定义部分和函数
        def get_partial_sum(x, n):
            if abs(x) >= 1:  # 收敛半径外返回None
                return None
            return sum(x**k for k in range(n+1))

        # 绘制不同阶数的部分和
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
        curves = []
        labels = []
        
        for i, n in enumerate([1, 2, 3, 5, 10]):
            # 创建部分和函数
            def partial_sum(x, current_n=n):
                return get_partial_sum(x, current_n)
            
            # 绘制曲线
            curve = axes.plot(
                partial_sum,
                color=colors[i],
                x_range=[-0.99, 0.99, 0.01]  # 避免在x=±1处的奇异点
            )
            curves.append(curve)
            
            # 添加标签
            label = MathTex(
                f"S_{n}(x) = \sum_{{k=0}}^{n} x^k",
                color=colors[i]
            ).scale(0.5)
            label.next_to(curve.point_from_proportion(0.7), UP)
            labels.append(label)
            
            # 显示动画
            self.play(
                Create(curve),
                Write(label)
            )
            self.wait(0.5)

        # 绘制极限函数 1/(1-x)
        def limit_function(x):
            return 1/(1-x) if abs(x) < 1 else None

        limit_curve = axes.plot(
            limit_function,
            color=WHITE,
            x_range=[-0.99, 0.99, 0.01]
        )
        limit_label = MathTex(
            r"f(x) = \frac{1}{1-x}", r"\quad |x| < 1",
            color=WHITE
        ).scale(0.6)
        limit_label.next_to(limit_curve.point_from_proportion(0.8), UP)

        self.play(
            Create(limit_curve),
            Write(limit_label)
        )
        self.wait(1)

        # 添加收敛半径说明
        radius_text = VGroup(
            Text("收敛半径", font="SimSun").scale(0.6),
            MathTex(r"R = 1").scale(0.6)
        ).arrange(RIGHT, buff=0.3)
        radius_text.next_to(axes, DOWN, buff=0.5)
        
        # 画出收敛区间
        convergence_interval = Line(
            axes.c2p(-1, 0),
            axes.c2p(1, 0),
            color=YELLOW
        )
        
        self.play(
            Write(radius_text),
            Create(convergence_interval)
        )
        self.wait(2)

def main():
    scene = PowerSeriesConvergence()
    scene.render()

if __name__ == "__main__":
    main() 