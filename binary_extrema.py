from manim import *
import numpy as np

class BinaryExtrema(ThreeDScene):
    def construct(self):
        # 设置相机角度
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建坐标系统
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            axis_config={"color": GRAY},
            tips=False
        )
        
        # 创建初始曲面（极小值点）
        surface = Surface(
            lambda u, v: np.array([u, v, u**2 + v**2]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            should_make_jagged=True,
            fill_opacity=0.8,
            stroke_width=0.5,
            stroke_opacity=0.5
        )
        
        # 创建信息面板
        info_panel = VGroup(
            Text("函数方程：", font="SimHei").scale(0.7),
            MathTex(r"z = x^2 + y^2").scale(0.8),
            Text("Hessian矩阵：", font="SimHei").scale(0.7),
            MathTex(r"H = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}").scale(0.8),
            Text("特征值：", font="SimHei").scale(0.7),
            MathTex(r"\lambda_1 = 2, \lambda_2 = 2").scale(0.7),
            Text("这是一个极小值点", font="SimHei").scale(0.6).set_color(GREEN)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        info_panel.to_corner(UL, buff=0.5)
        
        # 添加元素到场景
        self.add_fixed_in_frame_mobjects(info_panel)
        self.add(axes, surface)
        
        # 开始相机旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # 变形到鞍点
        new_surface = Surface(
            lambda u, v: np.array([u, v, u**2 - v**2]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            should_make_jagged=True,
            fill_opacity=0.8,
            stroke_width=0.5,
            stroke_opacity=0.5
        )
        
        new_info_panel = VGroup(
            Text("函数方程：", font="SimHei").scale(0.7),
            MathTex(r"z = x^2 - y^2").scale(0.8),
            Text("Hessian矩阵：", font="SimHei").scale(0.7),
            MathTex(r"H = \begin{bmatrix} 2 & 0 \\ 0 & -2 \end{bmatrix}").scale(0.8),
            Text("特征值：", font="SimHei").scale(0.7),
            MathTex(r"\lambda_1 = 2, \lambda_2 = -2").scale(0.7),
            Text("这是一个鞍点", font="SimHei").scale(0.6).set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        new_info_panel.to_corner(UL, buff=0.5)
        
        self.play(
            Transform(surface, new_surface),
            Transform(info_panel, new_info_panel)
        )
        self.wait(3)
        
        # 变形到极大值点
        new_surface = Surface(
            lambda u, v: np.array([u, v, -u**2 - v**2]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            should_make_jagged=True,
            fill_opacity=0.8,
            stroke_width=0.5,
            stroke_opacity=0.5
        )
        
        new_info_panel = VGroup(
            Text("函数方程：", font="SimHei").scale(0.7),
            MathTex(r"z = -x^2 - y^2").scale(0.8),
            Text("Hessian矩阵：", font="SimHei").scale(0.7),
            MathTex(r"H = \begin{bmatrix} -2 & 0 \\ 0 & -2 \end{bmatrix}").scale(0.8),
            Text("特征值：", font="SimHei").scale(0.7),
            MathTex(r"\lambda_1 = -2, \lambda_2 = -2").scale(0.7),
            Text("这是一个极大值点", font="SimHei").scale(0.6).set_color(BLUE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        new_info_panel.to_corner(UL, buff=0.5)
        
        self.play(
            Transform(surface, new_surface),
            Transform(info_panel, new_info_panel)
        )
        self.wait(3)
        
        # 结束场景
        self.clear()  # 清除所有元素
        self.remove_fixed_in_frame_mobjects(info_panel)  # 确保移除固定帧中的元素
        
        # 重置相机方向
        self.camera.reset()
        
        # 显示结束文字
        end_text = Text("谢谢观看", font="SimHei").scale(1.2)
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(Write(end_text))
        self.wait(2)
        self.remove_fixed_in_frame_mobjects(end_text) 