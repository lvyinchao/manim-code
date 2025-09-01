from manim import *
import numpy as np

class VolumeCalculationDemo(ThreeDScene):
    def construct(self):
        # 第一步：清屏显示题目
        problem_title = Text("求立体体积", font_size=32, color=YELLOW)
        problem_desc = Text("求由以下两曲面围成的立体体积", font_size=20, color=WHITE)
        surface_eq1 = MathTex("z = x^2 + y^2", color=BLUE).scale(1.2)
        surface_eq2 = MathTex("z = x + y", color=RED).scale(1.2)
        
        # 居中显示题目
        problem_title.move_to(ORIGIN + UP * 1.5)
        problem_desc.next_to(problem_title, DOWN, buff=0.5)
        surface_eq1.next_to(problem_desc, DOWN, buff=0.8)
        surface_eq2.next_to(surface_eq1, DOWN, buff=0.4)
        
        # 动画1：显示题目和曲面方程
        self.play(Write(problem_title))
        self.wait(1)
        self.play(Write(problem_desc))
        self.wait(1)
        self.play(Write(surface_eq1))
        self.wait(0.8)
        self.play(Write(surface_eq2))
        self.wait(2)
        
        # 动画2：将题目移到右上角保持显示（放大字体）
        title_corner = Text("求立体体积", font_size=24, color=YELLOW).to_corner(UR).shift(LEFT * 0.5 + DOWN * 0.5)
        desc_corner = Text("z=x²+y²与z=x+y围成的立体", font_size=16, color=WHITE).next_to(title_corner, DOWN, buff=0.2)
        
        self.play(
            Transform(problem_title, title_corner),
            Transform(problem_desc, desc_corner),
            FadeOut(surface_eq1),
            FadeOut(surface_eq2)
        )
        self.wait(0.5)
        
        # 设置3D相机
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)
        
        # 固定题目在屏幕上
        self.add_fixed_in_frame_mobjects(problem_title, problem_desc)
        
        # 创建坐标轴（全屏居中）
        axes = ThreeDAxes(
            x_range=[-2, 2, 0.5],
            y_range=[-2, 2, 0.5],
            z_range=[-1, 3, 0.5],
            x_length=6,
            y_length=6,
            z_length=6
        )
        
        # 坐标轴标签
        x_label = axes.get_x_axis_label("x").scale(0.8)
        y_label = axes.get_y_axis_label("y").scale(0.8)
        z_label = axes.get_z_axis_label("z").scale(0.8)
        
        # 动画3：创建坐标轴
        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
        self.wait(1)
        
        # 定义曲面函数
        def paraboloid(u, v):
            return np.array([u, v, u**2 + v**2])
        
        def plane(u, v):
            return np.array([u, v, u + v])
        
        # 创建抛物面 z = x² + y²
        paraboloid_surface = Surface(
            lambda u, v: paraboloid(u, v),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(20, 20),
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=BLUE,
            stroke_width=0.5
        )
        
        # 创建平面 z = x + y
        plane_surface = Surface(
            lambda u, v: plane(u, v),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(15, 15),
            fill_color=RED,
            fill_opacity=0.6,
            stroke_color=RED,
            stroke_width=0.5
        )
        
        # 创建角落显示的公式（左上角，放大字体）
        surface_eq1_corner = MathTex("z = x^2 + y^2", color=BLUE).scale(0.9).to_corner(UL).shift(DOWN * 0.3 + RIGHT * 0.2)
        surface_eq2_corner = MathTex("z = x + y", color=RED).scale(0.9).next_to(surface_eq1_corner, DOWN, buff=0.2)
        
        # 动画4：显示抛物面和公式
        self.add_fixed_in_frame_mobjects(surface_eq1_corner)
        self.play(Create(paraboloid_surface), Write(surface_eq1_corner))
        self.wait(1)
        
        # 动画5：显示平面和公式
        self.add_fixed_in_frame_mobjects(surface_eq2_corner)
        self.play(Create(plane_surface), Write(surface_eq2_corner))
        self.wait(1)
        
        # 动画6：旋转视角查看两个曲面
        self.move_camera(phi=60 * DEGREES, theta=120 * DEGREES, run_time=3)
        self.wait(1)
        
        # 计算交线：x² + y² = x + y
        # 即 x² - x + y² - y = 0
        # 完成平方：(x - 1/2)² + (y - 1/2)² = 1/2
        
        # 创建交线
        intersection_curve = ParametricFunction(
            lambda t: np.array([
                0.5 + np.sqrt(0.5) * np.cos(t),
                0.5 + np.sqrt(0.5) * np.sin(t),
                0.5 + np.sqrt(0.5) * np.cos(t) + 0.5 + np.sqrt(0.5) * np.sin(t)
            ]),
            t_range=[0, 2*PI],
            color=YELLOW,
            stroke_width=4
        )
        
        # 创建角落显示的交线公式（移动到右边投影区域下面）
        intersection_eq_corner = MathTex("x^2 + y^2 = x + y", color=YELLOW).scale(0.8).to_corner(UR).shift(LEFT * 1.2 + DOWN * 2.0)
        intersection_simplified_corner = MathTex(r"(x-\frac{1}{2})^2 + (y-\frac{1}{2})^2 = \frac{1}{2}", color=YELLOW).scale(0.7).next_to(intersection_eq_corner, DOWN, buff=0.15)
        
        # 动画7：显示交线
        self.play(Create(intersection_curve))
        self.wait(1)
        
        # 动画8：着重显示围成的立体区域
        # 突出显示两个曲面围成的立体
        self.play(
            paraboloid_surface.animate.set_fill_opacity(0.8),
            plane_surface.animate.set_fill_opacity(0.7),
            intersection_curve.animate.set_stroke(width=6),
            run_time=2
        )
        self.wait(1)
        
        # 动画9：先显示投影到xy平面
        # 创建投影圆
        projection_circle = Circle(
            radius=np.sqrt(0.5),
            color=GREEN,
            fill_opacity=0.4,
            stroke_color=GREEN,
            stroke_width=3
        ).shift([0.5, 0.5, 0])
        
        # 投影说明放在题目正下方（左移）
        projection_label = Text("投影区域边界", font_size=20, color=GREEN).to_corner(UR).shift(LEFT * 1.2 + DOWN * 1.5)
        self.add_fixed_in_frame_mobjects(projection_label)
        
        self.play(Create(projection_circle), Write(projection_label))
        self.wait(2)
        
        # 动画10：然后显示交线方程
        self.add_fixed_in_frame_mobjects(intersection_eq_corner)
        self.play(Write(intersection_eq_corner))
        self.wait(1)
        
        # 显示交线简化形式
        self.add_fixed_in_frame_mobjects(intersection_simplified_corner)
        self.play(Write(intersection_simplified_corner))
        self.wait(1)
        
        # 动画11：然后演示z上下限的确定方法
        # 创建一个垂直的线段来显示z的范围
        sample_point = [0.3, 0.3, 0]  # 在积分区域内选择一个点
        z_lower = sample_point[0]**2 + sample_point[1]**2  # 抛物面的z值
        z_upper = sample_point[0] + sample_point[1]  # 平面的z值
        
        # 创建垂直线段
        z_line = Line(
            [sample_point[0], sample_point[1], z_lower],
            [sample_point[0], sample_point[1], z_upper],
            color=ORANGE,
            stroke_width=6
        )
        
        # 标记点
        lower_point = Dot([sample_point[0], sample_point[1], z_lower], color=BLUE, radius=0.1)
        upper_point = Dot([sample_point[0], sample_point[1], z_upper], color=RED, radius=0.1)
        
        # 说明文字（在投影区域下方显示，左移）
        z_demo_text = Text("z的上下限演示", font_size=18, color=ORANGE).to_corner(UR).shift(LEFT * 1.2 + DOWN * 3.5)
        self.add_fixed_in_frame_mobjects(z_demo_text)
        
        self.play(
            Write(z_demo_text),
            Create(z_line),
            Create(lower_point),
            Create(upper_point)
        )
        self.wait(2)
        
        # z的上下限说明（在z演示下方显示，左移）
        z_limit_text = Text("确定z的上下限:", font_size=18, color=ORANGE).to_corner(UR).shift(LEFT * 1.2 + DOWN * 4.5)
        z_limit_label1 = Text("下限:", font_size=16, color=BLUE).next_to(z_limit_text, DOWN, buff=0.2)
        z_limit_eq = MathTex(r"z = x^2 + y^2").scale(0.8).next_to(z_limit_label1, RIGHT, buff=0.2)
        z_limit_label2 = Text("上限:", font_size=16, color=RED).next_to(z_limit_label1, DOWN, buff=0.15)
        z_limit_eq2 = MathTex(r"z = x + y").scale(0.8).next_to(z_limit_label2, RIGHT, buff=0.2)
        
        # 动画12：显示z上下限说明（右边）
        self.add_fixed_in_frame_mobjects(z_limit_text)
        self.play(Write(z_limit_text))
        self.wait(1)
        
        # 动画13：显示z下限
        self.add_fixed_in_frame_mobjects(z_limit_label1, z_limit_eq)
        self.play(Write(z_limit_label1), Write(z_limit_eq))
        self.wait(1)
        
        # 动画14：显示z上限
        self.add_fixed_in_frame_mobjects(z_limit_label2, z_limit_eq2)
        self.play(Write(z_limit_label2), Write(z_limit_eq2))
        self.wait(1)
        
        # 创建详细的计算过程公式（左下角上移并右移0.5个单位）
        step1 = Text("计算步骤:", font_size=18, color=YELLOW).to_corner(DL).shift(UP * 4.5 + RIGHT * 1.5)
        step2 = MathTex(r"V = \iint_D \int_{x^2+y^2}^{x+y} dz \, dx \, dy").scale(0.6).next_to(step1, DOWN, buff=0.15)
        step3 = MathTex(r"D: (x-\frac{1}{2})^2 + (y-\frac{1}{2})^2 \leq \frac{1}{2}").scale(0.55).next_to(step2, DOWN, buff=0.1)
        step4 = MathTex(r"V = \iint_D (x+y-x^2-y^2) \, dx \, dy").scale(0.6).next_to(step3, DOWN, buff=0.1)
        step5 = MathTex(r"x = \frac{1}{2} + r\cos\theta, y = \frac{1}{2} + r\sin\theta").scale(0.55).next_to(step4, DOWN, buff=0.1)
        step6 = MathTex(r"V = \int_0^{2\pi} \int_0^{\sqrt{1/2}} r \cdot (\frac{1}{2} - r^2) \, dr \, d\theta").scale(0.6).next_to(step5, DOWN, buff=0.1)
        step7 = MathTex(r"V = \frac{\pi}{8}", color=GREEN).scale(0.9).next_to(step6, DOWN, buff=0.15)
        
        # 动画15：显示积分设置
        self.move_camera(phi=30 * DEGREES, theta=0 * DEGREES, run_time=2)
        
        # 动画16：显示计算步骤标题（左下角）
        self.add_fixed_in_frame_mobjects(step1)
        self.play(Write(step1))
        self.wait(0.8)
        
        # 动画17：显示积分表达式
        self.add_fixed_in_frame_mobjects(step2)
        self.play(Write(step2))
        self.wait(1)
        
        # 动画18：显示积分区域
        self.add_fixed_in_frame_mobjects(step3)
        self.play(Write(step3))
        self.wait(1)
        
        # 动画19：显示简化的积分
        self.add_fixed_in_frame_mobjects(step4)
        self.play(Write(step4))
        self.wait(1)
        
        # 动画20：显示极坐标变换
        self.add_fixed_in_frame_mobjects(step5)
        self.play(Write(step5))
        self.wait(1.5)
        
        # 动画21：显示极坐标积分（包含具体的f表达式）
        self.add_fixed_in_frame_mobjects(step6)
        self.play(Write(step6))
        self.wait(2)
        
        # 动画22：显示最终结果
        self.add_fixed_in_frame_mobjects(step7)
        self.play(Write(step7))
        self.wait(1)
        
        # 动画23：最终旋转展示
        self.move_camera(phi=75 * DEGREES, theta=360 * DEGREES, run_time=4)
        
        self.wait(2)
        
        # 动画24：最终突出显示（避免放大造成重叠）
        self.play(
            projection_circle.animate.set_fill_opacity(0.6),
            projection_label.animate.scale(1.1),
            step7.animate.scale(1.1),
            run_time=2
        )
        
        self.wait(3) 