from manim import *
import numpy as np

class ConditionalExtremaDemo(ThreeDScene):
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # 创建标题
        title = Text("条件极值问题", font="PingFang SC", font_size=32)
        title.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait()

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": GRAY}
        )
        self.add(axes)
        self.wait()

        # 定义目标函数 f(x,y) = x^2 + y^2
        def f(x, y):
            return x**2 + y**2

        # 定义约束条件 g(x,y) = x^2 + y^2/2 - 1 = 0
        def g(x, y):
            return x**2 + y**2/2 - 1

        # 创建目标函数的曲面
        surface = Surface(
            lambda u, v: np.array([
                u,
                v,
                f(u, v)
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            checkerboard_colors=[BLUE_D, BLUE_E],
            resolution=(30, 30)
        )
        self.play(Create(surface))
        self.wait()

        # 创建约束条件的椭圆
        constraint_ellipse = ParametricFunction(
            lambda t: np.array([
                np.cos(t),
                np.sqrt(2) * np.sin(t),
                0
            ]),
            t_range=[0, 2*PI],
            color=YELLOW
        )
        self.play(Create(constraint_ellipse))
        self.wait()

        # 显示目标函数和约束条件
        equations = VGroup(
            Text("目标函数：", font="PingFang SC", color=WHITE, font_size=24),
            MathTex(r"f(x,y) = x^2 + y^2", color=WHITE, font_size=24),
            Text("约束条件：", font="PingFang SC", color=YELLOW, font_size=24),
            MathTex(r"g(x,y) = x^2 + \frac{y^2}{2} - 1 = 0", color=YELLOW, font_size=24)
        )
        equations.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        equations.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(equations)
        self.play(Write(equations))
        self.wait()

        # 创建等高线
        contour_levels = [0.25, 0.5, 0.75, 1.0, 1.25, 1.5]
        contours = VGroup()
        for level in contour_levels:
            contour = ParametricFunction(
                lambda t: np.array([
                    np.sqrt(level) * np.cos(t),
                    np.sqrt(level) * np.sin(t),
                    0
                ]),
                t_range=[0, 2*PI],
                color=BLUE_D
            )
            contours.add(contour)
        
        # 添加等高线说明
        contour_explanation = Text(
            "等高线",
            font="PingFang SC",
            color=BLUE_D,
            font_size=20
        )
        contour_explanation.next_to(contours, RIGHT, buff=0.5)
        self.add_fixed_in_frame_mobjects(contour_explanation)
        self.play(Write(contour_explanation))
        self.wait()
        
        self.play(Create(contours))
        self.wait()

        # 显示几个非极值点及其梯度
        non_extremum_points = [
            (-0.8, 0.4),  # 第一个点，在左下角
            (0.3, 1.2),  # 第二个点
            (-0.6, 0.8)  # 第三个点
        ]

        for x, y in non_extremum_points:
            # 创建点
            point = Dot3D(point=np.array([x, y, 0]), color=RED, radius=0.08)
            self.play(Create(point))

            # 计算梯度向量
            grad_f_vec = np.array([2*x, 2*y, 0])  # ∇f 的方向
            grad_g_vec = np.array([2*x, y, 0])    # ∇g 的方向
            
            # 归一化并缩放梯度向量
            scale = 1.0
            grad_f_vec = scale * grad_f_vec / np.linalg.norm(grad_f_vec)
            grad_g_vec = scale * grad_g_vec / np.linalg.norm(grad_g_vec)

            # 创建梯度箭头
            grad_f_arrow = Arrow(
                start=np.array([x, y, 0]),
                end=np.array([x + grad_f_vec[0], y + grad_f_vec[1], 0]),
                color=BLUE,
                buff=0.1,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.2
            )
            grad_g_arrow = Arrow(
                start=np.array([x, y, 0]),
                end=np.array([x + grad_g_vec[0], y + grad_g_vec[1], 0]),
                color=YELLOW,
                buff=0.1,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.2
            )
            self.play(Create(grad_f_arrow), Create(grad_g_arrow))
            self.wait()

        # 添加梯度方向的解释说明（移到左侧）
        gradient_explanation = VGroup(
            Text("蓝色箭头：目标函数f的梯度∇f", font="PingFang SC", color=BLUE, font_size=20),
            Text("黄色箭头：约束条件g的梯度∇g", font="PingFang SC", color=YELLOW, font_size=20)
        )
        gradient_explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        gradient_explanation.to_corner(UL, buff=0.5)
        gradient_explanation.shift(DOWN * 1.5)  # 向下移动一点，避免与标题重叠
        self.add_fixed_in_frame_mobjects(gradient_explanation)
        self.play(Write(gradient_explanation))
        self.wait(2)

        # 显示梯度条件
        gradient_condition = VGroup(
            MathTex(r"\nabla f = \lambda \nabla g", color=GREEN, font_size=24),
            MathTex(r"(2x, 2y) = \lambda(2x, y)", color=GREEN, font_size=24)
        )
        gradient_condition.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        gradient_condition.next_to(equations, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(gradient_condition)
        self.play(Write(gradient_condition))
        self.wait()

        # 显示方程组
        system_eq = VGroup(
            MathTex(r"2x - 2\lambda x = 0", color=WHITE, font_size=24),
            MathTex(r"2y - \lambda y = 0", color=WHITE, font_size=24),
            MathTex(r"x^2 + \frac{y^2}{2} - 1 = 0", color=WHITE, font_size=24)
        )
        system_eq.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        system_eq.next_to(gradient_condition, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(system_eq)
        self.play(Write(system_eq))
        self.wait()

        # 显示解
        solution = VGroup(
            MathTex(r"x = 0, y = \pm\sqrt{2}", color=RED, font_size=24),
            MathTex(r"x = \pm 1, y = 0", color=RED, font_size=24)
        )
        solution.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        solution.next_to(system_eq, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(solution)
        self.play(Write(solution))
        self.wait()

        # 显示极值点
        extremum_points = [
            (0, np.sqrt(2)),    # 最大值点
            (0, -np.sqrt(2)),   # 最大值点
            (1, 0),             # 最小值点
            (-1, 0)             # 最小值点
        ]
        
        for x, y in extremum_points:
            point = Dot3D(point=np.array([x, y, 0]), color=RED, radius=0.1)
            self.play(Create(point))
            
            # 在极值点处显示梯度向量
            grad_f = Arrow(
                start=np.array([x, y, 0]),
                end=np.array([x + 2*x, y + 2*y, 0]),
                color=BLUE,
                buff=0.1,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.2
            )
            grad_g = Arrow(
                start=np.array([x, y, 0]),
                end=np.array([x + 2*x, y + y, 0]),
                color=YELLOW,
                buff=0.1,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.2
            )
            self.play(
                Create(grad_f),
                Create(grad_g),
                Flash(point, color=RED, flash_radius=0.5)
            )
            self.wait()

        # 显示极值点坐标
        extremum_coords = VGroup(
            VGroup(
                MathTex(r"(0, \sqrt{2})", color=RED, font_size=24),
                MathTex(r"(0, -\sqrt{2})", color=RED, font_size=24)
            ),
            VGroup(
                MathTex(r"(1, 0)", color=RED, font_size=24),
                MathTex(r"(-1, 0)", color=RED, font_size=24)
            )
        )
        # 设置每列内部的对齐方式
        extremum_coords[0].arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        extremum_coords[1].arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        # 设置两列之间的间距
        extremum_coords.arrange(RIGHT, aligned_edge=UP, buff=0.5)
        extremum_coords.next_to(solution, DOWN, buff=0.3)
        extremum_coords.shift(LEFT * 0.5)  # 向左移动一点
        self.add_fixed_in_frame_mobjects(extremum_coords)
        self.play(Write(extremum_coords))
        self.wait()

        # 添加极值点处的说明
        extremum_explanation = VGroup(
            Text("在极值点处，两个梯度方向相同", font="PingFang SC", color=RED, font_size=20),
            Text("(1,0)和(-1,0)是最小值点", font="PingFang SC", color=RED, font_size=20),
            Text("(0,±√2)是最大值点", font="PingFang SC", color=RED, font_size=20)
        )
        extremum_explanation.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        extremum_explanation.next_to(extremum_coords, DOWN, buff=0.3)
        extremum_explanation.shift(LEFT * 0.5)  # 向左移动一点
        self.add_fixed_in_frame_mobjects(extremum_explanation)
        self.play(Write(extremum_explanation))
        self.wait(2)

        # 总结（移到最底部）
        summary = VGroup(
            Text(
                "在极值点处，目标函数的梯度与约束条件的梯度平行",
                font="PingFang SC",
                color=WHITE,
                font_size=24
            ),
            Text(
                "这就是拉格朗日乘数法的几何意义",
                font="PingFang SC",
                color=WHITE,
                font_size=24
            )
        )
        summary.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        summary.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(Write(summary))
        self.wait(2)

        # 旋转视角以更好地观察
        self.move_camera(phi=45 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait()

        # 开始环绕旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait()

        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        ) 