# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class FourierSeriesVisualization(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("傅立叶级数逼近").scale(0.8)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            axis_config={"include_tip": True},
            x_length=10,
            y_length=6
        ).scale(0.8)
        axes.shift(DOWN * 0.5 + LEFT * 3)  # 更多的左移
        
        # 添加坐标轴标签
        x_label = Text("x").scale(0.6)
        y_label = Text("y").scale(0.6)
        x_label.next_to(axes.x_axis, RIGHT)
        y_label.next_to(axes.y_axis, UP)
        
        axes_group = VGroup(axes, x_label, y_label)
        self.play(Create(axes_group))

        # 先显示原函数表达式
        function_text = VGroup(
            Text("原函数：", font="SimSun").scale(0.5),
            MathTex(
                r"f(x) = \begin{cases} 1, & 0 \leq x < \pi \\ -1, & -\pi \leq x < 0 \end{cases}"
            ).scale(0.5)
        ).arrange(RIGHT, buff=0.3)
        function_text.to_corner(UL, buff=0.8)
        self.play(Write(function_text))
        self.wait(1)

        # 定义方波函数
        def square_wave(x):
            return np.where(np.sin(x) >= 0, 1, -1)  # 恢复原来的方波函数定义

        # 定义傅立叶级数部分和函数
        def get_fourier_series(x, n):
            result = 0
            for k in range(1, n+1, 2):
                result += 4/(k*np.pi) * np.sin(k*x)
            return result

        # 显示原函数图像
        original = axes.plot(
            square_wave,
            color=BLUE,
            x_range=[-4, 4, 0.01]  # 移除discontinuities和dt参数
        )
        original_label = Text("原函数", font="SimSun", color=BLUE).scale(0.5)
        original_label.next_to(original.point_from_proportion(0.8), UP)
        
        self.play(
            Create(original),
            Write(original_label)
        )
        self.wait(1)

        # 显示傅立叶级数表达式
        final_series = VGroup(
            Text("傅立叶级数展开：", font="SimSun").scale(0.5),
            MathTex(
                r"f(x) = \frac{4}{\pi} \sum_{n=1,3,5,\cdots}^{\infty} \frac{\sin(nx)}{n}"
            ).scale(0.5)
        ).arrange(RIGHT, buff=0.3)
        final_series.to_corner(UR, buff=0.8)
        self.play(Write(final_series))
        self.wait(1)

        # 显示部分和表达式
        fourier_terms = VGroup(
            MathTex(r"S_1(x) = \frac{4}{\pi} \sin(x)", color=RED),
            MathTex(r"S_3(x) = \frac{4}{\pi} (\sin(x) + \frac{1}{3}\sin(3x))", color=GREEN),
            MathTex(r"S_5(x) = \frac{4}{\pi} (\sin(x) + \frac{1}{3}\sin(3x) + \frac{1}{5}\sin(5x))", color=YELLOW),
            MathTex(r"S_9(x) = \frac{4}{\pi} (\sin(x) + \frac{1}{3}\sin(3x) + \cdots + \frac{1}{9}\sin(9x))", color=PURPLE),
            MathTex(r"S_{15}(x) = \frac{4}{\pi} (\sin(x) + \frac{1}{3}\sin(3x) + \cdots + \frac{1}{15}\sin(15x))", color=WHITE),
            MathTex(r"S_{23}(x) = \frac{4}{\pi} (\sin(x) + \frac{1}{3}\sin(3x) + \cdots + \frac{1}{23}\sin(23x))", color=ORANGE)
        ).scale(0.4).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # 调整部分和位置到右上角，并向右移动更多以避免重叠
        fourier_terms.next_to(final_series, DOWN, buff=0.3)
        fourier_terms.shift(RIGHT * 1)  # 向右移动更多以避免重叠

        # 绘制不同阶数的傅立叶级数
        colors = [RED, GREEN, YELLOW, PURPLE, WHITE, ORANGE]
        approximations = []
        labels = []
        
        for i, n in enumerate([1, 3, 5, 9, 15, 23]):
            # 绘制第n项逼近
            approx = axes.plot(
                lambda x: get_fourier_series(x, n),
                color=colors[i],
                x_range=[-4, 4, 0.01]
            )
            approximations.append(approx)
            
            # 添加标签
            label = MathTex(f"n = {n}", color=colors[i]).scale(0.5)
            label.next_to(approx.point_from_proportion(0.6), UP + RIGHT)  # 向右偏移
            labels.append(label)
            
            if i == 0:
                self.play(
                    Create(approx),
                    Write(label),
                    Write(fourier_terms[0])  # 显示第一项
                )
            else:
                self.play(
                    ReplacementTransform(approximations[i-1], approx),
                    ReplacementTransform(labels[i-1], label),
                    Write(fourier_terms[i])  # 显示新的展开式
                )
            self.wait(0.5)

        # 添加说明文字
        explanation = Text(
            "随着项数增加，傅立叶级数逐渐逼近原函数",
            font="SimSun"
        ).scale(0.5)
        explanation.next_to(axes, DOWN, buff=0.5)
        
        self.play(Write(explanation))
        self.wait(2)

def main():
    scene = FourierSeriesVisualization()
    scene.render()

if __name__ == "__main__":
    main() 