from manim import *

class AllMeanValueTheorems(Scene):
    def construct(self):
        # 创建标题
        title = Text("三个中值定理动画演示", font="SimSun").to_edge(UP)
        self.play(Write(title))
        
        # 第一部分: 罗尔中值定理
        rolle_title = Text("罗尔中值定理", font="SimSun").next_to(title, DOWN)
        self.play(Write(rolle_title))
        
        # 创建坐标系
        axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-1, 1, 0.5],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # 定义函数 f(x) = x(x-2) 在区间[0,2]上满足条件f(0)=f(2)=0
        def f_rolle(x):
            return x * (x - 2)
            
        def df_rolle(x):
            return 2*x - 2
        
        # 绘制函数图像
        graph_rolle = axes.plot(lambda x: f_rolle(x), color=BLUE)
        graph_label = MathTex("f(x) = x(x-2)").next_to(rolle_title, DOWN)
        
        # 设置区间端点
        a, b = 0, 2
        
        # 在罗尔中值定理中，满足条件的点c是1
        c_rolle = 1
        
        # 标记端点
        point_a = Dot(axes.c2p(a, f_rolle(a)), color=RED)
        point_b = Dot(axes.c2p(b, f_rolle(b)), color=RED)
        label_a = MathTex("a").next_to(point_a, DOWN)
        label_b = MathTex("b").next_to(point_b, DOWN)
        
        # 绘制坐标系和函数
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph_rolle), Write(graph_label))
        self.wait()
        
        # 显示端点
        self.play(Create(point_a), Create(point_b))
        self.play(Write(label_a), Write(label_b))
        
        # 强调f(a)=f(b)
        equal_values = Text("f(a) = f(b) = 0", font="SimSun").scale(0.7).to_corner(UL)
        self.play(Write(equal_values))
        self.wait()
        
        # 寻找导数为零的点
        moving_point = Dot(axes.c2p(a, f_rolle(a)), color=GREEN)
        moving_tangent = always_redraw(
            lambda: Line(
                axes.c2p(
                    moving_point.get_center()[0]/axes.c2p(1,0)[0] - 0.5, 
                    f_rolle(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 
                    df_rolle(moving_point.get_center()[0]/axes.c2p(1,0)[0]) * (-0.5)
                ),
                axes.c2p(
                    moving_point.get_center()[0]/axes.c2p(1,0)[0] + 0.5, 
                    f_rolle(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 
                    df_rolle(moving_point.get_center()[0]/axes.c2p(1,0)[0]) * (0.5)
                ),
                color=GREEN
            )
        )
        
        # 显示当前斜率
        current_slope = always_redraw(
            lambda: Text(f"斜率: {df_rolle(moving_point.get_center()[0]/axes.c2p(1,0)[0]):.2f}", 
                       font="SimSun").scale(0.6).to_corner(UR)
        )
        
        self.play(Create(moving_point), Create(moving_tangent), Create(current_slope))
        
        # 沿曲线移动点
        curve_points = []
        num_points = 30
        for i in range(num_points + 1):
            t = i / num_points
            x = a + t * (c_rolle - a)
            y = f_rolle(x)
            curve_points.append(axes.c2p(x, y))
        
        self.play(
            MoveAlongPath(moving_point, VMobject().set_points_as_corners(curve_points)),
            run_time=2
        )
        
        # 标记c点
        self.play(Flash(moving_point, color=GREEN, flash_radius=0.3))
        
        # 显示罗尔中值定理
        rolle_theorem = MathTex(r"\exists c \in (a,b) : f'(c) = 0").scale(0.8).to_edge(DOWN)
        self.play(Write(rolle_theorem))
        
        final_text_rolle = Text(f"在 x = {c_rolle} 处，f'(c) = 0", font="SimSun").scale(0.7).next_to(rolle_theorem, UP)
        self.play(Write(final_text_rolle))
        self.wait(2)
        
        # 清除屏幕，准备下一个定理
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )
        
        # 第二部分: 拉格朗日中值定理（微分中值定理）
        mvt_title = Text("拉格朗日中值定理", font="SimSun").next_to(title, DOWN)
        self.play(Write(mvt_title))
        
        # 创建新坐标系
        axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-1, 5, 1],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        # 定义函数 f(x) = x^2
        def f_mvt(x):
            return x**2
            
        def df_mvt(x):
            return 2*x
        
        # 绘制函数图像
        graph_mvt = axes.plot(lambda x: f_mvt(x), color=BLUE)
        graph_label = MathTex("f(x) = x^2").next_to(mvt_title, DOWN)
        
        # 设置区间端点
        a, b = 0, 2
        
        # 计算割线斜率
        secant_slope = (f_mvt(b) - f_mvt(a)) / (b - a)  # = 2
        
        # 满足中值定理的点
        c_mvt = 1  # f'(1) = 2
        
        # 标记端点
        point_a = Dot(axes.c2p(a, f_mvt(a)), color=RED)
        point_b = Dot(axes.c2p(b, f_mvt(b)), color=RED)
        label_a = MathTex("a").next_to(point_a, DOWN)
        label_b = MathTex("b").next_to(point_b, DOWN)
        
        # 绘制坐标系和函数
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(graph_mvt), Write(graph_label))
        self.wait()
        
        # 显示端点并绘制割线
        self.play(Create(point_a), Create(point_b))
        self.play(Write(label_a), Write(label_b))
        
        secant_line = Line(
            axes.c2p(a, f_mvt(a)),
            axes.c2p(b, f_mvt(b)),
            color=RED
        )
        self.play(Create(secant_line))
        
        # 显示割线斜率
        secant_text = Text(f"割线斜率 = {secant_slope}", font="SimSun").scale(0.7).to_corner(UL)
        self.play(Write(secant_text))
        self.wait()
        
        # 寻找切线斜率等于割线斜率的点
        moving_point = Dot(axes.c2p(a, f_mvt(a)), color=GREEN)
        moving_tangent = always_redraw(
            lambda: Line(
                axes.c2p(
                    moving_point.get_center()[0]/axes.c2p(1,0)[0] - 0.5, 
                    f_mvt(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 
                    df_mvt(moving_point.get_center()[0]/axes.c2p(1,0)[0]) * (-0.5)
                ),
                axes.c2p(
                    moving_point.get_center()[0]/axes.c2p(1,0)[0] + 0.5, 
                    f_mvt(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 
                    df_mvt(moving_point.get_center()[0]/axes.c2p(1,0)[0]) * (0.5)
                ),
                color=GREEN
            )
        )
        
        # 显示当前斜率
        current_slope = always_redraw(
            lambda: Text(f"切线斜率: {df_mvt(moving_point.get_center()[0]/axes.c2p(1,0)[0]):.2f}", 
                       font="SimSun").scale(0.6).to_corner(UR)
        )
        
        self.play(Create(moving_point), Create(moving_tangent), Create(current_slope))
        
        # 沿曲线移动点
        curve_points = []
        num_points = 30
        for i in range(num_points + 1):
            t = i / num_points
            x = a + t * (c_mvt - a)
            y = f_mvt(x)
            curve_points.append(axes.c2p(x, y))
        
        self.play(
            MoveAlongPath(moving_point, VMobject().set_points_as_corners(curve_points)),
            run_time=2
        )
        
        # 标记c点
        self.play(Flash(moving_point, color=GREEN, flash_radius=0.3))
        
        # 显示拉格朗日中值定理
        mvt_theorem = MathTex(r"\exists c \in (a,b) : f'(c) = \frac{f(b) - f(a)}{b - a}").scale(0.8).to_edge(DOWN)
        self.play(Write(mvt_theorem))
        
        final_text_mvt = Text(f"在 x = {c_mvt} 处，f'(c) = {secant_slope}", font="SimSun").scale(0.7).next_to(mvt_theorem, UP)
        self.play(Write(final_text_mvt))
        
        # 强调切线和割线平行
        self.play(
            Indicate(moving_tangent, color=GREEN, scale_factor=1.2),
            Indicate(secant_line, color=RED, scale_factor=1.2),
            run_time=2
        )
        self.wait(2)
        
        # 清除屏幕，准备下一个定理
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )
        
        # 第三部分: 柯西中值定理
        cauchy_title = Text("柯西中值定理", font="SimSun").next_to(title, DOWN)
        self.play(Write(cauchy_title))
        
        # 创建新坐标系（分为左右两部分）
        left_axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-1, 5, 1],
            axis_config={"color": BLUE},
        ).scale(0.7).to_edge(LEFT)
        left_labels = left_axes.get_axis_labels(x_label="x", y_label="f(x)")
        
        right_axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-1, 5, 1],
            axis_config={"color": BLUE},
        ).scale(0.7).to_edge(RIGHT)
        right_labels = right_axes.get_axis_labels(x_label="x", y_label="g(x)")
        
        # 定义两个函数 f(x) = x^2 和 g(x) = x
        def f_cauchy(x):
            return x**2
            
        def df_cauchy(x):
            return 2*x
            
        def g_cauchy(x):
            return x
            
        def dg_cauchy(x):
            return 1
        
        # 绘制函数图像
        graph_f = left_axes.plot(lambda x: f_cauchy(x), color=BLUE)
        graph_g = right_axes.plot(lambda x: g_cauchy(x), color=GREEN)
        
        label_f = MathTex("f(x) = x^2").scale(0.7).next_to(left_axes, UP)
        label_g = MathTex("g(x) = x").scale(0.7).next_to(right_axes, UP)
        
        # 设置区间端点
        a, b = 0, 2
        
        # 计算比值
        ratio = (f_cauchy(b) - f_cauchy(a)) / (g_cauchy(b) - g_cauchy(a))  # = 2
        
        # 满足柯西中值定理的点
        c_cauchy = 1  # f'(1)/g'(1) = 2/1 = 2
        
        # 标记端点
        point_a_f = Dot(left_axes.c2p(a, f_cauchy(a)), color=RED)
        point_b_f = Dot(left_axes.c2p(b, f_cauchy(b)), color=RED)
        
        point_a_g = Dot(right_axes.c2p(a, g_cauchy(a)), color=RED)
        point_b_g = Dot(right_axes.c2p(b, g_cauchy(b)), color=RED)
        
        # 绘制坐标系和函数
        self.play(
            Create(left_axes), Write(left_labels),
            Create(right_axes), Write(right_labels)
        )
        self.play(
            Create(graph_f), Write(label_f),
            Create(graph_g), Write(label_g)
        )
        self.wait()
        
        # 显示端点
        self.play(
            Create(point_a_f), Create(point_b_f),
            Create(point_a_g), Create(point_b_g)
        )
        
        # 计算并显示比值
        ratio_text = MathTex(r"\frac{f(b) - f(a)}{g(b) - g(a)} = \frac{4 - 0}{2 - 0} = 2").scale(0.7).to_edge(DOWN)
        self.play(Write(ratio_text))
        self.wait()
        
        # 寻找导数比值等于函数值增量比值的点
        moving_point_f = Dot(left_axes.c2p(a, f_cauchy(a)), color=YELLOW)
        moving_point_g = Dot(right_axes.c2p(a, g_cauchy(a)), color=YELLOW)
        
        derivative_ratio = always_redraw(
            lambda: Text(
                f"f'(c)/g'(c) = {df_cauchy(moving_point_f.get_center()[0]/left_axes.c2p(1,0)[0]):.2f}/{dg_cauchy(moving_point_f.get_center()[0]/left_axes.c2p(1,0)[0]):.2f}", 
                font="SimSun"
            ).scale(0.6).next_to(ratio_text, UP)
        )
        
        self.play(Create(moving_point_f), Create(moving_point_g), Create(derivative_ratio))
        
        # 沿曲线移动点
        curve_points_f = []
        curve_points_g = []
        num_points = 30
        for i in range(num_points + 1):
            t = i / num_points
            x = a + t * (c_cauchy - a)
            y_f = f_cauchy(x)
            y_g = g_cauchy(x)
            curve_points_f.append(left_axes.c2p(x, y_f))
            curve_points_g.append(right_axes.c2p(x, y_g))
        
        self.play(
            MoveAlongPath(moving_point_f, VMobject().set_points_as_corners(curve_points_f)),
            MoveAlongPath(moving_point_g, VMobject().set_points_as_corners(curve_points_g)),
            run_time=2
        )
        
        # 标记c点
        self.play(
            Flash(moving_point_f, color=YELLOW, flash_radius=0.3),
            Flash(moving_point_g, color=YELLOW, flash_radius=0.3)
        )
        
        # 显示柯西中值定理
        cauchy_theorem = MathTex(
            r"\exists c \in (a,b) : \frac{f'(c)}{g'(c)} = \frac{f(b) - f(a)}{g(b) - g(a)}"
        ).scale(0.7).next_to(ratio_text, UP)
        
        self.play(FadeOut(derivative_ratio))
        self.play(Write(cauchy_theorem))
        
        final_text_cauchy = Text(
            f"在 x = {c_cauchy} 处，f'(c)/g'(c) = 2/1 = 2", font="SimSun"
        ).scale(0.6).next_to(cauchy_theorem, UP)
        
        self.play(Write(final_text_cauchy))
        self.wait(2)
        
        # 总结
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )
        
        summary = Text("三个中值定理的关系", font="SimSun").next_to(title, DOWN)
        self.play(Write(summary))
        
        relation_text = [
            Text("1. 罗尔中值定理是拉格朗日中值定理的特例(f(a)=f(b)时)", font="SimSun").scale(0.6),
            Text("2. 拉格朗日中值定理是柯西中值定理的特例(g(x)=x时)", font="SimSun").scale(0.6),
            Text("3. 柯西中值定理是最一般形式的中值定理", font="SimSun").scale(0.6)
        ]
        
        for i, text in enumerate(relation_text):
            text.next_to(summary, DOWN, buff=0.5 + i*0.6)
            self.play(Write(text))
        
        self.wait(3) 