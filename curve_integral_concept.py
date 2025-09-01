from manim import *
import numpy as np

class CurveIntegralTypeTwo(Scene):
    def construct(self):
        # 添加标题
        title = Text("第二型曲线积分", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[0, 4],
            y_range=[0, 4],
            axis_config={"color": GREY},
            x_length=6,
            y_length=6,
        ).add_coordinates()

        # 添加坐标轴标签
        x_label = axes.get_x_axis_label("x", direction=DOWN)
        y_label = axes.get_y_axis_label("y")
        
        # 显示坐标系和标签
        self.play(Create(axes), Write(VGroup(x_label, y_label)))
        
        # 定义参数曲线
        curve = ParametricFunction(
            lambda t: axes.c2p(t, 1 + np.sin(t), 0),
            t_range=[0, 3],
            color=BLUE
        )
        
        # 显示曲线
        self.play(Create(curve))
        self.wait(1)

        # 创建向量场
        def vector_field(point):
            x, y = axes.p2c(point)
            return axes.c2p(x/2, y/2, 0) - point

        vector_field = ArrowVectorField(
            vector_field,
            x_range=[0, 4, 0.5],
            y_range=[0, 4, 0.5],
            vector_config={"color": YELLOW, "max_tip_length_to_length_ratio": 0.3},
            length_func=lambda x: 0.5
        )
        
        # 显示向量场
        self.play(Create(vector_field))
        self.wait(1)

        # 在曲线上选取点
        n_points = 8
        t_values = np.linspace(0, 3, n_points)
        dots = VGroup()
        vectors = VGroup()
        
        # 创建并显示点和对应的向量
        for t in t_values:
            point = curve.point_from_proportion(t/3)
            dot = Dot(point, color=RED)
            vector = vector_field.get_vector(point)
            vector.set_color(RED)
            dots.add(dot)
            vectors.add(vector)
        
        self.play(Create(dots))
        self.play(Create(vectors))
        self.wait(1)

        # 添加积分符号和被积函数
        integral = MathTex(
            r"\int_C P(x,y)dx + Q(x,y)dy",
            font_size=32
        ).to_corner(UR)
        
        self.play(Write(integral))
        self.wait(2)

        # 添加说明文字
        explanation = Text(
            "沿曲线C对向量场进行积分",
            font="SimSun",
            font_size=24
        ).next_to(integral, DOWN)
        
        self.play(Write(explanation))
        self.wait(2)

        