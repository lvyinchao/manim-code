from manim import *
import numpy as np

class VectorCalculusScene(ThreeDScene):
    def construct(self):
        # 场景标题
        title = Text("向量微积分可视化", font="SimSun").scale(1.2)
        self.play(Write(title))
        self.wait()
        self.play(title.animate.to_edge(UP))
        
        # 1. 梯度部分
        def scalar_field(x, y):
            return np.sin(x) * np.cos(y)
        
        # 创建3D表面
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[-2, 2],
        )
        
        surface = Surface(
            lambda u, v: np.array([u, v, scalar_field(u, v)]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
        )
        surface.set_style(fill_opacity=0.7)
        surface.set_fill_by_value(axes=axes, colors=[(BLUE, -2), (GREEN, 0), (RED, 2)])
        
        # 梯度向量
        def gradient(x, y):
            return np.array([
                np.cos(x) * np.cos(y),
                -np.sin(x) * np.sin(y),
                0
            ])
        
        gradient_vectors = VGroup()
        for x in np.linspace(-2, 2, 5):
            for y in np.linspace(-2, 2, 5):
                vector = Arrow3D(
                    start=np.array([x, y, scalar_field(x, y)]),
                    end=np.array([x, y, scalar_field(x, y)]) + gradient(x, y),
                    color=YELLOW
                )
                gradient_vectors.add(vector)
        
        # 动画展示
        grad_title = Text("梯度 (Gradient)", font="SimSun").next_to(title, DOWN)
        grad_formula = MathTex(r"\nabla f = \left(\frac{\partial f}{\partial x}, \frac{\partial f}{\partial y}\right)")
        grad_formula.next_to(grad_title, DOWN)
        
        self.play(
            Write(grad_title),
            Write(grad_formula)
        )
        self.wait()
        
        # 设置3D视角
        self.set_camera_orientation(phi=60 * DEGREES, theta=30 * DEGREES)
        self.play(
            Create(surface),
            Create(axes),
            run_time=2
        )
        self.play(Create(gradient_vectors))
        self.wait()
        
        # 2. 散度部分
        self.play(
            *[FadeOut(mob) for mob in [surface, gradient_vectors, grad_title, grad_formula]],
            run_time=1
        )
        
        # 重置相机角度为2D视图
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        
        div_title = Text("散度 (Divergence)", font="SimSun").next_to(title, DOWN)
        div_formula = MathTex(r"\nabla \cdot \mathbf{F} = \frac{\partial F_x}{\partial x} + \frac{\partial F_y}{\partial y}")
        div_formula.next_to(div_title, DOWN)
        
        # 创建2D矢量场 - 使用StreamLines
        plane = NumberPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
        )
        
        def vector_field_func(point):
            x, y = point[:2]
            return np.array([x, -y, 0])
        
        stream_lines = StreamLines(
            vector_field_func,
            stroke_width=2,
            color=BLUE,
            x_range=[-3, 3, 0.5],  # start, end, step_size
            y_range=[-3, 3, 0.5],
            padding=1
        )
        
        self.play(
            Write(div_title),
            Write(div_formula)
        )
        self.wait()
        
        self.play(
            Create(plane),
            Create(stream_lines)
        )
        self.wait(2)
        
        # 添加动画效果：显示源和汇
        source_point = Dot(point=RIGHT*2, color=RED)
        sink_point = Dot(point=LEFT*2, color=BLUE)
        source_label = Text("源", font="SimSun").next_to(source_point, UP)
        sink_label = Text("汇", font="SimSun").next_to(sink_point, UP)
        
        self.play(
            Create(source_point),
            Create(sink_point),
            Write(source_label),
            Write(sink_label)
        )
        self.wait(2)
        
        # 清理场景
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )

class Arrow3D(Line):
    def __init__(self, start, end, **kwargs):
        super().__init__(start=start, end=end, **kwargs)
        self.add_tip() 