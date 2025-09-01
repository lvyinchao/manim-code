from manim import *
import numpy as np

class GradientField(Scene):
    def construct(self):
        # 添加标题
        title = Text("梯度场", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 创建坐标系
        axes = Axes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            axis_config={"color": GREY},
        ).add_coordinates()

        # 定义标量场函数 f(x,y) = x² + y²
        def scalar_field(point):
            x, y = point[:2]
            return x**2 + y**2

        # 创建等高线
        contours = []
        for level in [0.5, 1.0, 1.5, 2.0]:
            contour = ParametricFunction(
                lambda t: axes.c2p(
                    np.sqrt(level)*np.cos(t),
                    np.sqrt(level)*np.sin(t)
                ),
                t_range=[0, TAU],
                color=BLUE_C
            )
            contours.append(contour)

        # 定义梯度场函数
        def gradient_field(point):
            x, y = axes.p2c(point)
            return axes.c2p(2*x, 2*y, 0) - point

        # 创建梯度向量场
        vector_field = ArrowVectorField(
            gradient_field,
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            vector_config={"color": YELLOW},
            length_func=lambda x: 0.3
        )

        # 显示坐标系和等高线
        self.play(Create(axes))
        self.play(LaggedStart(*[Create(c) for c in contours]))
        
        # 显示向量场
        self.play(Create(vector_field))

        # 添加说明文字
        formula = MathTex(
            r"\nabla f = (\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y})",
            font_size=32
        ).next_to(title, DOWN)
        
        self.play(Write(formula))
        self.wait(2)

class DivergenceField(Scene):
    def construct(self):
        # 添加标题
        title = Text("散度场", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 创建坐标系
        axes = Axes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            axis_config={"color": GREY},
        ).add_coordinates()

        # 定义向量场（发散源）
        def vector_field_func(point):
            x, y = axes.p2c(point)
            return axes.c2p(x, y, 0) - point

        # 创建向量场
        vector_field = ArrowVectorField(
            vector_field_func,
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            vector_config={"color": RED},
            length_func=lambda x: 0.3
        )

        # 显示坐标系和向量场
        self.play(Create(axes))
        self.play(Create(vector_field))

        # 添加说明文字
        formula = MathTex(
            r"\nabla \cdot \mathbf{F} = \frac{\partial P}{\partial x} + \frac{\partial Q}{\partial y}",
            font_size=32
        ).next_to(title, DOWN)
        
        self.play(Write(formula))
        self.wait(2)

class CurlField(Scene):
    def construct(self):
        # 添加标题
        title = Text("旋度场", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))

        # 创建坐标系
        axes = Axes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            axis_config={"color": GREY},
        ).add_coordinates()

        # 定义向量场（旋转场）
        def vector_field_func(point):
            x, y = axes.p2c(point)
            return axes.c2p(-y, x, 0) - point

        # 创建向量场
        vector_field = ArrowVectorField(
            vector_field_func,
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            vector_config={"color": GREEN},
            length_func=lambda x: 0.3
        )

        # 显示坐标系和向量场
        self.play(Create(axes))
        self.play(Create(vector_field))

        # 添加说明文字
        formula = MathTex(
            r"\nabla \times \mathbf{F} = \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}",
            font_size=32
        ).next_to(title, DOWN)
        
        self.play(Write(formula))
        self.wait(2) 