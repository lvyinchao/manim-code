from manim import *
import numpy as np

class TripleIntegralConversion(ThreeDScene):
    def construct(self):
        # 添加标题
        title = Text("直角坐标计算三重积分", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)

        # 设置相机角度
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=30 * DEGREES
        )

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[0, 4],
            y_range=[0, 4],
            z_range=[0, 4],
            x_length=5,
            y_length=5,
            z_length=5,
            axis_config={"include_numbers": False}
        ).shift(LEFT * 2)

        # 添加坐标轴标签
        labels = VGroup(
            MathTex("x").next_to(axes.x_axis.get_end(), RIGHT),
            MathTex("y").next_to(axes.y_axis.get_end(), UP),
            MathTex("z").next_to(axes.z_axis.get_end(), OUT)
        )
        self.add_fixed_in_frame_mobjects(labels)

        # 显示坐标系
        self.play(Create(axes), Write(labels))
        self.wait(1)

        # 创建积分区域（一个立方体）
        cube = Cube(
            side_length=2,
            fill_opacity=0.2,
            stroke_width=2,
            fill_color=BLUE
        ).move_to(axes.c2p(2, 2, 1))

        # 显示积分区域
        self.play(Create(cube))
        self.wait(1)

        # 创建积分转换公式
        formulas = VGroup(
            # 三重积分
            MathTex(r"\iiint_V f(x,y,z)dxdydz"),
            # 第一次转换（z）
            MathTex(r"= \iint_D \left(\int_{z_1(x,y)}^{z_2(x,y)} f(x,y,z)dz\right)dxdy"),
            # 第二次转换（y）
            MathTex(r"= \int_a^b \left(\int_{\varphi_1(x)}^{\varphi_2(x)} \left(\int_{z_1(x,y)}^{z_2(x,y)} f(x,y,z)dz\right)dy\right)dx")
        ).scale(0.8).arrange(DOWN, buff=0.3).to_corner(DL)

        # 添加积分区域的边界标注
        boundary_labels = VGroup(
            MathTex("z=z_1(x,y)").next_to(cube, DOWN),
            MathTex("z=z_2(x,y)").next_to(cube, UP),
            MathTex("y=\\varphi_1(x)").next_to(cube, LEFT),
            MathTex("y=\\varphi_2(x)").next_to(cube, RIGHT),
            MathTex("x=a").next_to(cube, IN),
            MathTex("x=b").next_to(cube, OUT)
        ).scale(0.8)

        # 固定公式在屏幕上
        self.add_fixed_in_frame_mobjects(formulas)

        # 显示转换过程
        for i in range(len(formulas)):
            self.play(Write(formulas[i]))
            self.wait(1)

        # 显示边界标注
        self.play(Write(boundary_labels))
        self.wait(1)

        # 旋转查看
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.wait(2) 