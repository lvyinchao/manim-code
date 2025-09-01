from manim import *
import numpy as np
from scipy.stats import norm, uniform, expon

class ProbabilityDistributions(Scene):
    def construct(self):
        # 创建标题
        title = Text("常见概率分布的可视化", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            axis_config={"color": GREY},
            x_length=10,
            y_length=6
        ).shift(DOWN * 0.5)
        
        axes_labels = axes.get_axis_labels(
            x_label="x",
            y_label="f(x)"
        )

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # 创建正态分布
        def normal_dist(x):
            return norm.pdf(x, loc=0, scale=1)
        
        normal_graph = axes.plot(
            normal_dist,
            color=BLUE,
            x_range=[-4, 4, 0.01]
        )
        normal_label = MathTex(
            r"N(0,1): f(x)=\frac{1}{\sqrt{2\pi}}e^{-\frac{x^2}{2}}",
            color=BLUE
        ).scale(0.8).next_to(axes, UP, buff=0.2)

        # 创建均匀分布
        def uniform_dist(x):
            return uniform.pdf(x, loc=-2, scale=4)
        
        uniform_graph = axes.plot(
            uniform_dist,
            color=RED,
            x_range=[-2, 2, 0.01]
        )
        uniform_label = MathTex(
            r"U(-2,2): f(x)=\begin{cases}\frac{1}{4} & -2\leq x\leq 2 \\ 0 & \text{otherwise}\end{cases}",
            color=RED
        ).scale(0.8).next_to(normal_label, DOWN, buff=0.2)

        # 创建指数分布
        def exp_dist(x):
            return expon.pdf(x, scale=1)
        
        exp_graph = axes.plot(
            exp_dist,
            color=GREEN,
            x_range=[0, 4, 0.01]
        )
        exp_label = MathTex(
            r"\text{Exp}(1): f(x)=e^{-x}, x\geq 0",
            color=GREEN
        ).scale(0.8).next_to(uniform_label, DOWN, buff=0.2)

        # 显示分布曲线和标签
        self.play(Create(normal_graph), Write(normal_label))
        self.wait(1)
        self.play(Create(uniform_graph), Write(uniform_label))
        self.wait(1)
        self.play(Create(exp_graph), Write(exp_label))
        self.wait(1)

        # 创建面积填充动画
        def get_area(graph, x_min, x_max, axes, color):
            return axes.get_area(
                graph,
                x_range=[x_min, x_max],
                color=color,
                opacity=0.3
            )

        # 演示正态分布的标准差范围
        sigma1_area = get_area(normal_graph, -1, 1, axes, BLUE)
        sigma2_area = get_area(normal_graph, -2, 2, axes, BLUE)
        sigma3_area = get_area(normal_graph, -3, 3, axes, BLUE)

        # 添加标准差说明
        sigma1_text = Text("68.27%", font_size=24, color=BLUE).next_to(sigma1_area, UP)
        sigma2_text = Text("95.45%", font_size=24, color=BLUE).next_to(sigma2_area, UP, buff=0.5)
        sigma3_text = Text("99.73%", font_size=24, color=BLUE).next_to(sigma3_area, UP, buff=1)

        # 显示标准差范围
        self.play(FadeIn(sigma1_area), Write(sigma1_text))
        self.wait(1)
        self.play(FadeIn(sigma2_area), Write(sigma2_text))
        self.wait(1)
        self.play(FadeIn(sigma3_area), Write(sigma3_text))
        self.wait(1)

        # 创建均值和中位数的标注
        normal_mean = axes.get_vertical_line(axes.c2p(0, 0), color=YELLOW)
        normal_mean_label = Text("μ = 0", font_size=24, color=YELLOW).next_to(normal_mean, DOWN)

        # 显示均值线
        self.play(
            Create(normal_mean),
            Write(normal_mean_label)
        )
        self.wait(1)

        # 添加解释文本
        explanation = Text(
            "正态分布的特点：\n" + 
            "1. 关于均值对称\n" +
            "2. 68-95-99.7法则\n" +
            "3. 均值=中位数=众数",
            font="SimSun",
            font_size=24,
            line_spacing=1.2
        ).to_corner(DL)

        self.play(Write(explanation))
        self.wait(2)

def main():
    import os
    os.system("manim -pqh probability_distributions.py ProbabilityDistributions")

if __name__ == "__main__":
    main() 