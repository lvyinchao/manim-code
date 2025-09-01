#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
这个程序用Manim创建动画，对比一元函数和二元函数的概念及其极限
作者: Claude
"""

from manim import *
import numpy as np

# 配置中文支持
config.tex_template.add_to_preamble(r"\usepackage[UTF8]{ctex}")

# 定义全局变量A代表极限值1
A = 1

class OneVariableFunction(Scene):
    """演示一元函数及其极限"""
    
    def construct(self):
        # 标题
        title = Text("一元函数极限", font="SimSun")
        self.play(Write(title))
        self.wait()
        self.play(title.animate.scale(0.6).to_edge(UP))
        
        # 创建坐标系
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"include_tip": False},
        ).scale(0.8)
        
        # 坐标轴标签
        x_label = Text("x", font="SimSun").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("f(x)", font="SimSun").next_to(axes.y_axis.get_end(), UP)
        axes_labels = VGroup(x_label, y_label)
        
        # 函数标题
        func_title = Text("f(x) = sin(x)/x", font="SimSun", font_size=24)
        func_title.next_to(axes, UP)
        
        # 函数定义
        def f(x):
            return np.sin(x) / x if x != 0 else A
        
        # 创建函数图像
        graph = axes.plot(lambda x: f(x) if x != 0 else None, 
                          discontinuities=[0], color=BLUE)
        
        # 单点极限值
        limit_point = Dot(axes.c2p(0, A), color=RED)
        limit_label = Text("极限值 = A", font="SimSun", font_size=20, color=RED)
        limit_label.next_to(limit_point, UR, buff=0.1)
        
        # 显示所有元素
        self.play(
            Create(axes),
            Write(axes_labels),
            Write(func_title)
        )
        self.play(Create(graph))
        self.wait()
        
        # 动画演示点的趋近
        approach_dot = Dot(axes.c2p(3, f(3)), color=YELLOW)
        x_tracker = ValueTracker(3)
        
        approach_dot.add_updater(
            lambda d: d.move_to(axes.c2p(x_tracker.get_value(), 
                                         f(x_tracker.get_value())))
        )
        
        approach_arrow = Arrow(start=axes.c2p(3, 0), 
                              end=axes.c2p(3, f(3)), 
                              color=YELLOW, buff=0)
        approach_arrow.add_updater(
            lambda a: a.put_start_and_end_on(
                axes.c2p(x_tracker.get_value(), 0),
                axes.c2p(x_tracker.get_value(), f(x_tracker.get_value()))
            )
        )
        
        value_label = Text("", font="SimSun", font_size=18)
        value_label.add_updater(
            lambda t: t.become(
                Text(f"x = {x_tracker.get_value():.3f}\nf(x) = {f(x_tracker.get_value()):.3f}", 
                     font="SimSun", font_size=18)
            ).next_to(approach_dot, UR, buff=0.1)
        )
        
        self.play(Create(approach_dot), Create(approach_arrow), Create(value_label))
        
        # 从正向趋近
        self.play(x_tracker.animate.set_value(0.001), run_time=3)
        self.wait()
        
        # 从负向趋近
        self.play(x_tracker.animate.set_value(-3), run_time=1)
        self.play(x_tracker.animate.set_value(-0.001), run_time=3)
        self.wait()
        
        # 显示极限点和标签
        self.play(Create(limit_point), Write(limit_label))
        self.wait()
        
        # 清除更新器
        approach_dot.clear_updaters()
        approach_arrow.clear_updaters()
        value_label.clear_updaters()
        
        # 一元函数极限概念
        concept = Text(
            "一元函数极限：当x趋近于某个值a时，函数值f(x)趋近于的极限值L\n"
            "记为：lim(x→a) f(x) = L", 
            font="SimSun", font_size=24
        )
        concept.to_edge(DOWN, buff=0.5)
        
        self.play(Write(concept))
        self.wait(2)
        
        # 清场准备转入二元函数
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )

class TwoVariableFunction(ThreeDScene):
    """演示二元函数及其极限"""
    
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        
        # 标题
        title = Text("二元函数极限", font="SimSun")
        title_mobject = self.add_fixed_in_frame_mobjects(title)
        title.to_corner(UL)
        self.play(Write(title))
        
        # 函数信息
        func_info = Text("f(x,y) = sin(√(x²+y²))/√(x²+y²)", font="SimSun", font_size=24)
        func_info.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(func_info)
        self.play(Write(func_info))
        
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-1, 1.5, 0.5],
        ).scale(0.7)
        
        # 添加轴标签
        x_label = Text("x", font="SimSun").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("y", font="SimSun").next_to(axes.y_axis.get_end(), RIGHT)
        z_label = Text("f(x,y)", font="SimSun").next_to(axes.z_axis.get_end(), UP)
        
        # 固定标签在帧中
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        
        # 创建坐标系
        self.play(Create(axes))
        self.play(Write(VGroup(x_label, y_label, z_label)))
        
        # 函数定义
        def f(x, y):
            r = np.sqrt(x**2 + y**2)
            if r == 0:
                return A
            return np.sin(r) / r
        
        # 创建曲面
        surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(20, 20),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.7
        )
        
        # 显示曲面
        self.play(Create(surface), run_time=2)
        self.wait(0.5)
        
        # 添加说明文字
        approach_text_3d = Text("自变量沿多条路径趋向于原点", font="SimSun", font_size=24)
        approach_text_3d.next_to(title, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(approach_text_3d)
        self.play(Write(approach_text_3d))
        self.wait(0.5)
        self.play(FadeOut(approach_text_3d))
        
        # 创建原点
        origin = Dot3D(axes.c2p(0, 0, A), color=RED)
        
        # 极限点
        limit_point = Dot3D(axes.c2p(0, 0, A), color=RED)
        limit_label = Text("极限值 = A", font="SimSun", color=RED)
        limit_label.next_to(limit_point, UP)
        self.add_fixed_in_frame_mobjects(limit_label)
        
        self.play(Create(limit_point))
        self.play(Write(limit_label))
        
        # 修改描述文本
        paths_description = Text("不同路径趋向同一极限值", font="SimSun", font_size=28, color=BLUE)
        paths_description.to_edge(UP)
        self.add_fixed_in_frame_mobjects(paths_description)
        self.play(Write(paths_description))
        
        # 添加并显示不同路径
        paths = VGroup()
        
        # 沿x轴趋近
        x_path = ParametricFunction(
            lambda t: axes.c2p(t, 0, f(t, 0)),
            t_range=[4, 0.01, -0.01],
            color=YELLOW
        )
        paths.add(x_path)
        
        # 沿y轴趋近
        y_path = ParametricFunction(
            lambda t: axes.c2p(0, t, f(0, t)),
            t_range=[4, 0.01, -0.01],
            color=GREEN
        )
        paths.add(y_path)
        
        # 沿直线y=x趋近
        xy_path = ParametricFunction(
            lambda t: axes.c2p(t, t, f(t, t)),
            t_range=[4, 0.01, -0.01],
            color=PURPLE
        )
        paths.add(xy_path)
        
        # 沿螺旋线趋近
        spiral_path = ParametricFunction(
            lambda t: axes.c2p(
                t * np.cos(2 * t), 
                t * np.sin(2 * t), 
                f(t * np.cos(2 * t), t * np.sin(2 * t))
            ),
            t_range=[4, 0.01, -0.01],
            color=ORANGE
        )
        paths.add(spiral_path)
        
        # 逐个显示点
        self.play(
            Create(x_path),
            Create(y_path),
            Create(xy_path),
            Create(spiral_path),
        )
        
        # 显示所有路径
        self.play(Create(paths), run_time=2)
        self.wait(1)
        
        # 显示极限点和标签
        limit_point_3d = Dot3D(axes.c2p(0, 0, A), color=RED, radius=0.1)
        limit_label_3d = Text("极限值=A", font="SimSun", font_size=20, color=RED)
        limit_label_3d.next_to(limit_point_3d, UP, buff=0.2)
        
        self.play(Create(limit_point_3d))
        self.add_fixed_in_frame_mobjects(limit_label_3d)
        self.play(Write(limit_label_3d))
        
        # 二元函数极限概念
        concept = Text(
            "二元函数极限：当点(x,y)沿任意路径趋近于点(a,b)时，\n"
            "若函数值f(x,y)都趋近于同一个值L，则L为函数在该点的极限\n"
            "记为：lim(x,y)→(a,b) f(x,y) = L", 
            font="SimSun", font_size=24
        )
        concept.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(concept)
        
        self.play(Write(concept))
        self.wait(2)

class LimitDoesNotExist(ThreeDScene):
    """演示二元函数极限不存在的情况"""
    
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        
        # 标题
        title = Text("二元函数极限不存在示例", font="SimSun")
        self.add_fixed_in_frame_mobjects(title)
        title.to_corner(UL)
        self.play(Write(title))
        
        # 函数信息
        func_info = Text("f(x,y) = xy/(x²+y²)", font="SimSun", font_size=24)
        func_info.next_to(title, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(func_info)
        self.play(Write(func_info))
        
        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-1, 1, 0.5],
        ).scale(0.7)
        
        # 添加轴标签
        x_label = Text("x", font="SimSun").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = Text("y", font="SimSun").next_to(axes.y_axis.get_end(), RIGHT)
        
        # 修改z轴标签位置，不再放在z轴的顶部
        z_label = Text("f(x,y)", font="SimSun", color=BLUE_B)
        z_label.to_edge(LEFT).shift(DOWN * 2)  # 放在左侧边缘位置，不会阻碍视线
        
        # 固定标签在帧中
        self.add_fixed_in_frame_mobjects(x_label, y_label, z_label)
        
        # 创建坐标系
        self.play(Create(axes))
        self.play(Write(VGroup(x_label, y_label, z_label)))
        
        # 函数定义
        def f(x, y):
            r_squared = x**2 + y**2
            if r_squared == 0:
                return A  # 函数在原点未定义，但这里设为A便于可视化
            return (x * y) / r_squared
        
        # 创建表面，去除原点周围以避免奇点
        resolution = 20  # 减小以提高性能
        surface = Surface(
            lambda u, v: axes.c2p(
                u, v, f(u, v)
            ),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(resolution, resolution),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.7
        )
        
        # 添加表面
        self.play(Create(surface), run_time=2)
        self.wait()
        
        # 添加从不同方向趋近的路径
        paths = VGroup()
        
        # 沿x轴趋近
        x_path = ParametricFunction(
            lambda t: axes.c2p(t, 0, f(t, 0)),
            t_range=[4, 0.01, -0.01],
            color=YELLOW
        )
        paths.add(x_path)
        x_path_label = Text("x轴路径: 极限值 = A", font="SimSun", font_size=20, color=YELLOW)
        x_path_label.to_edge(LEFT).shift(UP * 1.5)
        self.add_fixed_in_frame_mobjects(x_path_label)
        
        # 沿y轴趋近
        y_path = ParametricFunction(
            lambda t: axes.c2p(0, t, f(0, t)),
            t_range=[4, 0.01, -0.01],
            color=GREEN
        )
        paths.add(y_path)
        y_path_label = Text("y轴路径: 极限值 = A", font="SimSun", font_size=20, color=GREEN)
        y_path_label.next_to(x_path_label, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(y_path_label)
        
        # 沿y=x直线趋近
        xy_path = ParametricFunction(
            lambda t: axes.c2p(t, t, f(t, t)),
            t_range=[4, 0.01, -0.01],
            color=PURPLE
        )
        paths.add(xy_path)
        xy_path_label = Text("y=x路径: 极限值 = A", font="SimSun", font_size=20, color=PURPLE)
        xy_path_label.next_to(y_path_label, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(xy_path_label)
        
        # 沿y=-x直线趋近
        xy_neg_path = ParametricFunction(
            lambda t: axes.c2p(t, -t, f(t, -t)),
            t_range=[4, 0.01, -0.01],
            color=ORANGE
        )
        paths.add(xy_neg_path)
        xy_neg_path_label = Text("y=-x路径: 极限值 = A", font="SimSun", font_size=20, color=ORANGE)
        xy_neg_path_label.next_to(xy_path_label, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(xy_neg_path_label)
        
        # 添加路径
        self.play(Create(paths), run_time=3)
        
        # 显示路径标签
        self.play(
            Write(x_path_label),
            Write(y_path_label),
            Write(xy_path_label),
            Write(xy_neg_path_label)
        )
        
        # 说明文本
        description = Text(
            "二元函数极限不存在情况：\n"
            "从不同方向趋近原点，得到不同的极限值", 
            font="SimSun", font_size=22, color=RED
        )
        description.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(description)
        
        self.play(Write(description))
        self.wait(1)
        
        # 旋转相机以更好地观察表面
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # 添加说明：不同路径得到不同极限值
        explanation_2 = Text(
            "不同路径趋近原点时得到不同的极限值",
            font="SimSun", color=YELLOW
        ).scale(0.5)
        explanation_2.next_to(axes, DOWN)
        self.play(Write(explanation_2), run_time=1)
        
        # 定义结论文本
        conclusion_2 = Text(
            "不同路径得到不同极限值，因此极限不存在",
            font="SimSun", color=RED
        ).scale(0.7)
        conclusion_2.to_edge(UP, buff=2)
        
        # 点沿着路径移动到原点
        self.play(FadeOut(description), Write(conclusion_2))
        self.wait(2)

class FunctionLimitComparison(Scene):
    """整合一元函数与二元函数极限的完整比较"""
    
    def construct(self):
        # 主标题 - 使用Text而非Title以避免TeX编译错误
        title = Text("函数极限概念对比", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait()
        
        # 说明文本
        intro_text = Text(
            "本动画将分三部分展示：\n"
            "1. 一元函数极限\n"
            "2. 二元函数极限\n"
            "3. 二元函数极限不存在的情况", 
            font="SimSun", 
            font_size=28
        )
        intro_text.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(intro_text))
        self.wait(2)
        
        # 第一部分提示
        part1_text = Text("第一部分：一元函数极限", font="SimSun", font_size=36, color=BLUE)
        self.play(
            FadeOut(intro_text),
            ReplacementTransform(title, part1_text)
        )
        self.wait()
        self.play(FadeOut(part1_text))
        
        # 一元函数极限场景
        # 主标题
        title = Text("一元函数极限", font="SimSun")
        self.play(Write(title))
        self.wait()
        self.play(title.animate.scale(0.6).to_edge(UP))
        
        # 说明文本
        intro = Text("一元函数 f(x) = sin(x)/x", font="SimSun", font_size=24)
        intro.next_to(title, DOWN)
        self.play(Write(intro))
        self.wait(2)
        
        # 清场准备展示一元函数
        self.play(
            FadeOut(intro),
            title.animate.scale(0.8).to_corner(UL)
        )
        
        # 创建坐标系
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"include_tip": False},
        ).scale(0.8)
        
        # 函数标题
        func_eq = Text("f(x) = sin(x)/x", font="SimSun", font_size=28)
        func_eq.next_to(axes, UP, buff=0.2)
        
        # 函数定义
        def f1(x):
            return np.sin(x) / x if x != 0 else A
        
        # 创建函数图像
        graph = axes.plot(lambda x: f1(x) if x != 0 else None, 
                          discontinuities=[0], color=BLUE)
        
        # 单点极限值
        limit_point = Dot(axes.c2p(0, A), color=RED)
        limit_label = Text("极限值 = A", font="SimSun", font_size=20, color=RED)
        limit_label.next_to(limit_point, UR, buff=0.1)
        
        # 显示元素
        self.play(
            Create(axes),
            Write(func_eq)
        )
        self.play(Create(graph))
        
        # 创建用于演示的两个点，分别从正向和负向趋近
        pos_x_start = 3.0
        neg_x_start = -3.0
        pos_dot = Dot(axes.c2p(pos_x_start, f1(pos_x_start)), color=YELLOW)
        neg_dot = Dot(axes.c2p(neg_x_start, f1(neg_x_start)), color=GREEN)
        
        # 使用ParametricFunction创建点的轨迹路径
        pos_path = ParametricFunction(
            lambda t: axes.c2p(
                pos_x_start * (1 - t) + 0.01 * t,  # 从pos_x_start到0.01
                f1(pos_x_start * (1 - t) + 0.01 * t)
            ),
            t_range=[0, 1],
            color=YELLOW_A,
            stroke_opacity=0.6
        )
        
        neg_path = ParametricFunction(
            lambda t: axes.c2p(
                neg_x_start * (1 - t) - 0.01 * t,  # 从neg_x_start到-0.01
                f1(neg_x_start * (1 - t) - 0.01 * t)
            ),
            t_range=[0, 1],
            color=GREEN_A,
            stroke_opacity=0.6
        )
        
        # 添加表示趋近方向的标签
        pos_direction = Text("x→0+", font="SimSun", font_size=20, color=YELLOW)
        pos_direction.next_to(pos_dot, UR, buff=0.1)
        
        neg_direction = Text("x→0-", font="SimSun", font_size=20, color=GREEN)
        neg_direction.next_to(neg_dot, UL, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(pos_direction, neg_direction)
        
        # 显示点和轨迹
        self.play(Create(pos_dot), Create(neg_dot))
        self.play(Create(pos_path), Create(neg_path), run_time=1)
        self.play(Write(pos_direction), Write(neg_direction))
        self.wait()
        
        # 沿着曲线移动点（使用单个动画，而不是分两个阶段）
        self.play(
            MoveAlongPath(pos_dot, pos_path),
            MoveAlongPath(neg_dot, neg_path),
            # 中途更新标签位置
            UpdateFromFunc(
                pos_direction,
                lambda m: m.next_to(axes.c2p(
                    pos_x_start * (1 - self.renderer.time / 5) + 0.01 * self.renderer.time / 5,
                    f1(pos_x_start * (1 - self.renderer.time / 5) + 0.01 * self.renderer.time / 5)
                ), UR, buff=0.1)
            ),
            UpdateFromFunc(
                neg_direction,
                lambda m: m.next_to(axes.c2p(
                    neg_x_start * (1 - self.renderer.time / 5) - 0.01 * self.renderer.time / 5,
                    f1(neg_x_start * (1 - self.renderer.time / 5) - 0.01 * self.renderer.time / 5)
                ), UL, buff=0.1)
            ),
            run_time=5
        )
        
        self.wait()
        
        # 显示极限点和标签（确保这段代码不会被跳过）
        self.play(Create(limit_point))
        self.add_fixed_in_frame_mobjects(limit_label)
        self.play(Write(limit_label))
        self.wait(1)  # 确保足够的暂停时间，让用户看清极限值标签

        # 使用Text创建极限符号表示（避免LaTeX错误）
        lim_text = Text("lim", font_size=28)
        x_to_0 = Text("x→0", font_size=22)
        x_to_0.next_to(lim_text, DOWN, buff=0.05, aligned_edge=LEFT)
        f_x_text = Text("f(x) = A", font_size=28)
        f_x_text.next_to(lim_text, RIGHT, buff=0.2)
        
        limit_group = VGroup(lim_text, x_to_0, f_x_text)
        limit_group.shift(DOWN * 2)
        
        self.add_fixed_in_frame_mobjects(limit_group)
        self.play(Write(lim_text), Write(x_to_0), Write(f_x_text))
        self.wait(2)
        
        # 清场，准备第二部分
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != lim_text],
            FadeOut(title),
            FadeOut(limit_label),
            FadeOut(func_eq),
            FadeOut(pos_direction),
            FadeOut(neg_direction),
            FadeOut(pos_dot),
            FadeOut(neg_dot),
            FadeOut(pos_path),
            FadeOut(neg_path)
        )
        
        # 第二部分提示
        part2_text = Text("第二部分：二元函数极限", font="SimSun", font_size=36, color=GREEN)
        self.play(Write(part2_text))
        self.wait()
        self.play(FadeOut(part2_text))
        
        # 显示提示信息
        tip_text = Text(
            "注意：接下来是三维场景演示\n"
            "请运行以下命令观看：\n"
            "manim -pql manim_function_limit_comparison.py TwoVariableFunction",
            font="SimSun", 
            font_size=28
        )
        
        self.play(Write(tip_text))
        self.wait(3)
        
        # 第三部分提示
        self.play(FadeOut(tip_text))
        part3_text = Text("第三部分：二元函数极限不存在的情况", font="SimSun", font_size=36, color=RED)
        self.play(Write(part3_text))
        self.wait()
        self.play(FadeOut(part3_text))
        
        # 显示提示信息
        tip_text2 = Text(
            "注意：接下来是三维场景演示\n"
            "请运行以下命令观看：\n"
            "manim -pql manim_function_limit_comparison.py LimitDoesNotExist",
            font="SimSun", 
            font_size=28
        )
        
        self.play(Write(tip_text2))
        self.wait(3)
        
        # 最后的总结
        self.play(FadeOut(tip_text2))
        summary = Text(
            "本演示展示了函数极限的概念区别：\n\n"
            "一元函数：极限存在当且仅当从左右两个方向趋近的值相同\n\n"
            "二元函数：极限存在当且仅当从任意方向趋近的值都相同",
            font="SimSun", 
            font_size=28
        )
        
        self.play(Write(summary))
        self.wait(3)
        
        # 结束
        end_text = Text(
            "动画演示结束，谢谢观看",
            font="SimSun", 
            font_size=36,
            color=BLUE
        )
        
        self.play(
            FadeOut(summary),
            Write(end_text)
        )
        self.wait(2)

class CompleteFunctionLimitDemo(ThreeDScene):
    """完整演示：依次展示一元函数极限、二元函数极限和二元函数极限不存在的情况"""
    
    def construct(self):
        # 添加总标题，修改为"二元函数极限演示"
        main_title = Text("二元函数极限演示", font="SimSun", font_size=36, color=BLUE)
        main_title.to_edge(UP)
        
        self.add_fixed_in_frame_mobjects(main_title)
        self.play(Write(main_title))
        self.wait(1)
        # 显示标题后淡出
        self.play(FadeOut(main_title))
        self.wait(0.5)
        
        # 设置为2D视角用于一元函数部分
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES)
        
        # 添加一元函数小标题
        one_var_title = Text("一元函数极限", font="SimSun", font_size=28, color=BLUE)
        one_var_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(one_var_title)
        self.play(Write(one_var_title))
        self.wait(0.5)
        
        # 创建坐标系
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"include_tip": False},
        ).scale(0.8)
        
        # 函数定义
        def f1(x):
            return np.sin(x) / x if x != 0 else A
        
        # 创建函数图像
        function_graph = axes.plot(lambda x: f1(x) if x != 0 else None, 
                                   discontinuities=[0], color=BLUE)
        
        self.play(
            Create(axes),
            Create(function_graph)
        )
        
        # 添加文字说明
        approach_text = Text("自变量从两个方向趋向于0点", font="SimSun", font_size=24)
        approach_text.next_to(one_var_title, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(approach_text)
        self.play(Write(approach_text))
        self.wait(0.5)
        self.play(FadeOut(approach_text))
        
        # 创建用于演示的两个点，分别从正向和负向趋近
        pos_x_start = 2.0
        neg_x_start = -2.0
        
        # 使用ParametricFunction创建点的轨迹路径
        pos_path = ParametricFunction(
            lambda t: axes.c2p(
                pos_x_start * (1 - t) + 0.01 * t,  # 从pos_x_start到0.01
                f1(pos_x_start * (1 - t) + 0.01 * t)
            ),
            t_range=[0, 1],
            color=YELLOW_A,
            stroke_opacity=0.6
        )
        
        neg_path = ParametricFunction(
            lambda t: axes.c2p(
                neg_x_start * (1 - t) - 0.01 * t,  # 从neg_x_start到-0.01
                f1(neg_x_start * (1 - t) - 0.01 * t)
            ),
            t_range=[0, 1],
            color=GREEN_A,
            stroke_opacity=0.6
        )
        
        self.play(Create(pos_path), Create(neg_path))
        
        # 创建移动点和标签
        pos_point = Dot(axes.c2p(pos_x_start, f1(pos_x_start)), color=YELLOW)
        neg_point = Dot(axes.c2p(neg_x_start, f1(neg_x_start)), color=GREEN)
        
        pos_label = Text("x→0+", font="SimSun", font_size=20).next_to(pos_point, UR, buff=0.1)
        neg_label = Text("x→0-", font="SimSun", font_size=20).next_to(neg_point, UL, buff=0.1)
        
        self.add_fixed_in_frame_mobjects(pos_label, neg_label)
        self.play(Create(pos_point), Create(neg_point))
        self.play(Write(pos_label), Write(neg_label))
        
        # 移动点到原点
        self.play(
            MoveAlongPath(pos_point, pos_path),
            MoveAlongPath(neg_point, neg_path),
            run_time=3
        )
        self.wait(0.5)
        
        # 移动点到达后显示极限点和标签
        limit_point = Dot(axes.c2p(0, A), color=RED)
        limit_label = Text("极限值=A", font="SimSun", font_size=20, color=RED)
        limit_label.next_to(limit_point, UR, buff=0.1)
        
        self.play(Create(limit_point))
        self.add_fixed_in_frame_mobjects(limit_label)
        self.play(Write(limit_label))
        self.wait(1)
        
        # 使用Text创建极限符号表示（避免LaTeX错误）
        lim_text = Text("lim", font_size=28)
        x_to_0 = Text("x→0", font_size=22)
        x_to_0.next_to(lim_text, DOWN, buff=0.05, aligned_edge=LEFT)
        f_x_text = Text("f(x) = A", font_size=28)
        f_x_text.next_to(lim_text, RIGHT, buff=0.2)
        
        limit_group = VGroup(lim_text, x_to_0, f_x_text)
        limit_group.shift(DOWN * 2)
        
        self.add_fixed_in_frame_mobjects(limit_group)
        self.play(Write(lim_text), Write(x_to_0), Write(f_x_text))
        self.wait(2)
        
        # 清除一元函数部分
        self.clear()
        
        # 开始二元函数部分
        two_var_title = Text("二元函数极限", font="SimSun", font_size=28, color=BLUE)
        two_var_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(two_var_title)
        self.play(Write(two_var_title))
        self.wait(0.5)
        
        # 添加二元函数极限结论到标题下方
        conclusion_2 = Text("二元函数极限存在：从任意路径趋近得到相同极限值", font="SimSun", font_size=20, color=BLUE)
        conclusion_2.next_to(two_var_title, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(conclusion_2)
        self.play(Write(conclusion_2))
        self.wait(0.5)
        
        # 设置3D相机角度
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)
        
        # 创建3D坐标轴
        axes_3d = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
            z_length=4,
        ).move_to(ORIGIN)
        
        # 显示3D坐标系
        self.play(Create(axes_3d))
        
        # 函数定义，计算曲面上的点
        def f(x, y):
            r = np.sqrt(x**2 + y**2)
            if r == 0:
                return A
            return np.sin(r) / r
        
        # 创建曲面
        surface = Surface(
            lambda u, v: axes_3d.c2p(u, v, f(u, v)),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(20, 20),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.7
        )
        
        # 显示曲面
        self.play(Create(surface), run_time=2)
        self.wait(0.5)
        
        # 添加说明文字
        approach_text_3d = Text("自变量沿多条路径趋向于原点", font="SimSun", font_size=24)
        approach_text_3d.next_to(two_var_title, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(approach_text_3d)
        self.play(Write(approach_text_3d))
        self.wait(0.5)
        self.play(FadeOut(approach_text_3d))
        
        # 创建原点
        origin = Dot3D(axes_3d.c2p(0, 0, A), color=RED)
        self.play(Create(origin))
        self.wait(0.5)
        
        # 添加从不同方向趋近的路径
        paths = VGroup()
        
        # 沿x轴趋近
        x_path = ParametricFunction(
            lambda t: axes_3d.c2p(t, 0, f(t, 0)),
            t_range=[4, 0.01, -0.01],
            color=YELLOW
        )
        paths.add(x_path)
        x_point = Sphere(radius=0.1, color=YELLOW).move_to(axes_3d.c2p(4, 0, f(4, 0)))

        # 沿y轴趋近
        y_path = ParametricFunction(
            lambda t: axes_3d.c2p(0, t, f(0, t)),
            t_range=[4, 0.01, -0.01],
            color=GREEN
        )
        paths.add(y_path)
        y_point = Sphere(radius=0.1, color=GREEN).move_to(axes_3d.c2p(0, 4, f(0, 4)))

        # 沿直线y=x趋近
        xy_path = ParametricFunction(
            lambda t: axes_3d.c2p(t, t, f(t, t)),
            t_range=[4, 0.01, -0.01],
            color=PURPLE
        )
        paths.add(xy_path)
        xy_point = Sphere(radius=0.1, color=PURPLE).move_to(axes_3d.c2p(3, 3, f(3, 3)))

        # 沿直线y=-x趋近
        xy_neg_path = ParametricFunction(
            lambda t: axes_3d.c2p(t, -t, f(t, -t)),
            t_range=[4, 0.01, -0.01],
            color=TEAL
        )
        paths.add(xy_neg_path)
        xy_neg_point = Sphere(radius=0.1, color=TEAL).move_to(axes_3d.c2p(3, -3, f(3, -3)))

        # 沿螺旋线趋近
        spiral_path = ParametricFunction(
            lambda t: axes_3d.c2p(
                t * np.cos(2 * t), 
                t * np.sin(2 * t), 
                f(t * np.cos(2 * t), t * np.sin(2 * t))
            ),
            t_range=[4, 0.01, -0.01],
            color=ORANGE
        )
        paths.add(spiral_path)
        spiral_point = Sphere(radius=0.1, color=ORANGE).move_to(
            axes_3d.c2p(4 * np.cos(8), 4 * np.sin(8), f(4 * np.cos(8), 4 * np.sin(8)))
        )

        # 逐个显示点
        self.play(
            Create(x_point),
            Create(y_point),
            Create(xy_point),
            Create(xy_neg_point),
            Create(spiral_point),
        )
        
        # 显示所有路径
        self.play(Create(paths), run_time=2)
        self.wait(1)
        
        # 显示极限点和标签
        limit_point_3d = Dot3D(axes_3d.c2p(0, 0, A), color=RED, radius=0.1)
        limit_label_3d = Text("极限值=A", font="SimSun", font_size=20, color=RED)
        limit_label_3d.next_to(limit_point_3d, UP, buff=0.2)
        
        # 添加进一步说明
        limit_explanation = Text("无论从哪个方向趋近，极限值都相同", font="SimSun", font_size=22, color=GREEN)
        limit_explanation.to_edge(DOWN, buff=1)
        
        self.play(Create(limit_point_3d))
        self.add_fixed_in_frame_mobjects(limit_label_3d, limit_explanation)
        self.play(Write(limit_label_3d))
        self.play(Write(limit_explanation))
        self.wait(1)
        
        # 使用Text创建极限符号表示（避免LaTeX错误）
        lim_text_2 = Text("lim", font_size=28)
        xy_to_00 = Text("(x,y)→(0,0)", font_size=22)
        xy_to_00.next_to(lim_text_2, DOWN, buff=0.05, aligned_edge=LEFT)
        f_xy_text_2 = Text("f(x,y) = A", font_size=28)
        f_xy_text_2.next_to(lim_text_2, RIGHT, buff=0.5)  # 增加右侧缓冲区，从0.2改为0.5
        
        limit_group_2 = VGroup(lim_text_2, xy_to_00, f_xy_text_2)
        limit_group_2.shift(DOWN * 3).scale(0.9)  # 缩小整体大小并调整位置
        
        self.add_fixed_in_frame_mobjects(limit_group_2)
        self.play(Write(lim_text_2), Write(xy_to_00), Write(f_xy_text_2))
        self.wait(2)
        
        # 清除场景
        self.clear()
        
        # 开始二元函数极限不存在的情况
        no_limit_title = Text("二元函数极限不存在的情况", font="SimSun", font_size=28, color=RED)
        no_limit_title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(no_limit_title)
        self.play(Write(no_limit_title))
        self.wait(0.5)
        
        # 添加二元函数极限不存在结论到标题下方
        conclusion_3 = Text("不同路径趋近得到不同极限值，因此极限不存在", font="SimSun", font_size=20, color=RED)
        conclusion_3.next_to(no_limit_title, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(conclusion_3)
        self.play(Write(conclusion_3))
        self.wait(0.5)
        
        # 设置3D相机角度
        self.set_camera_orientation(phi=75 * DEGREES, theta=-60 * DEGREES)
        
        # 创建新的3D坐标轴
        axes_3d_2 = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-1, 1, 0.5],
            x_length=6,
            y_length=6,
            z_length=4,
        ).move_to(ORIGIN)
        
        # 显示3D坐标系
        self.play(Create(axes_3d_2))
        
        # 创建函数 z = xy/(x^2+y^2) 的曲面
        def f2(x, y):
            r_squared = x**2 + y**2
            if r_squared < 0.001:  # 避免除以零
                return 0  # 返回0而不是A，因为在这个例子中沿x轴和y轴趋近的极限值是0
            return (x * y) / r_squared
        
        # 创建曲面
        surface_2 = Surface(
            lambda u, v: axes_3d_2.c2p(u, v, f2(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E],
        )
        
        # 创建函数公式
        func_formula = Text("z=f(x,y)=xy/(x²+y²)", font="SimSun", font_size=24, color=BLUE)
        func_formula.to_edge(UP, buff=1.5)
        
        self.play(Create(surface_2))
        self.add_fixed_in_frame_mobjects(func_formula)
        self.play(Write(func_formula))
        
        # 创建原点
        origin = Dot3D(axes_3d_2.c2p(0, 0, 0), color=RED)
        self.play(Create(origin))
        self.wait(0.5)
        
        # 显示解释文本
        explain_text = Text("观察不同路径趋近原点时的极限值", font="SimSun", font_size=20)
        explain_text.to_edge(UP, buff=2)
        self.add_fixed_in_frame_mobjects(explain_text)
        self.play(Write(explain_text))
        self.wait(1)
        self.play(FadeOut(explain_text))
        
        # 创建不同类型的路径及其标签
        paths_3d = VGroup()
        path_points = []
        path_labels = []
        
        # 1. 沿x轴趋近 - 极限值 = A
        x_path = ParametricFunction(
            lambda t: axes_3d_2.c2p(t, 0, f2(t, 0)),
            t_range=[2, 0.1, -0.05],
            color=YELLOW
        )
        paths_3d.add(x_path)
        x_point = Sphere(radius=0.08, color=YELLOW).move_to(axes_3d_2.c2p(2, 0, f2(2, 0)))
        x_label = Text("沿x轴路径趋近：极限值为A", font="SimSun", font_size=18, color=YELLOW)
        x_label.to_corner(UL).shift(DOWN * 2)
        self.add_fixed_in_frame_mobjects(x_label)
        path_points.append(x_point)
        path_labels.append(x_label)
        
        # 2. 沿y轴趋近 - 极限值 = A
        y_path = ParametricFunction(
            lambda t: axes_3d_2.c2p(0, t, f2(0, t)),
            t_range=[2, 0.1, -0.05],
            color=GREEN
        )
        paths_3d.add(y_path)
        y_point = Sphere(radius=0.08, color=GREEN).move_to(axes_3d_2.c2p(0, 2, f2(0, 2)))
        y_label = Text("沿y轴路径趋近：极限值为A", font="SimSun", font_size=18, color=GREEN)
        y_label.next_to(x_label, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(y_label)
        path_points.append(y_point)
        path_labels.append(y_label)
        
        # 3. 沿直线y=x路径趋近 - 极限值 = A
        xy_path = ParametricFunction(
            lambda t: axes_3d_2.c2p(t, t, f2(t, t)),
            t_range=[2, 0.1, -0.05],
            color=PURPLE
        )
        paths_3d.add(xy_path)
        xy_point = Sphere(radius=0.08, color=PURPLE).move_to(axes_3d_2.c2p(2, 2, f2(2, 2)))
        xy_label = Text("沿y=x路径趋近：极限值为A", font="SimSun", font_size=18, color=PURPLE)
        xy_label.next_to(y_label, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(xy_label)
        path_points.append(xy_point)
        path_labels.append(xy_label)
        
        # 4. 沿直线y=-x路径趋近 - 极限值 = A
        xy_neg_path = ParametricFunction(
            lambda t: axes_3d_2.c2p(t, -t, f2(t, -t)),
            t_range=[2, 0.1, -0.05],
            color=TEAL
        )
        paths_3d.add(xy_neg_path)
        xy_neg_point = Sphere(radius=0.08, color=TEAL).move_to(axes_3d_2.c2p(2, -2, f2(2, -2)))
        xy_neg_label = Text("沿y=-x路径趋近：极限值为A", font="SimSun", font_size=18, color=TEAL)
        xy_neg_label.next_to(xy_label, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(xy_neg_label)
        path_points.append(xy_neg_point)
        path_labels.append(xy_neg_label)

        # 创建极限点
        limit_points = [
            Dot3D(axes_3d_2.c2p(0, 0, 0), color=YELLOW, radius=0.08),  # x轴路径极限点：(0,0,0)
            Dot3D(axes_3d_2.c2p(0, 0, 0), color=GREEN, radius=0.08),   # y轴路径极限点：(0,0,0)
            Dot3D(axes_3d_2.c2p(0, 0, 0.5), color=PURPLE, radius=0.08), # y=x路径极限点：(0,0,0.5)
            Dot3D(axes_3d_2.c2p(0, 0, -0.5), color=TEAL, radius=0.08),  # y=-x路径极限点：(0,0,-0.5)
        ]
        
        # 显示极限点
        for limit_point in limit_points:
            self.play(Create(limit_point), run_time=0.5)
        
        # 然后逐个演示点沿着路径移动到各自的极限值
        for i, (point, limit_point) in enumerate(zip(path_points, limit_points)):
            # 对于每个点，创建一个路径从点的当前位置到对应的极限值
            self.play(
                point.animate.move_to(limit_point.get_center()),
                run_time=2
            )
            self.wait(0.5)
        
        # 使用Text创建极限符号表示（避免LaTeX错误）
        lim_text_3 = Text("lim", font_size=28)
        xy_to_00_3 = Text("(x,y)→(0,0)", font_size=22)
        xy_to_00_3.next_to(lim_text_3, DOWN, buff=0.05, aligned_edge=LEFT)
        f_xy_text_3 = Text("xy/(x²+y²) 不存在", font_size=28)
        f_xy_text_3.next_to(lim_text_3, RIGHT, buff=0.2)
        
        limit_group_3 = VGroup(lim_text_3, xy_to_00_3, f_xy_text_3)
        limit_group_3.to_edge(DOWN, buff=1)
        
        self.add_fixed_in_frame_mobjects(limit_group_3)
        self.play(Write(lim_text_3), Write(xy_to_00_3), Write(f_xy_text_3))
        self.wait(2)

if __name__ == "__main__":
    # 运行完整演示
    # manim -pql manim_function_limit_comparison.py CompleteFunctionLimitDemo
    pass 