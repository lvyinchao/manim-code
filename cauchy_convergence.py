from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class CauchyConvergence(Scene):
    def construct(self):
        # 创建标题
        title = Text("柯西收敛原理演示", font="STSong", font_size=48)
        
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建坐标系
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 1.2, 0.2],
            axis_config={"include_tip": True},
            x_length=10,
            y_length=6
        )
        
        x_label = axes.get_x_axis_label("n")
        y_label = axes.get_y_axis_label("a_n")
        
        self.play(Create(axes), Write(x_label), Write(y_label))

        # 创建数列点
        def get_points(n_points):
            return [axes.coords_to_point(x, 1/x) for x in range(1, n_points + 1)]

        dots = VGroup(*[Dot(point) for point in get_points(10)])
        
        # 显示点
        self.play(Create(dots))
        self.wait(1)

        # 演示柯西条件
        # 先创建柯西条件的数学表达式
        cauchy_condition = MathTex(
            r"\forall \varepsilon > 0, \exists N \in \mathbb{N}, ",
            r"\forall n,m > N: |a_n - a_m| < \varepsilon"
        ).scale(0.8)
        # 将表达式移到右上角
        cauchy_condition.to_corner(UR)
        self.play(Write(cauchy_condition))
        
        # 创建说明文字（在循环外创建）
        explanation = Text(
            "N之后任意两项差的绝对值不会超过ε",
            font="STSong",
            color=YELLOW
        ).scale(0.4)
        # 将说明文字固定在上方位置
        explanation.to_edge(UP).shift(DOWN * 2)

        # 依次演示不同的ε值
        for i, epsilon in enumerate([0.3, 0.2, 0.1]):
            N = int(1/epsilon) - 1
            min_y = 1/(N+5)  # N之后某个点的y值
            max_y = 1/N      # N处的y值
            reference_y = (max_y + min_y) / 2
            
            # 创建两条水平线，确保包含曲线，并延长到整个x轴范围
            upper_line = DashedLine(
                axes.coords_to_point(0, max_y + epsilon/4),
                axes.coords_to_point(10, max_y + epsilon/4),
                color=RED
            )
            lower_line = DashedLine(
                axes.coords_to_point(0, min_y - epsilon/4),
                axes.coords_to_point(10, min_y - epsilon/4),
                color=RED
            )
            
            # 添加竖直的距离标注（移到右侧）
            distance_line = Line(
                axes.coords_to_point(9.5, max_y + epsilon/4),
                axes.coords_to_point(9.5, min_y - epsilon/4),
                color=RED
            )
            epsilon_brace = Brace(distance_line, direction=RIGHT, color=RED)
            epsilon_label = MathTex(r"\varepsilon", color=RED).next_to(epsilon_brace, RIGHT)
            
            epsilon_band = VGroup(
                upper_line, lower_line,
                distance_line, epsilon_brace, epsilon_label
            )
            
            self.play(
                Create(upper_line),
                Create(lower_line),
                Create(distance_line),
                Create(epsilon_brace),
                Write(epsilon_label)
            )
            
            # 创建N的垂直线
            N_line = DashedLine(
                axes.coords_to_point(N, 0),
                axes.coords_to_point(N, 1.2),
                color=GREEN
            )
            # 将N的标注移到下方
            N_text = Text("N", font="STSong", color=GREEN).next_to(
                axes.coords_to_point(N, 0),
                DOWN
            )
            
            # 显示N线
            self.play(
                Create(N_line),
                Write(N_text)
            )

            # 在N显示后再显示说明文字
            if i == 0:
                self.play(Write(explanation))
            
            self.wait(1.5)
            
            # 清除当前ε的演示内容
            self.play(
                FadeOut(epsilon_band),
                FadeOut(N_line),
                FadeOut(N_text)
            )

        # 显示极限存在的结论
        limit_text = VGroup(
            MathTex(r"\lim_{n \to \infty} a_n"),
            Text("存在", font="STSong", color=WHITE).scale(0.8)
        ).arrange(RIGHT, buff=0.2)
        # 将结论放在定理下方
        limit_text.next_to(cauchy_condition, DOWN, buff=0.5)
        self.play(Write(limit_text))
        self.wait(2)

def main():
    import os
    os.system("manim -pql cauchy_convergence.py CauchyConvergence")

if __name__ == "__main__":
    main() 