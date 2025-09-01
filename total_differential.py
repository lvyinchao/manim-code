# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class TotalDifferential(ThreeDScene):
    def construct(self):
        # 创建3D坐标系并向右下方移动，增加刻度间距
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],  # 增加刻度间距
            y_range=[-2, 2, 0.5],
            z_range=[-1, 3, 0.5],
            x_length=12,  # 增加坐标轴长度以放大图像
            y_length=12,
            z_length=8
        ).shift(2 * DOWN + RIGHT)  # 向右下方移动更多
        
        # 设置初始相机角度
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)

        # 添加坐标轴标签
        x_label = MathTex("x").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), UP)
        z_label = MathTex("z").next_to(axes.z_axis.get_end(), OUT)
        labels = VGroup(x_label, y_label, z_label)

        # 创建函数z = x^2 + y^2的曲面，缩小范围
        def func(x, y):
            return x**2 + y**2

        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-1.5, 1.5],  # 缩小范围
            v_range=[-1.5, 1.5],
            resolution=(50, 50),  # 增加网格线密度
            fill_color=PURPLE,  # 更改曲面颜色为紫色
            fill_opacity=0.6  # 设置不透明度为0.6
        )

        # 显示坐标系和曲面
        self.play(Create(axes), Write(labels))
        self.play(Create(surface))
        self.wait(1)

        # 选择一个点(x,y)并显示
        x0, y0 = 0.5, 0.5
        point = Dot3D(axes.c2p(x0, y0, func(x0, y0)), color=YELLOW, radius=0.1)
        self.play(Create(point))

        # 创建垂直于z轴的水平平面并显示
        horizontal_plane = Surface(
            lambda u, v: axes.c2p(u, v, func(x0, y0)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(20, 20),  # 增加网格线密度
            fill_opacity=0.3,  # 设置不透明度为0.3
            color=BLUE
        )
        self.play(Create(horizontal_plane))

        # 在水平面上选取新点并创建垂线
        dx, dy = 0.3, 0.3
        new_point = axes.c2p(x0 + dx, y0 + dy, func(x0, y0))
        new_dot = Dot3D(new_point, color=WHITE, radius=0.05)
        self.play(Create(new_dot))

        # 垂线与实际增量相交
        actual_intersection = axes.c2p(x0 + dx, y0 + dy, func(x0 + dx, y0 + dy))
        actual_line = DashedLine(new_point, actual_intersection, color=YELLOW_D)
        self.play(Create(actual_line))

        # 创建切平面
        def get_tangent_plane(x0, y0, delta=1):
            # 计算偏导数
            fx = 2 * x0
            fy = 2 * y0
            f_val = func(x0, y0)
            
            # 切平面方程：z = f(x0,y0) + fx(x-x0) + fy(y-y0)
            def plane_func(x, y):
                return f_val + fx*(x-x0) + fy*(y-y0)
            
            plane = Surface(
                lambda u, v: axes.c2p(u, v, plane_func(u, v)),
                u_range=[x0-delta, x0+delta],
                v_range=[y0-delta, y0+delta],
                resolution=(40, 40),  # 增加网格线密度
                fill_opacity=0.6,
                color=ORANGE  # 更改切平面颜色为橙色
            )
            return plane

        # 创建并显示切平面
        tangent_plane = get_tangent_plane(x0, y0)
        self.play(Create(tangent_plane))

        # 垂线与线性近似相交
        approx_intersection = axes.c2p(x0 + dx, y0 + dy, func(x0, y0) + 2*x0*dx + 2*y0*dy)
        approx_line = DashedLine(new_point, approx_intersection, color=GREEN_D)
        self.play(Create(approx_line))

        # 显示误差线
        error_line = Line(actual_intersection, approx_intersection, color=RED_B, stroke_width=2)
        self.play(Create(error_line))

        # 添加文字说明
        explanation_text = VGroup(
            Text("点(x0+Δx, y0+Δy)到曲面距离为Δz", font="SimSun", color=YELLOW_D).scale(0.4),
            Text("点(x0+Δx, y0+Δy)到切平面距离为dz", font="SimSun", color=GREEN_D).scale(0.4),
           # Text("切平面到曲面的距离为误差", font="SimSun", color=RED_B).scale(0.4)
        ).arrange(DOWN, aligned_edge=LEFT)
        explanation_text.to_corner(DR)  # 移动到右下角
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