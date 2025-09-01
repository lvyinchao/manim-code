from manim import *
import numpy as np

class PointMassInertiaScene(ThreeDScene):
    def construct(self):
        # 设置相机
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.8)
        
        # 标题
        title = Text("质点的转动惯量", font_size=36)
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1)
        
        # 创建坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        self.play(
            Create(axes),
            Create(labels),
            run_time=1.5
        )
        
        # 创建旋转轴（x轴）
        rotation_axis = Line3D(
            start=np.array([-3, 0, 0]),
            end=np.array([3, 0, 0]),
            color=RED
        )
        axis_label = Text("旋转轴", font_size=24).set_color(RED)
        axis_label.next_to(rotation_axis.get_end(), RIGHT)
        self.add_fixed_in_frame_mobjects(axis_label)
        
        self.play(
            Create(rotation_axis),
            Write(axis_label),
            run_time=1
        )
        self.wait(0.5)
        
        # 创建质点
        point_position = np.array([1, 2, 0]) # 修改z坐标为0，使点位于xoy平面
        point = Sphere(radius=0.15, color=BLUE).move_to(point_position)
        point_label = Text("质点m", font_size=24).set_color(BLUE)
        point_label.next_to(point, UP+RIGHT)
        self.add_fixed_in_frame_mobjects(point_label)
        
        self.play(
            Create(point),
            Write(point_label),
            run_time=1
        )
        self.wait(0.5)
        
        # 显示质点到旋转轴的距离
        # 找到质点到x轴的最短距离点
        projection_point = np.array([point_position[0], 0, 0])
        
        # 创建从质点到投影点的线段（表示垂直距离）
        distance_line = Line3D(
            start=point_position,
            end=projection_point,
            color=GREEN
        )
        
        # 距离标签使用字母r
        distance_label = MathTex("r", font_size=30).set_color(GREEN)
        distance_label.move_to((point_position + projection_point) / 2 + np.array([0.3, 0.3, 0]))
        self.add_fixed_in_frame_mobjects(distance_label)
        
        self.play(
            Create(distance_line),
            Write(distance_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 展示转动惯量公式
        formula = MathTex(r"I = mr^2", font_size=36)
        formula.to_edge(RIGHT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula), run_time=1)
        self.wait(1)
        
        # 演示转动
        self.begin_ambient_camera_rotation(rate=0.2)
        
        self.play(
            Rotating(
                point,
                axis=RIGHT,
                about_point=ORIGIN,
                radians=2*PI,
                run_time=4,
                rate_func=linear
            )
        )
        
        # 显示多个质点的转动惯量
        self.stop_ambient_camera_rotation()
        
        # 淡出单个质点的内容
        self.play(
            FadeOut(point),
            FadeOut(point_label),
            FadeOut(distance_line),
            FadeOut(distance_label),
            run_time=1
        )
        
        # 创建多个质点
        points = []
        point_positions = [
            np.array([1, 2, 0]),   # 修改z坐标为0
            np.array([-1, 1, 0]),  # 修改z坐标为0
            np.array([0, -1.5, 0]), # 修改z坐标为0
            np.array([-2, -1, 0])   # 修改z坐标为0
        ]
        
        point_masses = [2, 1, 3, 2]  # 不同质点的质量，仅用于设置半径大小
        
        for i, pos in enumerate(point_positions):
            p = Sphere(radius=0.1 + 0.05 * point_masses[i], color=BLUE).move_to(pos)
            points.append(p)
        
        # 一次性创建所有质点
        self.play(
            *[Create(p) for p in points],
            run_time=1.5
        )
        
        # 为每个质点创建到旋转轴的距离线
        distance_lines = []
        distance_labels = []
        
        for i, pos in enumerate(point_positions):
            proj = np.array([pos[0], 0, 0])
            line = Line3D(start=pos, end=proj, color=GREEN)
            # 使用字母r_i表示距离
            label = MathTex(f"r_{i+1}", font_size=24).set_color(GREEN)
            label_pos = (pos + proj) / 2 + np.array([0.3, 0.3, 0])
            label.move_to(label_pos)
            
            distance_lines.append(line)
            distance_labels.append(label)
            self.add_fixed_in_frame_mobjects(label)
        
        self.play(
            *[Create(line) for line in distance_lines],
            *[Write(label) for label in distance_labels],
            run_time=2
        )
        
        # 计算每个质点的转动惯量贡献 - 使用字母
        inertia_contributions = []
        
        for i in range(4):
            contrib = MathTex(
                f"I_{i+1} = m_{i+1} r_{i+1}^2",
                font_size=24
            )
            inertia_contributions.append(contrib)
        
        # 垂直排列所有贡献
        contributions_group = VGroup(*inertia_contributions).arrange(DOWN, aligned_edge=LEFT)
        contributions_group.to_corner(DL).shift(UP * 2 + RIGHT)
        
        for contrib in inertia_contributions:
            self.add_fixed_in_frame_mobjects(contrib)
            self.play(Write(contrib), run_time=0.8)
        
        # 总和
        total_inertia = MathTex(
            r"I_{\text{total}} = \sum_i I_i = \sum_i m_i r_i^2",
            font_size=30
        )
        total_inertia.next_to(contributions_group, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(total_inertia)
        
        self.play(Write(total_inertia), run_time=1.5)
        
        # 强调总和
        total_box = SurroundingRectangle(total_inertia, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(total_box)
        self.play(Create(total_box), run_time=1)
        self.wait(1)
        
        # 展示所有质点同时转动
        self.begin_ambient_camera_rotation(rate=0.15)
        
        self.play(
            *[Rotating(
                p, 
                axis=RIGHT,
                about_point=ORIGIN, 
                radians=2*PI, 
                run_time=4,
                rate_func=linear
            ) for p in points],
            run_time=4
        )
        
        self.stop_ambient_camera_rotation()
        
        # 结论
        conclusion = Text("从离散质点到连续质量分布", font_size=32)
        conclusion.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(conclusion)
        
        self.play(
            FadeOut(contributions_group),
            FadeOut(total_inertia),
            FadeOut(total_box),
            Write(conclusion),
            run_time=1.5
        )
        
        self.wait(2)
        
        # 淡出所有元素，为下一个场景做准备
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )


class DiameterMomentOfInertiaScene(ThreeDScene):
    def construct(self):
        # 设置相机
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.8)
        
        # 标题 - 居中显示
        title = Text("圆盘对直径的转动惯量", font_size=36)
        title.to_edge(UP)  # 居中显示在顶部
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1)
        
        # 先创建坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        self.play(
            Create(axes),
            Create(labels),
            run_time=1.5
        )
        
        # 创建圆盘
        disk = Surface(
            lambda u, v: np.array([
                v * np.cos(u),
                v * np.sin(u),
                0
            ]),
            u_range=[0, 2*PI],
            v_range=[0, 2],
            resolution=(24, 10),
            fill_opacity=0.3,
            fill_color=BLUE,
            stroke_color=BLUE_E,
            stroke_width=1
        )
        
        # 创建直径旋转轴（x轴）
        diameter = Line3D(
            start=np.array([-2.5, 0, 0]),
            end=np.array([2.5, 0, 0]),
            color=RED
        )
        axis_label = Text("旋转轴（直径）", font_size=24).set_color(RED)
        axis_label.next_to(diameter.get_end(), RIGHT+UP)
        self.add_fixed_in_frame_mobjects(axis_label)
        
        # 显示圆盘和旋转轴
        self.play(
            Create(disk),
            Create(diameter),
            Write(axis_label),
            run_time=2
        )
        self.wait(1)
        
        # 展示圆盘微元（在圆盘平面内的水平矩形条带）
        strips = []
        strip_heights = []  # 每个条带的y坐标中心位置
        
        num_strips = 10
        strip_colors = [BLUE_B, BLUE_C, BLUE_D, BLUE_E] * 3
        radius = 2  # 圆盘半径
        
        strip_height = (2 * radius) / num_strips  # 每个矩形条带的高度
        
        for i in range(num_strips):
            # 计算条带中心的y坐标
            y_center = -radius + (i + 0.5) * strip_height
            strip_heights.append(y_center)
            
            # 根据圆的方程计算该y坐标处的宽度
            width = 2 * np.sqrt(radius**2 - y_center**2)
            
            # 创建矩形条带
            strip = Rectangle(
                width=width,
                height=strip_height,
                fill_opacity=0.4,
                fill_color=strip_colors[i % len(strip_colors)],
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # 将矩形移动到对应位置
            strip.move_to(np.array([0, y_center, 0]))
            strips.append(strip)
        
        # 一次性绘制所有矩形条带
        self.play(
            *[Create(strip) for strip in strips],
            run_time=1.5
        )
        self.wait(1)
        
        # 高亮显示一个条带 - 保持黄色高亮
        highlight_index = 6
        strips[highlight_index].set_fill(YELLOW, opacity=0.7)
        
        # 标记这个条带的y坐标（到x轴的距离）
        y_center = strip_heights[highlight_index]
        
        # 创建标记线和标签 - 使用更明显的颜色
        distance_line = Line3D(
            start=np.array([0, y_center, 0]),
            end=np.array([0, 0, 0]),
            color=ORANGE
        )
        
        # 创建距离标签 - 使用更明显的颜色
        distance_label = MathTex("r", font_size=30).set_color(ORANGE)
        distance_label.move_to(np.array([0.3, y_center/2, 0.1]))
        self.add_fixed_in_frame_mobjects(distance_label)
        
        # 添加微元标签
        dm_label = MathTex("dm", font_size=26).set_color(YELLOW)
        dm_label.move_to(np.array([1, y_center, 0.1]))
        self.add_fixed_in_frame_mobjects(dm_label)
        
        # 显示标记
        self.play(
            Create(distance_line),
            Write(distance_label),
            Write(dm_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 现在开始显示微元计算公式
        # 首先展示单个微元的转动惯量贡献 - 调整位置
        contribution = MathTex(r"dI = r^2 \cdot dm", font_size=28)
        contribution.next_to(title, DOWN, buff=0.5).align_to(title, LEFT).shift(LEFT * 4)  # 更靠左显示
        self.add_fixed_in_frame_mobjects(contribution)
        self.play(Write(contribution), run_time=1.5)
        
        # 解释微元的特点 - 右移
        explanation = Text("对于平行于y轴的条带微元，r=|y|是常量", font_size=20)
        explanation.next_to(contribution, RIGHT, buff=1.0)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation), run_time=1.5)
        
        # 添加I=积分dI的表达式
        integral_connection = MathTex(r"I = \iint_{D} dI", font_size=28)
        integral_connection.next_to(contribution, DOWN, buff=0.4).align_to(contribution, LEFT)
        self.add_fixed_in_frame_mobjects(integral_connection)
        self.play(Write(integral_connection), run_time=1.5)
        
        # 添加I=二重积分r^2dm的表示
        r_squared_dm = MathTex(r"I = \iint_{D} r^2 \, dm", font_size=28)
        r_squared_dm.next_to(integral_connection, DOWN, buff=0.4).align_to(integral_connection, LEFT)
        self.add_fixed_in_frame_mobjects(r_squared_dm)
        self.play(Write(r_squared_dm), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 展示二重积分形式 - 改用rho表示密度，dsigma表示面积微元
        double_integral = MathTex(r"I = \iint_D y^2 \, \rho \, d\sigma", font_size=24)
        double_integral.next_to(r_squared_dm, DOWN, buff=0.4).align_to(r_squared_dm, LEFT)
        self.add_fixed_in_frame_mobjects(double_integral)
        self.play(Write(double_integral), run_time=1.5)
        
        # 解释二重积分
        integral_explain = Text("D是圆盘区域，dσ是面积微元", font_size=16)
        integral_explain.next_to(double_integral, RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(integral_explain)
        self.play(Write(integral_explain), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 极坐标下的积分表达式 - 改用rho表示密度
        polar_integral = MathTex(r"I = \rho \int_{0}^{R} \int_{0}^{2\pi} r^2\sin^2\theta \cdot r \, d\theta \, dr", font_size=22)
        polar_integral.next_to(double_integral, DOWN, buff=0.4).align_to(double_integral, LEFT)
        self.add_fixed_in_frame_mobjects(polar_integral)
        self.play(Write(polar_integral), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 极坐标下的解释 - 修复错误
        explanation_1 = Text("ρ: 面密度", font_size=16)
        explanation_2 = Text("r sin θ: 到x轴的距离", font_size=16)
        polar_explanations = VGroup(explanation_1, explanation_2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        polar_explanations.next_to(polar_integral, RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(polar_explanations)
        self.play(Write(polar_explanations), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 积分计算过程 - 使用rho替代sigma
        calc_1 = MathTex(r"I &= \rho \int_{0}^{R} r^3 \, dr \int_{0}^{2\pi} \sin^2 \theta \, d\theta \\", font_size=20)
        calc_2 = MathTex(r"&= \rho \int_{0}^{R} r^3 \, dr \cdot \pi \\", font_size=20)
        calc_3 = MathTex(r"&= \pi \rho \cdot \frac{R^4}{4} \\", font_size=20)
        calc_4 = MathTex(r"&= \frac{\pi R^2 \rho \cdot R^2}{4} \\", font_size=20)
        calc_5 = MathTex(r"&= \frac{1}{4} M R^2", font_size=20)
        
        calculations = VGroup(calc_1, calc_2, calc_3, calc_4, calc_5).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        calculations.next_to(polar_integral, DOWN, buff=0.4, aligned_edge=LEFT)
        
        for calc in calculations:
            self.add_fixed_in_frame_mobjects(calc)
            self.play(Write(calc), run_time=0.6)  # 减少每步计算的显示时间
            self.wait(0.1)  # 减少每步之间的等待时间
        
        # 最终结果
        final_box = SurroundingRectangle(calc_5, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(final_box)
        self.play(Create(final_box), run_time=0.8)  # 减少框显示时间
        self.wait(0.2)  # 减少等待时间
        
        # 将最终结果显示在屏幕下方，不使用飞入动画
        final_result = MathTex(r"I = \frac{1}{4} M R^2", font_size=32, color=YELLOW)
        final_result.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(final_result)
        self.play(Write(final_result), run_time=1.0)  # 缩短结果显示时间
        self.wait(0.5)  # 减少最终结果后的等待时间
        
        # 淡出微元划分，只保留整个圆盘
        self.play(
            *[FadeOut(strip) for strip in strips],
            FadeOut(distance_line),
            FadeOut(distance_label),
            FadeOut(dm_label),
            run_time=1.0
        )
        
        # 演示旋转 - 只旋转圆盘
        self.move_camera(phi=90 * DEGREES, theta=0)
        self.begin_ambient_camera_rotation(rate=0.15)
        
        # 只旋转圆盘
        self.play(
            Rotating(
                disk,
                axis=RIGHT,
                radians=2*PI,
                run_time=5,
                rate_func=linear
            ),
            run_time=5
        )
        
        self.stop_ambient_camera_rotation()
        self.wait(2)  # 添加一点等待时间后结束


class CombinedInertiaScene(ThreeDScene):
    def construct(self):
        # 设置相机
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.8)
        
        # 标题
        title = Text("转动惯量计算演示", font_size=42)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.5)
        
        # 介绍文本
        intro = Text("从质点到连续质量分布", font_size=36)
        intro.next_to(title, DOWN, buff=1)
        self.add_fixed_in_frame_mobjects(intro)
        
        self.play(Write(intro), run_time=1.5)
        self.wait(1)
        
        # 淡出介绍
        self.play(
            FadeOut(title),
            FadeOut(intro),
            run_time=1.5
        )
        
        #-------------------------------------------
        # 第一部分：质点的转动惯量
        #-------------------------------------------
        # 标题
        title = Text("质点的转动惯量", font_size=36)
        title.to_edge(UP)  # 改为居中显示
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1)
        
        # 创建坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        self.play(
            Create(axes),
            Create(labels),
            run_time=1.5
        )
        
        # 创建旋转轴（x轴）- 修改为x轴
        rotation_axis = Line3D(
            start=np.array([-3, 0, 0]),
            end=np.array([3, 0, 0]),
            color=RED
        )
        axis_label = Text("旋转轴", font_size=24).set_color(RED)
        axis_label.next_to(rotation_axis.get_end(), RIGHT)
        self.add_fixed_in_frame_mobjects(axis_label)
        
        self.play(
            Create(rotation_axis),
            Write(axis_label),
            run_time=1
        )
        self.wait(0.5)
        
        # 创建质点
        point_position = np.array([1, 2, 0]) # 修改z坐标为0，使点位于xoy平面
        point = Sphere(radius=0.15, color=BLUE).move_to(point_position)
        point_label = Text("质点m", font_size=24).set_color(BLUE)
        point_label.next_to(point, UP+RIGHT)
        self.add_fixed_in_frame_mobjects(point_label)
        
        self.play(
            Create(point),
            Write(point_label),
            run_time=1
        )
        self.wait(0.5)
        
        # 显示质点到旋转轴的距离
        # 找到质点到x轴的最短距离点
        projection_point = np.array([point_position[0], 0, 0])
        
        # 创建从质点到投影点的线段（表示垂直距离）
        distance_line = Line3D(
            start=point_position,
            end=projection_point,
            color=GREEN
        )
        
        # 距离标签使用字母r
        distance_label = MathTex("r", font_size=30).set_color(GREEN)
        # 调整标签位置
        distance_label.move_to((point_position + projection_point) / 2 + np.array([0.3, 0.3, 0]))
        self.add_fixed_in_frame_mobjects(distance_label)
        
        self.play(
            Create(distance_line),
            Write(distance_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 展示转动惯量公式
        formula = MathTex(r"I = mr^2", font_size=36)
        formula.to_edge(RIGHT).shift(UP * 2)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula), run_time=1)
        self.wait(1)
        
        # 演示转动
        self.begin_ambient_camera_rotation(rate=0.2)
        
        self.play(
            Rotating(
                point,
                axis=RIGHT, # 修改为绕x轴旋转
                about_point=ORIGIN,
                radians=2*PI,
                run_time=4,
                rate_func=linear
            )
        )
        
        # 显示多个质点的转动惯量
        self.stop_ambient_camera_rotation()
        
        # 淡出单个质点的内容
        self.play(
            FadeOut(point),
            FadeOut(point_label),
            FadeOut(distance_line),
            FadeOut(distance_label),
            run_time=1
        )
        
        # 创建多个质点
        points = []
        point_positions = [
            np.array([1, 2, 0]),   # 修改z坐标为0
            np.array([-1, 1, 0]),  # 修改z坐标为0
            np.array([0, -1.5, 0]), # 修改z坐标为0
            np.array([-2, -1, 0])   # 修改z坐标为0
        ]
        
        point_masses = [2, 1, 3, 2]  # 不同质点的质量，仅用于设置半径大小
        
        for i, pos in enumerate(point_positions):
            p = Sphere(radius=0.1 + 0.05 * point_masses[i], color=BLUE).move_to(pos)
            points.append(p)
        
        # 一次性创建所有质点
        self.play(
            *[Create(p) for p in points],
            run_time=1.5
        )
        
        # 为每个质点创建到旋转轴的距离线
        distance_lines = []
        distance_labels = []
        
        for i, pos in enumerate(point_positions):
            proj = np.array([pos[0], 0, 0]) # 修改为到x轴的投影
            line = Line3D(start=pos, end=proj, color=GREEN)
            # 使用字母r_i表示距离
            label = MathTex(f"r_{i+1}", font_size=24).set_color(GREEN)
            label_pos = (pos + proj) / 2 + np.array([0.3, 0.3, 0])
            label.move_to(label_pos)
            
            distance_lines.append(line)
            distance_labels.append(label)
            self.add_fixed_in_frame_mobjects(label)
        
        self.play(
            *[Create(line) for line in distance_lines],
            *[Write(label) for label in distance_labels],
            run_time=2
        )
        
        # 计算每个质点的转动惯量贡献 - 使用字母
        inertia_contributions = []
        
        for i in range(4):
            contrib = MathTex(
                f"I_{i+1} = m_{i+1} r_{i+1}^2",
                font_size=24
            )
            inertia_contributions.append(contrib)
        
        # 垂直排列所有贡献
        contributions_group = VGroup(*inertia_contributions).arrange(DOWN, aligned_edge=LEFT)
        contributions_group.to_corner(DL).shift(UP * 2 + RIGHT)
        
        for contrib in inertia_contributions:
            self.add_fixed_in_frame_mobjects(contrib)
            self.play(Write(contrib), run_time=0.8)
        
        # 总和
        total_inertia = MathTex(
            r"I_{\text{total}} = \sum_i I_i = \sum_i m_i r_i^2",
            font_size=30
        )
        total_inertia.next_to(contributions_group, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(total_inertia)
        
        self.play(Write(total_inertia), run_time=1.5)
        
        # 强调总和
        total_box = SurroundingRectangle(total_inertia, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(total_box)
        self.play(Create(total_box), run_time=1)
        self.wait(1)
        
        # 展示所有质点同时转动
        self.begin_ambient_camera_rotation(rate=0.15)
        
        self.play(
            *[Rotating(
                p, 
                axis=RIGHT, # 修改为绕x轴旋转
                about_point=ORIGIN, 
                radians=2*PI, 
                run_time=4,
                rate_func=linear
            ) for p in points],
            run_time=4
        )
        
        self.stop_ambient_camera_rotation()
        
        # 结论和过渡到下一部分
        transition = Text("从离散质点到连续质量分布", font_size=32)
        transition.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(transition)
        
        self.play(
            FadeOut(contributions_group),
            FadeOut(total_inertia),
            FadeOut(total_box),
            Write(transition),
            run_time=1.5
        )
        
        self.wait(2)
        
        # 淡出所有元素，为下一个场景做准备
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )
        
        #-------------------------------------------
        # 第二部分：圆盘对直径的转动惯量
        #-------------------------------------------
        
        # 重新设置相机
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.8)
        
        # 标题 - 居中显示
        title = Text("圆盘对直径的转动惯量", font_size=36)
        title.to_edge(UP)  # 居中显示在顶部
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1)
        
        # 先创建坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )
        
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        self.play(
            Create(axes),
            Create(labels),
            run_time=1.5
        )
        
        # 创建圆盘
        disk = Surface(
            lambda u, v: np.array([
                v * np.cos(u),
                v * np.sin(u),
                0
            ]),
            u_range=[0, 2*PI],
            v_range=[0, 2],
            resolution=(24, 10),
            fill_opacity=0.3,
            fill_color=BLUE,
            stroke_color=BLUE_E,
            stroke_width=1
        )
        
        # 创建直径旋转轴（x轴）
        diameter = Line3D(
            start=np.array([-2.5, 0, 0]),
            end=np.array([2.5, 0, 0]),
            color=RED
        )
        axis_label = Text("旋转轴（直径）", font_size=24).set_color(RED)
        axis_label.next_to(diameter.get_end(), RIGHT+UP)
        self.add_fixed_in_frame_mobjects(axis_label)
        
        # 显示圆盘和旋转轴
        self.play(
            Create(disk),
            Create(diameter),
            Write(axis_label),
            run_time=2
        )
        self.wait(1)
        
        # 展示圆盘微元（在圆盘平面内的水平矩形条带）
        strips = []
        strip_heights = []  # 每个条带的y坐标中心位置
        
        num_strips = 10
        strip_colors = [BLUE_B, BLUE_C, BLUE_D, BLUE_E] * 3
        radius = 2  # 圆盘半径
        
        strip_height = (2 * radius) / num_strips  # 每个矩形条带的高度
        
        for i in range(num_strips):
            # 计算条带中心的y坐标
            y_center = -radius + (i + 0.5) * strip_height
            strip_heights.append(y_center)
            
            # 根据圆的方程计算该y坐标处的宽度
            width = 2 * np.sqrt(radius**2 - y_center**2)
            
            # 创建矩形条带
            strip = Rectangle(
                width=width,
                height=strip_height,
                fill_opacity=0.4,
                fill_color=strip_colors[i % len(strip_colors)],
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # 将矩形移动到对应位置
            strip.move_to(np.array([0, y_center, 0]))
            strips.append(strip)
        
        # 一次性绘制所有矩形条带
        self.play(
            *[Create(strip) for strip in strips],
            run_time=1.5
        )
        self.wait(1)
        
        # 高亮显示一个条带 - 保持黄色高亮
        highlight_index = 6
        strips[highlight_index].set_fill(YELLOW, opacity=0.7)
        
        # 标记这个条带的y坐标（到x轴的距离）
        y_center = strip_heights[highlight_index]
        
        # 创建标记线和标签 - 使用更明显的颜色
        distance_line = Line3D(
            start=np.array([0, y_center, 0]),
            end=np.array([0, 0, 0]),
            color=ORANGE
        )
        
        # 创建距离标签 - 使用更明显的颜色
        distance_label = MathTex("r", font_size=30).set_color(ORANGE)
        distance_label.move_to(np.array([0.3, y_center/2, 0.1]))
        self.add_fixed_in_frame_mobjects(distance_label)
        
        # 添加微元标签
        dm_label = MathTex("dm", font_size=26).set_color(YELLOW)
        dm_label.move_to(np.array([1, y_center, 0.1]))
        self.add_fixed_in_frame_mobjects(dm_label)
        
        # 显示标记
        self.play(
            Create(distance_line),
            Write(distance_label),
            Write(dm_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 现在开始显示微元计算公式
        # 首先展示单个微元的转动惯量贡献 - 调整位置
        contribution = MathTex(r"dI = r^2 \cdot dm", font_size=28)
        contribution.next_to(title, DOWN, buff=0.5).align_to(title, LEFT).shift(LEFT * 4)  # 更靠左显示
        self.add_fixed_in_frame_mobjects(contribution)
        self.play(Write(contribution), run_time=1.5)
        
        # 解释微元的特点 - 右移
        explanation = Text("对于平行于y轴的条带微元，r=|y|是形同的", font_size=20)
        explanation.next_to(contribution, RIGHT, buff=1.0)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation), run_time=1.5)
        
        # 添加I=积分dI的表达式
        integral_connection = MathTex(r"I = \iint_{D} dI", font_size=28)
        integral_connection.next_to(contribution, DOWN, buff=0.4).align_to(contribution, LEFT)
        self.add_fixed_in_frame_mobjects(integral_connection)
        self.play(Write(integral_connection), run_time=1.5)
        
        # 添加I=二重积分r^2dm的表示
        r_squared_dm = MathTex(r"I = \iint_{D} r^2 \, dm", font_size=28)
        r_squared_dm.next_to(integral_connection, DOWN, buff=0.4).align_to(integral_connection, LEFT)
        self.add_fixed_in_frame_mobjects(r_squared_dm)
        self.play(Write(r_squared_dm), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 展示二重积分形式 - 改用rho表示密度，dsigma表示面积微元
        double_integral = MathTex(r"I = \iint_D y^2 \, \rho \, d\sigma", font_size=24)
        double_integral.next_to(r_squared_dm, DOWN, buff=0.4).align_to(r_squared_dm, LEFT)
        self.add_fixed_in_frame_mobjects(double_integral)
        self.play(Write(double_integral), run_time=1.5)
        
        # 解释二重积分
        integral_explain = Text("D是圆盘区域，dσ是面积微元", font_size=16)
        integral_explain.next_to(double_integral, RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(integral_explain)
        self.play(Write(integral_explain), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 极坐标下的积分表达式 - 改用rho表示密度
        polar_integral = MathTex(r"I = \rho \int_{0}^{R} \int_{0}^{2\pi} r^2\sin^2\theta \cdot r \, d\theta \, dr", font_size=22)
        polar_integral.next_to(double_integral, DOWN, buff=0.4).align_to(double_integral, LEFT)
        self.add_fixed_in_frame_mobjects(polar_integral)
        self.play(Write(polar_integral), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 极坐标下的解释 - 修复错误
        explanation_1 = Text("ρ: 面密度", font_size=16)
        explanation_2 = Text("r sin θ: 到x轴的距离", font_size=16)
        polar_explanations = VGroup(explanation_1, explanation_2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        polar_explanations.next_to(polar_integral, RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(polar_explanations)
        self.play(Write(polar_explanations), run_time=1.5)
        self.wait(0.5)  # 减少等待时间
        
        # 积分计算过程 - 使用rho替代sigma
        calc_1 = MathTex(r"I &= \rho \int_{0}^{R} r^3 \, dr \int_{0}^{2\pi} \sin^2 \theta \, d\theta \\", font_size=20)
        calc_2 = MathTex(r"&= \rho \int_{0}^{R} r^3 \, dr \cdot \pi \\", font_size=20)
        calc_3 = MathTex(r"&= \pi \rho \cdot \frac{R^4}{4} \\", font_size=20)
        calc_4 = MathTex(r"&= \frac{\pi R^2 \rho \cdot R^2}{4} \\", font_size=20)
        calc_5 = MathTex(r"&= \frac{1}{4} M R^2", font_size=20)
        
        calculations = VGroup(calc_1, calc_2, calc_3, calc_4, calc_5).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        calculations.next_to(polar_integral, DOWN, buff=0.4, aligned_edge=LEFT)
        
        for calc in calculations:
            self.add_fixed_in_frame_mobjects(calc)
            self.play(Write(calc), run_time=0.6)  # 减少每步计算的显示时间
            self.wait(0.1)  # 减少每步之间的等待时间
        
        # 最终结果
        final_box = SurroundingRectangle(calc_5, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(final_box)
        self.play(Create(final_box), run_time=0.8)  # 减少框显示时间
        self.wait(0.2)  # 减少等待时间
        
        # 将最终结果显示在屏幕下方，不使用飞入动画
        final_result = MathTex(r"I = \frac{1}{4} M R^2", font_size=32, color=YELLOW)
        final_result.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(final_result)
        self.play(Write(final_result), run_time=1.0)  # 缩短结果显示时间
        self.wait(0.5)  # 减少最终结果后的等待时间
        
        # 淡出微元划分，只保留整个圆盘
        self.play(
            *[FadeOut(strip) for strip in strips],
            FadeOut(distance_line),
            FadeOut(distance_label),
            FadeOut(dm_label),
            run_time=1.0
        )
        
        # 演示旋转 - 只旋转圆盘
        self.move_camera(phi=90 * DEGREES, theta=0)
        self.begin_ambient_camera_rotation(rate=0.15)
        
        # 只旋转圆盘
        self.play(
            Rotating(
                disk,
                axis=RIGHT,
                radians=2*PI,
                run_time=5,
                rate_func=linear
            ),
            run_time=5
        )
        
        self.stop_ambient_camera_rotation()
        self.wait(2)  # 添加一点等待时间后结束

        # 删除以下结束语部分
        # self.move_camera(phi=70 * DEGREES, theta=30 * DEGREES)
        # 
        # end_title = Text("转动惯量计算演示完成", font_size=42)
        # end_title.to_edge(UP)
        # self.add_fixed_in_frame_mobjects(end_title)
        # 
        # conclusion = Text("从微元到积分的物理意义", font_size=36)
        # conclusion.next_to(end_title, DOWN, buff=1)
        # self.add_fixed_in_frame_mobjects(conclusion)
        # 
        # self.play(
        #     FadeOut(title),
        #     Write(end_title),
        #     Write(conclusion),
        #     run_time=2
        # )
        # self.wait(2)
        # 
        # self.play(
        #     FadeOut(end_title),
        #     FadeOut(conclusion),
        #     run_time=1.5
        # ) 