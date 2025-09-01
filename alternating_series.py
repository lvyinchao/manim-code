# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class AlternatingSeriesConvergence(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("交错级数收敛性").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # 创建交错级数的各项
        terms = VGroup()
        n_visible_terms = 6  # 减回到6项
        for i in range(n_visible_terms):
            if i == 0:
                term = MathTex("1")
            else:
                sign = "-" if i % 2 == 1 else "+"
                term = MathTex(f"{sign}\\frac{{1}}{{{i+1}}}")
            terms.add(term)
        terms.add(MathTex("\\cdots"))
        terms.arrange(RIGHT, buff=0.2)
        
        # 创建完整的级数表达式
        series = VGroup(
            MathTex("\\sum_{n=1}^{\\infty} (-1)^{n+1}\\frac{1}{n} ="),
            terms
        ).arrange(RIGHT, buff=0.3).scale(0.8)
        series.move_to(ORIGIN + UP * 2)  # 居中显示在上方

        # 添加收敛性说明（移到右上方）
        explanation = VGroup(
            Text("• 通项绝对值单调递减", font="SimSun"),
            Text("• 通项趋于零", font="SimSun"),
            Text("• 级数收敛于ln(2)", font="SimSun")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.5)
        explanation.to_corner(UR, buff=0.5)  # 移到右上角
        
        # 添加误差估计（跟随说明文字）
        error_bound = MathTex(
            r"|R_n| \leq \frac{1}{n+1}",
            color=BLUE
        ).scale(0.7)
        error_bound.next_to(explanation, DOWN, buff=0.5)
        
        error_text = Text(
            "误差界估计",
            font="SimSun"
        ).scale(0.5).next_to(error_bound, UP, buff=0.2)

        self.play(Write(series))
        self.wait(1)

        # 创建坐标系（居中显示）
        axes = Axes(
            x_range=[0, 20, 2],
            y_range=[-0.5, 1.5, 0.5],
            axis_config={
                "include_tip": True,
                "include_numbers": False
            },
            x_length=10,  # 增加宽度
            y_length=6    # 增加高度
        ).move_to(ORIGIN + DOWN * 0.5)  # 居中显示，稍微下移

        # 添加分数刻度标签
        y_labels = VGroup()
        y_values = [-0.5, 0, 0.5, 1, 1.5]
        for y in y_values:
            if y == 0:
                label = MathTex("0")
            elif y == 1:
                label = MathTex("1")
            else:
                num, den = float(y).as_integer_ratio()
                label = MathTex(f"\\frac{{{num}}}{{{den}}}")
            label.scale(0.5)
            label.next_to(axes.c2p(0, y), LEFT, buff=0.1)
            y_labels.add(label)

        # 添加x轴刻度标签（使用整数）
        x_labels = VGroup()
        for x in range(0, 21, 2):
            if x > 0:  # 跳过原点
                label = MathTex(f"{x}").scale(0.5)
                label.next_to(axes.c2p(x, 0), DOWN, buff=0.1)
                x_labels.add(label)

        # 添加坐标轴标签
        x_label = Text("n", font="SimSun").scale(0.6).next_to(axes.x_axis, RIGHT)
        y_label = Text("部分和", font="SimSun").scale(0.6).next_to(axes.y_axis, UP)
        
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            Write(x_labels),
            Write(y_labels)
        )

        # 计算部分和
        def get_partial_sum(n):
            return sum((-1)**(k+1)/k for k in range(1, n+1))

        # 创建高亮框
        highlight_box = SurroundingRectangle(terms[0], color=YELLOW)
        self.play(Create(highlight_box))

        # 创建部分和点和折线
        dots = VGroup()
        n_terms = 20
        partial_sums = [get_partial_sum(n) for n in range(1, n_terms+1)]
        
        # 创建点
        prev_dot = None
        for i, sum_value in enumerate(partial_sums):
            dot = Dot(axes.c2p(i+1, sum_value), color=RED)
            dots.add(dot)
            
            if prev_dot:
                line = Line(prev_dot.get_center(), dot.get_center(), color=YELLOW)
                self.play(
                    Create(dot),
                    Create(line),
                    run_time=0.3
                )
            else:
                self.play(Create(dot), run_time=0.3)
            prev_dot = dot

            # 更新高亮框位置
            if i < len(terms) - 1:
                new_box = SurroundingRectangle(terms[:i+1], color=YELLOW)
                self.play(
                    Transform(highlight_box, new_box),
                    run_time=0.3
                )

        # 显示极限值
        limit_value = np.log(2)
        limit_line = DashedLine(
            axes.c2p(0, limit_value),
            axes.c2p(20, limit_value),
            color=GREEN
        )
        limit_label = MathTex(r"\ln(2)", color=GREEN).scale(0.8)
        limit_label.next_to(limit_line.get_end(), RIGHT)

        self.play(
            Create(limit_line),
            Write(limit_label)
        )

        # 添加收敛性说明
        explanation = VGroup(
            Text("• 通项绝对值单调递减", font="SimSun"),
            Text("• 通项趋于零", font="SimSun"),
            Text("• 级数收敛于ln(2)", font="SimSun")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.5)
        explanation.to_corner(UR, buff=0.5)  # 移到右上角
        
        self.play(Write(explanation))
        
        # 显示振荡收敛的特点
        oscillation = Text(
            "交错级数的部分和在极限值附近振荡收敛",
            font="SimSun"
        ).scale(0.5)
        oscillation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(oscillation))
        self.wait(2)

        # 添加误差估计
        error_bound = MathTex(
            r"|R_n| \leq \frac{1}{n+1}",
            color=BLUE
        ).scale(0.7)
        error_bound.next_to(explanation, DOWN, buff=0.5)
        
        error_text = Text(
            "误差界估计",
            font="SimSun"
        ).scale(0.5).next_to(error_bound, UP, buff=0.2)
        
        self.play(
            Write(error_text),
            Write(error_bound)
        )
        self.wait(2) 