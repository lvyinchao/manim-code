from manim import *
import numpy as np

class MonotoneBoundedTheorem(Scene):
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
                "include_numbers": False
            }
        )
        
        # 创建标题
        title = Text("确界原理证明单调有界原理", font="SimSun").scale(0.8).to_edge(UP)
        
        # 设置场景
        self.play(
            Write(title, run_time=2),
            Create(axes, run_time=2)
        )
        
        # 创建单调递增数列 an = 2 - 1/n
        n_values = np.linspace(1, 8, 40)  # 在1到8之间创建40个点
        points = [(n, 2 - 1/n) for n in n_values]
        dots = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE, radius=0.04)
            for x, y in points
        ])
        
        # 显示数列说明
        sequence_text = VGroup(
            Text("单调递增数列", font="SimSun", color=BLUE),
            MathTex(r"\{a_n\}", color=BLUE)
        ).arrange(RIGHT,buff=0.1).scale(0.6)
        sequence_text.next_to(title, DOWN)
        
        # 显示数列
        self.play(Write(sequence_text), run_time=1.5)
        
        # 逐个显示点
        for dot in dots:
            self.play(Create(dot), run_time=0.2)
        
        # 显示性质2：有界性
        property2 = VGroup(
            Text("数列有上界必有上确界", font="SimSun"),
            MathTex(r"\exists L, \forall n, a_n \leq L")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6).to_edge(LEFT, buff=0.5).shift(UP)
        
        self.play(Write(property2), run_time=2.5)
        
        # 显示上界L
        L = 2  # 上确界
        L_line = DashedLine(
            axes.c2p(0, L),
            axes.c2p(8, L),
            color=RED,
            dash_length=0.2
        )
        L_text = Text("L（上确界）", font="SimSun", color=RED).scale(0.6)
        L_text.next_to(L_line.get_end(), LEFT)
        
        self.play(
            Create(L_line),
            Write(L_text),
            run_time=2.5
        )
        
        # 显示证明过程
        proof = VGroup(
            Text("对任意ε>0，", font="SimSun"),
            Text("L-ε不是上界", font="SimSun", color=GREEN),
            Text("存在N，使得", font="SimSun"),
            MathTex(r"a_N > L-\varepsilon", color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6).to_edge(RIGHT, buff=0.5).shift(DOWN)
        
        self.play(Write(proof), run_time=3)
        
        # 演示ε-N语言
        epsilon = 0.2
        epsilon_line = DashedLine(
            axes.c2p(0, L-epsilon),
            axes.c2p(8, L-epsilon),
            color=GREEN,
            dash_length=0.2
        )
        epsilon_text = Text("L-ε", font="SimSun", color=GREEN).scale(0.6)
        epsilon_text.next_to(epsilon_line.get_end(), LEFT)
        
        self.play(
            Create(epsilon_line),
            Write(epsilon_text),
            run_time=2.5
        )
        
        # 标注N点
        N_index = next(i for i, p in enumerate(points) if p[1] > L-epsilon)
        N_point = points[N_index]
        N_dot = Dot(axes.c2p(N_point[0], N_point[1]), color=YELLOW, radius=0.1)
        N_text = Text("N", font="SimSun", color=YELLOW).scale(0.6)
        N_text.next_to(N_dot, DR)
        
        self.play(
            Create(N_dot),
            Write(N_text),
            run_time=2.5
        )
        
        # 显示性质1：单调性（移到N点显示之后）
        property1 = VGroup(
            Text("数列单调递增", font="SimSun"),
            MathTex(r"\forall n>N, a_n \geq a_N > L-\varepsilon", color=BLUE)
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.6).to_edge(LEFT, buff=0.5)
        
        property1.next_to(property2, DOWN, buff=0.5, aligned_edge=LEFT)
        
        self.play(Write(property1), run_time=2.5)
        
        # 标注N之后的点
        points_after_N = [(x, y) for x, y in points if x > N_point[0]]
        highlight_dots = VGroup(*[
            Dot(axes.c2p(x, y), color=YELLOW, radius=0.08, fill_opacity=0.8)
            for x, y in points_after_N
        ])
        
        # 显示动画
        self.play(
            *[dot.animate.set_color(YELLOW) for dot in highlight_dots],
            run_time=3
        )
        
        # 突出显示两条边界线
        self.play(
            epsilon_line.animate.set_color(YELLOW).set_stroke(width=3),
            L_line.animate.set_color(YELLOW).set_stroke(width=3),
            run_time=2.5
        )
        
        # 显示不等式链
        inequality_chain = VGroup(
            MathTex("L-\\varepsilon", color=GREEN),
            MathTex("<"),
            MathTex("a_n", color=BLUE),
            MathTex("\\leq"),
            MathTex("L", color=RED)
        ).arrange(RIGHT, buff=0.2).scale(0.8)
        
        inequality_chain.next_to(axes, DOWN, buff=0.15)
        
        self.play(Write(inequality_chain), run_time=3.5)
        
        # 显示结论
        conclusion = Text(
            "数列必定收敛于其上确界L",
            font="SimSun"
        ).scale(0.6).next_to(inequality_chain, DOWN, buff=0.15)
        
        self.play(Write(conclusion), run_time=3.5)
        
        self.wait(6)

def main():
    import os
    os.system("manim -pql monotone_bounded_theorem.py MonotoneBoundedTheorem")

if __name__ == "__main__":
    main() 