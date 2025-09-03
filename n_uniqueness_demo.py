from manim import *
import numpy as np

class NUniquenessDemo(Scene):
    def construct(self):
        # Set default font
        Text.set_default(font="SimSun")
        
        # Title
        title = Text("极限定义中N的不唯一性", font="SimSun").scale(0.5)  # 缩小标题
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(1)
        
        # Problem statement
        problem = MathTex(r"\lim_{n \to \infty} \frac{3n^2}{n^2 - 3} = 3").scale(0.8)  # 缩小题目
        problem.next_to(title, DOWN, buff=0.3)  # 上移一点
        
        self.play(Write(problem))
        self.wait(2)
        
        # Create axes for visualization
        axes = Axes(
            x_range=[0, 30, 5],
            y_range=[2, 4, 0.5],
            axis_config={"include_tip": True},
            x_length=8,  # 缩小图像
            y_length=4   # 缩小图像
        )
        axes.next_to(problem, DOWN, buff=0.3).shift(RIGHT * 1.5)  # 上移一点并右移一些
        
        # Labels for axes
        x_label = MathTex("n").next_to(axes.x_axis, RIGHT, buff=0.3)
        y_label = MathTex("f(n)").next_to(axes.y_axis, UP, buff=0.3)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # Function to plot
        def func(x):
            return 3 * x**2 / (x**2 - 3)
        
        # Plot points on the graph
        points = VGroup()
        x_values = range(2, 31)  # 正整数n从2到30
        for x in x_values:
            y = func(x)
            point = Dot(axes.c2p(x, y), color=BLUE, radius=0.05)
            points.add(point)
        
        graph_label = MathTex(r"f(n) = \frac{3n^2}{n^2 - 3}").next_to(axes.c2p(25, func(25)), UP, buff=0.2).scale(0.7).shift(LEFT * 1.5)  # 左移一些
        graph_label.set_color(BLUE)
        
        # Plot the limit line y = 3
        limit_line = axes.plot(lambda x: 3, x_range=[0, 30], color=GREEN)
        limit_label = MathTex("y = 3").next_to(limit_line.get_end(), DOWN, buff=0.2).scale(0.7)
        limit_label.set_color(GREEN)
        
        self.play(Create(points), Write(graph_label))
        self.play(Create(limit_line), Write(limit_label))
        self.wait(2)
        
        # Show epsilon band
        epsilon = 0.2
        upper_epsilon_line = axes.plot(lambda x: 3 + epsilon, x_range=[0, 30], color=RED)
        lower_epsilon_line = axes.plot(lambda x: 3 - epsilon, x_range=[0, 30], color=RED)
        
        upper_epsilon_label = MathTex(f"y = 3 + \\varepsilon = {3 + epsilon}").next_to(upper_epsilon_line.get_end(), UP, buff=0.1).scale(0.6)
        upper_epsilon_label.set_color(RED)
        lower_epsilon_label = MathTex(f"y = 3 - \\varepsilon = {3 - epsilon}").next_to(lower_epsilon_line.get_end(), DOWN, buff=0.1).scale(0.6)
        lower_epsilon_label.set_color(RED)
        
        # 显示epsilon值右移一个单位
        epsilon_label = MathTex(f"\\varepsilon = {epsilon}").next_to(axes, DOWN, buff=0.1).shift(UP*1.5 + LEFT*3)
        epsilon_label.set_color(RED)
        
        self.play(Create(upper_epsilon_line), Create(lower_epsilon_line))
        self.play(Write(upper_epsilon_label), Write(lower_epsilon_label), Write(epsilon_label))
        self.wait(2)
        
        # Calculate different N values 
        # Method 1: Standard calculation (N = ceil(sqrt(9/ε + 3)))
        N1_float = np.sqrt(9/epsilon + 3)
        N1 = int(np.ceil(N1_float))
        
        # Method 2: More conservative estimation
        N2_float = np.sqrt(18/epsilon)
        N2 = int(np.ceil(N2_float))
        # But we also need n ≥ 4 for our approximation, so take max(4, N2)
        N2 = max(4, N2)
        
        # Method 3: Even more conservative estimation
        N3_float = np.sqrt(13.5/epsilon)
        N3 = int(np.ceil(N3_float))
        # But we also need n ≥ 3 for our approximation, so take max(3, N3)
        N3 = max(3, N3)
        
        # Display derivation methods title
        derivation_title = Text("不同的N推导方法:", font="SimSun").scale(0.5)
        derivation_title.to_corner(UL, buff=0.5).shift(RIGHT*0.1)  # 整体左移0.4个单位（从0.5到0.1）
        
        self.play(Write(derivation_title))
        self.wait(1)
        
        # Method 1
        method1_title = Text("方法1: 基本方法", font="SimSun").scale(0.4)
        method1_derivation = MathTex(
            r"|f(n)-3| = \left|\frac{9}{n^2-3}\right| < \varepsilon \Rightarrow n > \sqrt{\frac{9}{\varepsilon}+3}"
        ).scale(0.5)
        method1_result = MathTex("N_1 = \\left\\lceil \\sqrt{\\frac{9}{\\varepsilon}+3} \\right\\rceil = ").scale(0.6)
        
        method1_group = VGroup(method1_title, method1_derivation, method1_result).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        method1_group.next_to(derivation_title, DOWN, buff=0.3).scale(0.8).shift(RIGHT*0.1)  # 整体左移0.4个单位
        
        self.play(Write(method1_title))
        self.play(Write(method1_derivation))
        self.wait(2)
        
        # Show N1 result
        method1_result_N = MathTex(str(N1)).scale(0.6).next_to(method1_result, RIGHT, buff=0.1)
        
        self.play(Write(method1_result))
        self.wait(1)
        self.play(Write(method1_result_N))  # N1结果晚1秒显示
        self.wait(1)
        
        # Show N1 on graph
        n1_line = axes.get_vertical_line(
            axes.c2p(N1, 0),
            line_config={"color": YELLOW, "stroke_width": 4}
        )
        
        n1_label = MathTex(f"N_1 = {N1}").next_to(n1_line, UP, buff=0.1).scale(0.6)
        n1_label.set_color(YELLOW)
        
        # Create a dotted vertical line spanning the entire y-range
        n1_dotted_line = DashedLine(
            start=axes.c2p(N1, axes.get_y_range()[0]),
            end=axes.c2p(N1, axes.get_y_range()[1]),
            color=YELLOW,
            stroke_width=2,
            dash_length=0.1
        )
        
        self.play(Create(n1_dotted_line), run_time=0.5)
        self.play(Create(n1_line), Write(n1_label), run_time=0.5)
        self.wait(1)
        
        # Highlight points for N1
        highlight_points1 = VGroup()
        for x in x_values:
            if x > N1:
                y = func(x)
                point = Dot(axes.c2p(x, y), color=YELLOW, radius=0.07)
                highlight_points1.add(point)
        
        self.play(Create(highlight_points1), run_time=1.5)
        self.wait(2)
        
        # Method 2: Different estimation technique
        method2_title = Text("方法2: 不同放大技巧（n>3时）", font="SimSun").scale(0.4)
        method2_derivation = MathTex(
            r"n^2-3 \geq \frac{n^2}{2} \Rightarrow |f(n)-3| \leq \frac{18}{n^2} < \varepsilon \Rightarrow n > \sqrt{\frac{18}{\varepsilon}}"
        ).scale(0.5)
        
        method2_group = VGroup(method2_title, method2_derivation).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        method2_group.next_to(method1_group, DOWN, buff=0.3).scale(0.8).shift(RIGHT*0.2)  # 整体右移0.1个单位（从0.1到0.2）
        
        self.play(Write(method2_title))
        self.play(Write(method2_derivation))
        self.wait(2)
        
        # Show N2 result
        method2_result = MathTex("N_2 = \\max(3, \\left\\lceil \\sqrt{\\frac{18}{\\varepsilon}} \\right\\rceil) = ").scale(0.6)
        method2_result_N = MathTex(str(N2)).scale(0.6).next_to(method2_result, RIGHT, buff=0.1)
        method2_result.next_to(method2_group, DOWN, buff=0.2).shift(RIGHT*0.2)  # 整体右移0.1个单位
        method2_result_N.next_to(method2_result, RIGHT, buff=0.1)
        
        self.play(Write(method2_result))
        self.wait(1)
        self.play(Write(method2_result_N))  # N2结果晚1秒显示
        self.wait(0.5)
        
        # Show N2 on graph
        n2_line = axes.get_vertical_line(
            axes.c2p(N2, 0),
            line_config={"color": ORANGE, "stroke_width": 4}
        )
        
        n2_label = MathTex(f"N_2 = {N2}").next_to(n2_line, UP, buff=0.1).scale(0.6).shift(DOWN*0.3)  # N2标签下移
        n2_label.set_color(ORANGE)
        
        # Create a dotted vertical line spanning the entire y-range
        n2_dotted_line = DashedLine(
            start=axes.c2p(N2, axes.get_y_range()[0]),
            end=axes.c2p(N2, axes.get_y_range()[1]),
            color=ORANGE,
            stroke_width=2,
            dash_length=0.1
        )
        
        self.play(Create(n2_dotted_line), run_time=0.5)
        self.play(Create(n2_line), Write(n2_label), run_time=0.5)
        self.wait(0.5)
        
        # Highlight points for N2
        highlight_points2 = VGroup()
        for x in x_values:
            if x > N2:
                y = func(x)
                point = Dot(axes.c2p(x, y), color=ORANGE, radius=0.07)
                highlight_points2.add(point)
        
        self.play(Create(highlight_points2), run_time=1.5)
        self.wait(2)
        
        # Method 3: Another estimation technique
        method3_title = Text("方法3: 另一种放大技巧（n>3时）", font="SimSun").scale(0.4)
        method3_derivation = MathTex(
            r"n^2-3 \geq \frac{2n^2}{3} \Rightarrow |f(n)-3| \leq \frac{13.5}{n^2} < \varepsilon \Rightarrow n > \sqrt{\frac{13.5}{\varepsilon}}"
        ).scale(0.5)
        
        method3_group = VGroup(method3_title, method3_derivation).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        method3_group.next_to(method2_result, DOWN, buff=0.3).scale(0.8).shift(RIGHT*0.2)  # 整体右移0.1个单位（从0.1到0.2）
        
        self.play(Write(method3_title))
        self.play(Write(method3_derivation))
        self.wait(2)
        
        # Show N3 result
        method3_result = MathTex("N_3 = \\max(3, \\left\\lceil \\sqrt{\\frac{13.5}{\\varepsilon}} \\right\\rceil) = ").scale(0.6)
        method3_result_N = MathTex(str(N3)).scale(0.6).next_to(method3_result, RIGHT, buff=0.1)
        method3_result.next_to(method3_group, DOWN, buff=0.2).shift(RIGHT*0.2)  # 整体右移0.1个单位
        method3_result_N.next_to(method3_result, RIGHT, buff=0.1)
        
        self.play(Write(method3_result))
        self.wait(1)
        self.play(Write(method3_result_N))  # N3结果晚1秒显示
        self.wait(0.5)
        
        # Show N3 on graph
        n3_line = axes.get_vertical_line(
            axes.c2p(N3, 0),
            line_config={"color": PURPLE, "stroke_width": 4}
        )
        
        n3_label = MathTex(f"N_3 = {N3}").next_to(n3_line, UP, buff=0.1).scale(0.6).shift(DOWN*0.5)  # N3标签进一步下移
        
        n3_label.set_color(PURPLE)
        
        # Create a dotted vertical line spanning the entire y-range
        n3_dotted_line = DashedLine(
            start=axes.c2p(N3, axes.get_y_range()[0]),
            end=axes.c2p(N3, axes.get_y_range()[1]),
            color=PURPLE,
            stroke_width=2,
            dash_length=0.1
        )
        
        self.play(Create(n3_dotted_line), run_time=0.5)
        self.play(Create(n3_line), Write(n3_label), run_time=0.5)
        self.wait(1)
        
        # Highlight points for N3
        highlight_points3 = VGroup()
        for x in x_values:
            if x > N3:
                y = func(x)
                point = Dot(axes.c2p(x, y), color=PURPLE, radius=0.07)
                highlight_points3.add(point)
        
        self.play(Create(highlight_points3), run_time=1.5)
        self.wait(2)
        
        # Conclusion text at the bottom center
        conclusion = Text(
            "通过不同的不等式放大技巧，可以得到不同的N值",
            font="SimSun"
        ).scale(0.6).to_edge(DOWN, buff=0.5).shift(RIGHT*2)  # 结论右移两个单位
        
        self.play(Write(conclusion))
        self.wait(3)

def main():
    scene = NUniquenessDemo()
    scene.render()

if __name__ == "__main__":
    main()