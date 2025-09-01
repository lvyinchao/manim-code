from manim import *
import numpy as np

class ArcLengthMicroelementScene(Scene):
    def construct(self):
        # 标题
        title = Text("微元法求曲线弧长", font_size=42)
        title.to_edge(UP)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        
        # 淡出标题
        self.play(FadeOut(title), run_time=1)
        
        # 介绍文本
        intro = Text("将曲线分割为无数个微小弧段，每段近似为直线", font_size=28)
        intro.to_edge(UP, buff=0.5)  # 调整位置，因为标题已淡出
        self.play(Write(intro), run_time=1.5)
        self.wait(1)
        
        # 淡出介绍
        self.play(FadeOut(intro), run_time=1)
        
        # 创建坐标系
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=10,
            y_length=7,
            axis_config={"color": BLUE}
        )
        
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        # 显示坐标系
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            run_time=1.5
        )
        
        # 定义函数 - 弯曲程度较大的复合函数
        def func(x):
            return 0.3 * x * x * x + 0.5 * np.sin(4 * x) + 1
        
        def func_derivative(x):
            return 0.9 * x * x + 2 * np.cos(4 * x)
        
        # 创建函数曲线
        curve = axes.plot(func, x_range=[0, 2.5], color=RED, stroke_width=4)
        curve_label = MathTex("y = f(x)", font_size=28, color=RED)
        curve_label.next_to(curve.get_end(), UP + LEFT)
        
        self.play(
            Create(curve),
            Write(curve_label),
            run_time=2
        )
        self.wait(1)
        
        # 定义弧长计算区间 - 选择弯曲明显的区域
        a, b = 1.0, 2.0
        
        # 标记计算区间
        a_line = axes.get_vertical_line(axes.c2p(a, func(a)), color=GREEN)
        b_line = axes.get_vertical_line(axes.c2p(b, func(b)), color=GREEN)
        
        a_label = MathTex("a", font_size=28, color=GREEN)
        a_label.next_to(axes.c2p(a, 0), DOWN)
        
        b_label = MathTex("b", font_size=28, color=GREEN)
        b_label.next_to(axes.c2p(b, 0), DOWN)
        
        # 高亮弧长段
        arc_segment = axes.plot(func, x_range=[a, b], color=YELLOW, stroke_width=6)
        
        self.play(
            Create(a_line),
            Create(b_line),
            Write(a_label),
            Write(b_label),
            Create(arc_segment),
            run_time=2
        )
        self.wait(1)
        
        # 弧长标记
        arc_label = Text("待求弧长", font_size=24, color=YELLOW)
        arc_label.move_to(axes.c2p(2, func(2) + 0.3))
        self.play(Write(arc_label), run_time=1)
        self.wait(1.5)
        
        # 开始演示分割过程
        self.play(FadeOut(arc_label), run_time=0.5)
        
        # 演示分割 - 选择8段作为例子
        n = 8
        dx_seg = (b - a) / n
        
        # 显示分割说明
        division_title = Text("将弧长分割成若干段", font_size=30, color=ORANGE)
        division_title.to_corner(UL).shift(DOWN * 0.5)
        self.play(Write(division_title), run_time=1)
        
        # 创建分割点和弧段
        division_points = []
        micro_elements = []
        colors = [YELLOW, BLUE, GREEN, PINK]
        
        # 第一步：显示分割点
        for i in range(n + 1):  # n+1个分割点
            x_point = a + i * dx_seg
            point = Dot(axes.c2p(x_point, func(x_point)), color=WHITE, radius=0.04)
            division_points.append(point)
        
        self.play(
            *[Create(point) for point in division_points],
            run_time=2
        )
        self.wait(1)
        
        # 第二步：显示分割后的弧段
        for i in range(n):
            x_left = a + i * dx_seg
            x_right = a + (i + 1) * dx_seg
            
            micro_arc = axes.plot(func, x_range=[x_left, x_right], 
                                color=colors[i % len(colors)], stroke_width=5)
            micro_elements.append(micro_arc)
        
        self.play(
            *[Create(elem) for elem in micro_elements],
            run_time=2
        )
        self.wait(1.5)
        
        # 淡出分割说明
        self.play(FadeOut(division_title), run_time=0.5)
        
        # 演示一小段的近似计算
        segment_index = 1  # 选择第2段进行演示（靠近a点）
        x_left = a + segment_index * dx_seg
        x_right = a + (segment_index + 1) * dx_seg
        
        # 高亮选中的段
        highlight_text = Text("选择其中一段进行近似计算", font_size=26, color=RED)
        highlight_text.to_corner(UL).shift(DOWN * 0.5)
        self.play(Write(highlight_text), run_time=1)
        
        # 高亮显示选中的弧段
        selected_arc = axes.plot(func, x_range=[x_left, x_right], 
                               color=RED, stroke_width=8)
        self.play(
            *[FadeOut(elem) for i, elem in enumerate(micro_elements) if i != segment_index],
            *[FadeOut(point) for i, point in enumerate(division_points) if i != segment_index and i != segment_index + 1],
            Transform(micro_elements[segment_index], selected_arc),
            run_time=2
        )
        self.wait(1)
        
        # 显示端点
        point1 = Dot(axes.c2p(x_left, func(x_left)), color=RED, radius=0.06)
        point2 = Dot(axes.c2p(x_right, func(x_right)), color=RED, radius=0.06)
        
        self.play(
            Create(point1),
            Create(point2),
            run_time=1
        )
        self.wait(0.5)
        
        # 放大演示：展示曲线弧和切线的关系
        self.play(FadeOut(highlight_text), run_time=0.5)
        
        zoom_text = Text("放大观察：曲线段越短，与切线段越接近", font_size=26, color=BLUE)
        zoom_text.to_corner(UL).shift(DOWN * 0.5)
        self.play(Write(zoom_text), run_time=1)
        
        # 创建放大的视图区域
        zoom_center_x = (x_left + x_right) / 2
        zoom_center_y = func(zoom_center_x)
        
        # 放大的坐标系
        zoom_range = 0.3
        zoom_axes = Axes(
            x_range=[zoom_center_x - zoom_range, zoom_center_x + zoom_range, 0.1],
            y_range=[zoom_center_y - zoom_range, zoom_center_y + zoom_range, 0.1],
            x_length=5.5,
            y_length=4.5,
            axis_config={"color": GRAY, "stroke_width": 1}
        )
        zoom_axes.move_to(RIGHT * 3 + UP * 0.2)
        
        # 放大视图的边框
        zoom_box = Rectangle(
            width=5.8, height=4.8,
            color=BLUE, stroke_width=3
        ).move_to(RIGHT * 3 + UP * 0.2)
        
        # 显示放大视图框架
        self.play(
            Create(zoom_box),
            Create(zoom_axes),
            run_time=1.5
        )
        
        # 演示不断缩短的过程
        segment_lengths = [0.28, 0.18, 0.11, 0.06]  # 从0.28开始，逐步缩短
        colors = [RED, ORANGE, YELLOW, GREEN]
        
        for i, length in enumerate(segment_lengths):
            # 当前段的范围
            current_left = zoom_center_x - length / 2
            current_right = zoom_center_x + length / 2
            
            # 显示当前阶段说明
            if i == 0:
                stage_text = Text("较长的曲线段", font_size=22, color=colors[i])
            elif i == 1:
                stage_text = Text("缩短曲线段", font_size=22, color=colors[i])
            elif i == 2:
                stage_text = Text("进一步缩短", font_size=22, color=colors[i])
            else:
                stage_text = Text("很短的曲线段", font_size=22, color=colors[i])
                
            stage_text.next_to(zoom_text, DOWN, aligned_edge=LEFT, buff=0.3)
            
            if i > 0:
                self.play(Transform(prev_stage_text, stage_text), run_time=0.8)
            else:
                self.play(Write(stage_text), run_time=0.8)
                prev_stage_text = stage_text
            
            # 放大视图中的曲线段
            zoom_curve = zoom_axes.plot(
                func, 
                x_range=[current_left, current_right], 
                color=colors[i], 
                stroke_width=8
            )
            
            # 曲线段的端点
            zoom_point1 = Dot(zoom_axes.c2p(current_left, func(current_left)), color=colors[i], radius=0.06)
            zoom_point2 = Dot(zoom_axes.c2p(current_right, func(current_right)), color=colors[i], radius=0.06)
            
            # 计算切线（在段中点处的切线）
            mid_x = zoom_center_x
            mid_y = func(mid_x)
            slope = func_derivative(mid_x)  # 在中点处的导数（切线斜率）
            
            # 切线段（从左端点到右端点）
            tangent_y_left = mid_y + slope * (current_left - mid_x)
            tangent_y_right = mid_y + slope * (current_right - mid_x)
            
            zoom_tangent = Line(
                zoom_axes.c2p(current_left, tangent_y_left),
                zoom_axes.c2p(current_right, tangent_y_right),
                color=PURPLE, stroke_width=6
            )
            
            # 显示曲线段和切线段
            if i == 0:
                self.play(
                    Create(zoom_curve),
                    Create(zoom_point1),
                    Create(zoom_point2),
                    run_time=1.5
                )
                self.wait(1)
                self.play(Create(zoom_tangent), run_time=1.2)
                self.wait(1.5)
            else:
                # 端点移动、曲线缩短和长曲线消失同时进行
                self.play(
                    ReplacementTransform(prev_curve, zoom_curve),
                    ReplacementTransform(prev_point1, zoom_point1),
                    ReplacementTransform(prev_point2, zoom_point2),
                    ReplacementTransform(prev_tangent, zoom_tangent),
                    run_time=3.0  # 稍长的时间让变化过程更清晰自然
                )
                self.wait(1.5)
            
            # 保存当前对象以便下次更新
            prev_curve = zoom_curve
            prev_point1 = zoom_point1
            prev_point2 = zoom_point2
            prev_tangent = zoom_tangent
        
        # 最终说明
        self.play(FadeOut(zoom_text), run_time=0.5)
        final_zoom_text = Text("极限情况：曲线段与切线段完全重合", font_size=24, color=GREEN)
        final_zoom_text.to_corner(UL).shift(DOWN * 0.5)
        self.play(Write(final_zoom_text), run_time=1.5)
        self.wait(2)
        
        # 回到主视图进行详细分析
        self.play(
            FadeOut(final_zoom_text),
            FadeOut(prev_stage_text),
            *[FadeOut(mob) for mob in [zoom_box, zoom_axes, prev_curve, 
                                      prev_point1, prev_point2, prev_tangent]],
            run_time=1.5
        )
        
        # 添加原来的直线近似到主视图
        approx_line = Line(
            axes.c2p(x_left, func(x_left)),
            axes.c2p(x_right, func(x_right)),
            color=PURPLE, stroke_width=6
        )
        
        approximation_text = Text("用直线段近似这段弧长", font_size=26, color=PURPLE)
        approximation_text.to_corner(UL).shift(DOWN * 0.5)
        self.play(Write(approximation_text), run_time=1)
        
        self.play(Create(approx_line), run_time=1.5)
        self.wait(1)
        
        # 构造直角三角形进行详细分析
        dy = func(x_right) - func(x_left)
        
        # 水平线 (dx)
        horizontal_line = Line(
            axes.c2p(x_left, func(x_left)),
            axes.c2p(x_right, func(x_left)),
            color=BLUE, stroke_width=4
        )
        
        # 竖直线 (dy)
        vertical_line = Line(
            axes.c2p(x_right, func(x_left)),
            axes.c2p(x_right, func(x_right)),
            color=GREEN, stroke_width=4
        )
        
        # 标签
        dx_label = MathTex("dx", font_size=28, color=BLUE)
        dx_label.next_to(horizontal_line, DOWN, buff=0.2)
        
        dy_label = MathTex("dy", font_size=28, color=GREEN)
        dy_label.next_to(vertical_line, RIGHT, buff=0.2)
        
        ds_label = MathTex("ds", font_size=28, color=PURPLE)
        ds_label.next_to(approx_line.get_center(), UP + LEFT, buff=0.2)
        
        self.play(FadeOut(approximation_text), run_time=0.5)
        
        triangle_text = Text("构造直角三角形分析", font_size=26, color=WHITE)
        triangle_text.to_corner(UL).shift(DOWN * 0.5)
        self.play(Write(triangle_text), run_time=1)
        
        self.play(
            Create(horizontal_line),
            Create(vertical_line),
            Write(dx_label),
            Write(dy_label),
            Write(ds_label),
            run_time=2
        )
        self.wait(2)
        
        # 显示计算公式
        self.play(FadeOut(triangle_text), run_time=0.5)
        
        # 显示弧长微元公式（右侧）
        formula_group = VGroup()
        
        # 勾股定理
        pythagorean = MathTex(r"ds^2 = dx^2 + dy^2", font_size=24)
        pythagorean.to_corner(UR).shift(LEFT * 1.5 + DOWN * 0.5)
        formula_group.add(pythagorean)
        
        # 弧长微元公式
        ds_formula = MathTex(r"ds = \sqrt{dx^2 + dy^2}", font_size=24)
        ds_formula.next_to(pythagorean, DOWN, aligned_edge=LEFT, buff=0.2)
        formula_group.add(ds_formula)
        
        # 导数形式
        derivative_form = MathTex(r"ds = \sqrt{1 + \left(\frac{dy}{dx}\right)^2} dx", font_size=24)
        derivative_form.next_to(ds_formula, DOWN, aligned_edge=LEFT, buff=0.2)
        formula_group.add(derivative_form)
        
        self.play(Write(pythagorean), run_time=1)
        self.wait(0.5)
        self.play(Write(ds_formula), run_time=1)
        self.wait(0.5)
        self.play(Write(derivative_form), run_time=1)
        self.wait(2)
        
        # 清除详细分析，准备回到整体演示
        self.play(
            *[FadeOut(mob) for mob in [
                micro_elements[segment_index], point1, point2, approx_line,
                horizontal_line, vertical_line, dx_label, dy_label, ds_label,
                formula_group
            ]],
            run_time=1.5
        )
        
        # 恢复完整的弧长段用于后续演示
        complete_arc = axes.plot(func, x_range=[a, b], color=YELLOW, stroke_width=6)
        self.play(Create(complete_arc), run_time=1)
        self.wait(0.5)
        
        # 显示极限和积分概念
        limit_text = Text("当段长 → 0 时，所有直线段长度之和趋向于曲线弧长", font_size=24)
        limit_text.to_edge(DOWN)
        self.play(Write(limit_text), run_time=2)
        self.wait(1.5)
        
        # 最终的积分公式
        final_formula = MathTex(r"L = \int_a^b \sqrt{1 + \left(\frac{dy}{dx}\right)^2} dx", 
                              font_size=36, color=GOLD)
        final_box = SurroundingRectangle(final_formula, buff=0.3, color=GOLD)
        final_group = VGroup(final_formula, final_box)
        final_group.move_to(RIGHT * 4 + UP * 2.5)  # 右移到更右侧位置，避免重叠
        
        self.play(
            FadeOut(limit_text),
            Write(final_group),
            run_time=2
        )
        
        self.wait(2)
        
        # 结论
        conclusion = Text("微元法：将复杂的曲线问题转化为简单的直线问题", font_size=26)
        conclusion.to_edge(DOWN)
        self.play(Write(conclusion), run_time=2)
        
        self.wait(3)
        
        # 淡出所有元素
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=1.5)


if __name__ == "__main__":
    # 直接渲染场景
    scene = ArcLengthMicroelementScene()
    scene.render() 