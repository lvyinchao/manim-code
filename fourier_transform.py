# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class FourierTransformVisualization(ThreeDScene):
    def construct(self):
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[0, 3, 1],  # 仅绘制第一象限
            y_range=[0, 3, 1],
            z_range=[0, 9, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )

        # 定义复合函数 z = f(x, y) = (x^2 + y^2)^0.5
        def func(x, y):
            return (x**2 + y**2)**0.5

        # 创建曲面
        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[0, 2],  # 仅绘制第一象限
            v_range=[0, 2],
            resolution=(30, 30),
            fill_color=BLUE,
            fill_opacity=0.6
        )

        # 设置初始相机角度
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # 显示坐标系和曲面
        self.play(Create(axes), Create(surface))
        self.wait(1)

        # 选择一个点 (x0, y0) 并显示
        x0, y0 = 1, 1
        point = Dot3D(axes.c2p(x0, y0, func(x0, y0)), color=YELLOW, radius=0.1)
        self.play(Create(point))

        # 显示链式法则的切线
        dx = 0.1
        dy = 0.1
        partial_x = Line(
            axes.c2p(x0, y0, func(x0, y0)),
            axes.c2p(x0 + dx, y0, func(x0, y0) + (x0 / func(x0, y0)) * dx),
            color=RED
        )
        partial_y = Line(
            axes.c2p(x0, y0, func(x0, y0)),
            axes.c2p(x0, y0 + dy, func(x0, y0) + (y0 / func(x0, y0)) * dy),
            color=GREEN
        )

        self.play(Create(partial_x), Create(partial_y))
        self.wait(2)

        # 添加文字说明
        explanation_text = VGroup(
            Text("链式法则 ∂f/∂x 在 (x0, y0)", font="SimSun", color=RED).scale(0.4),
            Text("链式法则 ∂f/∂y 在 (x0, y0)", font="SimSun", color=GREEN).scale(0.4)
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

def main():
    scene = FourierTransformVisualization()
    scene.render()

if __name__ == "__main__":
    main() 