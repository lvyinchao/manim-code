from manim import *
import numpy as np

class ImplicitFunctionTheorem(ThreeDScene):
    def construct(self):
        # 设置场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"include_tip": True, "include_ticks": True}
        )
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z", direction=OUT)
        labels = VGroup(x_label, y_label, z_label)
        
        # 添加标题
        title = Text("隐函数存在定理", font="SimHei")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        # 添加坐标轴
        self.add(axes, labels)
        self.play(
            FadeIn(axes),
            FadeIn(labels),
            Write(title)
        )
        self.wait(1)

        # 定义隐函数的例子：F(x,y) = x^2 + y^2 - 1 = 0 (圆)
        def F(x, y):
            return x**2 + y**2 - 1
        
        # 创建表面 z = F(x,y)
        surface = Surface(
            lambda u, v: np.array([u, v, F(u, v)]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # 添加隐函数表面
        self.play(Create(surface))
        self.wait(1)
        
        # 添加 z=0 的平面
        z_plane = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(2, 2),
            fill_opacity=0.5,
            fill_color=RED_A
        )
        
        # 添加平面
        self.play(Create(z_plane))
        self.wait(1)
        
        # 显示隐函数的曲线 (z=0 与表面的交线)
        def parametric_circle(t):
            return np.array([np.cos(t), np.sin(t), 0])
        
        curve = ParametricFunction(
            parametric_circle,
            t_range=[0, 2*PI],
            color=YELLOW,
            stroke_width=6
        )
        
        self.play(Create(curve))
        self.wait(1)
        
        # 解释隐函数定理
        explanation1 = Text("对于方程 F(x,y) = 0", font="SimHei", font_size=24)
        explanation2 = Text("如果 F 在点 (a,b) 连续可微且 ∂F/∂y ≠ 0", font="SimHei", font_size=24)
        explanation3 = Text("则存在函数 y = g(x) 使得 F(x,g(x)) = 0", font="SimHei", font_size=24)
        
        for exp in [explanation1, explanation2, explanation3]:
            exp.to_corner(DR)
            self.add_fixed_in_frame_mobjects(exp)
        
        # 显示说明文字
        self.play(Write(explanation1))
        self.wait(2)
        self.play(ReplacementTransform(explanation1, explanation2))
        self.wait(2)
        self.play(ReplacementTransform(explanation2, explanation3))
        self.wait(2)
        self.play(FadeOut(explanation3))
        
        # 选择一个点 (a,b) 并演示
        point_a = 0.7
        point_b = np.sqrt(1 - point_a**2)  # 在圆上的点
        point = Dot3D(point=[point_a, point_b, 0], color=RED, radius=0.1)
        
        # 显示点
        self.play(Create(point))
        
        # 显示该点处的法向量（梯度）
        gradient_vector = Arrow3D(
            start=[point_a, point_b, 0],
            end=[point_a, point_b, 0] + normalize([2*point_a, 2*point_b, 0]),
            color=GREEN
        )
        
        self.play(Create(gradient_vector))
        
        # 添加偏导数文字说明
        gradient_text = Text("∇F(a,b) = (∂F/∂x, ∂F/∂y) ≠ 0", font="SimHei", font_size=24)
        gradient_text.to_corner(DR)
        self.add_fixed_in_frame_mobjects(gradient_text)
        self.play(Write(gradient_text))
        self.wait(2)
        
        # 显示切线
        def tangent_line(t):
            # 圆的切线方程
            return np.array([point_a - t*point_b, point_b + t*point_a, 0])
        
        tangent = ParametricFunction(
            tangent_line,
            t_range=[-1, 1],
            color=PURPLE,
            stroke_width=4
        )
        
        self.play(Create(tangent))
        
        # 显示局部函数存在的解释
        local_text = Text("在点(a,b)附近存在唯一的函数 y = g(x)", font="SimHei", font_size=24)
        local_text.to_corner(DR)
        self.add_fixed_in_frame_mobjects(local_text)
        self.play(ReplacementTransform(gradient_text, local_text))
        self.wait(2)
        
        # 显示隐函数的二维投影
        self.play(
            FadeOut(surface),
            FadeOut(z_plane),
            FadeOut(gradient_vector),
            FadeOut(tangent)
        )
        
        self.move_camera(phi=0, theta=-90 * DEGREES)
        
        # 添加新的二维坐标轴
        axes_2d = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            axis_config={"include_tip": True}
        )
        
        # 显示局部函数的存在
        # 确保 (point_a + t)^2 <= 1，即 t 的范围需调整为不超出合理值
        # 计算安全的 t 范围
        t_min = max(-0.5, -1 - point_a + 0.01)  # 加上小偏移避免精度问题
        t_max = min(0.5, 1 - point_a - 0.01)

        local_curve = ParametricFunction(
            lambda t: np.array([point_a + t, np.sqrt(max(0, 1 - (point_a + t)**2)), 0]),
            t_range=[t_min, t_max],
            color=RED,
            stroke_width=6
        )
        
        self.play(
            FadeIn(axes_2d),
            ReplacementTransform(curve, curve.copy()),
            FadeIn(local_curve)
        )
        
        # 显示函数可微性的说明
        differentiable_text = Text("该函数在局部区域内连续可微", font="SimHei", font_size=24)
        differentiable_text.to_corner(DR)
        self.add_fixed_in_frame_mobjects(differentiable_text)
        self.play(ReplacementTransform(local_text, differentiable_text))
        self.wait(2)
        
        # 结论
        conclusion = Text("这就是隐函数存在定理的几何意义", font="SimHei", font_size=28)
        conclusion.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)


# 另一个例子：双曲线 x^2 - y^2 = 1
class HyperbolicExample(ThreeDScene):
    def construct(self):
        # 设置场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=-30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1]
        )
        
        # 添加标题
        title = Text("隐函数例子：双曲线", font="SimHei")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        
        self.add(axes)
        
        # 定义隐函数 F(x,y) = x^2 - y^2 - 1 = 0
        def F(x, y):
            return x**2 - y**2 - 1
        
        # 创建表面 z = F(x,y)
        surface = Surface(
            lambda u, v: np.array([u, v, F(u, v)]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[GREEN_D, GREEN_E]
        )
        
        self.play(Create(surface))
        
        # 添加 z=0 的平面
        z_plane = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(2, 2),
            fill_opacity=0.5,
            fill_color=RED_A
        )
        
        self.play(Create(z_plane))
        
        # 生成双曲线的两个分支
        def hyperbola_right(t):
            x = np.cosh(t)
            y = np.sinh(t)
            return np.array([x, y, 0])
            
        def hyperbola_left(t):
            x = -np.cosh(t)
            y = np.sinh(t)
            return np.array([x, y, 0])
        
        curve_right = ParametricFunction(
            hyperbola_right,
            t_range=[-2, 2],
            color=YELLOW,
            stroke_width=6
        )
        
        curve_left = ParametricFunction(
            hyperbola_left,
            t_range=[-2, 2],
            color=YELLOW,
            stroke_width=6
        )
        
        self.play(Create(curve_right), Create(curve_left))
        
        # 解释这里不能全局表示为一个函数
        explanation = Text("注意：双曲线不能全局表示为函数 y = g(x)", font="SimHei", font_size=24)
        explanation.to_corner(DR)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)
        
        # 但可以局部表示为函数
        local_explanation = Text("但可以局部表示为函数", font="SimHei", font_size=24)
        local_explanation.to_corner(DR)
        self.add_fixed_in_frame_mobjects(local_explanation)
        self.play(ReplacementTransform(explanation, local_explanation))
        
        # 选择一个点和局部区域
        point_a = 1.5
        point_b = np.sqrt(point_a**2 - 1)  # 在双曲线上的点
        point = Dot3D(point=[point_a, point_b, 0], color=RED, radius=0.1)
        
        self.play(Create(point))
        
        # 显示局部函数
        def local_function(t):
            x = point_a + t
            y = np.sqrt(x**2 - 1)
            return np.array([x, y, 0])
        
        local_curve = ParametricFunction(
            local_function,
            t_range=[-0.5, 0.5],
            color=RED,
            stroke_width=6
        )
        
        self.play(Create(local_curve))
        self.wait(2)
        
        # 结论
        conclusion = Text("隐函数定理保证了局部存在性", font="SimHei", font_size=28)
        conclusion.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)


def normalize(vector):
    """归一化向量"""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm 

# 隐函数求导演示
class ImplicitDifferentiation(Scene):
    def construct(self):
        # 添加标题
        title = Text("隐函数求导", font="SimHei")
        title.to_corner(UL)
        self.play(Write(title))
        self.wait(1)
        
        # 介绍隐函数
        implicit_example = MathTex(r"F(x, y) = 0")
        self.play(Write(implicit_example))
        self.wait(1)
        
        # 具体例子：圆 x^2 + y^2 = 1
        circle_eq = MathTex(r"x^2 + y^2 = 1")
        self.play(ReplacementTransform(implicit_example, circle_eq))
        self.wait(1)
        
        # 说明：假设y是x的函数
        assumption = Text("假设y是x的函数: y = f(x)", font="SimHei", font_size=28)
        assumption.next_to(circle_eq, DOWN, buff=0.5)
        self.play(Write(assumption))
        self.wait(1)
        
        # 代入方程
        substitution = MathTex(r"x^2 + [f(x)]^2 = 1")
        substitution.next_to(assumption, DOWN, buff=0.5)
        self.play(Write(substitution))
        self.wait(1)
        
        # 对两边求导
        derivative_step1 = MathTex(r"\frac{d}{dx}(x^2 + [f(x)]^2) = \frac{d}{dx}(1)")
        derivative_step1.next_to(substitution, DOWN, buff=0.5)
        self.play(Write(derivative_step1))
        self.wait(1)
        
        # 求导结果
        derivative_step2 = MathTex(r"2x + 2f(x)f'(x) = 0")
        derivative_step2.next_to(derivative_step1, DOWN, buff=0.5)
        self.play(Write(derivative_step2))
        self.wait(1)
        
        # 解出f'(x)
        derivative_step3 = MathTex(r"f'(x) = -\frac{x}{f(x)}")
        derivative_step3.next_to(derivative_step2, DOWN, buff=0.5)
        self.play(Write(derivative_step3))
        self.wait(1)
        
        # 清除前面的内容，展示隐函数求导公式
        self.play(
            FadeOut(circle_eq),
            FadeOut(assumption),
            FadeOut(substitution),
            FadeOut(derivative_step1),
            FadeOut(derivative_step2),
            FadeOut(derivative_step3)
        )
        
        # 展示一般隐函数求导公式
        general_formula_title = Text("隐函数求导公式", font="SimHei", font_size=32)
        general_formula_title.to_edge(UP)
        self.play(Write(general_formula_title))
        
        # 修改：分离中文和数学公式
        formula1_text1 = Text("若", font="SimHei")
        formula1_math1 = MathTex(r"F(x, y) = 0")
        formula1_text2 = Text("且", font="SimHei")
        formula1_math2 = MathTex(r"y = f(x)")
        
        formula1_group = VGroup(formula1_text1, formula1_math1, formula1_text2, formula1_math2).arrange(RIGHT, buff=0.2)
        formula1_group.next_to(general_formula_title, DOWN, buff=0.5)
        
        # 修改：分离中文和数学公式
        formula2_text = Text("则", font="SimHei")
        formula2_math = MathTex(r"\frac{dy}{dx} = -\frac{\frac{\partial F}{\partial x}}{\frac{\partial F}{\partial y}}")
        
        formula2_group = VGroup(formula2_text, formula2_math).arrange(RIGHT, buff=0.2)
        formula2_group.next_to(formula1_group, DOWN, buff=0.5)
        
        self.play(Write(formula1_group), Write(formula2_group))
        self.wait(1)
        
        # 演示几何意义
        self.play(
            FadeOut(formula1_group),
            FadeOut(formula2_group)
        )
        
        # 创建坐标系
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=6
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # 创建圆
        circle = Circle(radius=2, color=BLUE)  # 半径应与坐标系匹配
        # 将圆调整到合适的位置和大小
        circle = Circle(radius=1, color=BLUE)
        circle.move_to(axes.coords_to_point(0, 0))
        circle.scale_to_fit_width(2 * axes.get_x_unit_size())
        
        # 显示坐标系和圆
        self.play(
            Create(axes),
            Create(axes_labels)
        )
        self.play(Create(circle))
        
        # 选择圆上的一点 - 不要选择(1,0)这样的特殊点
        point_on_circle_x = 0.7  # 选择一个安全的x值
        point_on_circle_y = np.sqrt(1 - point_on_circle_x**2)  # 在单位圆上的点

        point = Dot(axes.coords_to_point(point_on_circle_x, point_on_circle_y), color=RED)
        point_label = MathTex("(x, y)").next_to(point, UR, buff=0.1)
        
        self.play(Create(point), Write(point_label))
        
        # 切线
        slope = -point_on_circle_x / point_on_circle_y  # dy/dx 的值
        
        # 创建切线
        def get_tangent_line(x):
            return slope * (x - point_on_circle_x) + point_on_circle_y
            
        tangent = axes.plot(
            lambda x: get_tangent_line(x),
            x_range=[point_on_circle_x-1, point_on_circle_x+1],
            color=GREEN
        )
        
        # 显示切线
        self.play(Create(tangent))
        
        # 添加斜率标签
        slope_text = Text("斜率 =", font="SimHei")
        slope_value = MathTex(f"{slope:.2f}")
        slope_label = VGroup(slope_text, slope_value).arrange(RIGHT, buff=0.2)
        slope_label.next_to(tangent, UR, buff=0.5)
        self.play(Write(slope_label))
        
        # 添加求导公式对应的解释
        explanation_math = MathTex(r"\frac{dy}{dx} = -\frac{x}{y} = " + f"{slope:.2f}")
        explanation_math.to_edge(DOWN, buff=1)
        self.play(Write(explanation_math))
        
        # 计算偏导数
        partial_x = MathTex(r"\frac{\partial F}{\partial x} = 2x")
        partial_y = MathTex(r"\frac{\partial F}{\partial y} = 2y")
        
        partial_group = VGroup(partial_x, partial_y).arrange(DOWN, buff=0.3)
        partial_group.to_corner(DR)
        
        self.play(Write(partial_group))
        
        # 显示梯度向量
        # 梯度向量应该是 (2x, 2y)，对于圆函数 x^2 + y^2 = 1
        gradient_scale = 0.5  # 调整梯度向量的大小
        gradient_vector = Arrow(
            start=axes.coords_to_point(point_on_circle_x, point_on_circle_y),
            end=axes.coords_to_point(
                point_on_circle_x + gradient_scale * 2 * point_on_circle_x,
                point_on_circle_y + gradient_scale * 2 * point_on_circle_y
            ),
            buff=0,
            color=YELLOW,
            max_tip_length_to_length_ratio=0.2
        )
        
        gradient_label = Text("梯度 ∇F", font="SimHei", font_size=20).next_to(gradient_vector, UL)
        
        self.play(Create(gradient_vector), Write(gradient_label))
        
        # 解释切线与梯度正交
        orthogonal_explanation = Text("切线与梯度正交", font="SimHei", font_size=24)
        orthogonal_explanation.to_edge(DOWN)
        
        self.play(ReplacementTransform(explanation_math, orthogonal_explanation))
        
        # 总结
        self.wait(1)
        summary = Text("隐函数求导是求解曲线上点的斜率的有力工具", font="SimHei", font_size=28)
        summary.to_edge(DOWN)
        
        self.play(ReplacementTransform(orthogonal_explanation, summary))
        self.wait(2)
        
        # 添加二阶导数提示（可选）
        second_derivative = Text("还可以求二阶导数等更高阶导数", font="SimHei", font_size=24)
        second_derivative.to_edge(DOWN)
        
        self.play(ReplacementTransform(summary, second_derivative))
        self.wait(2)
        
        # 结束
        self.play(
            FadeOut(second_derivative),
            FadeOut(partial_group),
            FadeOut(gradient_vector),
            FadeOut(gradient_label),
            FadeOut(slope_label),
            FadeOut(tangent),
            FadeOut(point),
            FadeOut(point_label),
            FadeOut(circle),
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(title),
            FadeOut(general_formula_title)
        ) 

# 曲线上点移动时切线斜率变化展示
class MovingDerivativeDemo(Scene):
    def construct(self):
        # 添加标题
        title = Text("隐函数的切线斜率变化", font="SimHei")
        title.to_corner(UL)
        self.play(Write(title))
        self.wait(1)
        
        # 创建坐标系
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            axis_config={"include_tip": True},
            x_length=6,
            y_length=6
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # 显示坐标系
        self.play(
            Create(axes),
            Create(axes_labels)
        )
        
        # 定义隐函数 F(x,y) = x^2 + y^2 - 1 = 0 (单位圆)
        equation = MathTex(r"F(x,y) = x^2 + y^2 - 1 = 0")
        equation.to_edge(UP)
        self.play(Write(equation))
        
        # 创建圆
        circle = Circle(radius=1, color=BLUE)
        circle.move_to(axes.coords_to_point(0, 0))
        circle.scale_to_fit_width(2 * axes.get_x_unit_size())
        
        # 显示圆
        self.play(Create(circle))
        self.wait(1)
        
        # 创建在圆上移动的点
        def get_point_on_circle(t):
            # 参数方程：x = cos(t), y = sin(t)
            return axes.coords_to_point(np.cos(t), np.sin(t))
        
        moving_point = Dot(get_point_on_circle(0), color=RED)
        point_label = MathTex("P(x,y)").next_to(moving_point, UR, buff=0.1)
        point_label.add_updater(lambda m: m.next_to(moving_point, UR, buff=0.1))
        
        self.play(Create(moving_point), Write(point_label))
        
        # 创建切线
        def get_tangent_points(t):
            x = np.cos(t)
            y = np.sin(t)
            # 圆的切线斜率 = -x/y
            slope = -x/y if abs(y) > 0.01 else -1000 * np.sign(x)  # 避免除以0
            
            x_range = 1.0  # 切线延伸范围
            x1 = x - x_range
            y1 = y + slope * (-x_range)
            x2 = x + x_range
            y2 = y + slope * x_range
            
            return [axes.coords_to_point(x1, y1), axes.coords_to_point(x2, y2)]
        
        tangent_line = Line(*get_tangent_points(0), color=GREEN)
        
        # 更新切线位置
        def update_tangent(line, t_val):
            new_points = get_tangent_points(t_val)
            line.put_start_and_end_on(*new_points)
            return line
        
        self.play(Create(tangent_line))
        
        # 创建偏导数和斜率显示
        def get_derivative_values(t):
            x = np.cos(t)
            y = np.sin(t)
            df_dx = 2*x  # ∂F/∂x
            df_dy = 2*y  # ∂F/∂y
            slope = -df_dx/df_dy if abs(df_dy) > 0.01 else -1000 * np.sign(df_dx)  # -∂F/∂x ÷ ∂F/∂y
            return df_dx, df_dy, slope
        
        dx_val, dy_val, slope_val = get_derivative_values(0)
        
        # 显示偏导数
        derivatives_tex = MathTex(
            r"\frac{\partial F}{\partial x} = ", f"{dx_val:.2f},\\",
            r"\frac{\partial F}{\partial y} = ", f"{dy_val:.2f}"
        ).scale(0.7)
        derivatives_tex.to_corner(DL)
        self.add_fixed_in_frame_mobjects(derivatives_tex)
        self.play(Write(derivatives_tex))
        
        # 计算切线方向 - 对于曲面 z = F(x,y) 与平面 z = 1 的交线
        tangent_vector = np.array([-dy_val, dx_val, 0])
        tangent_vector = tangent_vector / np.linalg.norm(tangent_vector) * 0.5
        
        # 创建切线
        tangent_start = axes.coords_to_point(point_on_circle_x, point_on_circle_y) - tangent_vector * 0.5
        tangent_end = axes.coords_to_point(point_on_circle_x, point_on_circle_y) + tangent_vector * 0.5
        tangent_line = Line(
            start=tangent_start,
            end=tangent_end,
            color=GREEN
        )
        
        # 显示切线
        self.play(Create(tangent_line))
        
        # 添加斜率标签
        slope_text = Text("斜率 =", font="SimHei").scale(0.6)
        slope_math = MathTex(r"\propto \left(-\frac{\partial F}{\partial y}, \frac{\partial F}{\partial x}, 0\right)").scale(0.7)
        slope_formula = VGroup(slope_text, slope_math).arrange(RIGHT, buff=0.2)
        slope_formula.next_to(derivatives_tex, UP)
        self.add_fixed_in_frame_mobjects(slope_formula)
        self.play(Write(slope_formula))
        
        # 添加法向量
        normal_vector = np.array([dx_val, dy_val, -1])  # 梯度 (∂F/∂x, ∂F/∂y, -1)
        normal_vector = normal_vector / np.linalg.norm(normal_vector) * 0.5  # 归一化并缩放
        
        normal_arrow = Arrow3D(
            start=axes.coords_to_point(point_on_circle_x, point_on_circle_y),
            end=axes.coords_to_point(point_on_circle_x, point_on_circle_y) + normal_vector * 0.5,
            color=YELLOW
        )
        
        # 显示法向量
        self.play(Create(normal_arrow))
        
        # 显示法向量说明
        normal_label = Text("法向量", font="SimHei").scale(0.5)
        self.add_fixed_in_frame_mobjects(normal_label)
        normal_label.to_edge(UP, buff=1)  # 改为固定位置，避免与其他元素重叠
        self.play(Write(normal_label))
        
        # 添加对偏导数关系与隐函数的解释
        explanation_tx = Text("当z=1与曲面相交时", font="SimHei", font_size=20)
        explanation_tx.to_edge(DOWN, buff=0.8)
        self.add_fixed_in_frame_mobjects(explanation_tx)
        
        # 添加偏导数与隐函数导数的关系公式
        relationship = MathTex(
            r"\frac{dy}{dx} = -\frac{\frac{\partial F}{\partial x}}{\frac{\partial F}{\partial y}} = -\frac{2x}{2y}"
        ).scale(0.7)
        relationship.next_to(explanation_tx, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(relationship)
        
        self.play(Write(explanation_tx), Write(relationship))
        self.wait(2)
        
        # 更详细地解释隐函数定理的应用
        detail_explanation = Text(
            "这就是隐函数定理：在曲面与水平面的交线上，"
            "曲面的偏导数决定了隐函数的导数", 
            font="SimHei", 
            font_size=18
        )
        detail_explanation.next_to(relationship, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(detail_explanation)
        self.play(Write(detail_explanation))
        self.wait(2)
        
        # 在开始动画演示前清理这些解释文字
        self.play(
            FadeOut(explanation_tx),
            FadeOut(relationship),
            FadeOut(detail_explanation)
        )
        
        # 动画展示：点在曲线上移动，切线和法向量跟随变化
        self.wait(1)
        
        # 使用关键帧动画而不是updater
        # 定义几个关键帧位置
        key_frames = [0, PI/4, PI/2, 3*PI/4, PI, 5*PI/4, 3*PI/2, 7*PI/4, 2*PI]
        
        # 为每个关键帧创建对象
        for i, t_val in enumerate(key_frames):
            if i == 0:  # 第一帧已经创建
                continue
                
            # 计算新的点坐标
            new_coords = get_point_on_circle(t_val)
            x, y = new_coords
            
            # 创建新点
            new_point = Dot(axes.coords_to_point(x, y), color=RED)
            
            # 创建新标签
            new_label = MathTex("P(x,y)").next_to(new_point, UR, buff=0.1)
            
            # 计算新的切线和法向量
            dx, dy = get_derivative_values(t_val)
            
            # 创建新的偏导数文本
            new_derivatives = MathTex(
                r"\frac{\partial F}{\partial x} = ", f"{dx:.2f},\\",
                r"\frac{\partial F}{\partial y} = ", f"{dy:.2f}"
            ).scale(0.7)
            new_derivatives.to_corner(DL)
            
            # 计算新的切线
            tangent_vector = np.array([-dy, dx, 0])
            tangent_vector = tangent_vector / np.linalg.norm(tangent_vector) * 0.5
            
            new_tangent = Line(
                start=new_coords - tangent_vector,
                end=new_coords + tangent_vector,
                color=GREEN
            )
            
            # 计算新的法向量
            normal_vector = np.array([dx, dy, -1])
            normal_vector = normal_vector / np.linalg.norm(normal_vector) * 0.5
            
            new_normal = Arrow(
                start=new_coords,
                end=new_coords + normal_vector,
                color=YELLOW
            )
            
            # 动画转换到新帧
            self.play(
                Transform(moving_point, new_point),
                Transform(moving_point_label, new_label),
                Transform(tangent_line, new_tangent),
                Transform(normal_arrow, new_normal),
                Transform(derivatives_tex, new_derivatives),
                run_time=0.5
            )
        
        # 结束
        self.wait(1)
        conclusion = Text("隐函数定理在三维中的直观解释", font="SimHei")
        conclusion.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(2)
        
        # 清理场景
        self.play(
            FadeOut(moving_point),
            FadeOut(tangent_line),
            FadeOut(normal_arrow),
            FadeOut(point_label),
            FadeOut(circle),
            FadeOut(equation),
            FadeOut(axes),
            FadeOut(axes_labels),
            FadeOut(title)
        )
        self.remove_fixed_in_frame_mobjects(
            title,
            equation,
            moving_point_label,
            derivatives_tex,
            conclusion
        )
        self.wait(1) 

# 三维曲面上的隐函数定理演示
class ImplicitFunction3D(ThreeDScene):
    def construct(self):
        # 设置场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # 添加标题
        title = Text("三维曲面上的隐函数定理", font="SimHei")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        
        # 创建坐标系
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 4, 1],
            axis_config={"include_tip": True, "include_ticks": True}
        )
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z", direction=OUT)
        labels = VGroup(x_label, y_label, z_label)
        
        # 添加坐标轴和标签
        self.play(Create(axes), Create(labels))
        
        # 定义函数 F(x,y) = x^2 + y^2
        function_tex = MathTex(r"z = F(x,y) = x^2 + y^2")
        function_tex.to_corner(UR)
        self.add_fixed_in_frame_mobjects(function_tex)
        self.play(Write(function_tex))
        
        # 创建曲面 z = x^2 + y^2
        surface = Surface(
            lambda u, v: np.array([u, v, u**2 + v**2]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # 显示曲面
        self.play(Create(surface))
        self.wait(1)
        
        # 创建水平截面 z = 1
        z_level = 1
        plane = Surface(
            lambda u, v: np.array([u, v, z_level]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(2, 2),
            fill_opacity=0.5,
            fill_color=RED_A
        )
        
        # 显示水平截面
        self.play(Create(plane))
        self.wait(1)
        
        # 显示隐函数定义
        implicit_tex = MathTex(r"F(x,y) - z = 0 \Rightarrow x^2 + y^2 - 1 = 0")
        implicit_tex.next_to(function_tex, DOWN)
        self.add_fixed_in_frame_mobjects(implicit_tex)
        self.play(Write(implicit_tex))
        
        # 添加投影柱面的可视化 - 显示从点到xy平面的投影关系
        point_radius = 0.7  # 在圆上选择一个点的位置
        point_angle = PI/4  # 选择角度为45度的位置
        point_x = point_radius * np.cos(point_angle)
        point_y = point_radius * np.sin(point_angle)
        point_z = point_x**2 + point_y**2  # 曲面上的z值
        
        # 创建投影点和连线
        projection_point = Dot3D(point=[point_x, point_y, 0], color=BLUE, radius=0.05)
        surface_point = Dot3D(point=[point_x, point_y, point_z], color=RED, radius=0.05)
        projection_line = Line3D(
            start=[point_x, point_y, 0],
            end=[point_x, point_y, point_z],
            color=YELLOW
        )
        
        # 显示投影
        self.play(Create(projection_point), Create(surface_point), Create(projection_line))
        
        # 添加说明文字
        projection_label = Text("投影点", font="SimHei", font_size=18).scale(0.7)
        projection_label.next_to(projection_point, DOWN)
        self.add_fixed_in_frame_mobjects(projection_label)
        
        surface_label = Text("曲面点", font="SimHei", font_size=18).scale(0.7)
        surface_label.next_to(surface_point, UP)
        self.add_fixed_in_frame_mobjects(surface_label)
        
        self.play(Write(projection_label), Write(surface_label))
        self.wait(1)
        
        # 展示偏导数的几何意义
        # 创建x方向的小位移 - 展示∂z/∂x
        delta = 0.2
        dx_point = Dot3D(point=[point_x + delta, point_y, 0], color=GREEN, radius=0.05)
        dx_surface_point = Dot3D(
            point=[point_x + delta, point_y, (point_x + delta)**2 + point_y**2], 
            color=GREEN, 
            radius=0.05
        )
        dx_line = Line3D(
            start=[point_x + delta, point_y, 0],
            end=[point_x + delta, point_y, (point_x + delta)**2 + point_y**2],
            color=GREEN
        )
        
        # 显示x方向的偏导
        self.play(Create(dx_point), Create(dx_surface_point), Create(dx_line))
        
        # 连接曲面上的两点，展示偏导
        partial_x_line = Line3D(
            start=[point_x, point_y, point_z],
            end=[point_x + delta, point_y, (point_x + delta)**2 + point_y**2],
            color=GREEN
        )
        self.play(Create(partial_x_line))
        
        # 添加偏导数公式
        dx_value = 2 * point_x  # ∂F/∂x = 2x
        dx_label = Text(f"∂z/∂x ≈ {dx_value:.2f}", font="SimHei", font_size=18).scale(0.7)
        dx_label.next_to(partial_x_line, RIGHT)
        self.add_fixed_in_frame_mobjects(dx_label)
        self.play(Write(dx_label))
        
        # 展示y方向的偏导
        dy_point = Dot3D(point=[point_x, point_y + delta, 0], color=PURPLE, radius=0.05)
        dy_surface_point = Dot3D(
            point=[point_x, point_y + delta, point_x**2 + (point_y + delta)**2], 
            color=PURPLE, 
            radius=0.05
        )
        dy_line = Line3D(
            start=[point_x, point_y + delta, 0],
            end=[point_x, point_y + delta, point_x**2 + (point_y + delta)**2],
            color=PURPLE
        )
        
        # 显示y方向的偏导
        self.play(Create(dy_point), Create(dy_surface_point), Create(dy_line))
        
        # 连接曲面上的两点，展示偏导
        partial_y_line = Line3D(
            start=[point_x, point_y, point_z],
            end=[point_x, point_y + delta, point_x**2 + (point_y + delta)**2],
            color=PURPLE
        )
        self.play(Create(partial_y_line))
        
        # 添加偏导数公式
        dy_value = 2 * point_y  # ∂F/∂y = 2y
        dy_label = Text(f"∂z/∂y ≈ {dy_value:.2f}", font="SimHei", font_size=18).scale(0.7)
        dy_label.next_to(partial_y_line, LEFT)
        self.add_fixed_in_frame_mobjects(dy_label)
        self.play(Write(dy_label))
        
        self.wait(2)
        
        # 解释这些偏导数如何定义隐函数上的导数
        explanation = Text("在曲面z=f(x,y)上，偏导数∂z/∂x和∂z/∂y决定了曲面的局部形状", font="SimHei", font_size=20)
        explanation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)
        
        # 清理这些额外的元素，继续原有的演示
        self.play(
            FadeOut(projection_point), 
            FadeOut(surface_point), 
            FadeOut(projection_line),
            FadeOut(dx_point), 
            FadeOut(dx_surface_point), 
            FadeOut(dx_line),
            FadeOut(dy_point), 
            FadeOut(dy_surface_point), 
            FadeOut(dy_line),
            FadeOut(partial_x_line),
            FadeOut(partial_y_line)
        )
        self.remove_fixed_in_frame_mobjects(
            projection_label,
            surface_label,
            dx_label,
            dy_label,
            explanation
        )
        
        # 创建曲面与平面的交线(圆)
        def param_circle(t):
            # 圆的参数方程 x = cos(t), y = sin(t), z = 1
            return np.array([np.cos(t), np.sin(t), z_level])
        
        circle = ParametricFunction(
            param_circle,
            t_range=[0, 2*PI],
            color=YELLOW,
            stroke_width=6
        )
        
        # 显示交线
        self.play(Create(circle))
        self.wait(1)
        
        # 选择交线上的一点
        t_initial = PI/4  # 初始角度
        point_coords = param_circle(t_initial)
        point = Sphere(radius=0.05, color=RED).move_to(point_coords)
        
        # 添加点的坐标标签
        x_val, y_val, z_val = point_coords
        point_label = Text(f"P({x_val:.2f}, {y_val:.2f}, {z_val:.2f})", font="SimHei").scale(0.7)
        point_label.next_to(point, UP+RIGHT)
        self.add_fixed_in_frame_mobjects(point_label)
        
        # 显示点
        self.play(Create(point), Write(point_label))
        
        # 计算该点处的偏导数
        def get_partial_derivatives(x, y):
            df_dx = 2*x  # ∂F/∂x
            df_dy = 2*y  # ∂F/∂y
            return df_dx, df_dy
        
        dx_val, dy_val = get_partial_derivatives(x_val, y_val)
        
        # 显示偏导数
        derivatives_tex = MathTex(
            r"\frac{\partial F}{\partial x} = ", f"{dx_val:.2f},\\",
            r"\frac{\partial F}{\partial y} = ", f"{dy_val:.2f}"
        ).scale(0.7)
        derivatives_tex.to_corner(DL)
        self.add_fixed_in_frame_mobjects(derivatives_tex)
        self.play(Write(derivatives_tex))
        
        # 计算切线方向 - 对于曲面 z = F(x,y) 与平面 z = 1 的交线
        tangent_vector = np.array([-dy_val, dx_val, 0])
        tangent_vector = tangent_vector / np.linalg.norm(tangent_vector)  # 归一化
        
        # 创建切线
        tangent_start = point_coords - tangent_vector * 0.5
        tangent_end = point_coords + tangent_vector * 0.5
        tangent_line = Line3D(
            start=tangent_start,
            end=tangent_end,
            color=GREEN
        )
        
        # 显示切线
        self.play(Create(tangent_line))
        
        # 显示切线斜率公式
        slope_text = Text("切线方向", font="SimHei").scale(0.6)
        slope_math = MathTex(r"\propto \left(-\frac{\partial F}{\partial y}, \frac{\partial F}{\partial x}, 0\right)").scale(0.7)
        slope_formula = VGroup(slope_text, slope_math).arrange(RIGHT, buff=0.2)
        slope_formula.next_to(derivatives_tex, UP)
        self.add_fixed_in_frame_mobjects(slope_formula)
        self.play(Write(slope_formula))
        
        # 添加法向量
        normal_vector = np.array([dx_val, dy_val, -1])  # 梯度 (∂F/∂x, ∂F/∂y, -1)
        normal_vector = normal_vector / np.linalg.norm(normal_vector) * 0.5  # 归一化并缩放
        
        normal_arrow = Arrow3D(
            start=point_coords,
            end=point_coords + normal_vector,
            color=YELLOW
        )
        
        # 显示法向量
        self.play(Create(normal_arrow))
        
        # 显示法向量说明
        normal_label = Text("法向量", font="SimHei").scale(0.5)
        self.add_fixed_in_frame_mobjects(normal_label)
        normal_label.to_edge(UP, buff=1)  # 改为固定位置，避免与其他元素重叠
        self.play(Write(normal_label))
        
        # 添加对偏导数关系与隐函数的解释
        explanation_tx = Text("当z=1与曲面相交时", font="SimHei", font_size=20)
        explanation_tx.to_edge(DOWN, buff=0.8)
        self.add_fixed_in_frame_mobjects(explanation_tx)
        
        # 添加偏导数与隐函数导数的关系公式
        relationship = MathTex(
            r"\frac{dy}{dx} = -\frac{\frac{\partial F}{\partial x}}{\frac{\partial F}{\partial y}} = -\frac{2x}{2y}"
        ).scale(0.7)
        relationship.next_to(explanation_tx, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(relationship)
        
        self.play(Write(explanation_tx), Write(relationship))
        self.wait(2)
        
        # 更详细地解释隐函数定理的应用
        detail_explanation = Text(
            "这就是隐函数定理：在曲面与水平面的交线上，"
            "曲面的偏导数决定了隐函数的导数", 
            font="SimHei", 
            font_size=18
        )
        detail_explanation.next_to(relationship, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(detail_explanation)
        self.play(Write(detail_explanation))
        self.wait(2)
        
        # 在开始动画演示前清理这些解释文字
        self.play(
            FadeOut(explanation_tx),
            FadeOut(relationship),
            FadeOut(detail_explanation)
        )
        
        # 动画展示：点在曲线上移动，切线和法向量跟随变化
        self.wait(1)
        
        # 使用关键帧动画而不是updater
        # 定义几个关键帧位置
        key_frames = [0, PI/4, PI/2, 3*PI/4, PI, 5*PI/4, 3*PI/2, 7*PI/4, 2*PI]
        
        # 为每个关键帧创建对象
        for i, t_val in enumerate(key_frames):
            if i == 0:  # 第一帧已经创建
                continue
                
            # 计算新的点坐标
            new_coords = param_circle(t_val)
            x, y, z = new_coords
            
            # 创建新点
            new_point = Sphere(radius=0.05, color=RED).move_to(new_coords)
            
            # 创建新标签
            new_label = Text(f"P({x:.2f}, {y:.2f}, {z:.2f})", font="SimHei").scale(0.7)
            new_label.move_to(point_label.get_center())
            
            # 计算新的切线和法向量
            dx, dy = get_partial_derivatives(x, y)
            
            # 创建新的偏导数文本
            new_derivatives = MathTex(
                r"\frac{\partial F}{\partial x} = ", f"{dx:.2f},\\",
                r"\frac{\partial F}{\partial y} = ", f"{dy:.2f}"
            ).scale(0.7)
            new_derivatives.to_corner(DL)
            
            # 计算新的切线
            tangent_vector = np.array([-dy, dx, 0])
            tangent_vector = tangent_vector / np.linalg.norm(tangent_vector) * 0.5
            
            new_tangent = Line3D(
                start=new_coords - tangent_vector,
                end=new_coords + tangent_vector,
                color=GREEN
            )
            
            # 计算新的法向量
            normal_vector = np.array([dx, dy, -1])
            normal_vector = normal_vector / np.linalg.norm(normal_vector) * 0.5
            
            new_normal = Arrow3D(
                start=new_coords,
                end=new_coords + normal_vector,
                color=YELLOW
            )
            
            # 动画转换到新帧
            self.play(
                Transform(point, new_point),
                Transform(point_label, new_label),
                Transform(tangent_line, new_tangent),
                Transform(normal_arrow, new_normal),
                run_time=0.5
            )
        
        # 结束
        self.wait(1)
        conclusion = Text("隐函数定理在三维中的直观解释", font="SimHei")
        conclusion.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(2)
        
        # 清理场景
        self.play(
            FadeOut(point),
            FadeOut(point_label),
            FadeOut(circle),
            FadeOut(surface),
            FadeOut(plane),
            FadeOut(axes),
            FadeOut(labels)
        )
        self.remove_fixed_in_frame_mobjects(
            title,
            function_tex,
            implicit_tex,
            derivatives_tex,
            slope_formula,
            normal_label,
            conclusion
        )
        self.wait(1) 