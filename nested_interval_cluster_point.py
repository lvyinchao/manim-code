from manim import *
import numpy as np
import random

# 配置中文环境
config.tex_template = TexTemplateLibrary.ctex  # 使用ctex模板

class NestedIntervalClusterPoint(Scene):
    def construct(self):
        # 使用黑色背景
        self.camera.background_color = BLACK
        
        # 创建标题并快速显示/消失
        title = MathTex(r"\text{闭区间套定理} \Rightarrow \text{聚点定理}").scale(1.2)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # 创建数轴
        number_line = NumberLine(
            x_range=[-2, 8, 1],
            length=12,
            include_numbers=False,
            include_tip=True
        )
        self.play(Create(number_line))
        self.wait(0.5)
        
        # 定义有界无限集E的边界
        a, b = 0, 6
        
        # 添加边界标记
        a_dot = Dot(number_line.n2p(a), color=YELLOW)
        b_dot = Dot(number_line.n2p(b), color=YELLOW)
        a_label = MathTex("a").next_to(a_dot, DOWN)
        b_label = MathTex("b").next_to(b_dot, DOWN)
        
        self.play(
            Create(a_dot), Create(b_dot),
            Write(a_label), Write(b_label)
        )
        
        # 显示区间E
        interval_E = Line(
            start=number_line.n2p(a),
            end=number_line.n2p(b),
            color=BLUE_A,
            stroke_width=8
        )
        interval_E_label = MathTex("E").next_to(interval_E, DOWN, buff=0.5)
        
        self.play(Create(interval_E), Write(interval_E_label))
        
        # 在E上方添加集合的定义 - 修改E的无穷表达方式
        set_definition = MathTex(r"E \subset [a,b], E \text{ 是无限点集}").to_edge(UP, buff=0.8)
        self.play(Write(set_definition))
        
        # 创建随机点集(有界无限集的可视化)
        points_coords = [random.uniform(a, b) for _ in range(30)]
        points_coords.sort()
        
        points = VGroup()
        for coord in points_coords:
            dot = Dot(number_line.n2p(coord), radius=0.05, color=GREEN, z_index=2)  # 设置z_index=2，确保绿色点在上层显示
            points.add(dot)
        
        self.play(Create(points), run_time=1.5)
        
        # 构造闭区间套
        left, right = a, b
        interval_width = right - left
        intervals = []
        interval_labels = []
        
        # 创建初始区间I1
        interval = Line(
            start=number_line.n2p(left),
            end=number_line.n2p(right),
            color=YELLOW,
            stroke_width=6,
            z_index=1  # 设置z_index=1，确保区间在点的下层
        )
        interval_label = MathTex("I_1").next_to(interval, UP, buff=0.5)
        
        intervals.append(interval)
        interval_labels.append(interval_label)
        
        self.play(
            Create(interval),
            Write(interval_label)
        )
        
        # 显示I1区间的端点
        left_dot = Dot(number_line.n2p(left), color=RED)
        right_dot = Dot(number_line.n2p(right), color=RED)
        left_label = MathTex("a_1").next_to(left_dot, DOWN+LEFT, buff=0.2)
        right_label = MathTex("b_1").next_to(right_dot, DOWN+RIGHT, buff=0.2)
        
        self.play(
            Create(left_dot), Create(right_dot),
            Write(left_label), Write(right_label)
        )
        
        # 闭区间套公理
        axiom = MathTex(r"\text{闭区间套定理: } I_1 \supset I_2 \supset \cdots, |I_n| \to 0 \Rightarrow \bigcap_{n=1}^{\infty} I_n = \{c\}")
        axiom.scale(0.8).to_edge(UP, buff=0.2)
        
        # 先淡出集合定义，再显示公理
        self.play(FadeOut(set_definition))
        self.play(Write(axiom))
        
        # 存储所有端点标签以便处理重叠
        endpoint_labels = [left_label, right_label]
        endpoint_dots = [left_dot, right_dot]
        
        # 存储所有区间端点的值，用于后续演示
        a_n_values = [left]
        b_n_values = [right]
        
        # 构造后续区间
        for i in range(1, 5):
            # 将当前区间二分
            mid = (left + right) / 2
            
            # 计算左右子区间中点的数量
            left_points = sum(1 for coord in points_coords if left <= coord <= mid)
            right_points = sum(1 for coord in points_coords if mid < coord <= right)
            
            # 选择包含更多点的子区间
            if left_points >= right_points:
                new_left, new_right = left, mid
            else:
                new_left, new_right = mid, right
            
            # 存储端点值
            a_n_values.append(new_left)
            b_n_values.append(new_right)
            
            # 创建新区间
            new_interval = Line(
                start=number_line.n2p(new_left),
                end=number_line.n2p(new_right),
                color=YELLOW,
                stroke_width=6-i
            )
            new_interval_label = MathTex(f"I_{i+1}").next_to(new_interval, UP, buff=0.5)
            
            intervals.append(new_interval)
            interval_labels.append(new_interval_label)
            
            # 突出显示被选中的子区间
            highlight_rect = SurroundingRectangle(
                new_interval, 
                color=GREEN, 
                buff=0.1,
                stroke_width=2
            )
            
            # 每次选择一个子区间的数学描述 - 更改表达方式
            selection_formula = MathTex(r"I_{" + str(i+1) + r"} \text{ 包含E中无穷多点}")
            selection_formula.next_to(highlight_rect, UP, buff=1.0)
            
            # 寻找需要淡出的重叠标签
            labels_to_fade = []
            
            # 创建新的端点和标签
            new_left_dot = Dot(number_line.n2p(new_left), color=RED)
            new_right_dot = Dot(number_line.n2p(new_right), color=RED)
            new_left_label = MathTex(f"a_{i+1}").next_to(new_left_dot, DOWN+LEFT, buff=0.2)
            new_right_label = MathTex(f"b_{i+1}").next_to(new_right_dot, DOWN+RIGHT, buff=0.2)
            
            # 检查并收集需要淡出的重叠标签
            for old_label, old_dot in zip(endpoint_labels, endpoint_dots):
                # 如果新旧点太接近，将旧标签添加到淡出列表
                for new_dot in [new_left_dot, new_right_dot]:
                    if np.linalg.norm(new_dot.get_center() - old_dot.get_center()) < 0.3:
                        labels_to_fade.append(old_label)
            
            self.play(
                Create(highlight_rect),
                Write(selection_formula),
                run_time=0.8
            )
            
            # 先淡出重叠的标签
            if labels_to_fade:
                self.play(*[FadeOut(label) for label in labels_to_fade], run_time=0.5)
            
            self.play(
                Create(new_interval),
                Write(new_interval_label),
                Create(new_left_dot), Create(new_right_dot),
                Write(new_left_label), Write(new_right_label),
                run_time=1
            )
            self.play(
                FadeOut(highlight_rect),
                FadeOut(selection_formula)
            )
            
            # 更新端点标签和点集合
            endpoint_labels.extend([new_left_label, new_right_label])
            endpoint_dots.extend([new_left_dot, new_right_dot])
            
            # 更新区间边界
            left, right = new_left, new_right
        
        # 标记交点c
        c_point = (left + right) / 2
        cluster_point = Dot(number_line.n2p(c_point), color=WHITE, radius=0.1, z_index=3)  # 设置更高的z_index
        cluster_label = MathTex("c").next_to(cluster_point, UP, buff=0.3)
        
        # 交点c的出现动画
        self.play(
            FocusOn(number_line.n2p(c_point)),
            run_time=1
        )
        
        # 标记c为交点
        intersection_formula = MathTex(r"c \in \bigcap_{n=1}^{\infty} I_n")
        intersection_formula.next_to(cluster_point, UP, buff=1.0)
        
        # 找出需要淡出的元素，但保留点不淡出
        dots_to_remove = [mob for mob in self.mobjects if isinstance(mob, Dot) and mob != cluster_point]
        labels_to_remove = [mob for mob in self.mobjects if isinstance(mob, MathTex) and (mob in interval_labels or any(s in mob.tex_string for s in ["a_", "b_"]))]
        elements_to_clear = dots_to_remove + labels_to_remove
        
        # 确保最后一个区间(I5)也淡出
        last_interval = intervals[-1]
        
        # 清除一些元素，同时创建C点，但不降低点的不透明度
        self.play(
            *[FadeOut(elem) for elem in elements_to_clear],
            FadeOut(last_interval),  # 淡出I5
            Create(cluster_point),
            Write(cluster_label),
            run_time=1.5
        )
        
        self.play(Write(intersection_formula), run_time=1)
        self.wait(1)
        
        # 移除"FadeOut(axiom)"，保持闭区间套定理不淡出
        self.play(FadeOut(intersection_formula))
        
        # 演示c是聚点 - 创建ε邻域，但不显示括号
        epsilon = 0.8
        epsilon_interval = Line(
            start=number_line.n2p(c_point - epsilon),
            end=number_line.n2p(c_point + epsilon),
            color=ORANGE,
            stroke_width=4
        )
        epsilon_label = MathTex("(c-\\varepsilon, c+\\varepsilon)").next_to(epsilon_interval, UP, buff=0.5)
        
        self.play(
            Create(epsilon_interval),
            Write(epsilon_label)
        )
        
        # 创建在ε邻域内的点 - 修改为红色
        epsilon_points = []
        epsilon_old_dots = []
        # 复用已有的点，只改变颜色
        for coord in points_coords:
            if c_point - epsilon < coord < c_point + epsilon:
                # 找到对应的已有点并增加亮度
                for dot in points:
                    if np.allclose(dot.get_center(), number_line.n2p(coord), atol=0.01):
                        epsilon_point = Dot(number_line.n2p(coord), color=RED, radius=0.06, z_index=4)  # 改为红色
                        epsilon_points.append(epsilon_point)
                        epsilon_old_dots.append(dot)
                        break
        
        # 分批次显示ε邻域内的点
        for i in range(0, len(epsilon_points), 3):
            end_idx = min(i+3, len(epsilon_points))
            batch = epsilon_points[i:end_idx]
            self.play(*[Create(dot) for dot in batch], run_time=0.3)
        
        # 在显示完红色点之后，显示"必有区间[an, bn]在c的邻域内"
        # 选择一个足够大的n，使得[an, bn]完全包含在c的ε邻域内
        n = 4  # 使用区间I5
        
        # 创建显示[an, bn]的区间
        an_bn_interval = Line(
            start=number_line.n2p(a_n_values[n]),
            end=number_line.n2p(b_n_values[n]),
            color=YELLOW,
            stroke_width=3,
            z_index=2
        )
        
        # 创建[an, bn]的端点
        an_dot = Dot(number_line.n2p(a_n_values[n]), color=RED, radius=0.08)
        bn_dot = Dot(number_line.n2p(b_n_values[n]), color=RED, radius=0.08)
        # 使用通用的an和bn标签，而不是a5和b5
        an_label = MathTex("a_n").next_to(an_dot, DOWN+LEFT, buff=0.2)
        bn_label = MathTex("b_n").next_to(bn_dot, DOWN+RIGHT, buff=0.2)
        
        # 创建说明文本
        interval_in_neighborhood = MathTex(r"\exists n, [a_n, b_n] \subset (c-\varepsilon, c+\varepsilon)")
        interval_in_neighborhood.next_to(epsilon_label, UP, buff=0.5)
        
        # 显示区间和端点
        self.play(
            Create(an_bn_interval),
            Create(an_dot), Create(bn_dot),
            Write(an_label), Write(bn_label)
        )
        
        # 突出显示区间包含在ε邻域内
        highlight_inclusion = SurroundingRectangle(
            an_bn_interval, 
            color=GREEN_A, 
            buff=0.1,
            stroke_width=2
        )
        
        self.play(
            Create(highlight_inclusion),
            Write(interval_in_neighborhood)
        )
        self.wait(1)
        
        self.play(
            FadeOut(highlight_inclusion),
            FadeOut(interval_in_neighborhood),
            FadeOut(an_bn_interval),
            FadeOut(an_dot), FadeOut(bn_dot),
            FadeOut(an_label), FadeOut(bn_label)
        )
        
        # 最终结论
        conclusion = MathTex(r"\text{聚点定理: 任何有界无限点集} E \subset \mathbb{R} \text{ 至少有一个聚点}")
        conclusion.scale(0.8).to_edge(DOWN, buff=0.5)
        self.play(Write(conclusion))
        
        # 突出显示聚点
        self.play(
            cluster_point.animate.scale(1.5).set_color(YELLOW),
            run_time=1
        )
        self.play(
            cluster_point.animate.scale(1/1.5).set_color(WHITE),
            run_time=1
        )
        
        self.wait(2)

if __name__ == "__main__":
    import os
    os.system("manim -pqh nested_interval_cluster_point.py NestedIntervalClusterPoint") 