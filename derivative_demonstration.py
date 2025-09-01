from manim import *

# 配置中文环境
class DerivativeDefinition(Scene):
    def construct(self):
        # 使用黑色背景
        self.camera.background_color = BLACK
        
        # 创建坐标系 - 不显示数值
        axes = Axes(
            x_range=[-1, 4, 1],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": BLUE, "include_numbers": False},  # 移除数值
            x_length=6,
            y_length=6
        )
        
        # 创建坐标轴标签，并手动调整y标签位置
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y").shift(DOWN * 0.5)  # 将y标签下移
        axes_labels = VGroup(x_label, y_label)
        
        # 创建新函数 f(x) = sin(x)，但只用通用表达式显示
        func = lambda x: np.sin(x)
        graph = axes.plot(func, color=BLUE, stroke_width=3)
        
        # 修改为通用表达式 y = f(x)
        func_label = MathTex("y = f(x)").next_to(graph, UP).shift(RIGHT)
        
        # 选择点 x₀ = π/4 (原来的a)
        x0 = np.pi/4
        point_x0 = axes.coords_to_point(x0, func(x0))
        dot_x0 = Dot(point_x0, color=YELLOW, radius=0.08)  # 稍微增大点的半径
        
        # 添加点x₀的标签
        x0_label = MathTex("x_0").next_to(dot_x0, DOWN+RIGHT, buff=0.1).scale(0.9)
        
        # 创建切线 - 提前创建，一直显示
        exact_derivative = np.cos(x0)  # sin(x)的导数是cos(x)
        tangent_slope = exact_derivative
        tangent_line = Line(
            start=axes.coords_to_point(x0 - 2, func(x0) - 2*tangent_slope),  # 延长切线
            end=axes.coords_to_point(x0 + 2, func(x0) + 2*tangent_slope),    # 延长切线
            color=RED,
            stroke_width=2.5
        )
        
        # 创建切线标签
        tangent_label = Text("切线", font="SimSun", color=RED).scale(0.7)
        # 将标签定位到切线的左下角
        tangent_label.next_to(
            axes.coords_to_point(x0 - 1.5, func(x0) - 1.5*tangent_slope),  # 切线左下方的点
            DOWN + LEFT,  # 放在这个点的左下方
            buff=0.2
        )
        
        # 最终结论: 切线斜率 = 计算公式 = f'(x0)
        final_conclusion_1 = Text("切线斜率 =", font="SimSun").scale(0.7).to_corner(UL, buff=0.3)
        final_conclusion_2 = MathTex("\\lim_{\\Delta x \\to 0} \\frac{f(x_0+\\Delta x) - f(x_0)}{\\Delta x} = f'(x_0)").scale(0.7).next_to(final_conclusion_1, RIGHT, buff=0.1)
        
        # 在右侧显示割线斜率计算公式 - 调整为两行显示，并向右移动
        secant_slope_text = Text("割线斜率 =", font="SimSun").scale(0.7).to_edge(RIGHT, buff=2.0).shift(RIGHT * 1.0)  # 减小右边距，并额外右移
        secant_slope_formula_1 = MathTex("\\frac{f(x_0+\\Delta x) - f(x_0)}{\\Delta x}").scale(0.7).next_to(secant_slope_text, DOWN, buff=0.3).align_to(secant_slope_text, RIGHT)  # 对齐右侧
        
        # 初始设置
        self.play(
            Create(axes),
            Write(axes_labels),
            Create(graph),
            Write(func_label)
        )
        self.play(Create(dot_x0), Write(x0_label))
        self.wait()
        
        # 先显示切线，然后显示切线标签
        self.play(Create(tangent_line))
        self.play(Write(tangent_label))  # 添加切线标签
        self.add(tangent_line)  # 确保切线始终可见
        
        # 使用ValueTracker实现连续动画 - 变量h改为delta_x
        delta_x_tracker = ValueTracker(2.0)  # 起始Δx值更大，更明显
        
        # 创建依赖于delta_x_tracker的动态对象
        def get_secant_point():
            delta_x = delta_x_tracker.get_value()
            return axes.coords_to_point(x0 + delta_x, func(x0 + delta_x))
        
        dot_x0_plus_delta = Dot(color=GREEN, radius=0.08)
        dot_x0_plus_delta.add_updater(lambda d: d.move_to(get_secant_point()))
        
        # 添加x₀+Δx标签
        x0_plus_delta_label = MathTex("x_0 + \\Delta x").scale(0.8)
        x0_plus_delta_label.add_updater(
            lambda l: l.next_to(dot_x0_plus_delta, UP+RIGHT, buff=0.1)
        )
        
        # 创建延长的割线
        secant_line = Line(color=GREEN, stroke_width=4.0)
        
        # 更新函数，使割线延长
        def update_secant_line(line):
            delta_x = delta_x_tracker.get_value()
            end_point = axes.coords_to_point(x0 + delta_x, func(x0 + delta_x))
            
            # 计算延长线的向量方向
            direction = end_point - point_x0
            direction = direction / np.linalg.norm(direction)
            
            # 延长线的起点和终点
            extended_start = point_x0 - direction * 3  # 向后延长
            extended_end = end_point + direction * 3  # 向前延长
            
            line.put_start_and_end_on(extended_start, extended_end)
            return line
        
        secant_line.add_updater(update_secant_line)
        
        # 动态更新Δx值显示
        delta_x_label = Text("", font="SimSun")
        delta_x_label.add_updater(
            lambda t: t.become(
                Text(f"Δx = {delta_x_tracker.get_value():.2f}", font="SimSun")
            ).next_to(secant_slope_formula_1, DOWN, buff=0.3)
        )
        
        # 1. 首先显示割线和点 - 修改显示顺序
        self.play(Create(dot_x0_plus_delta), Write(x0_plus_delta_label), Create(secant_line))
        self.wait()
        
        # 2. 然后显示割线斜率计算公式 - 修改为两行显示
        self.play(Write(secant_slope_text), Write(secant_slope_formula_1), Write(delta_x_label))
        
        # 突出显示当前公式，表示极限过程
        limit_process_text = Text("极限过程", font="SimSun", color=YELLOW).scale(0.7).next_to(delta_x_label, DOWN, buff=0.5)
        limit_arrow = Arrow(limit_process_text.get_top(), delta_x_label.get_bottom(), buff=0.1, color=YELLOW)
        self.play(Write(limit_process_text), Create(limit_arrow))
        
        # 3. 执行Δx从大到小变化的动画，展示割线趋近于切线
        self.play(delta_x_tracker.animate.set_value(0.05), rate_func=lambda t: 1 - (1-t)**4, run_time=8)
        self.wait()
        
        # 4. 显示结论：割线趋近于切线
        conclusion = Text("当 Δx → 0 时，割线趋近于切线", font="SimSun").to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait()
        
        # 5. 最后显示总结性公式：切线斜率 = 计算公式 = f'(x0)
        self.play(Write(final_conclusion_1), Write(final_conclusion_2))
        self.wait(2) 