from manim import *
import numpy as np

class ImplicitFunctionDemo(ThreeDScene):
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # 创建标题
        title = Text("隐函数存在定理", font="PingFang SC", font_size=32)
        title.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait()

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": GRAY}
        )
        self.add(axes)
        self.wait()

        # 定义隐函数 F(x,y,z) = x^2 + y^2 + z^2 - 4 = 0
        def F(x, y, z):
            return x**2 + y**2 + z**2 - 4

        # 创建球面
        sphere = Surface(
            lambda u, v: np.array([
                2 * np.cos(u) * np.cos(v),
                2 * np.cos(u) * np.sin(v),
                2 * np.sin(u)
            ]),
            u_range=[-PI/2, PI/2],
            v_range=[0, 2*PI],
            checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(30, 30)
        )
        self.play(Create(sphere))
        self.wait()

        # 显示隐函数方程
        equation = MathTex(
            r"F(x,y,z) = x^2 + y^2 + z^2 - 4 = 0",
            color=WHITE,
            font_size=24
        )
        equation.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(Write(equation))
        self.wait()

        # 在球面上选择一点 P(√2, √2, 0)
        point = Dot3D(point=np.array([np.sqrt(2), np.sqrt(2), 0]), color=RED)
        self.play(Create(point))
        self.wait()

        # 显示选中点的坐标
        point_coords = MathTex(
            r"P(\sqrt{2}, \sqrt{2}, 0)",
            color=RED,
            font_size=24
        )
        point_coords.next_to(equation, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(point_coords)
        self.play(Write(point_coords))
        self.wait()

        # 显示偏导数
        partial_derivatives = VGroup(
            MathTex(r"\frac{\partial F}{\partial x} = 2x", color=YELLOW, font_size=24),
            MathTex(r"\frac{\partial F}{\partial y} = 2y", color=YELLOW, font_size=24),
            MathTex(r"\frac{\partial F}{\partial z} = 2z", color=YELLOW, font_size=24)
        )
        partial_derivatives.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        partial_derivatives.next_to(point_coords, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(partial_derivatives)
        self.play(Write(partial_derivatives))
        self.wait()

        # 显示在点P处的偏导数值
        values_at_p_text = Text("在点P处：", font="PingFang SC", font_size=20, color=RED)
        values_at_p_eq = MathTex(
            r"\frac{\partial F}{\partial z} = 0",
            color=RED,
            font_size=24
        )
        values_at_p = VGroup(values_at_p_text, values_at_p_eq)
        values_at_p.arrange(RIGHT, buff=0.2)
        values_at_p.next_to(partial_derivatives, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(values_at_p)
        self.play(Write(values_at_p))
        self.wait()

        # 显示定理结论
        conclusion = Text(
            "由于∂F/∂z = 0，不能用z表示x,y\n需选择其他变量作为因变量",
            font="PingFang SC",
            color=YELLOW,
            font_size=20
        )
        conclusion.next_to(values_at_p, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait()

        # 在点P的邻域内显示切平面
        normal = np.array([np.sqrt(2), np.sqrt(2), 0])
        tangent_plane = Surface(
            lambda u, v: np.array([
                np.sqrt(2) + u,
                np.sqrt(2) + v,
                -(normal[0]*u + normal[1]*v)/normal[2] if abs(normal[2]) > 1e-6 else 0
            ]),
            u_range=[-0.5, 0.5],
            v_range=[-0.5, 0.5],
            color=GREEN_D,
            fill_opacity=0.5
        )
        self.play(Create(tangent_plane))
        self.wait()

        # 旋转视角以更好地观察
        self.move_camera(phi=45 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait()

        # 开始环绕旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait()

        # 总结
        summary = Text(
            "隐函数存在定理要求相应的偏导数不为零",
            font="PingFang SC",
            color=WHITE,
            font_size=24
        )
        summary.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(Write(summary))
        self.wait(2)

        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        ) 