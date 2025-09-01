from manim import *
import numpy as np

class HessianAnimation(ThreeDScene):
    def construct(self):
        # 第一部分：Hessian矩阵的构成
        title = Text("Hessian矩阵与极值点判断", font="PingFang SC")
        title.to_edge(UP)
        self.add(title)
        self.wait()

        # 构建Hessian矩阵
        hessian = MathTex(
            r"H = \begin{bmatrix} \frac{\partial^2 f}{\partial x^2} & \frac{\partial^2 f}{\partial x \partial y} \\ \frac{\partial^2 f}{\partial y \partial x} & \frac{\partial^2 f}{\partial y^2} \end{bmatrix}"
        )
        hessian.next_to(title, DOWN)
        self.play(Write(hessian))
        self.wait()

        # 清除之前的2D内容
        self.clear()
        
        # 第二部分：3D场景展示
        # 创建3D场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建曲面函数
        def create_surface(a, b, c):
            return Surface(
                lambda u, v: np.array([u, v, a*u**2 + b*u*v + c*v**2]),
                u_range=[-2, 2],
                v_range=[-2, 2],
                resolution=(20, 20)
            )
        
        # 标记临界点
        critical_point = Dot3D(point=[0, 0, 0], color=RED)
        
        # 创建方程和Hessian矩阵的显示函数
        def create_equation(a, b, c):
            return MathTex(
                f"z = {a}x^2 + {b}xy + {c}y^2"
            ).scale(0.8)

        def create_hessian_matrix(a, b, c):
            return MathTex(
                r"H = \begin{bmatrix}" + f"{2*a} & {b}" + r"\\" + f"{b} & {2*c}" + r"\end{bmatrix}"
            ).scale(0.8)

        # 场景1：局部最小值
        title1 = Text("局部最小值：Hessian矩阵正定", font="PingFang SC")
        title1.to_corner(UP + LEFT)
        equation1 = create_equation(1, 0, 1)
        equation1.next_to(title1, DOWN)
        hessian1 = create_hessian_matrix(1, 0, 1)
        hessian1.next_to(equation1, DOWN)
        
        self.add_fixed_in_frame_mobjects(title1, equation1, hessian1)
        self.play(Write(title1), Write(equation1), Write(hessian1))
        
        surface1 = create_surface(1, 0, 1)  # x² + y²
        surface1.set_style(fill_opacity=0.5)
        self.add(surface1, critical_point)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(surface1), FadeOut(title1), FadeOut(equation1), FadeOut(hessian1))
        
        # 场景2：曲面系数的连续变化
        title2 = Text("曲面系数的连续变化", font="PingFang SC")
        title2.to_corner(UP + LEFT)
        self.add_fixed_in_frame_mobjects(title2)
        self.play(Write(title2))
        
        # 创建初始曲面和方程
        surface2 = create_surface(1, 0, 1)
        surface2.set_style(fill_opacity=0.5)
        equation2 = create_equation(1, 0, 1)
        equation2.next_to(title2, DOWN)
        hessian2 = create_hessian_matrix(1, 0, 1)
        hessian2.next_to(equation2, DOWN)
        self.add_fixed_in_frame_mobjects(equation2, hessian2)
        self.add(surface2)
        
        # 连续变化曲面系数
        self.begin_ambient_camera_rotation(rate=0.2)
        
        # 从局部最小值变化到鞍点
        for t in np.linspace(0, 1, 15):
            a, b, c = 1, 0, 1-2*t
            surface2_new = create_surface(a, b, c)
            surface2_new.set_style(fill_opacity=0.5)
            equation2_new = create_equation(a, b, c)
            equation2_new.next_to(title2, DOWN)
            hessian2_new = create_hessian_matrix(a, b, c)
            hessian2_new.next_to(equation2_new, DOWN)
            self.play(
                Transform(surface2, surface2_new),
                Transform(equation2, equation2_new),
                Transform(hessian2, hessian2_new),
                run_time=0.2
            )
        
        # 从鞍点变化到局部最大值
        for t in np.linspace(0, 1, 15):
            a, b, c = 1-2*t, 0, -1
            surface2_new = create_surface(a, b, c)
            surface2_new.set_style(fill_opacity=0.5)
            equation2_new = create_equation(a, b, c)
            equation2_new.next_to(title2, DOWN)
            hessian2_new = create_hessian_matrix(a, b, c)
            hessian2_new.next_to(equation2_new, DOWN)
            self.play(
                Transform(surface2, surface2_new),
                Transform(equation2, equation2_new),
                Transform(hessian2, hessian2_new),
                run_time=0.2
            )
        
        self.stop_ambient_camera_rotation()
        self.wait()
        self.play(FadeOut(surface2), FadeOut(title2), FadeOut(equation2), FadeOut(hessian2))
        
        # 场景3：鞍点
        title3 = Text("鞍点：Hessian矩阵不定", font="PingFang SC")
        title3.to_corner(UP + LEFT)
        equation3 = create_equation(1, 0, -1)
        equation3.next_to(title3, DOWN)
        hessian3 = create_hessian_matrix(1, 0, -1)
        hessian3.next_to(equation3, DOWN)
        
        self.add_fixed_in_frame_mobjects(title3, equation3, hessian3)
        self.play(Write(title3), Write(equation3), Write(hessian3))
        
        surface3 = create_surface(1, 0, -1)  # x² - y²
        surface3.set_style(fill_opacity=0.5)
        self.add(surface3)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait() 