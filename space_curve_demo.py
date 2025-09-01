from manim import *
import numpy as np

class SpaceCurveDemo(ThreeDScene):
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建标题
        title = Text("空间曲线的切线和法平面", font="PingFang SC", font_size=32)
        title.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait()

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 2, 1],
            axis_config={"color": GRAY}
        )
        self.add(axes)
        self.wait()

        # 定义螺旋线参数方程
        def helix(t):
            return np.array([
                1.5 * np.cos(t),
                1.5 * np.sin(t),
                t/6
            ])

        # 定义螺旋线的导数（切向量）
        def helix_derivative(t):
            return np.array([
                -1.5 * np.sin(t),
                1.5 * np.cos(t),
                1/6
            ])

        # 创建螺旋线
        curve = ParametricFunction(
            lambda t: helix(t),
            t_range=[0, 4*PI],
            color=BLUE
        )
        self.play(Create(curve))
        self.wait()

        # 显示参数方程
        param_eq = VGroup(
            MathTex(r"x = x(t)", color=BLUE, font_size=24),
            MathTex(r"y = y(t)", color=BLUE, font_size=24),
            MathTex(r"z = z(t)", color=BLUE, font_size=24)
        )
        param_eq.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        param_eq.to_corner(UR, buff=0.5)
        param_eq.shift(LEFT)  # 向左移动一个单位
        self.add_fixed_in_frame_mobjects(param_eq)
        self.play(Write(param_eq))
        self.wait()

        # 创建固定点和动点
        fixed_point = helix(1)
        fixed_dot = Dot3D(point=fixed_point, color=RED)
        self.add(fixed_dot)
        self.wait()

        # 创建割线
        def create_secant_line(t):
            point = helix(t)
            direction = point - fixed_point
            # 创建无限延伸的直线
            return Line(
                start=fixed_point - 2*direction,
                end=fixed_point + 2*direction,
                color=YELLOW
            )

        # 创建割线点
        secant_dot = Dot3D(point=helix(3), color=GREEN)
        secant_line = create_secant_line(3)
        self.add(secant_dot, secant_line)
        self.wait()

        # 显示割线方程标注
        secant_label = Text("割线方程", font="PingFang SC", font_size=16, color=YELLOW)
        secant_label.next_to(param_eq, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(secant_label)
        self.play(Write(secant_label))
        self.wait()

        # 显示割线方程
        secant_eq = MathTex(
            r"\frac{x-x(t_0)}{x(t)-x(t_0)} = \frac{y-y(t_0)}{y(t)-y(t_0)} = \frac{z-z(t_0)}{z(t)-z(t_0)}",
            color=YELLOW,
            font_size=20
        )
        secant_eq.next_to(secant_label, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(secant_eq)
        self.play(Write(secant_eq))
        self.wait()

        # 演示割线趋近于切线的过程
        def update_secant(mob, alpha):
            t = 3 - 2*alpha  # 从3趋近于1
            point = helix(t)
            # 更新割线
            direction = point - fixed_point
            if alpha < 0.99:  # 在接近极限之前保持割线
                mob.become(Line(
                    start=fixed_point - 2*direction,
                    end=fixed_point + 2*direction,
                    color=YELLOW
                ))
                # 更新动点位置
                secant_dot.move_to(point)
            else:  # 在最后直接变成切线
                derivative = helix_derivative(1)
                mob.become(Line(
                    start=fixed_point - 2*derivative,
                    end=fixed_point + 2*derivative,
                    color=YELLOW
                ))

        # 创建动画
        self.play(
            UpdateFromAlphaFunc(secant_line, update_secant),
            UpdateFromAlphaFunc(secant_dot, lambda m, a: m.move_to(helix(3 - 2*a))),
            run_time=3
        )
        self.wait()

        # 移除割线点
        self.remove(secant_dot)
        self.wait()

        # 显示极限表示
        limit_eq = MathTex(
            r"\lim_{t \to t_0} \frac{x(t)-x(t_0)}{t-t_0} = x'(t_0)",
            color=YELLOW,
            font_size=20
        )
        limit_eq.next_to(secant_eq, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(limit_eq)
        self.play(Write(limit_eq))
        self.wait()

        # 显示切线方程标注
        tangent_label = Text("切线方程", font="PingFang SC", font_size=16, color=YELLOW)
        tangent_label.next_to(limit_eq, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(tangent_label)
        self.play(Write(tangent_label))
        self.wait()

        # 显示切线方程
        tangent_eq = MathTex(
            r"\frac{x-x(t_0)}{x'(t_0)} = \frac{y-y(t_0)}{y'(t_0)} = \frac{z-z(t_0)}{z'(t_0)}",
            color=YELLOW,
            font_size=20
        )
        tangent_eq.next_to(tangent_label, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(tangent_eq)
        self.play(Write(tangent_eq))
        self.wait()

        # 清理残影
        self.clear()
        self.add(axes, curve, fixed_dot, secant_line, title, param_eq, secant_label, secant_eq, limit_eq, tangent_label, tangent_eq)
        self.wait()

        # 改变视角以更好地观察
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait()

        # 旋转3D视图
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait()

        # 总结
        summary = Text(
            "空间曲线的切线是割线的极限",
            font="PingFang SC",
            color=WHITE,
            font_size=24
        )
        summary.to_edge(DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(Write(summary))
        self.wait(2)

        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        ) 