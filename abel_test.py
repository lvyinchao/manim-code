# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class AbelTest(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("阿贝尔判别法").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # 创建公式
        formula = VGroup(
            MathTex(r"\sum_{n=1}^{\infty} a_n b_n", color=BLUE),
            Text("收敛，若：", font="SimSun", color=BLUE).scale(0.8)
        ).arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.8)
        
        conditions = VGroup(
            VGroup(
                MathTex(r"1.\ ", color=RED),
                MathTex(r"\{a_n\}", color=RED),
                Text(" 单调递减", font="SimSun", color=RED).scale(0.8)
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                MathTex(r"2.\ ", color=GREEN),
                MathTex(r"\left|\sum_{k=1}^n b_k\right| \leq M", color=GREEN)
            ).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, buff=0.5).next_to(formula, DOWN, buff=0.8)
        
        self.play(Write(formula))
        self.play(Write(conditions))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            axis_config={"include_tip": True},
            x_length=8,
            y_length=5
        ).shift(DOWN * 0.5)

        # 添加坐标轴标签
        x_label = Text("n").scale(0.6).next_to(axes.x_axis, RIGHT)
        y_label = Text("值").scale(0.6).next_to(axes.y_axis, UP)
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label)
        )

        # 创建{an}序列的点和连线
        a_points = []
        for n in range(1, 11):
            a_value = 1/n  # 单调递减序列
            a_point = axes.c2p(n, a_value)
            a_points.append(a_point)

        a_line = VMobject(color=RED)
        a_line.set_points_smoothly(a_points)

        # 创建部分和{Sn}的点和连线
        b_points = []
        s_n = 0
        for n in range(1, 11):
            b_n = (-1)**(n+1)  # 交错序列
            s_n += b_n
            b_point = axes.c2p(n, s_n)
            b_points.append(b_point)

        b_line = VMobject(color=GREEN)
        b_line.set_points_smoothly(b_points)

        # 创建有界线
        bound_up = DashedLine(
            axes.c2p(0, 1),
            axes.c2p(10, 1),
            color=YELLOW
        )
        bound_down = DashedLine(
            axes.c2p(0, -1),
            axes.c2p(10, -1),
            color=YELLOW
        )

        # 动画展示
        self.play(Create(bound_up), Create(bound_down))
        self.play(Create(a_line), Create(b_line))
        
        # 添加图例
        legend = VGroup(
            Dot(color=RED), Text("{an} 单调递减", font="SimSun", color=RED).scale(0.6),
            Dot(color=GREEN), Text("部分和有界", font="SimSun", color=GREEN).scale(0.6)
        ).arrange(RIGHT, buff=0.3)
        legend.to_corner(UR)
        
        self.play(Write(legend))
        self.wait(2) 