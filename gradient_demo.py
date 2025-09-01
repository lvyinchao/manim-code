from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class GradientDemo(Scene):
    def construct(self):
        # 标题
        title = Text("梯度演示", font="STSong", font_size=36)
        subtitle = Text("∇f = (∂f/∂x, ∂f/∂y)", font_size=24)
        VGroup(title, subtitle).arrange(DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            axis_config={"color": GREY},
            x_length=8,
            y_length=8
        ).add_coordinates()
        
        # 定义标量场函数 f(x,y) = x² + y²
        def scalar_field(x, y):
            return x**2 + y**2

        # 创建等高线
        def get_level_curves():
            curves = VGroup()
            levels = [0.5, 1, 2, 4, 8, 16]
            for level in levels:
                curve = ParametricFunction(
                    lambda t: axes.c2p(
                        np.sqrt(level) * np.cos(t),
                        np.sqrt(level) * np.sin(t),
                        0
                    ),
                    t_range=[0, TAU],
                    color=BLUE_C
                )
                curves.add(curve)
            return curves

        level_curves = get_level_curves()

        # 创建梯度场
        def gradient_field(point):
            x, y = axes.p2c(point)
            grad = np.array([2*x, 2*y, 0])  # ∇f = (2x, 2y)
            magnitude = np.linalg.norm(grad)
            if magnitude > 0:
                grad = grad / magnitude * 0.5  # 归一化并缩放
            return Vector(grad, color=YELLOW).shift(point)

        # 在网格点上创建梯度向量
        vectors = VGroup(*[
            gradient_field(axes.c2p(x, y))
            for x in np.arange(-3, 3.1, 0.7)
            for y in np.arange(-3, 3.1, 0.7)
        ])

        # 展示坐标系
        self.play(Create(axes))
        self.wait(1)

        # 展示标量场函数
        func_tex = MathTex(r"f(x,y) = x^2 + y^2").to_corner(UL)
        self.play(Write(func_tex))
        self.wait(1)

        # 展示等高线
        level_curves_label = Text("等高线", font="STSong").next_to(func_tex, DOWN)
        self.play(
            Create(level_curves),
            Write(level_curves_label)
        )
        self.wait(1)

        # 展示梯度场
        gradient_label = Text("梯度场", font="STSong").next_to(level_curves_label, DOWN)
        self.play(
            LaggedStart(*[GrowArrow(vec) for vec in vectors]),
            Write(gradient_label),
            run_time=3
        )
        self.wait(1)

        # 演示梯度与等高线的正交关系
        def create_point_and_gradient(pos):
            point = Dot(pos, color=RED)
            x, y = axes.p2c(pos)
            grad = np.array([2*x, 2*y, 0])
            grad = grad / np.linalg.norm(grad)
            vector = Vector(grad, color=GREEN).shift(pos)
            return VGroup(point, vector)

        # 选择几个示例点
        demo_points = [
            axes.c2p(1, 1),
            axes.c2p(-2, 0),
            axes.c2p(0, -1.5),
            axes.c2p(2, -1)
        ]

        # 添加说明文本
        orthogonal_text = Text(
            "梯度垂直于等高线",
            font="STSong",
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(orthogonal_text))

        # 演示每个点的梯度
        for pos in demo_points:
            point_grad = create_point_and_gradient(pos)
            self.play(
                Create(point_grad),
                run_time=1
            )
            self.wait(0.5)
            self.play(
                FadeOut(point_grad),
                run_time=0.5
            )

        # 展示梯度公式
        gradient_formula = MathTex(
            r"\nabla f = \begin{pmatrix} \frac{\partial f}{\partial x} \\ \frac{\partial f}{\partial y} \end{pmatrix} = \begin{pmatrix} 2x \\ 2y \end{pmatrix}"
        ).to_edge(RIGHT)
        
        self.play(Write(gradient_formula))
        self.wait(2)

        # 添加性质说明
        properties = VGroup(
            Text("梯度的性质:", font="STSong"),
            Text("1. 指向函数值增长最快的方向", font="STSong"),
            Text("2. 大小等于方向导数的最大值", font="STSong"),
            Text("3. 垂直于等值线", font="STSong")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN)
        
        self.play(Write(properties))
        self.wait(3)

def main():
    import os
    os.system("manim -pqh gradient_demo.py GradientDemo")

if __name__ == "__main__":
    main() 