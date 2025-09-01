from manim import *
import numpy as np

class HessianVisualization(ThreeDScene):
    def construct(self):
        # 设置相机角度
        self.set_camera_orientation(phi=65 * DEGREES, theta=35 * DEGREES)
        
        # 开场介绍
        title = Text("多元函数极值判别与Hessian矩阵", font="SimHei").scale(1.2)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # Hessian矩阵的介绍
        self.introduce_hessian()
        
        # 动态演示曲面变化与特征值关系
        self.demonstrate_surface_morphing()
    
    def introduce_hessian(self):
        # Hessian矩阵的介绍
        hessian_title = Text("Hessian矩阵的构造与特征值", font="SimHei").scale(0.8).to_edge(UP)
        self.add_fixed_in_frame_mobjects(hessian_title)
        self.play(Write(hessian_title))
        
        # 创建坐标系 - 确保完全没有标签
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={"include_numbers": False, "include_ticks": False, "include_tip": False}  # 完全禁用所有标签、刻度和箭头尖端
        ).scale(0.8)
        
        # 修改坐标轴颜色
        axes.set_color(GRAY)
        
        # 创建曲面
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 + v**2),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(30, 30),
            checkerboard_colors=[GREEN_D, GREEN_E],
            fill_opacity=0.7
        )
        
        # 左侧面板：函数方程、Hessian矩阵和特征值
        left_panel = VGroup()
        
        # 函数方程
        func_eq = VGroup(
            Text("函数方程：", font="SimHei").scale(0.7),
            MathTex(r"z = f(x,y)").scale(0.9)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # Hessian矩阵
        hessian_title_local = Text("Hessian矩阵：", font="SimHei").scale(0.7)
        hessian_matrix = MathTex(
            r"H = \begin{bmatrix} \frac{\partial^2 f}{\partial x^2} & \frac{\partial^2 f}{\partial x \partial y} \\ \frac{\partial^2 f}{\partial y \partial x} & \frac{\partial^2 f}{\partial y^2} \end{bmatrix}"
        ).scale(0.9)
        
        hessian_group = VGroup(hessian_title_local, hessian_matrix).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        
        # 特征值判别法则
        eigenvalues_title = Text("特征值判别法则：", font="SimHei").scale(0.7)
        eigenvalues_items = VGroup(
            Text("• 全为正 → 极小值点", font="SimHei").scale(0.6).set_color(GREEN),
            Text("• 全为负 → 极大值点", font="SimHei").scale(0.6).set_color(BLUE),
            Text("• 有正有负 → 鞍点", font="SimHei").scale(0.6).set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        eigenvalues_group = VGroup(eigenvalues_title, eigenvalues_items).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        # 组织左侧面板
        left_panel = VGroup(
            func_eq,
            hessian_group,
            eigenvalues_group
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        left_panel.to_edge(LEFT).shift(UP * 0.5)
        
        # 先添加固定文字，再添加3D元素
        self.add_fixed_in_frame_mobjects(left_panel)
        
        # 添加3D元素
        self.add(axes)
        self.play(Create(axes))
        self.play(Create(surface))
        
        # 信息面板淡入
        self.play(FadeIn(left_panel), run_time=1.5)
        
        self.wait(3)
        
        # 清除场景
        self.remove_fixed_in_frame_mobjects(hessian_title, left_panel)
        self.remove(axes, surface)
    
    def demonstrate_surface_morphing(self):
        # 创建坐标系统
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
            axis_config={"color": GRAY},
            tips=False
        )
        
        # 创建初始曲面
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
        surface.set_style(fill_opacity=0.8, stroke_width=0.5)
        
        # 创建信息面板
        # info_panel = VGroup(
        #     Text("函数方程：", font="SimHei").scale(0.7),
        #     MathTex(r"z = x^2 + y^2").scale(0.8),
        #     Text("Hessian矩阵：", font="SimHei").scale(0.7),
        #     MathTex(r"H = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}").scale(0.8),
        #     Text("特征值：", font="SimHei").scale(0.7),
        #     MathTex(r"\lambda_1 = 2, \lambda_2 = 2").scale(0.7),
        #     Text("这是一个极小值点", font="SimHei").scale(0.6).set_color(GREEN)
        # ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        # info_panel.to_corner(UL, buff=0.5)
        
        # 添加元素到场景
        self.add_fixed_in_frame_mobjects(info_panel)
        self.add(axes, surface)
        
        # 开始相机旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # 定义变形步骤
        morphing_steps = [
            (0.5, "这是一个临界状态", YELLOW),
            (1.0, "这是一个鞍点", RED)
        ]
        
        # 执行变形
        for t, conclusion, color in morphing_steps:
            # 创建新的曲面
            new_surface = Surface(
                lambda u, v: np.array([u, v, u**2 + (1-2*t)*v**2]),
                u_range=[-2, 2],
                v_range=[-2, 2],
                resolution=(30, 30),
                should_make_jagged=True,
                fill_opacity=0.8,
                stroke_width=0.5,
                stroke_opacity=0.5
            )
            new_surface.set_style(fill_opacity=0.8, stroke_width=0.5)
            
            # 计算新的特征值
            lambda2 = 2 - 4*t
            
            # 创建新的信息面板
            new_info_panel = VGroup(
                Text("函数方程：", font="SimHei").scale(0.7),
                MathTex(r"z = x^2 + " + f"{(1-2*t):.2f}" + r"y^2").scale(0.8),
                Text("Hessian矩阵：", font="SimHei").scale(0.7),
                MathTex(r"H = \begin{bmatrix} 2 & 0 \\ 0 & " + f"{2-4*t:.2f}" + r" \end{bmatrix}").scale(0.8),
                Text("特征值：", font="SimHei").scale(0.7),
                MathTex(r"\lambda_1 = 2, \lambda_2 = " + f"{lambda2:.1f}").scale(0.7),
                Text(conclusion, font="SimHei").scale(0.6).set_color(color)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            new_info_panel.to_corner(UL, buff=0.5)
            
            # 更新场景
            self.play(
                Transform(surface, new_surface),
                Transform(info_panel, new_info_panel)
            )
            self.wait(2)
        
        # 结束场景
        self.wait(2)
        self.remove_fixed_in_frame_mobjects(info_panel)
        self.remove(axes, surface)
        
        # 重置相机方向
        self.camera.reset()
        
        # 显示结束文字
        end_text = Text("谢谢观看", font="SimHei").scale(1.2)
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(Write(end_text))
        self.wait(2)
        self.remove_fixed_in_frame_mobjects(end_text) 