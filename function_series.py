# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class FunctionSeriesConvergence(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("函数项级数的收敛性").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # 展示级数表达式
        series = MathTex(
            r"\sum_{n=1}^{\infty} \frac{1}{n^2x^2+1}"
        ).scale(0.8)
        series.next_to(title, DOWN, buff=0.5)
        self.play(Write(series))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 2, 0.5],
            axis_config={"include_tip": True},
            x_length=10,
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

        # 定义每一项函数
        def get_term(x, n):
            return 1/(n**2 * x**2 + 1)

        # 定义部分和函数
        def get_partial_sum(x, N):
            return sum(get_term(x, n) for n in range(1, N+1))

        # 绘制前几项
        colors = [RED, GREEN, BLUE, YELLOW, PURPLE]
        terms = []
        term_labels = []
        
        # 先显示前3项
        for i in range(3):
            n = i + 1
            # 绘制单项函数
            term_curve = axes.plot(
                lambda x: get_term(x, n),
                color=colors[i],
                x_range=[-4, 4, 0.01]
            )
            terms.append(term_curve)
            
            # 添加标签
            label = MathTex(
                f"f_{n}(x) = \\frac{{1}}{{" + str(n) + "^2x^2+1}}",
                color=colors[i]
            ).scale(0.5)
            label.next_to(term_curve.point_from_proportion(0.8), UP)
            term_labels.append(label)
            
            self.play(
                Create(term_curve),
                Write(label)
            )
            self.wait(0.5)

        # 显示部分和
        partial_sums = []
        sum_labels = []
        
        for i, N in enumerate([1, 2, 3, 5, 10]):
            # 绘制部分和
            sum_curve = axes.plot(
                lambda x: get_partial_sum(x, N),
                color=WHITE,
                x_range=[-4, 4, 0.01]
            )
            partial_sums.append(sum_curve)
            
            # 添加标签
            sum_label = MathTex(
                f"S_{N}(x) = \sum_{{n=1}}^{N} \\frac{{1}}{{n^2x^2+1}}",
                color=WHITE
            ).scale(0.5)
            sum_label.to_corner(UR, buff=0.5)
            sum_labels.append(sum_label)
            
            if i == 0:
                self.play(
                    Create(sum_curve),
                    Write(sum_label)
                )
            else:
                self.play(
                    ReplacementTransform(partial_sums[i-1], sum_curve),
                    ReplacementTransform(sum_labels[i-1], sum_label)
                )
            self.wait(0.5)

        # 添加收敛性说明
        convergence_text = VGroup(
            Text("级数一致收敛于", font="SimSun").scale(0.6),
            MathTex(r"f(x) = \sum_{n=1}^{\infty} \frac{1}{n^2x^2+1}").scale(0.6)
        ).arrange(RIGHT, buff=0.3)
        convergence_text.next_to(axes, DOWN, buff=0.5)
        
        self.play(Write(convergence_text))
        self.wait(2)

def main():
    scene = FunctionSeriesConvergence()
    scene.render()

if __name__ == "__main__":
    main() 