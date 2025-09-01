# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class FiniteCoveringProof(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-0.5, 3.5, 0.5],
            x_length=10,
            y_length=6,
            axis_config={"include_tip": True}
        )
        
        self.play(Create(axes), run_time=1.5)
        
        # 创建闭区间 [0,5]
        interval = Line(
            axes.c2p(0, 0),
            axes.c2p(5, 0),
            color=WHITE,
            stroke_width=4
        )
        endpoints = VGroup(
            Dot(axes.c2p(0, 0), radius=0.07),
            Dot(axes.c2p(5, 0), radius=0.07)
        )
        interval_labels = VGroup(
            MathTex("a").next_to(axes.c2p(0, 0), DOWN),
            MathTex("b").next_to(axes.c2p(5, 0), DOWN)
        )
        
        self.play(
            Create(interval),
            Create(endpoints),
            Write(interval_labels),
            run_time=1.5
        )

        # 标题和反证法说明
        title = Text("有限覆盖定理的证明", color=BLUE).scale(0.8)
        title.to_corner(UP)
        self.play(Write(title), run_time=1.5)
        
        # 添加反证法假设
        assumption = Text("反证法：假设不存在有限子覆盖", color=RED).scale(0.6)
        assumption.next_to(title, DOWN)
        self.play(Write(assumption), run_time=1.5)
        
        # 展示开覆盖 - 修改为包含更多开集并明确是无限覆盖
        centers = [0.4, 1.2, 2.0, 2.8, 3.6, 4.4, 5.2]  # 增加更多中心点
        radii = [0.8, 0.7, 0.8, 0.7, 0.8, 0.7, 0.8]    # 对应的半径
        colors = [BLUE, RED, GREEN, YELLOW, BLUE_B, RED_B, GREEN_B]  # 更多颜色
        y_positions = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
        
        open_sets = VGroup()
        
        for i, (center, radius, color, y_pos) in enumerate(zip(centers, radii, colors, y_positions)):
            arc = Arc(
                radius=radius,
                angle=PI,
                color=color,
                stroke_width=3,
                fill_opacity=0.2,
                fill_color=color
            ).shift(axes.c2p(center, y_pos))
            
            # 只给前5个开集添加标签
            if i < 5:
                label = MathTex(f"U_{{{i+1}}}").set_color(color)
                label.next_to(arc, UP, buff=0.2)
                open_sets.add(VGroup(arc, label))
                
                self.play(
                    Create(arc),
                    Write(label),
                    run_time=0.8  # 放慢速度
                )
            else:
                # 最后几个开集快速创建，不添加标签
                open_sets.add(arc)
                self.play(Create(arc), run_time=0.6)  # 放慢速度
        
        # 添加省略号表示无限继续
        dots = MathTex(r"\ldots").scale(1.2).set_color(WHITE)
        dots.next_to(axes.c2p(5.5, 1.0), RIGHT, buff=0.1)
        self.play(Write(dots), run_time=1.0)
        
        # 添加无限开集的标签
        infinity_label = MathTex(r"U_n, n \in \mathbb{N}").set_color(WHITE)
        infinity_label.next_to(dots, UP, buff=0.2)
        self.play(Write(infinity_label), run_time=1.2)

        self.wait(1.5)
        
        # 淡化开覆盖，进入二分过程
        self.play(
            open_sets.animate.set_opacity(0.3),
            dots.animate.set_opacity(0.3),
            infinity_label.animate.set_opacity(0.3),
            run_time=1.5
        )
        
        # 初始划分
        mid_point = 2.5
        mid_dot = Dot(axes.c2p(mid_point, 0.5), color=YELLOW)
        left_interval = Line(
            axes.c2p(0, 0.5),
            axes.c2p(mid_point, 0.5),
            color=YELLOW
        )
        right_interval = Line(
            axes.c2p(mid_point, 0.5),
            axes.c2p(5, 0.5),
            color=YELLOW
        )
        
        # 添加区间端点标签
        a0_label = MathTex("a_0").scale(0.6).next_to(axes.c2p(0, 0.5), DOWN, buff=0.15)
        b0_label = MathTex("b_0").scale(0.6).next_to(axes.c2p(5, 0.5), DOWN, buff=0.15)
        
        # 添加简短说明
        split_text = Text("初始划分", color=YELLOW).scale(0.5)
        split_text.next_to(left_interval, UP, buff=0.2)
        
        self.play(
            Create(mid_dot),
            Create(left_interval),
            Create(right_interval),
            Write(split_text),
            Write(a0_label),
            Write(b0_label),
            run_time=1.8
        )
        
        # 选择左区间
        left_brace = Brace(left_interval, DOWN)
        left_text = Text("不能有限覆盖（下同）", color=YELLOW).scale(0.4)
        left_text.next_to(left_brace, DOWN, buff=0.1)
        
        self.play(
            Create(left_brace),
            Write(left_text),
            right_interval.animate.set_opacity(0.3),
            run_time=1.5
        )
        
        # 递归过程
        recursive_intervals = []
        current_left, current_right = 0, mid_point
        bisection_colors = [YELLOW_B, YELLOW_C, YELLOW_D]
        interval_endpoints = []  # 保存各区间端点
        endpoint_labels = VGroup()  # 端点标签组
        
        for i, color in enumerate(bisection_colors):
            y_level = 1.0 + (i+1) * 0.4
            new_mid = (current_left + current_right) / 2
            
            new_mid_dot = Dot(axes.c2p(new_mid, y_level), color=color)
            new_left = Line(
                axes.c2p(current_left, y_level),
                axes.c2p(new_mid, y_level),
                color=color
            )
            new_right = Line(
                axes.c2p(new_mid, y_level),
                axes.c2p(current_right, y_level),
                color=color
            )
            
            # 添加端点标签（不显示具体数值）
            a_label = MathTex(f"a_{{{i+1}}}").scale(0.5)
            a_label.next_to(axes.c2p(current_left, y_level), DOWN+LEFT, buff=0.1)
            mid_label = MathTex("").scale(0.5)  # 空标签，不显示中点值
            mid_label.next_to(axes.c2p(new_mid, y_level), DOWN, buff=0.1)
            b_label = MathTex(f"b_{{{i+1}}}").scale(0.5)
            b_label.next_to(axes.c2p(current_right, y_level), DOWN+RIGHT, buff=0.1)
            endpoint_labels.add(a_label, mid_label, b_label)
            
            recursive_intervals.append((current_left, current_right))
            
            self.play(
                Create(new_mid_dot),
                Create(new_left),
                Create(new_right),
                run_time=1.2
            )
            
            self.play(
                Write(a_label),
                Write(b_label),
                run_time=1.0
            )
            
            # 选择左区间或右区间（交替选择以展示递归过程）
            select_left = (i % 2 == 0)
            selected_line = new_left if select_left else new_right
            selected_brace = Brace(selected_line, DOWN)
            
            self.play(
                Create(selected_brace),
                (new_right if select_left else new_left).animate.set_opacity(0.3),
                run_time=1.2
            )
            
            # 保存区间端点
            if select_left:
                interval_endpoints.append((current_left, new_mid))
                current_right = new_mid
            else:
                interval_endpoints.append((new_mid, current_right))
                current_left = new_mid
        
        # 添加区间套说明
        interval_desc = Text("构造闭区间套", color=YELLOW_B).scale(0.5)
        interval_desc.to_corner(RIGHT).shift(LEFT * 2 + UP * 1)
        self.play(Write(interval_desc), run_time=1.2)
        
        # 计算最终区间位置和ξ的位置
        final_left, final_right = interval_endpoints[-1]
        # 确保ξ位于最终区间内
        xi_position = (final_left + final_right) / 2  # 选择区间中点作为ξ
        
        # 极限点
        limit_point = Dot(axes.c2p(xi_position, 0), color=WHITE, radius=0.1)
        limit_label = MathTex(r"\xi").scale(1.2).next_to(limit_point, UP, buff=0.2)
        
        # 分开处理中文和数学符号
        limit_text_ch = Text("存在唯一点", color=WHITE).scale(0.5)
        limit_math = MathTex(r"\xi \in [a_{n}, b_{n}]", color=WHITE).scale(0.7)
        limit_text_n = Text("，n=1,2,...", color=WHITE).scale(0.5)
        
        # 将这些元素组合成一组
        limit_group = VGroup(limit_text_ch, limit_math, limit_text_n)
        limit_group.arrange(RIGHT, buff=0.1)
        limit_group.next_to(interval_desc, DOWN, buff=0.3)
        
        self.play(
            FadeIn(limit_point, scale=1.5),
            Write(limit_label),
            Write(limit_group),
            run_time=1.8
        )
        
        # 强调ξ在最终区间内
        final_interval_with_brackets = VGroup(
            Line(axes.c2p(final_left, 0), axes.c2p(final_right, 0), color=YELLOW_D, stroke_width=5),
            Brace(Line(axes.c2p(final_left, 0), axes.c2p(final_right, 0)), DOWN, color=YELLOW_D)
        )
        
        final_interval_label = MathTex(r"[a_{n},b_{n}]").set_color(YELLOW_D).scale(0.8)
        final_interval_label.next_to(final_interval_with_brackets, DOWN, buff=0.2)
        
        self.play(
            Create(final_interval_with_brackets),
            Write(final_interval_label),
            run_time=1.5
        )
        
        # 创建epsilon说明文本 - 先显示这个
        epsilon_text_ch = Text("存在ε>0", color=WHITE).scale(0.5)
        epsilon_text_ch.next_to(limit_group, DOWN, buff=0.3)
        
        # 先显示文本说明
        self.play(Write(epsilon_text_ch), run_time=1.2)
        
        # 显示ξ的ε-邻域 - 更加明显，改为红色
        epsilon = (final_right - final_left) * 1.5  # 增大邻域范围，使其明显大于[a_n,b_n]
        epsilon_interval = Line(
            axes.c2p(xi_position-epsilon, 0),
            axes.c2p(xi_position+epsilon, 0),
            color=RED,  # 改为红色
            stroke_width=8
        )
        
        # 创建ε-邻域两端的点和标记 - 改为红色
        epsilon_left_dot = Dot(axes.c2p(xi_position-epsilon, 0), color=RED, radius=0.08)
        epsilon_right_dot = Dot(axes.c2p(xi_position+epsilon, 0), color=RED, radius=0.08)
        
        # 放在[a_n,b_n]标签下方 - 改为红色
        epsilon_brace = Brace(epsilon_interval, DOWN, color=RED)
        
        # 显示包含关系 - 将包含符号和标签放在同一行
        inclusion_symbol = MathTex(r"\subset", color=RED).scale(0.9)
        inclusion_symbol.next_to(final_interval_label, RIGHT, buff=0.2)
        
        epsilon_label = MathTex(r"({\xi}-\epsilon,{\xi}+\epsilon)").set_color(RED).scale(0.8)
        epsilon_label.next_to(inclusion_symbol, RIGHT, buff=0.2)  # 放在包含符号右侧
        
        # 然后再显示ε-邻域相关动画
        self.play(
            Create(epsilon_interval),
            FadeIn(epsilon_left_dot),
            FadeIn(epsilon_right_dot),
            Create(epsilon_brace),
            run_time=1.5
        )
        
        # 显示包含关系和标签在同一行
        self.play(
            Write(inclusion_symbol),
            Write(epsilon_label),
            run_time=1.5
        )
        
        # 当n足够大时的矛盾
        final_interval = Line(
            axes.c2p(final_left, 0),
            axes.c2p(final_right, 0),
            color=YELLOW_D,
            stroke_width=5
        )
        
        # 可视化包含关系 - 区间缩小的动画
        self.play(
            final_interval_with_brackets.animate.scale(0.9, about_point=axes.c2p(xi_position, 0)),
            rate_func=there_and_back_with_pause,
            run_time=2.5  # 加长这个动画
        )
        
        # 分开处理中文和数学符号，保持原来的位置
        n_large_ch = Text("当n足够大时，", color=YELLOW_D).scale(0.5)
        n_large_math = MathTex(r"[a_{n},b_{n}] \subset (\xi-\epsilon,\xi+\epsilon)", color=YELLOW_D).scale(0.7)
        n_large_group = VGroup(n_large_ch, n_large_math)
        n_large_group.arrange(RIGHT, buff=0.1)
        n_large_group.next_to(epsilon_text_ch, DOWN, buff=0.3)  # 保持相对位置引用
        
        self.play(
            Write(n_large_group),
            run_time=1.5
        )
        
        # 显示矛盾
        contradiction_ch = Text("矛盾！", color=RED).scale(0.6)
        contradiction_math = MathTex(r"[a_{n},b_{n}]", color=RED).scale(0.7)
        contradiction_ch2 = Text("可被单个开集覆盖!", color=RED).scale(0.6)
        contradiction_group = VGroup(contradiction_ch, contradiction_math, contradiction_ch2)
        contradiction_group.arrange(RIGHT, buff=0.1)
        contradiction_group.next_to(n_large_group, DOWN, buff=0.3)
        
        contradiction = Cross(scale_factor=0.5, stroke_width=6, color=RED)
        contradiction.move_to(final_interval)
        
        self.play(
            Create(contradiction),
            Write(contradiction_group),
            run_time=1.8
        )
        
        # 结论 - 向右移动一个单位并稍微下移
        conclusion = Text("结论：任意开覆盖存在有限子覆盖", color=GREEN).scale(0.6)
        conclusion.to_edge(DOWN, buff=0.3).shift(RIGHT)  # 减小buff值，使其下移一点
        self.play(Write(conclusion), run_time=1.5)
        
        self.wait(2.5)

def main():
    import os
    os.system("manim -pql finite_covering_theorem.py FiniteCoveringProof")

if __name__ == "__main__":
    main() 