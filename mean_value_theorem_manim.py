from manim import *

class MeanValueTheorem(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-1, 5, 1],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # 定义函数 f(x) = x^3 - 2x^2 + 2
        def f(x):
            return x**3 - 2*x**2 + 2
            
        # 定义函数的导数 f'(x)
        def df(x):
            return 3*x**2 - 4*x
            
        # 绘制函数图像
        graph = axes.plot(lambda x: f(x), color=BLUE)
        graph_label = MathTex("f(x) = x^3 - 2x^2 + 2").to_corner(UL)
        
        # 设置区间端点
        a, b = 0, 2
        
        # 标记端点
        point_a = Dot(axes.c2p(a, f(a)), color=RED)
        point_b = Dot(axes.c2p(b, f(b)), color=RED)
        label_a = MathTex("a").next_to(point_a, DOWN)
        label_b = MathTex("b").next_to(point_b, DOWN)
        
        # 计算割线斜率
        secant_slope = (f(b) - f(a)) / (b - a)
        
        # 绘制割线
        secant_line = Line(
            axes.c2p(a, f(a)),
            axes.c2p(b, f(b)),
            color=RED
        )
        
        # 寻找满足微分中值定理的点 c
        c = 1  # 对于我们的函数，c 约为 1
        point_c = Dot(axes.c2p(c, f(c)), color=GREEN)
        
        # 绘制切线
        tangent_slope = df(c)
        x_min, x_max = c - 0.5, c + 0.5
        tangent_line = Line(
            axes.c2p(x_min, f(c) + tangent_slope * (x_min - c)),
            axes.c2p(x_max, f(c) + tangent_slope * (x_max - c)),
            color=GREEN
        )
        
        # 创建说明性文本
        theorem_text = MathTex(
            r"\exists c \in (a,b) : f'(c) = \frac{f(b) - f(a)}{b - a}"
        ).to_edge(DOWN)
        
        # 动画序列
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), Write(graph_label))
        self.wait()
        
        self.play(Create(point_a), Create(point_b))
        self.play(Write(label_a), Write(label_b))
        self.wait()
        
        self.play(Create(secant_line))
        secant_formula = MathTex(r"\frac{f(b) - f(a)}{b - a} = " + f"{secant_slope:.2f}")
        secant_label = Text("割线斜率 = ", font="SimSun")
        secant_text = VGroup(secant_label, secant_formula).arrange(RIGHT).next_to(secant_line, UP)
        self.play(Write(secant_text))
        self.wait()
        
        # 动态寻找满足定理的点
        moving_point = Dot(axes.c2p(a, f(a)), color=GREEN)
        moving_tangent = always_redraw(
            lambda: Line(
                axes.c2p(
                    moving_point.get_center()[0]/axes.c2p(1,0)[0] - 0.5, 
                    f(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 
                    df(moving_point.get_center()[0]/axes.c2p(1,0)[0]) * (-0.5)
                ),
                axes.c2p(
                    moving_point.get_center()[0]/axes.c2p(1,0)[0] + 0.5, 
                    f(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 
                    df(moving_point.get_center()[0]/axes.c2p(1,0)[0]) * (0.5)
                ),
                color=GREEN
            )
        )
        
        self.play(Create(moving_point), Create(moving_tangent))
        self.wait()
        
        # 移动点来寻找满足条件的 c
        self.play(
            moving_point.animate.move_to(axes.c2p(c, f(c))),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=3
        )
        self.wait()
        
        final_formula = MathTex(r"f'(c) = " + f"{df(c):.2f}")
        final_label = Text("在 x = " + f"{c:.2f}" + " 处，", font="SimSun")
        final_text = VGroup(final_label, final_formula).arrange(RIGHT).next_to(theorem_text, UP)
        
        self.play(Write(theorem_text))
        self.play(Write(final_text))
        self.wait(2)
        
        # 在找到满足条件的点 c 后，可以添加以下效果
        self.play(
            Flash(moving_point, color=GREEN, flash_radius=0.3),
            run_time=1
        )
        
        # 高亮显示切线和割线的平行关系
        parallel_indicator = MathTex("f'(c) = \\frac{f(b) - f(a)}{b - a}").scale(0.8)
        parallel_indicator.next_to(point_c, UP)
        self.play(Write(parallel_indicator))
        
        # 添加一个小动画来强调切线和割线的平行
        parallel_lines = VGroup()
        for i in range(3):
            line = Line(
                axes.c2p(c - 0.3 + i*0.3, f(c) + tangent_slope * (-0.3 + i*0.3)),
                axes.c2p(c - 0.1 + i*0.3, f(c) + tangent_slope * (-0.1 + i*0.3)),
                color=YELLOW
            )
            parallel_lines.add(line)
        
        self.play(Create(parallel_lines))
        self.wait() 