from manim import *
import numpy as np

class SpaceCurveWithTangent(ZoomedScene):
    def construct(self):
        # 创建2D坐标系
        axes = Axes(
            x_range=[0, 2 * PI, PI],
            y_range=[0, 2.5, 0.5],
            axis_config={"color": GREY}
        )

        # 定义平面曲线的参数方程，并平移到第一象限
        def parametric_curve(t):
            return np.array([t, np.sin(t) + 1.5, 0])  # 平移到第一象限

        # 绘制曲线
        curve = ParametricFunction(
            parametric_curve,
            t_range=[0, 2 * PI],
            color=BLUE
        ).shift(LEFT * 5 + DOWN * 1.25)  # 向左平移两个单位

        # 显示坐标系和曲线
        self.play(Create(axes), Create(curve))
        self.wait(1)

        # 分割曲线并显示分段点
        n = 10  # 分割段数减少一半
        t_values = np.linspace(0, 2 * PI, n)
        dots = VGroup()
        tangent_lines = VGroup()
        for i in range(len(t_values) - 1):
            t0 = t_values[i]
            t1 = t_values[i + 1]
            mid_t = (t0 + t1) / 2  # 取中点

            # 计算中点的切线段
            delta_t = 0.01
            point = parametric_curve(mid_t)
            tangent_vector = (parametric_curve(mid_t + delta_t) - parametric_curve(mid_t)) / delta_t
            tangent_vector = tangent_vector / np.linalg.norm(tangent_vector) * 0.5  # 规范化并缩短

            tangent_line = Line(
                start=point - tangent_vector,
                end=point + tangent_vector,
                color=YELLOW
            ).shift(LEFT * 5 + DOWN * 1.25)  # 平移切线段
            tangent_lines.add(tangent_line)

            # 在分段点上添加红色点
            dot = Dot(point=parametric_curve(t0), color=RED).shift(LEFT * 5 + DOWN * 1.25)
            dots.add(dot)

        # 显示分段点和切线段
        self.play(Create(dots), Create(tangent_lines))
        self.wait(1)

        # 选择第五段进行放大
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        zoomed_display_frame = zoomed_camera.frame
        zoomed_display_frame.set_color(RED)

        # 设置放大区域
        zoom_factor = 0.3
        self.activate_zooming(animate=True)
        zoomed_display.scale(zoom_factor)
        zoomed_display.move_to(UP * 3 + RIGHT * 3)

        # 选择要放大的区域
        segment_index = 4  # 第五段的索引
        target_t0 = t_values[segment_index]
        target_t1 = t_values[segment_index + 1]
        target_coords = parametric_curve((target_t0 + target_t1) / 2)
        target_point = axes.c2p(*target_coords[:2]) + LEFT * 5 + DOWN * 1.25
        zoomed_display_frame.move_to(target_point)

        # 在放大区域中添加曲线弧和切线段
        arc = ParametricFunction(
            parametric_curve,
            t_range=[target_t0, target_t1],
            color=BLUE
        ).shift(LEFT * 5 + DOWN * 1.25)

        tangent_line_zoomed = Line(
            start=point - tangent_vector,
            end=point + tangent_vector,
            color=YELLOW
        ).shift(LEFT * 5 + DOWN * 1.25)

        # 将放大区域的内容添加到放大显示中
        self.add_foreground_mobject(VGroup(arc, tangent_line_zoomed))

        # 确保放大器框架也进行相同的平移
        zoomed_display_frame.shift(LEFT * 5 + DOWN * 1.25)

        self.play(Create(arc), Create(tangent_line_zoomed))
        self.wait(2) 