from manim import *
import numpy as np

class NestedIntervalTheorem(Scene):
    def construct(self):
        # 配置参数
        x_range = [-1, 8, 1]
        y_range = [-0.5, 3.5, 0.5]
        
        # 创建坐标系
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=10,
            y_length=6,
            axis_config={
                "include_tip": True,
                "include_numbers": False  # 不显示坐标轴数值
            }
        )
        
        self.play(Create(axes, run_time=3))
        
        # 第一步：展示区间套的构造
        intervals = []
        interval_labels = []
        y_positions = [0.5, 1.5, 2.5]
        interval_data = [
            (1, 7, BLUE),    # [a₁, b₁]
            (2, 5, RED),     # [a₂, b₂]
            (3, 4, GREEN)    # [a₃, b₃]
        ]
        
        # 逐个显示区间及其标签
        for i, (a, b, color) in enumerate(interval_data):
            interval = Line(
                axes.c2p(a, y_positions[i]),
                axes.c2p(b, y_positions[i]),
                color=color,
                stroke_width=3
            )
            # 添加端点标签
            left_point = Dot(axes.c2p(a, y_positions[i]), color=color, radius=0.05)
            right_point = Dot(axes.c2p(b, y_positions[i]), color=color, radius=0.05)
            left_label = MathTex(f"a_{i+1}", color=color).scale(0.6)
            right_label = MathTex(f"b_{i+1}", color=color).scale(0.6)
            left_label.next_to(left_point, DL, buff=0.1)
            right_label.next_to(right_point, DR, buff=0.1)
            
            # 区间标签
            interval_label = MathTex(f"[a_{i+1}, b_{i+1}]", color=color).scale(0.8)
            interval_label.next_to(interval, UP, buff=0.2)
            
            intervals.append(interval)
            interval_labels.append(interval_label)
            
            self.play(
                Create(interval),
                Create(left_point),
                Create(right_point),
                Write(left_label),
                Write(right_label),
                Write(interval_label),
                run_time=2
            )
            
            # 显示包含关系
            if i > 0:
                subset_symbol = MathTex(r"\subset", color=YELLOW).scale(0.6)
                subset_symbol.next_to(interval, LEFT, buff=0.2)
                
                left_proj = DashedLine(
                    axes.c2p(interval_data[i-1][0], y_positions[i-1]),
                    axes.c2p(interval_data[i-1][0], y_positions[i]),
                    color=YELLOW,
                    dash_length=0.1
                )
                right_proj = DashedLine(
                    axes.c2p(interval_data[i-1][1], y_positions[i-1]),
                    axes.c2p(interval_data[i-1][1], y_positions[i]),
                    color=YELLOW,
                    dash_length=0.1
                )
                self.play(
                    Create(left_proj),
                    Create(right_proj),
                    Write(subset_symbol),
                    run_time=1
                )

        # 第二步：先展示单调性
        monotone_arrows = VGroup()
        for i in range(len(interval_data)-1):
            # an的单调递增箭头
            a_monotone = Arrow(
                axes.c2p(interval_data[i][0], y_positions[i]),
                axes.c2p(interval_data[i+1][0], y_positions[i+1]),
                color=BLUE,
                buff=0.1,
                max_tip_length_to_length_ratio=0.15
            )
            # bn的单调递减箭头
            b_monotone = Arrow(
                axes.c2p(interval_data[i][1], y_positions[i]),
                axes.c2p(interval_data[i+1][1], y_positions[i+1]),
                color=RED,
                buff=0.1,
                max_tip_length_to_length_ratio=0.15
            )
            monotone_arrows.add(a_monotone, b_monotone)
        
        # 显示单调性标签（缩小并上移）
        monotone_labels = VGroup(
            VGroup(
                MathTex(r"\{a_n\}", color=BLUE),
                Text("单调递增有上界", font="SimSun")
            ).arrange(RIGHT, buff=0.1),
            VGroup(
                MathTex(r"\{b_n\}", color=RED),
                Text("单调递减有下界", font="SimSun")
            ).arrange(RIGHT, buff=0.1)
        ).arrange(DOWN, buff=0.2).scale(0.6)  # 缩小字体
        monotone_labels.to_edge(LEFT, buff=0.5).shift(UP * 1.5)  # 上移
        
        self.play(
            Write(monotone_labels),
            Create(monotone_arrows),
            run_time=3
        )
        
        # 定义极限点位置
        xi = 3.5  # 在这里定义xi
        
        # 然后展示收敛性
        # 显示an和bn的极限
        limit_arrows = VGroup()
        # an的极限箭头（向上）
        a_limit_arrow = Arrow(
            axes.c2p(interval_data[-1][0], y_positions[-1]),
            axes.c2p(xi, 3.2),
            color=BLUE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        # bn的极限箭头（向上）
        b_limit_arrow = Arrow(
            axes.c2p(interval_data[-1][1], y_positions[-1]),
            axes.c2p(xi, 3.2),
            color=RED,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        limit_arrows.add(a_limit_arrow, b_limit_arrow)

        # # 显示极限值标签
        # limit_labels = VGroup(
        #     MathTex(r"\lim_{n \to \infty} a_n = a", color=BLUE),
        #     MathTex(r"\lim_{n \to \infty} b_n = b", color=RED)
        # ).arrange(DOWN, buff=0.3).scale(0.8)
        # limit_labels.next_to(monotone_labels, DOWN, buff=0.5)

        # self.play(
        #     Create(limit_arrows),
        #     Write(limit_labels),
        #     run_time=2
        # )

        # # 显示收敛性标签（放在极限值标签下面）
        # convergence_label = MathTex(
        #     r"\lim_{n \to \infty}(b_n - a_n) = 0", 
        #     color=YELLOW
        # ).scale(0.8)
        # convergence_label.next_to(limit_labels, DOWN, buff=0.3)
        
        # self.play(
        #     Write(convergence_label),
        #     run_time=2
        # )

        # # 显示极限值相等（放在收敛性标签下面）
        # equals_label = MathTex(r"a = b = \xi", color=YELLOW).scale(0.8)
        # equals_label.next_to(convergence_label, DOWN, buff=0.3)

        # self.play(
        #     Write(equals_label),
        #     run_time=1.5
       # )

        # 1. 显示第n个区间
        final_interval = Line(
            axes.c2p(3.3, 3.2),
            axes.c2p(3.7, 3.2),
            color=GREEN,
            stroke_width=4
        )
        final_left_point = Dot(axes.c2p(3.3, 3.2), color=GREEN, radius=0.05)
        final_right_point = Dot(axes.c2p(3.7, 3.2), color=GREEN, radius=0.05)
        final_left_label = MathTex("a_n", color=GREEN).scale(0.7)
        final_right_label = MathTex("b_n", color=GREEN).scale(0.7)
        final_left_label.next_to(final_left_point, LEFT, buff=0.1)
        final_right_label.next_to(final_right_point, RIGHT, buff=0.1)
        
        self.play(
            Create(final_interval),
            Create(final_left_point),
            Create(final_right_point),
            Write(final_left_label),
            Write(final_right_label),
            run_time=2
        )

        # 显示a3到aN和b3到bN的箭头
        a3_to_aN = Arrow(
            axes.c2p(interval_data[-1][0], y_positions[-1]),  # 从a3
            axes.c2p(3.3, 3.2),  # 到aN
            color=BLUE,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        b3_to_bN = Arrow(
            axes.c2p(interval_data[-1][1], y_positions[-1]),  # 从b3
            axes.c2p(3.7, 3.2),  # 到bN
            color=RED,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(
            Create(a3_to_aN),
            Create(b3_to_bN),
            run_time=2
        )

        # 2. 显示极限值标签
        limit_labels = VGroup(
            MathTex(r"\lim_{n \to \infty} a_n = a", color=BLUE),
            MathTex(r"\lim_{n \to \infty} b_n = b", color=RED)
        ).arrange(DOWN, buff=0.3).scale(0.8)
        limit_labels.next_to(monotone_labels, DOWN, buff=0.5)

        self.play(Write(limit_labels), run_time=3)

        # 3. 显示极限点
        limit_point = Dot(axes.c2p(xi, 3.5), color=YELLOW, radius=0.08)
        limit_label = MathTex(r"\xi", color=YELLOW).scale(0.8)
        limit_label.next_to(limit_point, UP)
        
        vertical_line = DashedLine(
            axes.c2p(xi, y_positions[0]),
            axes.c2p(xi, 3.5),
            color=YELLOW,
            dash_length=0.1
        )
        
        self.play(
            Create(vertical_line),
            Create(limit_point),
            Write(limit_label),
            run_time=2
        )

        # 显示从aN,bN到极限点的箭头
        aN_to_xi = Arrow(
            axes.c2p(3.3, 3.2),  # 从aN
            axes.c2p(xi, 3.5),  # 到ξ
            color=BLUE_A,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        bN_to_xi = Arrow(
            axes.c2p(3.7, 3.2),  # 从bN
            axes.c2p(xi, 3.5),  # 到ξ
            color=RED_A,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        self.play(
            Create(aN_to_xi),
            Create(bN_to_xi),
            run_time=2
        )

        # 4. 显示收敛性和极限值相等
        convergence_label = MathTex(
            r"\lim_{n \to \infty}(b_n - a_n) = 0", 
            color=YELLOW
        ).scale(0.8)
        convergence_label.next_to(limit_labels, DOWN, buff=0.3)
        
        equals_label = MathTex(r"a = b = \xi", color=YELLOW).scale(0.8)
        equals_label.next_to(convergence_label, DOWN, buff=0.3)

        self.play(
            Write(convergence_label),
            run_time=3
        )
        self.play(
            Write(equals_label),
            run_time=2
        )

        # 5. 反证法演示
        eta = 4.2
        other_point = Dot(axes.c2p(eta, 3.5), color=RED, radius=0.08)
        other_label = MathTex(r"\eta", color=RED).scale(0.8)
        other_label.next_to(other_point, UP)
        
        self.play(
            Create(other_point),
            Write(other_label),
            run_time=2.5
        )

        # 显示η不等于极限点，加上"任意"的表述
        neq_label = MathTex(r"\forall \eta \neq \xi", color=RED).scale(0.8)  # 添加任意符号
        neq_label.next_to(other_point, RIGHT, buff=0.3)
        
        self.play(Write(neq_label), run_time=1.5)

        # 显示存在区间使得η不属于该区间
        notin_label = MathTex(r"\exists n: \eta \notin [a_n, b_n]", color=RED).scale(0.8)  # 添加存在符号
        notin_label.next_to(neq_label, RIGHT, buff=0.2)
        
        self.play(Write(notin_label), run_time=1.5)

        # 用垂直向下的箭头表示η不在区间内（加粗）
        down_arrow = Arrow(
            axes.c2p(eta, 3.5),
            axes.c2p(eta, 3.2),
            color=RED,
            buff=0.1,
            max_tip_length_to_length_ratio=0.2,
            stroke_width=6
        )
        
        self.play(Create(down_arrow), run_time=2)

        # 添加an, bn的向上虚线和延长线
        left_proj = DashedLine(
            axes.c2p(3.3, 3.2),  # 从an开始
            axes.c2p(3.3, 3.5),  # 向上延伸
            color=YELLOW,
            dash_length=0.1
        )
        right_proj = DashedLine(
            axes.c2p(3.7, 3.2),  # 从bn开始
            axes.c2p(3.7, 3.5),  # 向上延伸
            color=YELLOW,
            dash_length=0.1
        )
        right_extension = DashedLine(
            axes.c2p(3.7, 3.2),  # 从bn开始
            axes.c2p(4.5, 3.2),  # 向右延伸超过η
            color=GREEN_A,
            dash_length=0.1
        )
        
        self.play(
            Create(left_proj),
            Create(right_proj),
            Create(right_extension),
            run_time=2
        )

        # 显示矛盾（只显示叉号）
        x = Cross(scale_factor=0.25, stroke_width=6).move_to(other_point)  # 叉号保持在η点
        
        self.play(Create(x), run_time=1.5)
        
        self.wait(2)

        # 最后强调唯一性
        xi_label = MathTex(r"\xi", color=YELLOW).scale(0.8)
        unique_text = Text("唯一", font="SimSun", color=YELLOW).scale(0.7)
        
        # 将ξ和"唯一"水平排列
        unique_group = VGroup(xi_label, unique_text).arrange(RIGHT, buff=0.2)
        unique_group.next_to(notin_label, DOWN, buff=0.3)  # 放在不等式下方
        
        self.play(
            limit_point.animate.scale(1.5).set_color(YELLOW),
            limit_label.animate.scale(1.5).set_color(YELLOW),
            Write(unique_group),
            run_time=2.5
        )
        
        self.wait(5)  # 最后的等待时间

def main():
    import os
    os.system("manim -pql nested_interval_theorem.py NestedIntervalTheorem")

if __name__ == "__main__":
    main() 