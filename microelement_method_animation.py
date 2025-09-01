from manim import *
import numpy as np

class MicroelementMethodScene(ThreeDScene):
    def construct(self):
        # 设置相机
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.8)
        
        # 标题
        title = Text("微元法的原理与应用", font_size=42)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.5)
        
        # 介绍文本
        intro = Text("将物体划分为无数个微小元素，再对所有微元进行积分", font_size=28)
        intro.next_to(title, DOWN, buff=0.8)
        self.add_fixed_in_frame_mobjects(intro)
        self.play(Write(intro), run_time=1.5)
        self.wait(1)
        
        # 淡出介绍
        self.play(FadeOut(intro), run_time=1)
        
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
        
        # 第一个示例：使用微元法计算圆的面积
        example_title = Text("示例1：计算圆的面积", font_size=32)
        example_title.next_to(title, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(example_title)
        self.play(Write(example_title), run_time=1.2)
        
        # 创建圆
        circle = Circle(radius=2, color=BLUE, fill_opacity=0.2)
        circle.move_to(ORIGIN)
        self.play(Create(circle), run_time=1.5)
        self.wait(0.5)
        
        # 创建径向划分的微元
        num_sectors = 20
        sectors = []
        sector_angles = []
        radius = 2
        
        for i in range(num_sectors):
            start_angle = i * (2*PI/num_sectors)
            end_angle = (i+1) * (2*PI/num_sectors)
            sector_angles.append((start_angle, end_angle))
            
            sector = Sector(
                outer_radius=radius,
                angle=end_angle - start_angle,
                start_angle=start_angle,
                fill_opacity=0.4,
                fill_color=BLUE_C,
                stroke_color=WHITE,
                stroke_width=1
            )
            sectors.append(sector)
        
        # 一次性绘制所有扇形
        self.play(
            FadeOut(circle),
            *[Create(sector) for sector in sectors],
            run_time=2
        )
        self.wait(1)
        
        # 高亮显示一个扇形微元
        highlight_index = 5
        sectors[highlight_index].set_fill(YELLOW, opacity=0.7)
        
        # 标记微元
        dm_label = MathTex("dA", font_size=28).set_color(YELLOW)
        angle_mid = (sector_angles[highlight_index][0] + sector_angles[highlight_index][1]) / 2
        dm_pos = np.array([
            1.2 * np.cos(angle_mid),
            1.2 * np.sin(angle_mid),
            0
        ])
        dm_label.move_to(dm_pos)
        self.add_fixed_in_frame_mobjects(dm_label)
        
        # 标记半径
        radius_line = Line(
            start=ORIGIN,
            end=np.array([radius * np.cos(angle_mid), radius * np.sin(angle_mid), 0]),
            color=RED
        )
        radius_label = MathTex("r", font_size=28).set_color(RED)
        radius_label.move_to(radius_line.get_center() + np.array([0.3, 0.3, 0]))
        self.add_fixed_in_frame_mobjects(radius_label)
        
        # 显示标记
        self.play(
            Create(radius_line),
            Write(radius_label),
            Write(dm_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 微元面积公式
        element_area = MathTex(r"dA = \frac{1}{2} r^2 d\theta", font_size=28)
        element_area.to_corner(UR).shift(LEFT * 2 + DOWN * 1)
        self.add_fixed_in_frame_mobjects(element_area)
        self.play(Write(element_area), run_time=1.5)
        
        # 积分公式
        integral = MathTex(r"A = \int_0^{2\pi} dA = \int_0^{2\pi} \frac{1}{2} r^2 d\theta", font_size=28)
        integral.next_to(element_area, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(integral)
        self.play(Write(integral), run_time=1.5)
        
        # 积分结果
        result = MathTex(r"A = \frac{1}{2} r^2 \cdot 2\pi = \pi r^2", font_size=28)
        result.next_to(integral, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(result)
        self.play(Write(result), run_time=1.5)
        
        # 强调结果
        result_box = SurroundingRectangle(result, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(result_box)
        self.play(Create(result_box), run_time=1)
        self.wait(1)
        
        # 淡出第一个示例
        self.play(
            *[FadeOut(mob) for mob in [
                example_title, *sectors, radius_line, radius_label, 
                dm_label, element_area, integral, result, result_box
            ]],
            run_time=1.5
        )
        
        # 第二个示例：使用微元法计算圆柱体的体积
        example2_title = Text("示例2：计算圆柱体的体积", font_size=32)
        example2_title.next_to(title, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(example2_title)
        self.play(Write(example2_title), run_time=1.2)
        
        # 创建圆柱体
        cylinder = Cylinder(radius=1.5, height=3, fill_opacity=0.2, color=BLUE)
        cylinder.move_to(ORIGIN)
        self.play(Create(cylinder), run_time=1.5)
        self.wait(0.5)
        
        # 创建水平切片微元
        num_slices = 12
        slices = []
        slice_heights = []
        cylinder_height = 3
        cylinder_radius = 1.5
        
        slice_height = cylinder_height / num_slices
        
        for i in range(num_slices):
            # 计算切片中心的z坐标
            z_center = -cylinder_height/2 + (i + 0.5) * slice_height
            slice_heights.append(z_center)
            
            # 创建圆柱切片
            slice_cylinder = Cylinder(
                radius=cylinder_radius,
                height=slice_height,
                fill_opacity=0.4,
                color=BLUE_C,
                stroke_color=WHITE,
                stroke_width=1
            )
            
            # 将切片移动到对应位置
            slice_cylinder.move_to(np.array([0, 0, z_center]))
            slices.append(slice_cylinder)
        
        # 一次性绘制所有切片
        self.play(
            FadeOut(cylinder),
            *[Create(slice) for slice in slices],
            run_time=2
        )
        self.wait(1)
        
        # 高亮显示一个切片微元
        highlight_index = 6
        slices[highlight_index].set_fill(YELLOW, opacity=0.7)
        
        # 标记微元
        dv_label = MathTex("dV", font_size=28).set_color(YELLOW)
        dv_label.move_to(np.array([2, 0, slice_heights[highlight_index]]))
        self.add_fixed_in_frame_mobjects(dv_label)
        
        # 标记底面积
        base_label = MathTex("A", font_size=28).set_color(GREEN)
        base_label.move_to(np.array([0, 0, slice_heights[highlight_index]]) + np.array([0, 0.8, 0]))
        self.add_fixed_in_frame_mobjects(base_label)
        
        # 标记高度
        height_line = Line3D(
            start=np.array([2, 0, slice_heights[highlight_index] - slice_height/2]),
            end=np.array([2, 0, slice_heights[highlight_index] + slice_height/2]),
            color=RED
        )
        height_label = MathTex("dh", font_size=28).set_color(RED)
        height_label.move_to(np.array([2.3, 0, slice_heights[highlight_index]]))
        self.add_fixed_in_frame_mobjects(height_label)
        
        # 显示标记
        self.play(
            Create(height_line),
            Write(height_label),
            Write(base_label),
            Write(dv_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 微元体积公式
        element_volume = MathTex(r"dV = A \cdot dh", font_size=28)
        element_volume.to_corner(UR).shift(LEFT * 2 + DOWN * 1)
        self.add_fixed_in_frame_mobjects(element_volume)
        self.play(Write(element_volume), run_time=1.5)
        
        # 底面积公式
        base_area = MathTex(r"A = \pi r^2", font_size=28)
        base_area.next_to(element_volume, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(base_area)
        self.play(Write(base_area), run_time=1.5)
        
        # 积分公式
        integral2 = MathTex(r"V = \int_0^h dV = \int_0^h A \cdot dh = A \int_0^h dh", font_size=28)
        integral2.next_to(base_area, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(integral2)
        self.play(Write(integral2), run_time=1.5)
        
        # 积分结果
        result2 = MathTex(r"V = A \cdot h = \pi r^2 h", font_size=28)
        result2.next_to(integral2, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(result2)
        self.play(Write(result2), run_time=1.5)
        
        # 强调结果
        result2_box = SurroundingRectangle(result2, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(result2_box)
        self.play(Create(result2_box), run_time=1)
        self.wait(1)
        
        # 第三个示例：转动惯量的微元法
        self.play(
            FadeOut(example2_title),
            *[FadeOut(slice) for slice in slices],
            FadeOut(height_line),
            FadeOut(height_label),
            FadeOut(base_label),
            FadeOut(dv_label),
            FadeOut(element_volume),
            FadeOut(base_area),
            FadeOut(integral2),
            FadeOut(result2),
            FadeOut(result2_box),
            run_time=1.5
        )
        
        example3_title = Text("示例3：计算转动惯量", font_size=32)
        example3_title.next_to(title, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(example3_title)
        self.play(Write(example3_title), run_time=1.2)
        
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
        
        # 创建旋转轴（x轴）
        axis = Line3D(
            start=np.array([-2.5, 0, 0]),
            end=np.array([2.5, 0, 0]),
            color=RED
        )
        axis_label = Text("旋转轴", font_size=24).set_color(RED)
        axis_label.next_to(axis.get_end(), RIGHT)
        self.add_fixed_in_frame_mobjects(axis_label)
        
        # 显示圆盘和旋转轴
        self.play(
            Create(disk),
            Create(axis),
            Write(axis_label),
            run_time=2
        )
        self.wait(1)
        
        # 创建同心环微元
        num_rings = 8
        rings = []
        ring_radii = []
        max_radius = 2
        
        for i in range(num_rings):
            inner_radius = i * (max_radius / num_rings)
            outer_radius = (i + 1) * (max_radius / num_rings)
            ring_radii.append((inner_radius + outer_radius) / 2)
            
            ring = Annulus(
                inner_radius=inner_radius,
                outer_radius=outer_radius,
                fill_opacity=0.4,
                fill_color=BLUE_C,
                stroke_color=WHITE,
                stroke_width=1
            )
            rings.append(ring)
        
        # 一次性绘制所有环形
        self.play(
            FadeOut(disk),
            *[Create(ring) for ring in rings],
            run_time=2
        )
        self.wait(1)
        
        # 高亮显示一个环形微元
        highlight_index = 5
        rings[highlight_index].set_fill(YELLOW, opacity=0.7)
        
        # 标记微元
        dm_label = MathTex("dm", font_size=28).set_color(YELLOW)
        dm_label.move_to(np.array([ring_radii[highlight_index] * np.cos(PI/4), 
                                   ring_radii[highlight_index] * np.sin(PI/4), 0]))
        self.add_fixed_in_frame_mobjects(dm_label)
        
        # 标记半径
        r_label = MathTex("r", font_size=28).set_color(GREEN)
        r_label.move_to(np.array([ring_radii[highlight_index]/2, 0, 0.1]))
        self.add_fixed_in_frame_mobjects(r_label)
        
        # 显示标记
        self.play(
            Write(dm_label),
            Write(r_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 微元转动惯量公式
        element_inertia = MathTex(r"dI = r^2 \cdot dm", font_size=28)
        element_inertia.to_corner(UR).shift(LEFT * 2 + DOWN * 1)
        self.add_fixed_in_frame_mobjects(element_inertia)
        self.play(Write(element_inertia), run_time=1.5)
        
        # 积分公式
        integral3 = MathTex(r"I = \int_D r^2 \, dm = \int_D r^2 \, \rho \, dA", font_size=28)
        integral3.next_to(element_inertia, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(integral3)
        self.play(Write(integral3), run_time=1.5)
        
        # 极坐标形式
        polar_form = MathTex(r"I = \int_0^R \int_0^{2\pi} r^2 \cdot \rho \cdot r \, d\theta \, dr", font_size=28)
        polar_form.next_to(integral3, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(polar_form)
        self.play(Write(polar_form), run_time=1.5)
        
        # 积分结果
        result3 = MathTex(r"I = 2\pi \rho \int_0^R r^3 \, dr = \frac{1}{2} \pi \rho R^4 = \frac{1}{2} M R^2", font_size=28)
        result3.next_to(polar_form, DOWN, aligned_edge=LEFT)
        self.add_fixed_in_frame_mobjects(result3)
        self.play(Write(result3), run_time=1.5)
        
        # 强调结果
        result3_box = SurroundingRectangle(result3, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(result3_box)
        self.play(Create(result3_box), run_time=1)
        self.wait(1)
        
        # 演示转动
        self.play(
            FadeOut(example3_title),
            FadeOut(dm_label),
            FadeOut(r_label),
            FadeOut(element_inertia),
            FadeOut(integral3),
            FadeOut(polar_form),
            FadeOut(result3),
            FadeOut(result3_box),
            run_time=1.5
        )
        
        # 恢复完整圆盘显示
        self.play(
            *[FadeOut(ring) for ring in rings],
            FadeIn(disk),
            run_time=1.5
        )
        
        # 展示旋转动画
        self.move_camera(phi=90 * DEGREES, theta=0)
        self.begin_ambient_camera_rotation(rate=0.15)
        
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
        self.wait(1)
        
        # 结论
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES)
        
        conclusion = Text("微元法的核心思想：", font_size=32)
        conclusion.to_edge(DOWN).shift(UP * 0.5)
        self.add_fixed_in_frame_mobjects(conclusion)
        
        conclusion_points = [
            "1. 将物体划分为无数个微小元素",
            "2. 对每个微元应用基本公式",
            "3. 对所有微元进行积分得到总量"
        ]
        
        conclusion_text = VGroup(*[
            Text(point, font_size=24) for point in conclusion_points
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        conclusion_text.next_to(conclusion, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(conclusion_text)
        
        self.play(
            Write(conclusion),
            Write(conclusion_text),
            run_time=2
        )
        
        self.wait(2)
        
        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )


if __name__ == "__main__":
    # 使用manim渲染动画
    from manim import config
    config.quality = "fourk_quality"  # 高清4K质量
    MicroelementMethodScene().render() 