# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class PartialDerivative(ThreeDScene):
    def construct(self):
        # 设置初始相机角度
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-1, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        # 添加坐标轴标签
        x_label = MathTex("x").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), UP)
        z_label = MathTex("z").next_to(axes.z_axis.get_end(), OUT)
        labels = VGroup(x_label, y_label, z_label)

        # 创建函数z = x^2 + y^2的曲面
        def func(x, y):
            return x**2 + y**2

        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.15  # 降低透明度使其若隐若现
        )

        # 显示坐标系和曲面
        self.play(Create(axes), Write(labels))
        self.play(Create(surface))
        self.wait(1)

        # 选择一个点(a,b)
        a, b = 1, 1
        point = Dot3D(axes.c2p(a, b, func(a, b)), color=YELLOW, radius=0.1)
        point_label = MathTex("(a,b)", color=YELLOW).scale(0.7)
        point_coords = VGroup(point, point_label)
        point_label.add_updater(lambda m: m.next_to(point, UP + RIGHT))
        
        # 在显示x方向截面前调整相机角度
        self.move_camera(phi=60 * DEGREES, theta=-30 * DEGREES, run_time=2)
        
        # 创建x方向的截面平面
        x_plane = Surface(
            lambda u, v: axes.c2p(u, b, v),
            u_range=[-2, 2],
            v_range=[-1, 3],
            resolution=(2, 2),
            fill_opacity=0.8,  # 降低不透明度
            color="#FF9999"  # 使用更鲜艳的粉色
        )
        
        # 创建x方向的截面曲线
        x_curve = ParametricFunction(
            lambda t: axes.c2p(t, b, func(t, b)),
            t_range=[-2, 2],
            color="#FF0000",  # 使用更鲜艳的红色
            stroke_width=4  # 增加线宽
        )
        
        # 修改x方向的切线
        def get_x_tangent_points(a, b, delta=1.5):  # 增加delta使切线更长
            center = axes.c2p(a, b, func(a, b))
            slope = 2 * a
            left = axes.c2p(a - delta, b, func(a, b) - slope * delta)
            right = axes.c2p(a + delta, b, func(a, b) + slope * delta)
            return left, center, right

        left_point, center_point, right_point = get_x_tangent_points(a, b)
        x_tangent = Line(
            left_point,
            right_point,
            color="#FF0000",  # 与曲线同色
            stroke_width=3
        )
        
        # 显示x方向的偏导数几何意义
        self.play(Create(point), Write(point_label))
        self.play(Create(x_plane))
        self.play(Create(x_curve))
        self.play(Create(x_tangent))  # 移除 x_tangent_extension
        
        # 删除原来的偏导数公式，只保留说明文字
        x_explanation = VGroup(
            Text("x方向偏导数：", font="SimSun", color=RED_B).scale(0.5),
            VGroup(
                Text("固定y=b时，曲线", font="SimSun", color=RED_A).scale(0.4),
                Text("在点(a,b)处的切线斜率", font="SimSun", color=RED_A).scale(0.4)
            ).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, aligned_edge=LEFT)
        x_explanation.to_corner(UL).shift(RIGHT * 0.5)  # 向右移动一些
        self.add_fixed_in_frame_mobjects(x_explanation)
        self.play(Write(x_explanation))
        self.wait(1)

        # 在显示y方向截面前调整相机角度
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=2)
        
        # 创建y方向的截面平面
        y_plane = Surface(
            lambda u, v: axes.c2p(a, u, v),
            u_range=[-2, 2],
            v_range=[-1, 3],
            resolution=(2, 2),
            fill_opacity=0.8,  # 降低不透明度
            color="#99FF99"  # 使用更鲜艳的绿色
        )

        # 创建y方向的截面曲线
        y_curve = ParametricFunction(
            lambda t: axes.c2p(a, t, func(a, t)),
            t_range=[-2, 2],
            color="#00FF00",  # 使用更鲜艳的绿色
            stroke_width=4  # 增加线宽
        )

        # 修改y方向的切线
        def get_y_tangent_points(a, b, delta=1.5):  # 增加delta使切线更长
            center = axes.c2p(a, b, func(a, b))
            slope = 2 * b
            left = axes.c2p(a, b - delta, func(a, b) - slope * delta)
            right = axes.c2p(a, b + delta, func(a, b) + slope * delta)
            return left, center, right

        left_point, center_point, right_point = get_y_tangent_points(a, b)
        y_tangent = Line(
            left_point,
            right_point,
            color="#00FF00",  # 与曲线同色
            stroke_width=3
        )
        
        # 显示y方向的偏导数几何意义
        self.play(Create(y_plane))
        self.play(Create(y_curve))
        self.play(Create(y_tangent))  # 移除 y_tangent_extension
        
        # 删除原来的偏导数公式，只保留说明文字
        y_explanation = VGroup(
            Text("y方向偏导数：", font="SimSun", color=GREEN_B).scale(0.5),
            VGroup(
                Text("固定x=a时，曲线", font="SimSun", color=GREEN_A).scale(0.4),
                Text("在点(a,b)处的切线斜率", font="SimSun", color=GREEN_A).scale(0.4)
            ).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, aligned_edge=LEFT)
        y_explanation.next_to(x_explanation, DOWN, buff=0.8)  # 增加垂直间距
        self.add_fixed_in_frame_mobjects(y_explanation)
        self.play(Write(y_explanation))
        self.wait(1)

        # 最后旋转时调整相机运动
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        # 修改最终说明文字
        final_explanation = VGroup(
            Text("偏导数的几何意义：", font="SimSun").scale(0.5),
            Text("在曲面上固定一个变量，", font="SimSun").scale(0.4),
            Text("得到的一元函数图像上的切线斜率", font="SimSun").scale(0.4)
        ).arrange(DOWN, aligned_edge=LEFT)
        final_explanation.to_corner(DOWN)
        self.add_fixed_in_frame_mobjects(final_explanation)
        self.play(Write(final_explanation))
        
        self.wait(2) 