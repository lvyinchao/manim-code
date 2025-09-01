from manim import *
import numpy as np

class SeriesConvergence(Scene):
    def construct(self):
        # 创建标题
        title = Text("级数收敛性演示", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 2.5, 0.5],
            axis_config={"color": GREY},
            x_length=10,
            y_length=6
        ).shift(DOWN * 0.5)
        
        axes_labels = axes.get_axis_labels(
            x_label="n",
            y_label="S_n"
        )

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # 创建几何级数 Sn = 1 + 1/2 + 1/4 + ... + 1/2^n
        def geometric_sum(n):
            return 2 * (1 - 1/2**(n+1))

        geometric_points = [axes.c2p(n, geometric_sum(n)) for n in range(10)]
        geometric_dots = VGroup(*[Dot(point, color=BLUE) for point in geometric_points])
        geometric_line = VMobject(color=BLUE)
        geometric_line.set_points_smoothly(geometric_points)

        geometric_label = MathTex(
            r"S_n = \sum_{k=0}^n \frac{1}{2^k}",
            color=BLUE
        ).scale(0.8).next_to(axes, UP, buff=0.2)

        # 创建调和级数 Sn = 1 + 1/2 + 1/3 + ... + 1/n
        def harmonic_sum(n):
            return sum(1/k for k in range(1, n+2))

        harmonic_points = [axes.c2p(n, harmonic_sum(n)) for n in range(10)]
        harmonic_dots = VGroup(*[Dot(point, color=RED) for point in harmonic_points])
        harmonic_line = VMobject(color=RED)
        harmonic_line.set_points_smoothly(harmonic_points)

        harmonic_label = MathTex(
            r"H_n = \sum_{k=1}^n \frac{1}{k}",
            color=RED
        ).scale(0.8).next_to(geometric_label, DOWN, buff=0.2)

        # 显示几何级数
        self.play(Write(geometric_label))
        for i in range(len(geometric_dots)):
            self.play(
                Create(geometric_dots[i]),
                Create(geometric_line) if i == len(geometric_dots)-1 else Wait(),
                run_time=0.3
            )
        self.wait(1)

        # 显示调和级数
        self.play(Write(harmonic_label))
        for i in range(len(harmonic_dots)):
            self.play(
                Create(harmonic_dots[i]),
                Create(harmonic_line) if i == len(harmonic_dots)-1 else Wait(),
                run_time=0.3
            )
        self.wait(1)

        # 添加极限线
        limit_line = DashedLine(
            axes.c2p(0, 2),
            axes.c2p(10, 2),
            color=BLUE_A
        )
        limit_label = MathTex(r"\lim_{n \to \infty} S_n = 2", color=BLUE_A).next_to(limit_line, RIGHT)

        self.play(
            Create(limit_line),
            Write(limit_label)
        )
        self.wait(1)

        # 添加发散箭头
        divergent_arrow = Arrow(
            axes.c2p(9, 2.3),
            axes.c2p(10, 2.5),
            color=RED_A,
            buff=0
        )
        divergent_label = MathTex(
            r"\lim_{n \to \infty} H_n = \infty",
            color=RED_A
        ).next_to(divergent_arrow, RIGHT)

        self.play(
            Create(divergent_arrow),
            Write(divergent_label)
        )
        self.wait(1)

        # 添加部分和公式
        geometric_sum_formula = MathTex(
            r"S_n = 2(1-\frac{1}{2^{n+1}})",
            color=BLUE
        ).scale(0.8).to_corner(DL)

        harmonic_sum_formula = MathTex(
            r"H_n \approx \ln(n) + \gamma",
            color=RED
        ).scale(0.8).next_to(geometric_sum_formula, DOWN, buff=0.2)

        self.play(
            Write(geometric_sum_formula),
            Write(harmonic_sum_formula)
        )

        # 添加解释文本
        explanation = Text(
            "几何级数收敛性分析：\n" + 
            "1. 首项为1，公比为1/2\n" +
            "2. |q| = 1/2 < 1，级数收敛\n" +
            "3. 收敛于S∞ = a/(1-q) = 2",
            font="SimSun",
            font_size=24,
            line_spacing=1.2
        ).to_corner(DR)

        self.play(Write(explanation))
        self.wait(2)

def main():
    import os
    os.system("manim -pqh series_convergence.py SeriesConvergence")

if __name__ == "__main__":
    main() 