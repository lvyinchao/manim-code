# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class ParametricCurve(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("一次函数轨迹合成").scale(0.8)
        title.to_edge(UP, buff=0.3)
        title.shift(RIGHT * 2)  # 右移避免重叠
        self.play(Write(title))
        self.wait(1)

        # 创建三个坐标系
        # x(t)的坐标系
        axes_xt = Axes(
            x_range=[0, 2, 0.5],  # t范围
            y_range=[-2, 8, 1],   # x范围
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_xt.shift(LEFT * 4 + UP * 1.5)  # 左上角

        # y(t)的坐标系
        axes_yt = Axes(
            x_range=[0, 2, 0.5],  # t范围
            y_range=[-2, 6, 1],   # y范围
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_yt.shift(LEFT * 4 + DOWN * 2)  # 左下角，下移更多（从1.5改为2）

        # x-y平面的坐标系
        axes_xy = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=6
        ).scale(0.7)
        axes_xy.shift(RIGHT * 2)

        # 添加坐标系标签
        xt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_xt.x_axis, RIGHT),
            Text("x").scale(0.4).next_to(axes_xt.y_axis, UP)
        )
        yt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_yt.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_yt.y_axis, UP)
        )
        xy_labels = VGroup(
            Text("x").scale(0.4).next_to(axes_xy.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_xy.y_axis, UP)
        )

        # 显示坐标系
        self.play(
            Create(axes_xt), Write(xt_labels),
            Create(axes_yt), Write(yt_labels),
            Create(axes_xy), Write(xy_labels)
        )

        # 定义参数方程
        def param_x(t): return 3*t + 4  # x = 3t + 4
        def param_y(t): return 2*t      # y = 2t

        # 显示参数方程
        equations = VGroup(
            MathTex(r"x = 3t + 4", color=BLUE),
            MathTex(r"y = 2t", color=RED),
            MathTex(r"\rightarrow y = \frac{2}{3}(x-4)", color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        equations.next_to(axes_xy, LEFT, buff=0.3)
        
        self.play(Write(equations[:2]))

        # 创建x(t)曲线
        x_curve = axes_xt.plot(
            param_x,
            x_range=[0, 1, 0.01],
            color=BLUE
        )

        # 创建y(t)曲线
        y_curve = axes_yt.plot(
            param_y,
            x_range=[0, 1, 0.01],
            color=RED
        )

        # 创建合成轨迹
        trajectory = ParametricFunction(
            lambda t: axes_xy.c2p(param_x(t), param_y(t)),
            t_range=[0, 1],
            color=GREEN
        )

        # 创建运动点
        dot_xt = Dot(color=YELLOW, radius=0.08)
        dot_yt = Dot(color=YELLOW, radius=0.08)
        dot_xy = Dot(color=YELLOW, radius=0.08)

        # 创建时间追踪器
        t_tracker = ValueTracker(0)

        # 添加点的更新函数
        dot_xt.add_updater(lambda m: m.move_to(axes_xt.c2p(t_tracker.get_value(), param_x(t_tracker.get_value()))))
        dot_yt.add_updater(lambda m: m.move_to(axes_yt.c2p(t_tracker.get_value(), param_y(t_tracker.get_value()))))
        dot_xy.add_updater(lambda m: m.move_to(axes_xy.c2p(param_x(t_tracker.get_value()), param_y(t_tracker.get_value()))))

        # 添加t值显示
        t_value = DecimalNumber(
            0,
            num_decimal_places=1,
            include_sign=True,
            unit="t = ",
        ).scale(0.6)
        t_value.next_to(equations, DOWN, buff=0.5)
        t_value.add_updater(lambda m: m.set_value(t_tracker.get_value()))

        # 显示曲线和运动
        self.play(Create(x_curve))
        self.play(Create(y_curve))
        self.wait(1)

        self.play(Write(equations[2]))
        self.wait(1)

        self.add(dot_xt, dot_yt, dot_xy, t_value)
        self.play(
            Create(trajectory),
            t_tracker.animate.set_value(1),
            run_time=8,
            rate_func=linear
        )
        
        self.wait(2) 

class QuadraticParametricCurve(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("一次函数与二次函数轨迹合成").scale(0.8)
        title.to_edge(UP, buff=0.3)
        title.shift(RIGHT * 2)
        self.play(Write(title))
        self.wait(1)

        # 创建三个坐标系
        # x(t)的坐标系
        axes_xt = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2, 8, 1],
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_xt.shift(LEFT * 4 + UP * 1.5)

        # y(t)的坐标系
        axes_yt = Axes(
            x_range=[0, 2, 0.5],
            y_range=[-2, 8, 1],
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_yt.shift(LEFT * 4 + DOWN * 2)

        # x-y平面的坐标系
        axes_xy = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=6
        ).scale(0.7)
        axes_xy.shift(RIGHT * 2)

        # 添加坐标系标签
        xt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_xt.x_axis, RIGHT),
            Text("x").scale(0.4).next_to(axes_xt.y_axis, UP)
        )
        yt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_yt.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_yt.y_axis, UP)
        )
        xy_labels = VGroup(
            Text("x").scale(0.4).next_to(axes_xy.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_xy.y_axis, UP)
        )

        # 显示坐标系
        self.play(
            Create(axes_xt), Write(xt_labels),
            Create(axes_yt), Write(yt_labels),
            Create(axes_xy), Write(xy_labels)
        )

        # 定义参数方程（一次函数和二次函数）
        def param_x(t): return 2*t + 1      # x = 2t + 1
        def param_y(t): return t*t          # y = t²

        # 显示参数方程
        equations = VGroup(
            MathTex(r"x = 2t + 1", color=BLUE),
            MathTex(r"y = t^2", color=RED),
            MathTex(r"\rightarrow y = \frac{(x-1)^2}{4}", color=GREEN)  # 消去参数t后的轨迹方程
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        equations.next_to(axes_xy, LEFT, buff=0.3)
        
        self.play(Write(equations[:2]))

        # 创建x(t)曲线
        x_curve = axes_xt.plot(
            param_x,
            x_range=[0, 1.5, 0.01],
            color=BLUE
        )

        # 创建y(t)曲线
        y_curve = axes_yt.plot(
            param_y,
            x_range=[0, 1.5, 0.01],
            color=RED
        )

        # 创建合成轨迹
        trajectory = ParametricFunction(
            lambda t: axes_xy.c2p(param_x(t), param_y(t)),
            t_range=[0, 1.5],
            color=GREEN
        )

        # 创建运动点
        dot_xt = Dot(color=YELLOW, radius=0.08)
        dot_yt = Dot(color=YELLOW, radius=0.08)
        dot_xy = Dot(color=YELLOW, radius=0.08)

        # 创建时间追踪器
        t_tracker = ValueTracker(0)

        # 添加点的更新函数
        dot_xt.add_updater(lambda m: m.move_to(axes_xt.c2p(t_tracker.get_value(), param_x(t_tracker.get_value()))))
        dot_yt.add_updater(lambda m: m.move_to(axes_yt.c2p(t_tracker.get_value(), param_y(t_tracker.get_value()))))
        dot_xy.add_updater(lambda m: m.move_to(axes_xy.c2p(param_x(t_tracker.get_value()), param_y(t_tracker.get_value()))))

        # 添加t值显示
        t_value = DecimalNumber(
            0,
            num_decimal_places=1,
            include_sign=True,
            unit="t = ",
        ).scale(0.6)
        t_value.next_to(equations, DOWN, buff=0.5)
        t_value.add_updater(lambda m: m.set_value(t_tracker.get_value()))

        # 显示曲线和运动
        self.play(Create(x_curve))
        self.play(Create(y_curve))
        self.wait(1)

        self.play(Write(equations[2]))
        self.wait(1)

        self.add(dot_xt, dot_yt, dot_xy, t_value)
        self.play(
            Create(trajectory),
            t_tracker.animate.set_value(1.5),
            run_time=8,
            rate_func=linear
        )
        
        self.wait(2) 

class TrigonometricParametricCurve(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("正弦余弦函数轨迹合成").scale(0.8)
        title.to_edge(UP, buff=0.3)
        title.shift(RIGHT * 2)
        self.play(Write(title))
        self.wait(1)

        # 创建三个坐标系
        # x(t)的坐标系
        axes_xt = Axes(
            x_range=[0, 4*PI, PI],  # t范围为0到4π
            y_range=[-2, 2, 1],     # x范围为-2到2
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_xt.shift(LEFT * 4 + UP * 1.5)

        # y(t)的坐标系
        axes_yt = Axes(
            x_range=[0, 4*PI, PI],  # t范围为0到4π
            y_range=[-2, 2, 1],     # y范围为-2到2
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_yt.shift(LEFT * 4 + DOWN * 2)

        # x-y平面的坐标系
        axes_xy = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=6
        ).scale(0.7)
        axes_xy.shift(RIGHT * 2)

        # 添加坐标系标签
        xt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_xt.x_axis, RIGHT),
            Text("x").scale(0.4).next_to(axes_xt.y_axis, UP)
        )
        yt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_yt.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_yt.y_axis, UP)
        )
        xy_labels = VGroup(
            Text("x").scale(0.4).next_to(axes_xy.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_xy.y_axis, UP)
        )

        # 显示坐标系
        self.play(
            Create(axes_xt), Write(xt_labels),
            Create(axes_yt), Write(yt_labels),
            Create(axes_xy), Write(xy_labels)
        )

        # 定义参数方程（正弦和余弦函数）
        def param_x(t): return np.cos(t)      # x = cos(t)
        def param_y(t): return np.sin(t)      # y = sin(t)

        # 显示参数方程
        equations = VGroup(
            MathTex(r"x = \cos t", color=BLUE),
            MathTex(r"y = \sin t", color=RED),
            MathTex(r"\rightarrow x^2 + y^2 = 1", color=GREEN)  # 消去参数t后的轨迹方程（圆）
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        equations.next_to(axes_xy, LEFT, buff=0.3)
        
        self.play(Write(equations[:2]))

        # 创建x(t)曲线
        x_curve = axes_xt.plot(
            param_x,
            x_range=[0, 4*PI, 0.01],
            color=BLUE
        )

        # 创建y(t)曲线
        y_curve = axes_yt.plot(
            param_y,
            x_range=[0, 4*PI, 0.01],
            color=RED
        )

        # 创建合成轨迹（圆）
        trajectory = ParametricFunction(
            lambda t: axes_xy.c2p(param_x(t), param_y(t)),
            t_range=[0, 4*PI],
            color=GREEN
        )

        # 创建运动点
        dot_xt = Dot(color=YELLOW, radius=0.08)
        dot_yt = Dot(color=YELLOW, radius=0.08)
        dot_xy = Dot(color=YELLOW, radius=0.08)

        # 创建时间追踪器
        t_tracker = ValueTracker(0)

        # 添加点的更新函数
        dot_xt.add_updater(lambda m: m.move_to(axes_xt.c2p(t_tracker.get_value(), param_x(t_tracker.get_value()))))
        dot_yt.add_updater(lambda m: m.move_to(axes_yt.c2p(t_tracker.get_value(), param_y(t_tracker.get_value()))))
        dot_xy.add_updater(lambda m: m.move_to(axes_xy.c2p(param_x(t_tracker.get_value()), param_y(t_tracker.get_value()))))

        # 添加t值显示
        t_value = DecimalNumber(
            0,
            num_decimal_places=1,
            include_sign=True,
            unit="t = ",
        ).scale(0.6)
        t_value.next_to(equations, DOWN, buff=0.5)
        t_value.add_updater(lambda m: m.set_value(t_tracker.get_value()))

        # 显示曲线和运动
        self.play(Create(x_curve))
        self.play(Create(y_curve))
        self.wait(1)

        self.play(Write(equations[2]))
        self.wait(1)

        self.add(dot_xt, dot_yt, dot_xy, t_value)
        self.play(
            Create(trajectory),
            t_tracker.animate.set_value(4*PI),  # 运行两个完整的周期
            run_time=12,  # 增加运行时间
            rate_func=linear
        )
        
        self.wait(2) 

class EllipticParametricCurve(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("正弦余弦函数椭圆轨迹合成").scale(0.8)
        title.to_edge(UP, buff=0.3)
        title.shift(RIGHT * 2)
        self.play(Write(title))
        self.wait(1)

        # 创建三个坐标系
        # x(t)的坐标系
        axes_xt = Axes(
            x_range=[0, 4*PI, PI],  # t范围为0到4π
            y_range=[-3, 3, 1],     # x范围为-3到3
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_xt.shift(LEFT * 4 + UP * 1.5)

        # y(t)的坐标系
        axes_yt = Axes(
            x_range=[0, 4*PI, PI],  # t范围为0到4π
            y_range=[-2, 2, 1],     # y范围为-2到2
            axis_config={"include_tip": True},
            x_length=4,
            y_length=4
        ).scale(0.7)
        axes_yt.shift(LEFT * 4 + DOWN * 2)

        # x-y平面的坐标系
        axes_xy = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=6
        ).scale(0.7)
        axes_xy.shift(RIGHT * 2)

        # 添加坐标系标签
        xt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_xt.x_axis, RIGHT),
            Text("x").scale(0.4).next_to(axes_xt.y_axis, UP)
        )
        yt_labels = VGroup(
            Text("t").scale(0.4).next_to(axes_yt.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_yt.y_axis, UP)
        )
        xy_labels = VGroup(
            Text("x").scale(0.4).next_to(axes_xy.x_axis, RIGHT),
            Text("y").scale(0.4).next_to(axes_xy.y_axis, UP)
        )

        # 显示坐标系
        self.play(
            Create(axes_xt), Write(xt_labels),
            Create(axes_yt), Write(yt_labels),
            Create(axes_xy), Write(xy_labels)
        )

        # 定义参数方程（椭圆）
        def param_x(t): return 3 * np.cos(t)  # x = 3cos(t)
        def param_y(t): return 2 * np.sin(t)  # y = 2sin(t)

        # 显示参数方程
        equations = VGroup(
            MathTex(r"x = 3\cos t", color=BLUE),
            MathTex(r"y = 2\sin t", color=RED),
            MathTex(r"\rightarrow \frac{x^2}{9} + \frac{y^2}{4} = 1", color=GREEN)  # 椭圆方程
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6)
        equations.next_to(axes_xy, LEFT, buff=0.3)
        
        self.play(Write(equations[:2]))

        # 创建x(t)曲线
        x_curve = axes_xt.plot(
            param_x,
            x_range=[0, 4*PI, 0.01],
            color=BLUE
        )

        # 创建y(t)曲线
        y_curve = axes_yt.plot(
            param_y,
            x_range=[0, 4*PI, 0.01],
            color=RED
        )

        # 创建合成轨迹（椭圆）
        trajectory = ParametricFunction(
            lambda t: axes_xy.c2p(param_x(t), param_y(t)),
            t_range=[0, 4*PI],
            color=GREEN
        )

        # 创建运动点
        dot_xt = Dot(color=YELLOW, radius=0.08)
        dot_yt = Dot(color=YELLOW, radius=0.08)
        dot_xy = Dot(color=YELLOW, radius=0.08)

        # 创建时间追踪器
        t_tracker = ValueTracker(0)

        # 添加点的更新函数
        dot_xt.add_updater(lambda m: m.move_to(axes_xt.c2p(t_tracker.get_value(), param_x(t_tracker.get_value()))))
        dot_yt.add_updater(lambda m: m.move_to(axes_yt.c2p(t_tracker.get_value(), param_y(t_tracker.get_value()))))
        dot_xy.add_updater(lambda m: m.move_to(axes_xy.c2p(param_x(t_tracker.get_value()), param_y(t_tracker.get_value()))))

        # 添加t值显示
        t_value = DecimalNumber(
            0,
            num_decimal_places=1,
            include_sign=True,
            unit="t = ",
        ).scale(0.6)
        t_value.next_to(equations, DOWN, buff=0.5)
        t_value.add_updater(lambda m: m.set_value(t_tracker.get_value()))

        # 显示曲线和运动
        self.play(Create(x_curve))
        self.play(Create(y_curve))
        self.wait(1)

        self.play(Write(equations[2]))
        self.wait(1)

        self.add(dot_xt, dot_yt, dot_xy, t_value)
        self.play(
            Create(trajectory),
            t_tracker.animate.set_value(4*PI),  # 运行两个完整的周期
            run_time=12,  # 增加运行时间
            rate_func=linear
        )
        
        self.wait(2) 