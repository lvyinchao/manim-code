from manim import *
import numpy as np

class TaylorSeriesDemo(ThreeDScene):
    def construct(self):
        # 设置3D场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 标题
        title = Text("二元函数泰勒展开", font="PingFang SC")
        title.to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait()
        
        # 在左侧显示一般函数的泰勒公式（展开式形式）
        general_taylor = MathTex(
            r"f(x,y) &= f(0,0) + \frac{\partial f}{\partial x}(0,0)x + \frac{\partial f}{\partial y}(0,0)y \\",
            r"&+ \frac{1}{2!}\frac{\partial^2 f}{\partial x^2}(0,0)x^2 + \frac{1}{1!1!}\frac{\partial^2 f}{\partial x \partial y}(0,0)xy + \frac{1}{2!}\frac{\partial^2 f}{\partial y^2}(0,0)y^2 \\",
            r"&+ \frac{1}{3!}\frac{\partial^3 f}{\partial x^3}(0,0)x^3 + \ldots",
            font_size=20
        )
        general_taylor.to_edge(LEFT, buff=1.3)  # 增加左侧边距，使公式更靠左
        general_taylor.shift(UP * 2 + LEFT * 1)  # 额外向左移动
        self.add_fixed_in_frame_mobjects(general_taylor)
        self.play(Write(general_taylor))
        self.wait()
        
        # 使用 f(x,y) = e^(-x^2-y^2) 作为例子，高斯函数
        def f(x, y):
            return np.exp(-x**2 - y**2)
        
        # 创建坐标轴，调整范围以更好地显示函数，缩小范围
        axes = ThreeDAxes(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            z_range=[0, 1.2, 0.2],
            x_length=6,
            y_length=6,
            z_length=3,
        )
        self.add(axes)
        
        # 创建原始曲面，缩小范围
        original_surface = Surface(
            lambda u, v: axes.c2p(u, v, f(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),  # 增加分辨率使曲面更平滑
            fill_opacity=0.7,
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        
        # 显示原始曲面
        self.play(Create(original_surface))
        
        # 添加原始函数说明
        original_func = MathTex(r"f(x,y) = e^{-x^2-y^2}", font_size=28, color=BLUE)
        original_func.to_edge(UP, buff=0.2)  # 将函数说明移到顶部中间位置
        self.add_fixed_in_frame_mobjects(original_func)
        self.play(Write(original_func))
        self.wait()
        
        # 泰勒展开零阶
        def taylor_0_func(x, y):
            # f(0,0) = 1
            return 1
        
        taylor_0 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_0_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.5,
            checkerboard_colors=[RED_D, RED_E]
        )
        
        # 公式显示在右侧，位于T0下方
        taylor_0_eq = MathTex(r"T_0(x,y) = 1", font_size=28, color=RED)
        taylor_0_eq.to_edge(RIGHT, buff=0.7)  # 增加右侧边距
        taylor_0_eq.shift(UP * 3)  # 移到屏幕上方
        self.add_fixed_in_frame_mobjects(taylor_0_eq)
        
        self.play(Create(taylor_0), Write(taylor_0_eq))
        self.wait()
        
        # 泰勒展开一阶
        def taylor_1_func(x, y):
            # 一阶展开: f(0,0) = 1
            # ∂f/∂x(0,0) = ∂f/∂y(0,0) = 0
            return 1
        
        taylor_1 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_1_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.5,
            checkerboard_colors=[GOLD_D, GOLD_E]
        )
        
        # 公式显示在右侧，位于T0下方
        taylor_1_eq = MathTex(r"T_1(x,y) = 1", font_size=28, color=GOLD)
        taylor_1_eq.to_edge(RIGHT, buff=0.7)
        taylor_1_eq.shift(UP * 2.4)
        self.add_fixed_in_frame_mobjects(taylor_1_eq)
        
        self.play(
            ReplacementTransform(taylor_0, taylor_1),
            FadeIn(taylor_1_eq)
        )
        self.wait()
        
        # 泰勒展开二阶
        def taylor_2_func(x, y):
            # 二阶展开: 添加二阶项
            # ∂²f/∂x²(0,0) = ∂²f/∂y²(0,0) = -2
            # ∂²f/∂x∂y(0,0) = 0
            return 1 - x**2 - y**2
        
        taylor_2 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_2_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.5,
            checkerboard_colors=[GREEN_D, GREEN_E]
        )
        
        # 公式显示在右侧，位于T1下方
        taylor_2_eq = MathTex(r"T_2(x,y) = 1 - x^2 - y^2", font_size=28, color=GREEN)
        taylor_2_eq.to_edge(RIGHT, buff=0.7)
        taylor_2_eq.shift(UP * 1.8)
        self.add_fixed_in_frame_mobjects(taylor_2_eq)
        
        self.play(
            ReplacementTransform(taylor_1, taylor_2),
            FadeIn(taylor_2_eq)
        )
        self.wait()
        
        # 泰勒展开三阶
        def taylor_3_func(x, y):
            # 三阶展开，三阶导数在(0,0)处均为0
            return 1 - x**2 - y**2
        
        taylor_3 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_3_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.5,
            checkerboard_colors=[TEAL_D, TEAL_E]
        )
        
        # 公式显示在右侧，位于T2下方
        # 三阶导数在(0,0)处为0，所以T3 = T2
        taylor_3_eq = MathTex(r"T_3(x,y) = T_2(x,y)", font_size=26, color=TEAL)
        taylor_3_eq.to_edge(RIGHT, buff=0.7)
        taylor_3_eq.shift(UP * 1.2)
        self.add_fixed_in_frame_mobjects(taylor_3_eq)
        
        self.play(
            ReplacementTransform(taylor_2, taylor_3),
            FadeIn(taylor_3_eq)
        )
        self.wait()
        
        # 泰勒展开四阶
        def taylor_4_func(x, y):
            # 四阶展开，增加四阶项
            # ∂⁴f/∂x⁴(0,0) = ∂⁴f/∂y⁴(0,0) = 12
            # ∂⁴f/∂x²∂y²(0,0) = 4
            return 1 - x**2 - y**2 + x**4/2 + x**2*y**2 + y**4/2
        
        taylor_4 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_4_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.5,
            checkerboard_colors=[PURPLE_D, PURPLE_E]
        )
        
        # 公式显示在右侧，位于T3下方，由于长度较长，字体稍小
        taylor_4_eq = MathTex(r"T_4(x,y) = 1 - x^2 - y^2", r"+ \frac{1}{2}x^4 + x^2y^2 + \frac{1}{2}y^4", font_size=24, color=PURPLE)
        taylor_4_eq.arrange(DOWN, aligned_edge=LEFT)
        taylor_4_eq.to_edge(RIGHT, buff=0.7)
        taylor_4_eq.shift(UP * 0.3)  # 调整向下移动
        self.add_fixed_in_frame_mobjects(taylor_4_eq)
        
        self.play(
            ReplacementTransform(taylor_3, taylor_4),
            FadeIn(taylor_4_eq)
        )
        self.wait()
        
        # 泰勒展开五阶
        def taylor_5_func(x, y):
            # 五阶展开，五阶导数在(0,0)处均为0
            return 1 - x**2 - y**2 + x**4/2 + x**2*y**2 + y**4/2
        
        taylor_5 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_5_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.5,
            checkerboard_colors=[YELLOW_D, YELLOW_E]
        )
        
        # 公式显示在右侧，位于T4下方
        taylor_5_eq = MathTex(r"T_5(x,y) = T_4(x,y)", font_size=26, color=YELLOW)
        taylor_5_eq.to_edge(RIGHT, buff=0.7)
        taylor_5_eq.shift(DOWN * 0.6)  # 调整位置以适应T4的新位置
        self.add_fixed_in_frame_mobjects(taylor_5_eq)
        
        self.play(
            ReplacementTransform(taylor_4, taylor_5),
            FadeIn(taylor_5_eq)
        )
        self.wait()
        
        # 泰勒展开六阶
        def taylor_6_func(x, y):
            # 六阶展开，增加六阶项
            # ∂⁶f/∂x⁶(0,0) = ∂⁶f/∂y⁶(0,0) = -120
            # ∂⁶f/∂x⁴∂y²(0,0) = ∂⁶f/∂x²∂y⁴(0,0) = -24
            return (1 - x**2 - y**2 + x**4/2 + x**2*y**2 + y**4/2 - 
                   x**6/6 - x**4*y**2/2 - x**2*y**4/2 - y**6/6)
        
        taylor_6 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_6_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.5,
            checkerboard_colors=[MAROON_D, MAROON_E]
        )
        
        # 公式显示在右侧，位于T5下方，简化显示，将公式分成两行以避免过长
        taylor_6_eq = MathTex(r"T_6(x,y) = T_5(x,y) - \frac{1}{6}x^6", r"- \frac{1}{2}x^4y^2 - \frac{1}{2}x^2y^4 - \frac{1}{6}y^6", font_size=24, color=MAROON)
        taylor_6_eq.arrange(DOWN, aligned_edge=LEFT)
        taylor_6_eq.to_edge(RIGHT, buff=0.7)
        taylor_6_eq.shift(DOWN * 1.5)  # 调整为更低的位置
        self.add_fixed_in_frame_mobjects(taylor_6_eq)
        
        self.play(
            ReplacementTransform(taylor_5, taylor_6),
            FadeIn(taylor_6_eq)
        )
        self.wait()
        
        # 对比原始曲面和最终的泰勒展开曲面
        self.play(
            FadeOut(taylor_6),
            original_surface.animate.set_fill_opacity(0.8)
        )
        self.wait()
        
        # 重新创建一个新的泰勒六阶曲面，避免使用之前可能存在残影的对象
        new_taylor_6 = Surface(
            lambda u, v: axes.c2p(u, v, taylor_6_func(u, v)),
            u_range=[-1.5, 1.5],
            v_range=[-1.5, 1.5],
            resolution=(25, 25),
            fill_opacity=0.4,  # 直接设置为半透明
            checkerboard_colors=[MAROON_D, MAROON_E]
        )
        
        self.play(
            FadeIn(new_taylor_6)
        )
        self.wait()
        
        # 改变视角以更好地观察差异
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait()
        
        # 旋转相机观察匹配程度
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        
        # 结论
        conclusion = Text("随着泰勒展开阶数增加，近似度不断提高", font="PingFang SC", font_size=28)
        conclusion.to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(2) 