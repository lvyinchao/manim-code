from manim import *

class DoubleIntegralVisualization(ThreeDScene):
    def construct(self):
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 9, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )

        # 定义函数 z = f(x, y) = 9 - x^2 - y^2
        def func(x, y):
            return 9 - x**2 - y**2

        # 创建曲面
        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            fill_color=BLUE,
            fill_opacity=0.6
        )

        # 显示坐标系和曲面
        self.play(Create(axes), Create(surface))
        self.wait(1)

        # 创建积分区域
        region = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            u_range=[-2, 2],
            v_range=[-2, 2],
            fill_color=GREEN,
            fill_opacity=0.3
        )
        self.play(Create(region))
        self.wait(1)

        # 显示积分符号和公式
        integral_text = MathTex(
            r"\iint_R (9 - x^2 - y^2) \, dx \, dy",
            color=YELLOW
        ).scale(0.8)
        integral_text.to_corner(UL)
        self.play(Write(integral_text))
        self.wait(1)

        # 添加文字说明
        explanation_text = VGroup(
            Text("计算区域R下的体积", font="SimSun", color=YELLOW).scale(0.5),
            Text("通过二重积分求解", font="SimSun", color=YELLOW).scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT)
        explanation_text.to_corner(DR)
        self.add_fixed_in_frame_mobjects(explanation_text)
        self.play(Write(explanation_text))

        # 调整相机运动
        self.move_camera(phi=70 * DEGREES, theta=-30 * DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(6)
        self.stop_ambient_camera_rotation()

        # 最后移动到另一个角度以更好地观察
        self.move_camera(phi=45 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait(2) 