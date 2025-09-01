from manim import *
import numpy as np

class EpsilonNVisualization(Scene):
    def construct(self):
        # Set default font
        Text.set_default(font="SimSun")
        
        # Title
        title = Text("极限的 ε-N 定义可视化", font="SimSun").scale(0.6)  # 缩小标题字体
        title.to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.wait(1)
        
        # Fade out title
        self.play(FadeOut(title))
        
        # Problem statement with mathematical notation
        problem = MathTex(r"\lim_{n \to \infty} \frac{3n^2}{n^2 - 3} = 3").scale(1.0)  # 缩小题目字体
        problem.to_edge(UP, buff=0.3)
        
        self.play(Write(problem))
        self.wait(2)
        
        # Create axes for visualization
        axes = Axes(
            x_range=[0, 25, 5],
            y_range=[2, 4, 0.5],
            axis_config={"include_tip": True},
            x_length=8,  # 缩小图像宽度
            y_length=4   # 缩小图像高度
        )
        axes.next_to(problem, DOWN, buff=0.5)  # 下移一点点动画
        
        # Labels for axes
        x_label = MathTex("n").next_to(axes.x_axis, RIGHT, buff=0.3)
        y_label = MathTex("f(n)").next_to(axes.y_axis, UP, buff=0.3)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # Function to plot
        def func(x):
            return 3 * x**2 / (x**2 - 3)
        
        # 先显示数列散点图，按照n为正整数取值绘制点
        points = VGroup()
        x_values = range(2, 26)  # 正整数n从2到25
        for x in x_values:
            y = func(x)
            point = Dot(axes.c2p(x, y), color=BLUE, radius=0.05)
            points.add(point)
        
        graph_label = MathTex(r"f(n) = \frac{3n^2}{n^2 - 3}").next_to(axes.c2p(20, func(20)), UP, buff=0.2).scale(0.7)
        graph_label.set_color(BLUE)
        
        # Plot the limit line y = 3
        limit_line = axes.plot(lambda x: 3, x_range=[0, 25], color=GREEN)
        limit_label = MathTex("y = 3").next_to(limit_line.get_end(), DOWN, buff=0.2).scale(0.7)
        limit_label.set_color(GREEN)
        
        self.play(Create(points), Write(graph_label))
        self.play(Create(limit_line), Write(limit_label))
        self.wait(2)
        
        # 然后显示N的推导过程
        # 添加一般形式的推导过程
        derivation_title = Text("N 的一般形式推导过程:", font="SimSun").scale(0.4)  # 缩小字体
        derivation_title.to_corner(UL, buff=0.3)  # 调整位置
        derivation_title.shift(DOWN * 1.2)  # 下移一点点
        
        derivation_step1 = MathTex(r"|f(n) - 3| = \left|\frac{9}{n^2 - 3}\right|").scale(0.4)  # 缩小字体
        derivation_step2_part1 = Text("当", font="SimSun").scale(0.4)
        derivation_step2_part2 = MathTex(r"n > \sqrt{3}").scale(0.4)
        derivation_step2_part3 = Text("时", font="SimSun").scale(0.4)
        derivation_step2_part4 = MathTex(r"\frac{9}{n^2 - 3} < \varepsilon").scale(0.4)
        
        # 组合 derivation_step2
        derivation_step2 = VGroup(derivation_step2_part1, derivation_step2_part2, derivation_step2_part3, derivation_step2_part4)
        derivation_step2.arrange(RIGHT, buff=0.1)
        
        derivation_step3 = MathTex(r"n^2 - 3 > \frac{9}{\varepsilon}").scale(0.4)  # 缩小字体
        derivation_step4 = MathTex(r"n^2 > \frac{9}{\varepsilon} + 3").scale(0.4)  # 缩小字体
        derivation_step5 = MathTex(r"n > \sqrt{\frac{9}{\varepsilon} + 3}").scale(0.4)  # 缩小字体
        
        derivation_step6_part1 = Text("因此", font="SimSun").scale(0.4)
        derivation_step6_part2 = MathTex(r"N = \left\lceil \sqrt{\frac{9}{\varepsilon} + 3} \right\rceil").scale(0.4)
        
        # 组合 derivation_step6
        derivation_step6 = VGroup(derivation_step6_part1, derivation_step6_part2)
        derivation_step6.arrange(RIGHT, buff=0.1)
        
        derivation_group = VGroup(derivation_title, derivation_step1, derivation_step2, derivation_step3, derivation_step4, derivation_step5, derivation_step6)
        derivation_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)  # 减小行间距
        derivation_group.to_corner(UL, buff=0.3)  # 调整位置
        derivation_group.shift(DOWN * 1.2)  # 下移一点点
        
        self.play(Write(derivation_title))
        self.wait(1)
        self.play(Write(derivation_step1))
        self.wait(1)
        self.play(Write(derivation_step2_part1), Write(derivation_step2_part2), Write(derivation_step2_part3), Write(derivation_step2_part4))
        self.wait(1)
        self.play(Write(derivation_step3))
        self.wait(1)
        self.play(Write(derivation_step4))
        self.wait(1)
        self.play(Write(derivation_step5))
        self.wait(1)
        self.play(Write(derivation_step6_part1), Write(derivation_step6_part2))
        self.wait(2)
        
        # Show different epsilon values and corresponding N calculations
        epsilons = [0.5, 0.15]
        colors = [RED, ORANGE]
        highlight_colors = [YELLOW, PURPLE]
        
        for i, (epsilon, color, highlight_color) in enumerate(zip(epsilons, colors, highlight_colors)):
            # Calculate N for this epsilon
            N_float = np.sqrt(9/epsilon + 3)
            N = int(np.ceil(N_float))  # Take the ceiling of N
            
            # 将N具体数值的计算移到右上角
            if i == 0:
                # For first epsilon, show full calculation
                n_value_title = Text(f"当ε = {epsilon}时:", font="SimSun").scale(0.4)  # 缩小字体
                n_value_title.to_corner(UR, buff=0.3)  # 调整位置到右上角
                n_value_title.shift(DOWN * 0.5)  # 下移一点点
                
                n_value_step1 = MathTex(f"N = \\left\\lceil \\sqrt{{\\frac{{9}}{{{epsilon}}} + 3}} \\right\\rceil").scale(0.5)  # 缩小字体
                n_value_step2 = MathTex(f"N = \\left\\lceil {N_float:.2f} \\right\\rceil = {N}").scale(0.5)  # 缩小字体
                
                n_value_group = VGroup(n_value_title, n_value_step1, n_value_step2)
                n_value_group.arrange(DOWN, aligned_edge=LEFT, buff=0.1)  # 减小行间距
                n_value_group.to_corner(UR, buff=0.3)  # 调整位置到右上角
                n_value_group.shift(DOWN * 0.5)  # 下移一点点
                
                self.play(Write(n_value_title))
                self.play(Write(n_value_step1))
                self.wait(0.5)
                self.play(Write(n_value_step2))
                self.wait(1)
                
                n_value_group_prev = n_value_group
            else:
                # For second epsilon, just show the result
                n_result_part1 = Text("当", font="SimSun").scale(0.4)
                n_result_part2 = MathTex(r"\varepsilon").scale(0.4)
                n_result_part3 = Text(f"= {epsilon}时，N = {N}", font="SimSun").scale(0.4)
                
                n_result = VGroup(n_result_part1, n_result_part2, n_result_part3)
                n_result.arrange(RIGHT, buff=0.1)
                n_result.to_corner(UR, buff=0.3)  # 调整位置到右上角
                n_result.shift(DOWN * 0.5)  # 下移一点点
                
                self.play(Transform(n_value_group_prev, n_result))
                self.wait(2)
            
            # 最后显示y=3+epsilon和y=3-epsilon的直线
            upper_epsilon_line = axes.plot(lambda x: 3 + epsilon, x_range=[0, 25], color=color)
            lower_epsilon_line = axes.plot(lambda x: 3 - epsilon, x_range=[0, 25], color=color)
            
            upper_epsilon_label = MathTex(f"y = 3 + \\varepsilon = {3 + epsilon}").next_to(upper_epsilon_line.get_end(), UP, buff=0.1).scale(0.6)
            upper_epsilon_label.set_color(color)
            lower_epsilon_label = MathTex(f"y = 3 - \\varepsilon = {3 - epsilon}").next_to(lower_epsilon_line.get_end(), DOWN, buff=0.1).scale(0.6)
            lower_epsilon_label.set_color(color)
            
            if i == 0:
                # Show epsilon lines and labels
                self.play(Create(upper_epsilon_line), Create(lower_epsilon_line))
                self.play(Write(upper_epsilon_label), Write(lower_epsilon_label))
                self.wait(2)
            else:
                # Transform to new epsilon lines
                self.play(
                    Transform(upper_epsilon_line_prev, upper_epsilon_line),
                    Transform(lower_epsilon_line_prev, lower_epsilon_line),
                    Transform(upper_epsilon_label_prev, upper_epsilon_label),
                    Transform(lower_epsilon_label_prev, lower_epsilon_label)
                )
                self.wait(2)
            
            # Store references for next iteration
            upper_epsilon_line_prev = upper_epsilon_line
            lower_epsilon_line_prev = lower_epsilon_line
            upper_epsilon_label_prev = upper_epsilon_label
            lower_epsilon_label_prev = lower_epsilon_label
            
            # 2. Then show the absolute value |f(n) - 3|
            if i == 0:
                # Create a vertical brace between the epsilon lines in the middle of the graph, on the left side
                epsilon_brace = BraceBetweenPoints(
                    axes.c2p(10, 3 + epsilon),
                    axes.c2p(10, 3 - epsilon),
                    color=color,
                    direction=LEFT  # Point brace to the left
                )
                epsilon_condition = MathTex(f"|f(n) - 3| < \\varepsilon = {epsilon}").scale(0.7)
                epsilon_condition.next_to(epsilon_brace, LEFT, buff=0.2)
                epsilon_condition.set_color(color)
                
                self.play(Create(epsilon_brace), Write(epsilon_condition))
                epsilon_brace_prev = epsilon_brace
                epsilon_condition_prev = epsilon_condition
                self.wait(2)
            else:
                # Update epsilon condition
                new_epsilon_brace = BraceBetweenPoints(
                    axes.c2p(10, 3 + epsilon),
                    axes.c2p(10, 3 - epsilon),
                    color=color,
                    direction=LEFT  # Point brace to the left
                )
                new_epsilon_condition = MathTex(f"|f(n) - 3| < \\varepsilon = {epsilon}").scale(0.7)
                new_epsilon_condition.next_to(new_epsilon_brace, LEFT, buff=0.2)
                new_epsilon_condition.set_color(color)
                
                self.play(
                    Transform(epsilon_brace_prev, new_epsilon_brace),
                    Transform(epsilon_condition_prev, new_epsilon_condition)
                )
                self.wait(2)
            
            # Draw vertical line at N
            N_line = axes.get_vertical_line(
                axes.c2p(N, 0),
                line_config={"color": highlight_color, "stroke_width": 4}
            )
            N_label = MathTex(f"N = {N}").next_to(N_line, UP, buff=0.1).scale(0.7)
            N_label.set_color(highlight_color)
            
            # Create a dotted vertical line spanning the entire y-range for better visibility
            N_dotted_line = DashedLine(
                start=axes.c2p(N, axes.get_y_range()[0]),
                end=axes.c2p(N, axes.get_y_range()[1]),
                color=highlight_color,
                stroke_width=2,
                dash_length=0.1
            )
            
            if i == 0:
                # Show N line
                self.play(Create(N_dotted_line))
                self.play(Create(N_line), Write(N_label))
                self.wait(1)
                
                # Store references
                N_line_prev = N_line
                N_label_prev = N_label
                N_dotted_line_prev = N_dotted_line
            else:
                # Move N line to new position
                self.play(
                    Transform(N_dotted_line_prev, N_dotted_line),
                    Transform(N_line_prev, N_line),
                    Transform(N_label_prev, N_label)
                )
                self.wait(1)
            
            # 高亮满足条件的点
            highlight_points = VGroup()
            for x in x_values:
                if x > N:
                    y = func(x)
                    point = Dot(axes.c2p(x, y), color=highlight_color, radius=0.07)
                    highlight_points.add(point)
            
            if i == 0:
                # Show highlight
                self.play(Create(highlight_points))
                highlight_points_prev = highlight_points
                self.wait(2)
            else:
                # Update highlight
                self.play(Transform(highlight_points_prev, highlight_points))
                self.wait(2)
        
        # Show the relationship between epsilon and N
        relationship = MathTex(
            "\\varepsilon \\downarrow \\quad \\Rightarrow \\quad N \\uparrow",
            color=YELLOW
        ).scale(1.0)  # 缩小字体
        relationship.to_edge(DOWN, buff=0.7)  # 下移一点点
        
        self.play(Write(relationship))
        self.wait(2)
        
        # Final conclusion
        conclusion = Text(
            "当ε减小时，满足条件的N必须增大，这体现了极限的ε-N定义本质",
            font="SimSun"
        ).scale(0.5)  # 缩小字体
        conclusion.next_to(relationship, DOWN, buff=0.3)  # 调整位置和间距
        
        self.play(Write(conclusion))
        self.wait(3)

def main():
    scene = EpsilonNVisualization()
    scene.render()

if __name__ == "__main__":
    main()