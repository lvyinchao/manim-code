from manim import *
import numpy as np

class LimitProofVisualization(Scene):
    def construct(self):
        # Set default font
        Text.set_default(font="SimSun")
        
        # Title
        title = Text("极限证明可视化: ε-N 定义", font="SimSun").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Show the limit we want to prove
        limit_eq = MathTex(r"\lim_{n \to \infty} \frac{3n^2}{n^2 - 3} = 3").scale(1.2)
        limit_eq.next_to(title, DOWN, buff=1)
        self.play(Write(limit_eq))
        self.wait(2)
        
        # Fade out limit equation
        self.play(FadeOut(limit_eq))
        
        # Show what we need to prove: |f(n) - 3| < ε
        statement = MathTex(r"\left| \frac{3n^2}{n^2 - 3} - 3 \right| < \varepsilon").scale(1.2)
        statement.next_to(title, DOWN, buff=1)
        self.play(Write(statement))
        self.wait(2)
        
        # Transform to simplified form
        simplified = MathTex(r"\frac{9}{n^2 - 3} < \varepsilon").scale(1.2)
        simplified.next_to(title, DOWN, buff=1)
        self.play(Transform(statement, simplified))
        self.wait(2)
        
        # Show the process of finding N
        self.play(FadeOut(statement))
        
        # Create axes for visualization
        axes = Axes(
            x_range=[0, 20, 2],
            y_range=[0, 5, 1],
            axis_config={"include_tip": True},
            x_length=8,
            y_length=5
        )
        axes.next_to(title, DOWN, buff=1.5)
        
        # Labels for axes
        x_label = MathTex("n").next_to(axes.x_axis, RIGHT)
        y_label = MathTex(r"|f(n) - 3|").next_to(axes.y_axis, UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # Function to plot: 9/(n^2 - 3)
        def func(n):
            return 9 / (n**2 - 3) if n**2 > 3 else 5  # Avoid division by zero or negative
        
        # Plot the function
        graph = axes.plot(func, x_range=[2, 19, 0.1], color=BLUE)
        graph_label = MathTex(r"\frac{9}{n^2 - 3}").next_to(graph, UP, buff=0.2).scale(0.7)
        self.play(Create(graph), Write(graph_label))
        self.wait(2)
        
        # Show different epsilon values and corresponding N
        epsilons = [1.0, 0.5, 0.1]
        colors = [RED, GREEN, YELLOW]
        
        for i, (epsilon, color) in enumerate(zip(epsilons, colors)):
            # Draw epsilon line
            epsilon_line = axes.get_horizontal_line(
                axes.c2p(0, epsilon),
                line_config={"color": color, "stroke_width": 2}
            )
            epsilon_label = MathTex(f"\\varepsilon = {epsilon}").next_to(epsilon_line, RIGHT, buff=0.1).scale(0.7)
            epsilon_label.set_color(color)
            
            self.play(Create(epsilon_line), Write(epsilon_label))
            self.wait(1)
            
            # Calculate N for this epsilon
            N = np.sqrt(9/epsilon + 3)
            
            # Draw vertical line at N
            N_line = axes.get_vertical_line(
                axes.c2p(N, 0),
                line_config={"color": color, "stroke_width": 2}
            )
            N_label = MathTex(f"N = {N:.2f}").next_to(N_line, UP, buff=0.1).scale(0.7)
            N_label.set_color(color)
            
            self.play(Create(N_line), Write(N_label))
            self.wait(1)
            
            # Highlight the region where |f(n) - 3| < ε
            area = axes.get_area(
                graph,
                x_range=(N, 19),
                color=color,
                opacity=0.3
            )
            self.play(Create(area))
            self.wait(1)
            
            # Show the mathematical relationship
            relation = MathTex(f"\\varepsilon = {epsilon} \\Rightarrow N = {N:.2f}").scale(0.7)
            relation.to_corner(DL, buff=1)
            relation.set_color(color)
            
            if i == 0:
                relation_group = VGroup(relation)
                self.play(Write(relation))
            else:
                relation.next_to(relation_group, DOWN, buff=0.2)
                relation_group.add(relation)
                self.play(Write(relation))
            
            self.wait(1)
        
        # Final conclusion
        conclusion = Text(
            "对于任意 ε > 0，存在 N = √(9/ε + 3)，当 n > N 时，|f(n) - 3| < ε",
            font="SimSun"
        ).scale(0.6)
        conclusion.to_edge(DOWN, buff=0.5)
        
        self.play(Write(conclusion))
        self.wait(3)
        
        # Emphasize the key point
        box = SurroundingRectangle(conclusion, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)

class EpsilonNProcess(Scene):
    def construct(self):
        # Set default font
        Text.set_default(font="SimSun")
        
        # Title
        title = Text("ε-N 过程详解", font="SimSun").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Create axes for visualization
        axes = Axes(
            x_range=[0, 20, 2],
            y_range=[2, 4, 0.5],
            axis_config={"include_tip": True},
            x_length=10,
            y_length=6
        )
        axes.next_to(title, DOWN, buff=1)
        
        # Labels for axes
        x_label = MathTex("n").next_to(axes.x_axis, RIGHT, buff=0.5)
        y_label = MathTex("f(n)").next_to(axes.y_axis, UP, buff=0.5)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(1)
        
        # Function to plot: 3n^2/(n^2 - 3)
        def func(n):
            return 3*n**2 / (n**2 - 3) if n**2 > 3 else 4  # Avoid division by zero or negative
        
        # Plot the function
        graph = axes.plot(func, x_range=[2.5, 19, 0.1], color=BLUE)
        graph_label = MathTex(r"f(n) = \frac{3n^2}{n^2 - 3}").next_to(graph, UP, buff=0.2).scale(0.7)
        graph_label.set_color(BLUE)
        
        # Plot the limit line y = 3
        limit_line = axes.plot(lambda x: 3, x_range=[0, 20], color=GREEN)
        limit_label = MathTex("y = 3").next_to(limit_line, DOWN, buff=0.2).scale(0.7)
        limit_label.set_color(GREEN)
        
        self.play(Create(graph), Write(graph_label))
        self.play(Create(limit_line), Write(limit_label))
        self.wait(2)
        
        # Show different epsilon values and corresponding N
        epsilons = [0.5, 0.2, 0.1]
        colors = [RED, YELLOW, PURPLE]
        
        # Draw epsilon bands around y = 3
        for i, (epsilon, color) in enumerate(zip(epsilons, colors)):
            # Draw epsilon lines above and below y = 3
            upper_epsilon_line = axes.get_horizontal_line(
                axes.c2p(0, 3 + epsilon),
                line_config={"color": color, "stroke_width": 2, "stroke_opacity": 0.7}
            )
            lower_epsilon_line = axes.get_horizontal_line(
                axes.c2p(0, 3 - epsilon),
                line_config={"color": color, "stroke_width": 2, "stroke_opacity": 0.7}
            )
            
            upper_epsilon_label = MathTex(f"y = 3 + \\varepsilon = {3 + epsilon}").next_to(upper_epsilon_line, RIGHT, buff=0.1).scale(0.5)
            upper_epsilon_label.set_color(color)
            lower_epsilon_label = MathTex(f"y = 3 - \\varepsilon = {3 - epsilon}").next_to(lower_epsilon_line, RIGHT, buff=0.1).scale(0.5)
            lower_epsilon_label.set_color(color)
            
            self.play(Create(upper_epsilon_line), Create(lower_epsilon_line))
            self.play(Write(upper_epsilon_label), Write(lower_epsilon_label))
            self.wait(1)
            
            # Calculate N for this epsilon
            N = np.sqrt(9/epsilon + 3)
            
            # Draw vertical line at N
            N_line = axes.get_vertical_line(
                axes.c2p(N, 0),
                line_config={"color": color, "stroke_width": 2}
            )
            N_label = MathTex(f"N = {N:.2f}").next_to(N_line, UP, buff=0.1).scale(0.7)
            N_label.set_color(color)
            
            self.play(Create(N_line), Write(N_label))
            self.wait(1)
            
            # Highlight the region where |f(n) - 3| < ε (for n > N)
            # Create a line showing that after N, the function is within epsilon of 3
            highlight_line = axes.plot(
                func,
                x_range=[N, 19, 0.1],
                color=color,
                stroke_width=5
            )
            
            self.play(Create(highlight_line))
            self.wait(1)
            
            # Show the mathematical relationship
            relation = MathTex(f"\\varepsilon = {epsilon} \\Rightarrow N = {N:.2f}").scale(0.7)
            relation.to_corner(DL, buff=1)
            relation.set_color(color)
            
            if i == 0:
                relation_group = VGroup(relation)
                self.play(Write(relation))
            else:
                relation.next_to(relation_group, DOWN, buff=0.2)
                relation_group.add(relation)
                self.play(Write(relation))
            
            self.wait(1)
        
        # Step by step process
        steps = VGroup(
            Text("1. 给定任意 ε > 0", font="SimSun"),
            Text("2. 化简 |f(n) - L|", font="SimSun"),
            Text("3. 解不等式 |f(n) - L| < ε", font="SimSun"),
            Text("4. 找到 N = √(9/ε + 3)", font="SimSun"),
            Text("5. 验证当 n > N 时，|f(n) - L| < ε", font="SimSun")
        ).scale(0.5)
        
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        steps.to_corner(UR, buff=0.5)
        
        for i, step in enumerate(steps):
            self.play(Write(step))
            self.wait(0.5)
        
        # Show the key formula
        formula = MathTex(r"N = \sqrt{\frac{9}{\varepsilon} + 3}").scale(1.0)
        formula.next_to(steps, DOWN, buff=0.5)
        formula.set_color(YELLOW)
        
        self.play(Write(formula))
        self.wait(3)
        
        # Final conclusion
        conclusion = Text(
            "对于任意 ε > 0，存在 N = √(9/ε + 3)，当 n > N 时，|f(n) - 3| < ε",
            font="SimSun"
        ).scale(0.6)
        conclusion.to_edge(DOWN, buff=0.5)
        
        self.play(Write(conclusion))
        self.wait(2)
        
        # Emphasize the key point
        box = SurroundingRectangle(conclusion, color=YELLOW, buff=0.2)
        self.play(Create(box))
        self.wait(2)

def main():
    scene1 = LimitProofVisualization()
    scene1.render()
    
    scene2 = EpsilonNProcess()
    scene2.render()

if __name__ == "__main__":
    main()