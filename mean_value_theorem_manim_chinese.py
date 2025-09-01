from manim import *

class MeanValueTheorem(Scene):
    def construct(self):
        # 创建标题
        title = Text("微分中值定理动画演示", font="SimSun").to_edge(UP)
        self.play(Write(title))
        
        # 创建坐标系
        axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-1, 5, 1],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # 定义新函数 f(x) = x^2
        def f(x):
            return x**2
            
        # 定义函数的导数 f'(x) = 2x
        def df(x):
            return 2*x
            
        # 绘制函数图像
        graph = axes.plot(lambda x: f(x), color=BLUE)
        graph_label = MathTex("f(x) = x^2").next_to(title, DOWN)
        
        # 设置区间端点
        a, b = 0, 2
        
        # 标记端点
        point_a = Dot(axes.c2p(a, f(a)), color=RED)
        point_b = Dot(axes.c2p(b, f(b)), color=RED)
        label_a = MathTex("a").next_to(point_a, DOWN)
        label_b = MathTex("b").next_to(point_b, DOWN)
        
        # 计算割线斜率
        secant_slope = (f(b) - f(a)) / (b - a)  # = 2
        print(f"割线斜率: {secant_slope}")
        
        # 满足定理的点 c
        c = 1  # f'(1) = 2*1 = 2
        print(f"在c={c}处的导数值: {df(c)}")
        
        # 绘制坐标系和函数
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph), Write(graph_label))
        self.wait()
        
        # 显示区间端点
        self.play(Create(point_a), Create(point_b))
        self.play(Write(label_a), Write(label_b))
        self.wait()
        
        # 绘制割线
        secant_line = Line(
            axes.c2p(a, f(a)),
            axes.c2p(b, f(b)),
            color=RED
        )
        self.play(Create(secant_line))
        
        # 显示割线斜率
        secant_label = Text("割线斜率 = ", font="SimSun")
        secant_formula = MathTex(f"{secant_slope:.2f}")
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
        
        # 添加当前斜率显示
        current_slope_text = always_redraw(
            lambda: Text(f"当前切线斜率: {df(moving_point.get_center()[0]/axes.c2p(1,0)[0]):.2f}", 
                        font="SimSun").scale(0.6).to_corner(UR)
        )
        self.play(Create(moving_point), Create(moving_tangent), Create(current_slope_text))
        self.wait()
        
        # 创建多个点来形成沿曲线的路径
        curve_points = []
        num_points = 30
        for i in range(num_points + 1):
            t = i / num_points
            x = a + t * (c - a)  # 从a到c的x值
            y = f(x)  # 对应的函数值
            curve_points.append(axes.c2p(x, y))
        
        # 沿曲线路径移动点
        self.play(
            MoveAlongPath(moving_point, VMobject().set_points_as_corners(curve_points)),
            rate_func=rate_functions.linear,
            run_time=3
        )
        self.wait()
        
        # 创建说明性文本
        theorem_text = MathTex(
            r"\exists c \in (a,b) : f'(c) = \frac{f(b) - f(a)}{b - a}"
        ).to_edge(DOWN)
        
        # 显示最终结果
        final_label = Text(f"在 x = {c:.2f} 处，", font="SimSun")
        final_formula = MathTex(f"f'(c) = {df(c):.2f} = {secant_slope:.2f}")
        final_text = VGroup(final_label, final_formula).arrange(RIGHT).next_to(theorem_text, UP)
        
        self.play(Write(theorem_text))
        self.play(Write(final_text))
        self.wait()
        
        # 在找到满足条件的点 c 后，添加特效
        self.play(
            Flash(moving_point, color=GREEN, flash_radius=0.3),
            run_time=1
        )
        
        # 明确显示切线和割线的平行关系
        parallel_indicator = MathTex("f'(c) = \\frac{f(b) - f(a)}{b - a} = 2").scale(0.8)
        parallel_indicator.next_to(moving_point, UP)
        self.play(Write(parallel_indicator))
        
        # 添加平行线指示
        parallel_lines = VGroup()
        for i in range(3):
            line = Line(
                axes.c2p(c - 0.3 + i*0.3, f(c) + df(c) * (-0.3 + i*0.3)),
                axes.c2p(c - 0.1 + i*0.3, f(c) + df(c) * (-0.1 + i*0.3)),
                color=YELLOW
            )
            parallel_lines.add(line)
        
        self.play(Create(parallel_lines))
        
        # 强调切线和割线的平行
        self.play(
            Indicate(moving_tangent, color=GREEN, scale_factor=1.2),
            Indicate(secant_line, color=RED, scale_factor=1.2),
            run_time=2
        )
        self.wait(2) 