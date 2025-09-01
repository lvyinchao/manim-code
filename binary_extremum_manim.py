from manim import *
import numpy as np

class BinaryExtremumDemo(ThreeDScene):
    def construct(self):
        # 第一部分：Hessian矩阵的构造
        # 创建标题
        title1 = Text("Hessian矩阵的构造", font="PingFang SC", font_size=36)
        title1.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title1)
        self.play(Write(title1))
        self.wait()

        # 显示一般形式的二元函数
        func = MathTex(
            "z = f(x,y)",
            color=BLUE,
            font_size=32
        )
        func.to_edge(LEFT, buff=1)
        func.shift(UP * 1)
        self.add_fixed_in_frame_mobjects(func)
        self.play(Write(func))
        self.wait()

        # 显示Hessian矩阵
        hessian = MathTex(
            "H = \\begin{bmatrix} f_{xx} & f_{xy} \\\\ f_{yx} & f_{yy} \\end{bmatrix}",
            color=YELLOW,
            font_size=32
        )
        hessian.next_to(func, DOWN, buff=1)
        self.add_fixed_in_frame_mobjects(hessian)
        self.play(Write(hessian))
        self.wait()

        # 显示判断方法（右侧）
        right_group = VGroup(
            Text("Hessian矩阵的正定性判断：", font="PingFang SC", font_size=28, color=WHITE),
            Text("• 正定矩阵 → 极小值", font="PingFang SC", font_size=28, color=GREEN),
            Text("• 负定矩阵 → 极大值", font="PingFang SC", font_size=28, color=RED),
            Text("• 不定矩阵 → 鞍点", font="PingFang SC", font_size=28, color=YELLOW)
        )
        right_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right_group.to_edge(RIGHT, buff=1)
        right_group.shift(UP * 1)
        self.add_fixed_in_frame_mobjects(right_group)
        self.play(Write(right_group))
        self.wait(2)

        # 淡出第一部分
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )

        # 第二部分：3D曲面演示
        # 设置3D场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建标题
        title2 = Text("Hessian矩阵判断极值", font="PingFang SC", font_size=36)
        title2.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(title2)
        self.play(Write(title2))
        self.wait()

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-2, 10, 2],
            axis_config={"color": GRAY}
        )
        self.add(axes)
        self.wait()

        # 创建函数表达式和Hessian矩阵显示
        func = MathTex(
            "f(x,y) = x^2 + 2y^2",
            color=BLUE,
            font_size=32
        )
        func.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(func)
        self.play(Write(func))
        
        hessian = MathTex(
            "H = \\begin{bmatrix} 2 & 0 \\\\ 0 & 4 \\end{bmatrix}",
            color=YELLOW,
            font_size=28
        )
        hessian.next_to(func, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(hessian)
        self.play(Write(hessian))

        # 添加判断结果和说明
        judgment_group = VGroup(
            Text("正定矩阵 → 极小值", font="PingFang SC", font_size=28, color=GREEN),
            Text("在点(0,0)处取得极小值", font="PingFang SC", font_size=24, color=WHITE)
        )
        judgment_group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        judgment_group.next_to(hessian, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(judgment_group)
        self.play(Write(judgment_group))
        self.wait()

        # 创建曲面
        def create_surface(a, c):
            return Surface(
                lambda u, v: np.array([
                    u, v, a*u**2 + c*v**2
                ]),
                u_range=[-3, 3],
                v_range=[-3, 3],
                resolution=(40, 40),
                should_make_jagged=False
            )

        # 创建初始曲面 (a=1, c=2, 极小值)
        surface = create_surface(1, 2)
        surface.set_style(fill_opacity=0.8, stroke_width=0.5)
        surface.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)
        self.add(surface)
        self.wait()

        # 从极小值(a=1, c=2)到鞍点(a=1, c=-2)
        def update_surface1(surface, alpha):
            c = 2 - 4*alpha
            surface.become(create_surface(1, c))
            surface.set_style(fill_opacity=0.8, stroke_width=0.5)
            surface.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        def update_hessian1(hessian, alpha):
            c = 2 - 4*alpha
            hessian.become(MathTex(
                f"H = \\begin{{bmatrix}} 2 & 0 \\\\ 0 & {2*c:.1f} \\end{{bmatrix}}",
                color=YELLOW,
                font_size=28
            ))
            hessian.next_to(func, DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(hessian)

        def update_func1(func, alpha):
            c = 2 - 4*alpha
            func.become(MathTex(
                f"f(x,y) = x^2 + {c:.1f}y^2",
                color=BLUE,
                font_size=32
            ))
            func.to_corner(UR, buff=0.5)
            self.add_fixed_in_frame_mobjects(func)

        def update_judgment1(group, alpha):
            if alpha < 0.5:
                group.become(VGroup(
                    Text("正定矩阵 → 极小值", font="PingFang SC", font_size=28, color=GREEN),
                    Text("在点(0,0)处取得极小值", font="PingFang SC", font_size=24, color=WHITE)
                ))
            else:
                group.become(VGroup(
                    Text("不定矩阵 → 鞍点", font="PingFang SC", font_size=28, color=YELLOW),
                    Text("点(0,0)是鞍点", font="PingFang SC", font_size=24, color=WHITE)
                ))
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            group.next_to(hessian, DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(group)

        self.play(
            UpdateFromAlphaFunc(surface, update_surface1),
            UpdateFromAlphaFunc(hessian, update_hessian1),
            UpdateFromAlphaFunc(func, update_func1),
            UpdateFromAlphaFunc(judgment_group, update_judgment1),
            run_time=3
        )
        self.wait()

        # 从鞍点(a=1, c=-2)到极大值(a=-1, c=-2)
        def update_surface2(surface, alpha):
            a = 1 - 2*alpha
            surface.become(create_surface(a, -2))
            surface.set_style(fill_opacity=0.8, stroke_width=0.5)
            surface.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        def update_hessian2(hessian, alpha):
            a = 1 - 2*alpha
            hessian.become(MathTex(
                f"H = \\begin{{bmatrix}} {2*a:.1f} & 0 \\\\ 0 & -4 \\end{{bmatrix}}",
                color=YELLOW,
                font_size=28
            ))
            hessian.next_to(func, DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(hessian)

        def update_func2(func, alpha):
            a = 1 - 2*alpha
            func.become(MathTex(
                f"f(x,y) = {a:.1f}x^2 - 2y^2",
                color=BLUE,
                font_size=32
            ))
            func.to_corner(UR, buff=0.5)
            self.add_fixed_in_frame_mobjects(func)

        def update_judgment2(group, alpha):
            if alpha < 0.5:
                group.become(VGroup(
                    Text("不定矩阵 → 鞍点", font="PingFang SC", font_size=28, color=YELLOW),
                    Text("点(0,0)是鞍点", font="PingFang SC", font_size=24, color=WHITE)
                ))
            else:
                group.become(VGroup(
                    Text("负定矩阵 → 极大值", font="PingFang SC", font_size=28, color=RED),
                    Text("在点(0,0)处取得极大值", font="PingFang SC", font_size=24, color=WHITE)
                ))
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            group.next_to(hessian, DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(group)

        self.play(
            UpdateFromAlphaFunc(surface, update_surface2),
            UpdateFromAlphaFunc(hessian, update_hessian2),
            UpdateFromAlphaFunc(func, update_func2),
            UpdateFromAlphaFunc(judgment_group, update_judgment2),
            run_time=3
        )
        self.wait()

        # 从极大值(a=-1, c=-2)回到极小值(a=1, c=2)
        def update_surface3(surface, alpha):
            a = -1 + 2*alpha
            c = -2 + 4*alpha
            surface.become(create_surface(a, c))
            surface.set_style(fill_opacity=0.8, stroke_width=0.5)
            surface.set_fill_by_checkerboard(ORANGE, BLUE, opacity=0.5)

        def update_hessian3(hessian, alpha):
            a = -1 + 2*alpha
            c = -2 + 4*alpha
            hessian.become(MathTex(
                f"H = \\begin{{bmatrix}} {2*a:.1f} & 0 \\\\ 0 & {2*c:.1f} \\end{{bmatrix}}",
                color=YELLOW,
                font_size=28
            ))
            hessian.next_to(func, DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(hessian)

        def update_func3(func, alpha):
            a = -1 + 2*alpha
            c = -2 + 4*alpha
            func.become(MathTex(
                f"f(x,y) = {a:.1f}x^2 + {c:.1f}y^2",
                color=BLUE,
                font_size=32
            ))
            func.to_corner(UR, buff=0.5)
            self.add_fixed_in_frame_mobjects(func)

        def update_judgment3(group, alpha):
            if alpha < 0.4:
                group.become(VGroup(
                    Text("负定矩阵 → 极大值", font="PingFang SC", font_size=28, color=RED),
                    Text("在点(0,0)处取得极大值", font="PingFang SC", font_size=24, color=WHITE)
                ))
            elif alpha < 0.8:
                group.become(VGroup(
                    Text("不定矩阵 → 鞍点", font="PingFang SC", font_size=28, color=YELLOW),
                    Text("点(0,0)是鞍点", font="PingFang SC", font_size=24, color=WHITE)
                ))
            else:
                group.become(VGroup(
                    Text("正定矩阵 → 极小值", font="PingFang SC", font_size=28, color=GREEN),
                    Text("在点(0,0)处取得极小值", font="PingFang SC", font_size=24, color=WHITE)
                ))
            group.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            group.next_to(hessian, DOWN, buff=0.5)
            self.add_fixed_in_frame_mobjects(group)

        self.play(
            UpdateFromAlphaFunc(surface, update_surface3),
            UpdateFromAlphaFunc(hessian, update_hessian3),
            UpdateFromAlphaFunc(func, update_func3),
            UpdateFromAlphaFunc(judgment_group, update_judgment3),
            run_time=3
        )
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
            "通过Hessian矩阵的正定性判断极值类型",
            font="PingFang SC",
            color=WHITE,
            font_size=32
        )
        summary.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(summary)
        self.play(Write(summary))
        self.wait(2)

        # 淡出所有元素
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        ) 