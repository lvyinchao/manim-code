from manim import *
import numpy as np

class MomentOfInertiaScene(ThreeDScene):
    def construct(self):
        # 设置场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.camera.set_zoom(0.8)
        
        # 创建坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)
        
        # 旋转轴（z轴）
        rotation_axis = Line3D(
            start=np.array([0, 0, -1]),
            end=np.array([0, 0, 5]),
            color=RED
        )
        axis_label = Text("旋转轴", font_size=24).set_color(RED)
        axis_label.next_to(rotation_axis.get_end(), UP+RIGHT)
        
        # 展示基本元素
        self.play(
            Create(axes),
            Create(labels),
            run_time=1
        )
        self.play(
            Create(rotation_axis),
            Write(axis_label),
            run_time=1
        )
        self.wait(1)
        
        # 创建物体（例如圆柱体）
        cylinder = Cylinder(radius=2, height=3, direction=OUT, resolution=(20, 20))
        cylinder.set_fill(BLUE, opacity=0.3)
        cylinder.set_stroke(BLUE_E, opacity=0.8, width=0.5)
        cylinder.move_to(axes.c2p(0, 0, 1.5))
        
        formula = MathTex(r"I = \int r^2 dm", font_size=36)
        formula.to_corner(UL)
        
        self.play(
            Create(cylinder),
            Write(formula),
            run_time=1.5
        )
        self.wait(1)
        
        # 展示微元
        dm_point = Dot3D(axes.c2p(1.5, 0, 1.5), color=YELLOW, radius=0.05)
        r_line = Line3D(
            start=axes.c2p(0, 0, 1.5),
            end=axes.c2p(1.5, 0, 1.5),
            color=GREEN
        )
        r_label = MathTex("r", font_size=28).set_color(GREEN)
        r_label.move_to(axes.c2p(0.8, 0.3, 1.5))
        
        dm_label = MathTex("dm", font_size=24).set_color(YELLOW)
        dm_label.move_to(axes.c2p(1.7, 0.2, 1.5))
        
        self.play(
            Create(dm_point),
            Create(r_line),
            Write(r_label),
            Write(dm_label),
            run_time=1.5
        )
        self.wait(1)
        
        # 展示r^2因子
        r_squared = MathTex("r^2 =", font_size=24).set_color(GREEN)
        r_value = DecimalNumber(1.5**2, num_decimal_places=2, font_size=24)
        r_squared_group = VGroup(r_squared, r_value).arrange(RIGHT)
        r_squared_group.move_to(axes.c2p(0, -2, 3))
        
        self.play(
            Write(r_squared_group),
            run_time=1
        )
        self.wait(1)
        
        # 创建更多微元以展示积分过程
        dots = []
        r_lines = []
        
        for theta in np.linspace(0, 2*np.pi, 8, endpoint=False):
            for r in np.linspace(0.5, 1.8, 3):
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                dot = Dot3D(axes.c2p(x, y, 1.5), color=YELLOW, radius=0.05)
                line = Line3D(
                    start=axes.c2p(0, 0, 1.5),
                    end=axes.c2p(x, y, 1.5),
                    color=GREEN_E
                )
                dots.append(dot)
                r_lines.append(line)
        
        self.play(
            *[Create(dot) for dot in dots],
            *[Create(line) for line in r_lines],
            run_time=2
        )
        self.wait(1)
        
        # 展示求和到积分的过程
        discrete_formula = MathTex(r"I \approx \sum_i r_i^2 \Delta m_i", font_size=36)
        discrete_formula.move_to(formula.get_center())
        
        self.play(
            TransformMatchingTex(formula, discrete_formula),
            run_time=1.5
        )
        self.wait(1)
        
        integral_formula = MathTex(r"I = \int_V r^2 \rho dV", font_size=36)
        integral_formula.move_to(discrete_formula.get_center())
        
        self.play(
            TransformMatchingTex(discrete_formula, integral_formula),
            run_time=1.5
        )
        self.wait(1)
        
        # 展示转动惯量的值
        final_formula = MathTex(r"I = \frac{1}{2}MR^2", font_size=36)
        final_formula.move_to(integral_formula.get_center() + DOWN)
        
        self.play(
            Write(final_formula),
            run_time=1.5
        )
        self.wait(1)
        
        # 显示一些常见物体的转动惯量公式
        formulas_title = Text("常见物体的转动惯量", font_size=28)
        formulas_title.to_corner(UR).shift(DOWN)
        
        # 使用Text类和MathTex类的组合来显示公式
        rod_text = Text("细杆(端点):", font_size=24)
        rod_formula = MathTex(r"I = \frac{1}{3}ML^2", font_size=24)
        rod_group = VGroup(rod_text, rod_formula).arrange(RIGHT)
        
        disk_text = Text("圆盘(中心):", font_size=24)
        disk_formula = MathTex(r"I = \frac{1}{2}MR^2", font_size=24)
        disk_group = VGroup(disk_text, disk_formula).arrange(RIGHT)
        
        sphere_text = Text("球体(中心):", font_size=24)
        sphere_formula = MathTex(r"I = \frac{2}{5}MR^2", font_size=24)
        sphere_group = VGroup(sphere_text, sphere_formula).arrange(RIGHT)
        
        formulas = VGroup(rod_group, disk_group, sphere_group).arrange(DOWN, aligned_edge=LEFT)
        formulas.next_to(formulas_title, DOWN, aligned_edge=LEFT)
        
        self.play(
            Write(formulas_title),
            run_time=1
        )
        self.play(
            Write(formulas),
            run_time=2
        )
        
        # 旋转物体以展示转动惯量的物理意义
        self.move_camera(phi=65 * DEGREES, theta=0 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)
        
        self.play(
            Rotating(
                cylinder,
                axis=OUT,
                radians=2*PI,
                about_point=axes.c2p(0, 0, 0),
                run_time=4,
                rate_func=linear
            )
        )
        
        self.stop_ambient_camera_rotation()
        self.wait(2)


class AngularAccelerationScene(Scene):
    def construct(self):
        # 创建标题
        title = Text("转动惯量与角加速度的关系", font_size=36)
        subtitle = MathTex(r"\tau = I \alpha", font_size=40)
        
        self.play(Write(title), run_time=1)
        self.play(
            title.animate.to_edge(UP),
            run_time=1
        )
        self.play(Write(subtitle), run_time=1)
        self.play(
            subtitle.animate.next_to(title, DOWN),
            run_time=1
        )
        self.wait(1)
        
        # 解释力矩、转动惯量和角加速度的关系
        explanation = MathTex(
            r"\tau", r"&=", r"I", r"\alpha\\",
            r"\alpha", r"&=", r"\frac{\tau}{I}",
            font_size=36
        )
        explanation.next_to(subtitle, DOWN, buff=1)
        
        self.play(Write(explanation), run_time=2)
        self.wait(1)
        
        # 创建两个不同转动惯量的物体
        disk_small = Circle(radius=1, color=BLUE)
        disk_small.set_fill(BLUE, opacity=0.3)
        disk_small.move_to(LEFT * 3)
        
        disk_large = Circle(radius=2, color=RED)
        disk_large.set_fill(RED, opacity=0.3)
        disk_large.move_to(RIGHT * 3)
        
        disk_small_label = Text("小转动惯量", font_size=24, color=BLUE)
        disk_small_label.next_to(disk_small, UP)
        
        disk_large_label = Text("大转动惯量", font_size=24, color=RED)
        disk_large_label.next_to(disk_large, UP)
        
        # 显示两个物体
        self.play(
            Create(disk_small),
            Create(disk_large),
            Write(disk_small_label),
            Write(disk_large_label),
            run_time=2
        )
        self.wait(1)
        
        # 物体的转动惯量值
        I_small = MathTex(r"I_1 = 1", font_size=30, color=BLUE)
        I_small.next_to(disk_small, DOWN)
        
        I_large = MathTex(r"I_2 = 4", font_size=30, color=RED)
        I_large.next_to(disk_large, DOWN)
        
        self.play(
            Write(I_small),
            Write(I_large),
            run_time=1
        )
        self.wait(1)
        
        # 施加相同的力矩
        torque = MathTex(r"\tau = 2", font_size=30)
        torque.to_edge(DOWN).shift(UP)
        
        self.play(Write(torque), run_time=1)
        self.wait(1)
        
        # 计算角加速度
        alpha_small = MathTex(r"\alpha_1 = \frac{\tau}{I_1} = \frac{2}{1} = 2", font_size=30, color=BLUE)
        alpha_small.next_to(I_small, DOWN)
        
        alpha_large = MathTex(r"\alpha_2 = \frac{\tau}{I_2} = \frac{2}{4} = 0.5", font_size=30, color=RED)
        alpha_large.next_to(I_large, DOWN)
        
        self.play(
            Write(alpha_small),
            Write(alpha_large),
            run_time=2
        )
        self.wait(1)
        
        # 旋转两个圆盘以显示角加速度的差异
        self.play(
            Rotating(
                disk_small,
                radians=4*PI,
                run_time=4,
                rate_func=lambda t: t**2  # 模拟加速度为常数的旋转
            ),
            Rotating(
                disk_large,
                radians=PI,
                run_time=4,
                rate_func=lambda t: t**2  # 模拟加速度为常数的旋转
            ),
            run_time=4
        )
        self.wait(1)
        
        # 展示结论
        conclusion = Text("转动惯量越大，角加速度越小", font_size=32)
        conclusion.to_edge(DOWN).shift(UP * 2)
        
        self.play(
            ReplacementTransform(torque, conclusion),
            run_time=1
        )
        self.wait(2)


class InertiaApplicationScene(Scene):
    def construct(self):
        # 标题
        title = Text("转动惯量的应用", font_size=36)
        self.play(Write(title), run_time=1)
        self.play(title.animate.to_edge(UP), run_time=1)
        self.wait(1)
        
        # 创建几个应用场景
        
        # 1. 陀螺仪
        gyroscope_title = Text("陀螺仪稳定性", font_size=28)
        gyroscope_title.next_to(title, DOWN, buff=0.8).to_edge(LEFT).shift(RIGHT)
        
        gyroscope = Circle(radius=1.5, color=BLUE)
        gyroscope.set_fill(BLUE, opacity=0.2)
        gyroscope.next_to(gyroscope_title, DOWN, buff=0.5)
        
        gyro_axis = Line(
            start=gyroscope.get_center() + LEFT * 1.5,
            end=gyroscope.get_center() + RIGHT * 1.5,
            color=RED
        )
        
        gyro_formula = MathTex(r"L = I\omega", font_size=28)
        gyro_formula.next_to(gyroscope, DOWN, buff=0.5)
        
        gyro_group = VGroup(gyroscope, gyro_axis, gyro_formula)
        
        # 2. 飞轮
        flywheel_title = Text("飞轮能量存储", font_size=28)
        flywheel_title.next_to(title, DOWN, buff=0.8).to_edge(RIGHT).shift(LEFT)
        
        flywheel = Circle(radius=1.5, color=GREEN)
        flywheel.set_fill(GREEN, opacity=0.2)
        flywheel.next_to(flywheel_title, DOWN, buff=0.5)
        
        flywheel_formula = MathTex(r"E = \frac{1}{2}I\omega^2", font_size=28)
        flywheel_formula.next_to(flywheel, DOWN, buff=0.5)
        
        flywheel_group = VGroup(flywheel, flywheel_formula)
        
        # 展示应用
        self.play(
            Write(gyroscope_title),
            Create(gyroscope),
            Create(gyro_axis),
            run_time=1.5
        )
        self.play(Write(gyro_formula), run_time=1)
        
        self.play(
            Write(flywheel_title),
            Create(flywheel),
            run_time=1.5
        )
        self.play(Write(flywheel_formula), run_time=1)
        self.wait(1)
        
        # 演示陀螺仪旋转
        self.play(
            Rotating(gyro_group, axis=RIGHT, radians=PI/2, run_time=2),
            Rotating(gyroscope, axis=IN, radians=4*PI, run_time=2, rate_func=linear),
        )
        self.play(
            Rotating(gyro_group, axis=UP, radians=PI, run_time=2),
            Rotating(gyroscope, axis=IN, radians=4*PI, run_time=2, rate_func=linear),
        )
        
        # 演示飞轮旋转和储能
        energy_label = Text("储存动能", font_size=24, color=GREEN)
        energy_label.next_to(flywheel, UP)
        
        self.play(
            Rotating(
                flywheel,
                radians=8*PI,
                run_time=4,
                rate_func=rush_into
            ),
            Write(energy_label),
            run_time=2
        )
        
        # 总结
        conclusion = Text("转动惯量在工程中的重要应用", font_size=32)
        conclusion.to_edge(DOWN).shift(UP)
        
        self.play(Write(conclusion), run_time=1.5)
        self.wait(2) 