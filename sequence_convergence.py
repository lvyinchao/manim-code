from manim import *
import numpy as np

class SequenceConvergence(Scene):
    def construct(self):
        # 创建标题
        title = Text("数列的收敛性演示", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[0, 20, 5],
            y_range=[-0.5, 2, 0.5],
            axis_config={"color": GREY},
            x_length=10,
            y_length=6
        ).shift(DOWN * 0.2)
        
        axes_labels = axes.get_axis_labels(
            x_label="n",
            y_label="a_n"
        )

        self.play(Create(axes), Write(axes_labels))
        self.wait(1)

        # 创建收敛数列 an = 1 + 1/n
        def converge_seq(n):
            return 1 + 1/n if n > 0 else 2

        converge_points = [axes.c2p(n, converge_seq(n)) for n in range(1, 21)]
        converge_dots = VGroup(*[Dot(point, color=BLUE) for point in converge_points])
        
        # 创建连线
        converge_lines = VMobject(color=BLUE_A, stroke_width=2)
        converge_lines.set_points_smoothly(converge_points)

        converge_label = MathTex(
            r"a_n",
            color=BLUE
        ).scale(0.8).to_edge(UP, buff=1.5).to_edge(RIGHT, buff=1.0)

        # 创建振荡数列 bn = (-1)^n/n + 1
        def oscillate_seq(n):
            return (-1)**n/n + 1 if n > 0 else 1.5

        oscillate_points = [axes.c2p(n, oscillate_seq(n)) for n in range(1, 21)]
        oscillate_dots = VGroup(*[Dot(point, color=RED) for point in oscillate_points])
        
        oscillate_lines = VMobject(color=RED_A, stroke_width=2)
        oscillate_lines.set_points_as_corners(oscillate_points)

        oscillate_label = MathTex(
            r"b_n",
            color=RED
        ).scale(0.8).next_to(converge_label, DOWN, buff=0.3)

        # 显示收敛数列
        self.play(Write(converge_label))
        for i in range(len(converge_dots)):
            self.play(
                Create(converge_dots[i]),
                Create(converge_lines) if i == len(converge_dots)-1 else Wait(),
                run_time=0.2
            )
        self.wait(1)

        # 显示振荡数列
        self.play(Write(oscillate_label))
        for i in range(len(oscillate_dots)):
            self.play(
                Create(oscillate_dots[i]),
                Create(oscillate_lines) if i == len(oscillate_dots)-1 else Wait(),
                run_time=0.2
            )
        self.wait(1)

        # 添加极限线
        limit_line = DashedLine(
            axes.c2p(0, 1),
            axes.c2p(20, 1),
            color=YELLOW
        )
        limit_label = MathTex(
            r"\lim_{n \to \infty} a_n = \lim_{n \to \infty} b_n = a", 
            color=YELLOW
        ).next_to(limit_line, RIGHT, buff=0.2).shift(DOWN * 1 + LEFT * 5)

        self.play(
            Create(limit_line),
            Write(limit_label)
        )
        self.wait(1)

        # 创建动态ε带和N标注的更新函数
        def update_epsilon_band(epsilon_val):
            # 更新ε带
            upper_line = DashedLine(
                axes.c2p(0, 1 + epsilon_val),
                axes.c2p(20, 1 + epsilon_val),
                color=GREEN_A
            )
            middle_line = DashedLine(  # 添加中间线
                axes.c2p(0, 1),
                axes.c2p(20, 1),
                color=YELLOW,
                dash_length=0.1
            )
            lower_line = DashedLine(
                axes.c2p(0, 1 - epsilon_val),
                axes.c2p(20, 1 - epsilon_val),
                color=GREEN_A
            )
            
            # 添加标注
            upper_label = MathTex(r"a+\varepsilon", color=GREEN_A).next_to(
                axes.c2p(0, 1 + epsilon_val), LEFT
            )
            middle_label = MathTex(r"a", color=YELLOW).next_to(
                axes.c2p(0, 1), LEFT
            )
            lower_label = MathTex(r"a-\varepsilon", color=GREEN_A).next_to(
                axes.c2p(0, 1 - epsilon_val), LEFT
            )
            
            epsilon_brace = BraceBetweenPoints(
                axes.c2p(19, 1 + epsilon_val),
                axes.c2p(19, 1 - epsilon_val),
                color=GREEN_A,
                direction=RIGHT
            )
            epsilon_text = MathTex(r"2\varepsilon", color=GREEN_A).next_to(epsilon_brace, RIGHT)

            # 计算对应的N值
            # 对于an = 1 + 1/n，要使|an - 1| < ε，需要n > 1/ε
            N_value = max(5, int(1/epsilon_val))

            # 添加N处的垂直虚线
            N_line = DashedLine(
                axes.c2p(N_value, 0),
                axes.c2p(N_value, 2),  # 延伸到足够高
                color=GREEN,
                dash_length=0.1
            )

            # 简化N标签
            N_arrow = Arrow(
                axes.c2p(N_value, -0.3),
                axes.c2p(N_value, 0),
                color=GREEN,
                buff=0
            )
            N_label = MathTex(r"N", color=GREEN).next_to(N_arrow, DOWN)

            return VGroup(
                upper_line, middle_line, lower_line,
                upper_label, middle_label, lower_label,
                epsilon_brace, epsilon_text,
                N_line, N_arrow, N_label
            )

        # 创建动画序列
        epsilon_values = [0.5, 0.3, 0.2, 0.1]
        epsilon_bands = []
        
        # 显示初始ε带
        current_band = update_epsilon_band(epsilon_values[0])
        self.play(Create(current_band))
        self.wait(1)

        # 动态更新ε带和N
        for i in range(1, len(epsilon_values)):
            new_band = update_epsilon_band(epsilon_values[i])
            self.play(
                ReplacementTransform(current_band, new_band),
                run_time=2
            )
            current_band = new_band
            self.wait(1)

        # 修改解释文本的位置和大小
        explanation = Text(
            "数列收敛的定义：\n" + 
            "∀ε>0, ∃N>0, 当n>N时，" +
            "|an-a| < ε" +
            "其中a是数列的极限。" +
            "注意：ε越小，N越大",
            font="SimSun",
            font_size=22,  # 稍微减小字体
            line_spacing=1.1  # 稍微减小行距
        ).next_to(
            axes,  # 只相对于坐标系定位，不包括current_band
            DOWN,
            buff=0.3  # 减小间距
        ).align_to(axes, LEFT).shift(UP * 0.5)  # 整体上移一点

        # 创建背景矩形，确保文字清晰可见
        explanation_bg = BackgroundRectangle(
            explanation,
            color=BLACK,
            fill_opacity=0.8,
            buff=0.2
        )

        # 先显示背景，再显示文字
        self.play(
            FadeIn(explanation_bg),
            Write(explanation)
        )
        self.wait(2)
def main():
    import os
    os.system("manim -pqh sequence_convergence.py SequenceConvergence")

if __name__ == "__main__":
    main() 