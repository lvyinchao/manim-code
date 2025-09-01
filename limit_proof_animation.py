from manim import *

class LimitProofAnimation(Scene):
    def construct(self):
        # Set default font
        Text.set_default(font="SimSun")
        
        # Title
        title = Text("极限证明动画演示").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)
        
        # Original limit expression
        limit_expr = MathTex(r"\lim_{n \to \infty} \frac{3n^2}{n^2 - 3} = 3")
        limit_expr.next_to(title, DOWN, buff=0.5)
        self.play(Write(limit_expr))
        self.wait(1)
        
        # Simplify the expression
        simplify_title = Text("简化表达式").scale(0.6)
        simplify_title.next_to(limit_expr, DOWN, buff=0.5)
        self.play(Write(simplify_title))
        
        simplify_expr = MathTex(
            r"\left| \frac{3n^2}{n^2 - 3} - 3 \right| = \left| \frac{3n^2 - 3(n^2 - 3)}{n^2 - 3} \right| = \left| \frac{3n^2 - 3n^2 + 9}{n^2 - 3} \right| = \left| \frac{9}{n^2 - 3} \right| = \frac{9}{n^2 - 3}"
        )
        simplify_expr.scale(0.7)
        simplify_expr.next_to(simplify_title, DOWN, buff=0.3)
        self.play(Write(simplify_expr))
        self.wait(2)
        
        # Epsilon definition
        epsilon_title = Text("epsilon 定义").scale(0.6)
        epsilon_title.next_to(simplify_expr, DOWN, buff=0.5)
        self.play(Write(epsilon_title))
        
        epsilon_expr = MathTex(r"\frac{9}{n^2 - 3} < \epsilon")
        epsilon_expr.scale(0.7)
        epsilon_expr.next_to(epsilon_title, DOWN, buff=0.3)
        self.play(Write(epsilon_expr))
        self.wait(2)
        
        # Solve for N
        solve_title = Text("求解 N").scale(0.6)
        solve_title.next_to(epsilon_expr, DOWN, buff=0.5)
        self.play(Write(solve_title))
        
        solve_expr = MathTex(
            r"\frac{9}{n^2 - 3} < \epsilon \implies n^2 - 3 > \frac{9}{\epsilon} \implies n^2 > \frac{9}{\epsilon} + 3 \implies n > \sqrt{\frac{9}{\epsilon} + 3}"
        )
        solve_expr.scale(0.7)
        solve_expr.next_to(solve_title, DOWN, buff=0.3)
        self.play(Write(solve_expr))
        self.wait(2)
        
        # Highlight final result
        final_result = MathTex(r"N = \sqrt{\frac{9}{\epsilon} + 3}")
        final_result.scale(0.8)
        final_result.next_to(solve_expr, DOWN, buff=0.5)
        final_result.set_color(YELLOW)
        self.play(Write(final_result))
        self.wait(2)
        
        # Explanation
        explanation = Text(
            "因此，对于任意 ε > 0，存在 N = √(9/ε + 3)，当 n > N 时，|3n²/(n² - 3) - 3| < ε，即证明了极限为 3。",
            font="SimSun"
        ).scale(0.6)
        explanation.next_to(final_result, DOWN, buff=0.5)
        self.play(Write(explanation))
        self.wait(3)