from manim import *
import numpy as np

class ParametricCauchyTheorem(Scene):
    def construct(self):
        # 创建标题
        title = Text("柯西中值定理的参数曲线解释", font="SimSun").to_edge(UP)
        self.play(Write(title))
        
        # 参数方程说明
        parametric_eq = MathTex(
            r"\gamma(t) = \begin{cases} x = g(t) \\ y = f(t) \end{cases}, t \in [a,b]"
        ).next_to(title, DOWN)
        self.play(Write(parametric_eq))
        
        # 参数方程解释
        param_explanation = Text(
            "用参数方程表示曲线，柯西中值定理有更直观的几何意义", 
            font="SimSun"
        ).scale(0.6).next_to(parametric_eq, DOWN)
        self.play(Write(param_explanation))
        self.wait()
        
        # 添加淡出标题的动画
        self.play(FadeOut(title), FadeOut(parametric_eq))
        
        # 创建参数曲线的坐标系
        axes = Axes(
            x_range=[-1, 3, 0.5],
            y_range=[-1, 3, 0.5],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="g(t)", y_label="f(t)")
        
        # 定义函数 f(t) 和 g(t)
        def f(t):
            return t**3 - 3*t**2 + 2*t
            
        def g(t):
            return t
        
        # 计算导数
        def df(t):
            return 3*t**2 - 6*t + 2
            
        def dg(t):
            return 1
        
        # 区间端点
        a, b = 0, 2
        
        # 满足柯西定理的c值
        c_cauchy = self.find_cauchy_c(f, df, g, dg, a, b)
        
        # 在坐标系创建前进行淡出
        self.play(
            FadeOut(param_explanation),
            Create(axes), 
            Write(axes_labels)
        )
        
        # 绘制参数曲线 (g(t), f(t))
        parametric_curve = ParametricFunction(
            lambda t: axes.c2p(g(t), f(t)),
            t_range=[0, 2.5],
            color=BLUE
        )
        
        curve_eq = MathTex(
            r"\gamma(t) = \begin{cases} x = g(t) \\ y = f(t) \end{cases}"
        ).scale(0.6).to_corner(UL)
        self.play(Create(parametric_curve), Write(curve_eq))
        
        # 参数化图示 - 添加箭头从t到曲线点
        t_line = NumberLine(
            x_range=[0, 2, 0.5],
            length=3,
            include_numbers=True,
        ).to_edge(DOWN, buff=1)
        t_label = Text("参数 t", font="SimSun").scale(0.5).next_to(t_line, LEFT)
        
        self.play(Create(t_line), Write(t_label))
        
        # 展示参数t如何映射到曲线上的点
        t_points = [0, 0.5, 1, 1.5, 2]
        animations = []
        
        for t in t_points:
            dot_t = Dot(t_line.n2p(t), color=YELLOW, radius=0.05)
            dot_curve = Dot(axes.c2p(g(t), f(t)), color=YELLOW, radius=0.05)
            arrow = Arrow(dot_t.get_center(), dot_curve.get_center(), buff=0.1, color=YELLOW_A)
            
            animations.append(AnimationGroup(
                Create(dot_t),
                Create(arrow),
                Create(dot_curve),
                lag_ratio=0.3
            ))
        
        for anim in animations:
            self.play(anim, run_time=0.8)
        
        self.wait()
        self.play(*[FadeOut(obj) for obj in animations])
        
        # 标记曲线上的端点
        point_a = Dot(axes.c2p(g(a), f(a)), color=RED)
        point_b = Dot(axes.c2p(g(b), f(b)), color=RED)
        
        label_a = MathTex(r"\gamma(a)").next_to(point_a, DOWN)
        label_b = MathTex(r"\gamma(b)").next_to(point_b, DOWN)
        
        self.play(Create(point_a), Create(point_b))
        self.play(Write(label_a), Write(label_b))
        
        # 绘制从A到B的割线（参数视角下的弦）
        secant_line = Line(
            axes.c2p(g(a), f(a)),
            axes.c2p(g(b), f(b)),
            color=RED
        )
        self.play(Create(secant_line))
        
        # 创建沿曲线移动的点
        moving_point = Dot(axes.c2p(g(a), f(a)), color=YELLOW)
        moving_label = MathTex(r"\gamma(t)").next_to(moving_point, UP, buff=0.1)
        
        # 切线 - 参数曲线视角下的切向量
        tangent = always_redraw(
            lambda: Line(
                axes.c2p(
                    g(moving_point.get_center()[0]/axes.c2p(1,0)[0]) - 0.5, 
                    f(moving_point.get_center()[0]/axes.c2p(1,0)[0]) - 
                    0.5 * (df(moving_point.get_center()[0]/axes.c2p(1,0)[0])/dg(moving_point.get_center()[0]/axes.c2p(1,0)[0]))
                ),
                axes.c2p(
                    g(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 0.5, 
                    f(moving_point.get_center()[0]/axes.c2p(1,0)[0]) + 
                    0.5 * (df(moving_point.get_center()[0]/axes.c2p(1,0)[0])/dg(moving_point.get_center()[0]/axes.c2p(1,0)[0]))
                ),
                color=GREEN
            )
        )
        
        tangent_label = VGroup(
            Text("切线:", font="SimSun").scale(0.5),
            MathTex(r"\gamma'(t)").scale(0.6)
        ).arrange(RIGHT, buff=0.2).set_color(GREEN)
        tangent_label.to_corner(UR)
        
        # 在移动点的动画部分，添加参数值显示
        t_tracker = DecimalNumber(
            a,
            num_decimal_places=2,
            include_sign=False,
        ).scale(0.6).next_to(moving_point, RIGHT, buff=0.1)

        t_label = MathTex(r"t = ").scale(0.6).next_to(t_tracker, LEFT, buff=0.05)

        t_group = VGroup(t_label, t_tracker)

        self.play(
            Create(moving_point),
            Write(moving_label),
            Write(t_group),
            Create(tangent),
            Write(tangent_label)
        )
        
        # 修改点移动动画，同时更新t值
        def update_t_value(mob):
            # 获取当前点的x坐标，对应参数t
            x = moving_point.get_center()[0]
            # 转换回参数t值
            t_value = x / axes.c2p(1,0)[0]
            # 更新数值
            mob.set_value(t_value)

        t_tracker.add_updater(update_t_value)
        t_group.add_updater(lambda m: m.next_to(moving_point, RIGHT, buff=0.1))

        # 在点移动动画结束后记得移除updater
        t_tracker.remove_updater(update_t_value)
        t_group.remove_updater(lambda m: m.next_to(moving_point, RIGHT, buff=0.1))
        
        # 沿曲线移动点
        curve_points = []
        num_points = 30
        for i in range(num_points + 1):
            t = a + i * (c_cauchy - a) / num_points
            curve_points.append(axes.c2p(g(t), f(t)))
        
        self.play(
            MoveAlongPath(moving_point, VMobject().set_points_as_corners(curve_points)),
            MaintainPositionRelativeTo(moving_label, moving_point),
            run_time=3
        )
        
        # 高亮显示c点，此时切线平行于割线
        self.play(Flash(moving_point, color=YELLOW, flash_radius=0.3))
        
        # 标记c点
        point_c = Dot(axes.c2p(g(c_cauchy), f(c_cauchy)), color=YELLOW)
        label_c = MathTex(r"\gamma(\xi)").next_to(point_c, UP)
        
        self.play(
            ReplacementTransform(moving_point, point_c),
            ReplacementTransform(moving_label, label_c),
            FadeOut(t_group)
        )
        
        # 显示切向量和弦向量以强调平行关系
        secant_slope_display = VGroup(
            Text("弦斜率:", font="SimSun").scale(0.4),
            MathTex(r"\frac{f(b) - f(a)}{g(b) - g(a)}").scale(0.5)
        ).arrange(RIGHT, buff=0.1).set_color(RED)
        secant_slope_display.next_to(secant_line.get_center(), UP, buff=0.2)

        tangent_slope_display = VGroup(
            Text("切线斜率:", font="SimSun").scale(0.4),
            MathTex(r"\frac{f'(\xi)}{g'(\xi)}").scale(0.5)
        ).arrange(RIGHT, buff=0.1).set_color(GREEN).next_to(point_c, UP+RIGHT, buff=0.2)

        self.play(Create(point_c), Write(label_c))
        self.play(Create(secant_line))
        self.play(Write(secant_slope_display), Write(tangent_slope_display))
        
        # 等显示完斜率后，再显示柯西定理内容
        self.wait(1)  # 给观众一点时间理解斜率

        # 显示参数形式的柯西中值定理
        theorem_text = MathTex(
            r"\exists \xi \in (a,b) : \frac{f'(\xi)}{g'(\xi)} = \frac{f(b) - f(a)}{g(b) - g(a)}"
        ).scale(0.7)

        # 使用参数形式重写
        parametric_theorem = MathTex(
            r"\exists \xi \in (a,b) : \gamma'(\xi) \parallel (\gamma(b) - \gamma(a))"
        ).scale(0.7)

        theorem_group = VGroup(theorem_text, parametric_theorem).arrange(DOWN, buff=0.3)
        theorem_group.to_edge(DOWN)

        self.play(Write(theorem_text))
        self.play(Write(parametric_theorem))
        
        # 显示切向量和弦向量以强调平行关系
        secant_slope_display = VGroup(
            Text("弦斜率:", font="SimSun").scale(0.4),
            MathTex(r"\frac{f(b) - f(a)}{g(b) - g(a)}").scale(0.5)
        ).arrange(RIGHT, buff=0.1).set_color(RED)
        secant_slope_display.next_to(secant_line.get_center(), UP, buff=0.2)

        tangent_slope_display = VGroup(
            Text("切线斜率:", font="SimSun").scale(0.4),
            MathTex(r"\frac{f'(\xi)}{g'(\xi)}").scale(0.5)
        ).arrange(RIGHT, buff=0.1).set_color(GREEN).next_to(point_c, UP+RIGHT, buff=0.2)

        self.play(Create(point_c), Write(label_c))
        self.play(Create(secant_line))
        self.play(Write(secant_slope_display), Write(tangent_slope_display))
        
        # 强调平行关系
        parallel_text = Text(
            "柯西中值定理：存在点ξ使得切线斜率等于弦斜率", 
            font="SimSun"
        ).scale(0.6).next_to(parametric_theorem, UP, buff=0.3)
        
        self.play(Write(parallel_text))
        
        # 高亮显示平行关系
        self.play(
            Indicate(secant_line, color=RED, scale_factor=1.1),
            Indicate(secant_slope_display, color=RED, scale_factor=1.1),
            Indicate(tangent_slope_display, color=GREEN, scale_factor=1.1),
            run_time=2
        )
        
        self.wait(2)

        # 在显示参数形式的柯西中值定理部分（约在第160行），添加更直观的参数表达
        # 在parametric_theorem之后添加:
        param_explanation = Text(
            "其中 γ'(t) = (g'(t), f'(t)) 是切向量", 
            font="SimSun"
        ).scale(0.6).next_to(parametric_theorem, DOWN, buff=0.2)
        self.play(Write(param_explanation))


class UnifiedMeanValueTheorems(Scene):
    def construct(self):
        # 标题保持不变
        title = Text("从柯西到拉格朗日到罗尔：三个中值定理的联系", font="SimSun").scale(0.8).to_edge(UP)
        self.play(Write(title))
        
        # 添加初始说明
        intro_text = Text(
            "三个中值定理体现了数学中的一般到特殊的演化", 
            font="SimSun"
        ).scale(0.6).next_to(title, DOWN)
        self.play(Write(intro_text))
        self.wait()
        
        # 添加淡出标题的动画
        self.play(FadeOut(title), FadeOut(intro_text))
        
        # 创建坐标系
        axes = Axes(
            x_range=[-0.5, 3.5, 0.5],
            y_range=[-2, 4, 0.5],
            axis_config={"color": BLUE},
        )
        axes_labels = axes.get_axis_labels(x_label="g(t)", y_label="f(t)")  # 改为参数形式的标记
        
        # 选用一个函数能同时展示三个定理
        def f(t):
            return t**3 - 3*t**2 + 2*t
        
        def df(t):
            return 3*t**2 - 6*t + 2
            
        def g(t):
            return t  # 改回与ParametricCauchyTheorem类相同的定义
        
        def dg(t):
            return 1
            
        # 绘制坐标系和曲线
        self.play(
            Create(axes), 
            Write(axes_labels)
        )
        
        # 绘制参数曲线 (g(t), f(t))
        parametric_curve = ParametricFunction(
            lambda t: axes.c2p(g(t), f(t)),
            t_range=[0, 3],
            color=BLUE
        )
        
        curve_label = MathTex(
            r"\gamma(t) = \begin{cases} x = g(t) \\ y = f(t) \end{cases}"
        ).scale(0.8).to_edge(UP, buff=0.5)
        self.play(Create(parametric_curve), Write(curve_label))
        
        # 1. 柯西中值定理 - 参数曲线视角
        cauchy_title = Text("柯西中值定理（参数曲线视角）", font="SimSun").scale(0.7)
        cauchy_title.to_edge(DOWN, buff=0.1)
        
        a, b = 0.5, 2.5  # 选择参数端点
        c_cauchy = self.find_cauchy_c(f, df, g, dg, a, b)
        
        # 标记端点
        point_a = Dot(axes.c2p(g(a), f(a)), color=RED)
        point_b = Dot(axes.c2p(g(b), f(b)), color=RED)
        label_a = MathTex(r"\gamma(a)").next_to(point_a, DOWN)
        label_b = MathTex(r"\gamma(b)").next_to(point_b, DOWN)
        
        self.play(Write(cauchy_title))
        self.play(Create(point_a), Create(point_b), Write(label_a), Write(label_b))
        
        # 绘制从A到B的割线（参数视角下的弦）
        secant_line = Line(
            axes.c2p(g(a), f(a)),
            axes.c2p(g(b), f(b)),
            color=RED
        )
        self.play(Create(secant_line))
        
        # 找到满足平行条件的c点
        c_point = Dot(axes.c2p(g(c_cauchy), f(c_cauchy)), color=YELLOW)
        c_label = MathTex(r"\gamma(\xi)").next_to(c_point, UP)

        # 切线 - 参数曲线在c点的导数
        c_tangent_line = Line(
            axes.c2p(g(c_cauchy) - 0.5, f(c_cauchy) - 0.5 * (df(c_cauchy)/dg(c_cauchy))),
            axes.c2p(g(c_cauchy) + 0.5, f(c_cauchy) + 0.5 * (df(c_cauchy)/dg(c_cauchy))),
            color=GREEN
        )

        secant_slope_display = VGroup(
            Text("弦斜率:", font="SimSun").scale(0.4),
            MathTex(r"\frac{f(b) - f(a)}{g(b) - g(a)}").scale(0.5)
        ).arrange(RIGHT, buff=0.1).set_color(RED)
        secant_slope_display.next_to(secant_line.get_center(), UP, buff=0.2)

        tangent_slope_display = VGroup(
            Text("切线斜率:", font="SimSun").scale(0.4),
            MathTex(r"\frac{f'(\xi)}{g'(\xi)}").scale(0.5)
        ).arrange(RIGHT, buff=0.1).set_color(GREEN).next_to(c_point, UP+RIGHT, buff=0.2)

        self.play(Create(c_point), Write(c_label))
        self.play(Create(c_tangent_line))
        self.play(Write(secant_slope_display), Write(tangent_slope_display))
        
        # 先等待观察斜率
        self.wait(1)  

        # 然后再显示柯西定理公式
        cauchy_formula = MathTex(
            r"\exists \xi \in (a,b) : \frac{f'(\xi)}{g'(\xi)} = \frac{f(b) - f(a)}{g(b) - g(a)}"
        ).scale(0.7).next_to(cauchy_title, UP)

        # 参数化形式的解释
        cauchy_explanation = Text(
            "柯西定理表明：存在一点ξ，使得该点切线方向与弦平行", 
            font="SimSun"
        ).scale(0.5).next_to(cauchy_formula, UP)

        self.play(Write(cauchy_formula))
        self.play(Write(cauchy_explanation))
        
        # 突出显示切向量与弦向量平行
        self.play(
            Indicate(c_tangent_line, scale_factor=1.2, color=GREEN),
            Indicate(secant_slope_display, scale_factor=1.1, color=RED),
            Indicate(tangent_slope_display, scale_factor=1.1, color=GREEN),
            Indicate(secant_line, color=RED, scale_factor=1.1),
            run_time=2
        )
        
        self.wait(2)
        
        # 2. 拉格朗日中值定理 (g(t)=t时的特例)
        self.play(
            FadeOut(cauchy_explanation),
            FadeOut(cauchy_formula),
            FadeOut(curve_label),
            FadeOut(secant_slope_display),
            FadeOut(tangent_slope_display),
            FadeOut(c_tangent_line)
        )
        
        lagrange_title = Text("拉格朗日中值定理 (g(t)=t时的特例)", font="SimSun").scale(0.7)
        
        self.play(ReplacementTransform(cauchy_title, lagrange_title))
        
        # 为拉格朗日定理选择新的端点
        a_lag, b_lag = 0.8, 2.3  # 新的非坐标轴上点
        
        # 更新端点 - 确保在曲线上
        self.play(FadeOut(point_a), FadeOut(point_b), FadeOut(label_a), FadeOut(label_b))

        point_a = Dot(axes.c2p(a_lag, f(a_lag)), color=RED)  # 重新创建点
        point_b = Dot(axes.c2p(b_lag, f(b_lag)), color=RED)
        label_a = MathTex("a").next_to(point_a, DOWN)
        label_b = MathTex("b").next_to(point_b, DOWN)

        self.play(
            Create(point_a),
            Create(point_b),
            Write(label_a),
            Write(label_b)
        )
        
        # 更新割线
        new_secant = Line(
            axes.c2p(a_lag, f(a_lag)),
            axes.c2p(b_lag, f(b_lag)),
            color=RED
        )
        self.play(ReplacementTransform(secant_line, new_secant))
        secant_line = new_secant
        
        # 计算拉格朗日定理的c值
        c_lag = self.find_lagrange_c(f, df, a_lag, b_lag)

        # 先显示拉格朗日定理的公式
        lag_formula = MathTex(
            r"\exists \xi \in (a,b) : f'(\xi) = \frac{f(b) - f(a)}{b - a}"
        ).scale(0.7).next_to(lagrange_title, UP, buff=0.2)

        self.play(Write(lag_formula))

        # 更新c点位置和标签
        new_c_label = MathTex(r"\xi").next_to(axes.c2p(c_lag, f(c_lag)), UP, buff=0.1)

        self.play(
            c_point.animate.move_to(axes.c2p(c_lag, f(c_lag))),
            FadeOut(c_label),
            FadeIn(new_c_label)
        )
        c_label = new_c_label  # 更新标签引用

        # 添加c点处的切线
        lag_tangent_line = Line(
            axes.c2p(c_lag - 0.5, f(c_lag) - 0.5 * df(c_lag)),
            axes.c2p(c_lag + 0.5, f(c_lag) + 0.5 * df(c_lag)),
            color=GREEN
        )
        self.play(Create(lag_tangent_line))

        # 强调切线斜率等于割线斜率
        self.play(
            Indicate(lag_tangent_line, scale_factor=1.2, color=GREEN),
            Indicate(secant_line, scale_factor=1.2, color=RED),
            run_time=2
        )

        self.wait(1)

        # 3. 罗尔中值定理 (当f(a)=f(b)时的特例)
        self.play(
            FadeOut(lag_formula),
            FadeOut(c_label),
            FadeOut(c_point),
            FadeOut(lag_tangent_line),
            FadeOut(point_a),
            FadeOut(point_b),
            FadeOut(label_a),
            FadeOut(label_b),
            FadeOut(secant_line)
        )
        
        rolle_title = Text("罗尔中值定理 (f(a)=f(b)时的特例)", font="SimSun").scale(0.7)
        
        self.play(ReplacementTransform(lagrange_title, rolle_title))
        
        # 为罗尔定理选择函数值相等的两点
        # 对于f(t) = t^3 - 3t^2 + 2t = t(t-1)(t-2)，函数在t=0,1,2处为0
        rolle_a, rolle_b = 1, 2  # 选择t=1和t=2，使得f(1)=f(2)=0

        # 标记罗尔定理的端点 - 两个函数值相同的点
        rolle_point_a = Dot(axes.c2p(rolle_a, f(rolle_a)), color=PURPLE)
        rolle_point_b = Dot(axes.c2p(rolle_b, f(rolle_b)), color=PURPLE)
        rolle_label_a = MathTex("a").next_to(rolle_point_a, DOWN)
        rolle_label_b = MathTex("b").next_to(rolle_point_b, DOWN)
        
        self.play(
            Create(rolle_point_a),
            Create(rolle_point_b),
            Write(rolle_label_a),
            Write(rolle_label_b)
        )

        # 绘制罗尔区间的割线（水平线，因为f(a)=f(b)=0）
        rolle_secant = Line(
            axes.c2p(rolle_a, f(rolle_a)),
            axes.c2p(rolle_b, f(rolle_b)),
            color=PURPLE
        )
        self.play(Create(rolle_secant))

        # 修改f(a)=f(b)的显示方式（大约在第523行）
        # 将:
        equal_values = MathTex(r"f(a) = f(b) = 0").scale(0.7).next_to(rolle_title, UP)

        # 修改为:
        equal_values = MathTex(r"f(a) = f(b)").scale(0.7).next_to(rolle_title, UP)
        self.play(Write(equal_values))

        # 找到f'(c)=0的点
        # 解方程f'(c) = 0，即 3c^2 - 6c + 2 = 0
        # 这个方程有两个解：c ≈ 0.423 和 c ≈ 1.577
        # 对于区间[1,2]，我们需要使用1.577
        c_rolle = (6 + np.sqrt(12))/6  # 约等于1.577，在[1,2]区间内的极值点

        # 标记c点
        c_rolle_point = Dot(axes.c2p(c_rolle, f(c_rolle)), color=YELLOW)
        c_rolle_label = MathTex(r"\xi").next_to(c_rolle_point, DOWN)

        # 水平切线
        horizontal_tangent = Line(
            axes.c2p(c_rolle - 0.8, f(c_rolle)),
            axes.c2p(c_rolle + 0.8, f(c_rolle)),
            color=GREEN
        )

        self.play(
            Create(c_rolle_point),
            Write(c_rolle_label),
            Create(horizontal_tangent)
        )

        # 添加等待时间，让观众有时间观察水平切线
        self.wait(2)

        # 显示罗尔定理公式
        rolle_formula = MathTex(
            r"\exists \xi \in (a,b) : f'(\xi) = 0"
        ).scale(0.7).next_to(equal_values, UP, buff=0.2)
        self.play(Write(rolle_formula))

        # 再次等待，强调水平切线与公式的关系
        self.play(
            Indicate(horizontal_tangent, scale_factor=1.2, color=GREEN),
            Indicate(c_rolle_point, scale_factor=1.2, color=YELLOW),
            run_time=1.5
        )
        self.wait(1)

        # 清除所有内容，展示定理关系图
        self.play(
            *[FadeOut(mob) for mob in self.mobjects if mob != title]
        )
        
        # 创建定理关系图
        relation_diagram = VGroup()
        
        # 创建三个框和文本
        cauchy_box = Rectangle(height=1, width=4, color=BLUE)
        cauchy_text = Text("柯西中值定理", font="SimSun").scale(0.6)
        cauchy_group = VGroup(cauchy_box, cauchy_text).arrange(ORIGIN)
        
        lagrange_box = Rectangle(height=1, width=4, color=GREEN)
        lagrange_text = Text("拉格朗日中值定理", font="SimSun").scale(0.6)
        lagrange_group = VGroup(lagrange_box, lagrange_text).arrange(ORIGIN)
        
        rolle_box = Rectangle(height=1, width=4, color=RED)
        rolle_text = Text("罗尔中值定理", font="SimSun").scale(0.6)
        rolle_group = VGroup(rolle_box, rolle_text).arrange(ORIGIN)
        
        # 排列定理框
        relation_diagram.add(cauchy_group, lagrange_group, rolle_group)
        relation_diagram.arrange(DOWN, buff=1.5)
        
        # 添加箭头和说明
        arrow1 = Arrow(cauchy_group.get_bottom(), lagrange_group.get_top(), color=BLUE)
        arrow_text1 = Text("g(t)=t, g'(t)=1", font="SimSun").scale(0.4).next_to(arrow1, RIGHT)
        
        arrow2 = Arrow(lagrange_group.get_bottom(), rolle_group.get_top(), color=GREEN)
        arrow_text2 = Text("f(a)=f(b)", font="SimSun").scale(0.4).next_to(arrow2, RIGHT)
        
        # 创建公式组
        formulas = VGroup(
            MathTex(r"\frac{f'(\xi)}{g'(\xi)} = \frac{f(b)-f(a)}{g(b)-g(a)}").scale(0.5).next_to(cauchy_group, LEFT, buff=0.5),
            MathTex(r"f'(\xi) = \frac{f(b)-f(a)}{b-a}").scale(0.5).next_to(lagrange_group, LEFT, buff=0.5),
            MathTex(r"f'(\xi) = 0").scale(0.5).next_to(rolle_group, LEFT, buff=0.5)
        )
        
        # 组合所有元素
        final_diagram = VGroup(
            relation_diagram, 
            arrow1, arrow_text1, 
            arrow2, arrow_text2,
            formulas
        )
        
        final_diagram.move_to(ORIGIN)
        
        # 显示关系图
        self.play(Create(relation_diagram))
        self.play(Create(arrow1), Write(arrow_text1), Create(arrow2), Write(arrow_text2))
        self.play(Write(formulas))
        
        # 总结文字
        summary = Text(
            "三个中值定理展示了数学中特例与一般化的美妙关系", 
            font="SimSun"
        ).scale(0.6).to_edge(DOWN)
        
        self.play(Write(summary))
        
        self.wait(3)

    def find_cauchy_c(self, f, df, g, dg, a, b):
        """计算满足柯西中值定理的c值"""
        # 计算割线斜率
        secant_slope = (f(b) - f(a)) / (g(b) - g(a))
        
        # 定义方程 f'(\xi)/g'(\xi) = secant_slope
        def equation(x):
            return df(x) / dg(x) - secant_slope
        
        # 使用二分法求解
        left, right = a, b
        epsilon = 1e-10
        while right - left > epsilon:
            mid = (left + right) / 2
            if equation(mid) * equation(left) <= 0:
                right = mid
            else:
                left = mid
        
        return (left + right) / 2

    def find_lagrange_c(self, f, df, a, b):
        """计算满足拉格朗日中值定理的c值"""
        # 计算割线斜率
        secant_slope = (f(b) - f(a)) / (b - a)
        
        # 定义方程 f'(\xi) = secant_slope
        def equation(x):
            return df(x) - secant_slope
        
        # 使用二分法求解
        left, right = a, b
        epsilon = 1e-10
        while right - left > epsilon:
            mid = (left + right) / 2
            if equation(mid) * equation(left) <= 0:
                right = mid
            else:
                left = mid
        
        return (left + right) / 2 