from manim import *
import numpy as np

class TripleIntegralScene(ThreeDScene):
    def construct(self):
        # 设置更好的相机角度和更美观的外观
        self.set_camera_orientation(phi=70 * DEGREES, theta=20 * DEGREES, zoom=0.8)
        
        # 创建更美观的坐标轴
        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[0, 4.5, 1],
            x_length=5,
            y_length=5,
            z_length=5,
            axis_config={"color": BLUE_B}
        )
        labels = axes.get_axis_labels(
            x_label=MathTex("x", color=BLUE_B),
            y_label=MathTex("y", color=BLUE_B),
            z_label=MathTex("z", color=BLUE_B)
        )
        
        # 调整布局 - 顶部标题和说明更靠上
        problem_title = Text("三重积分计算（先二后一）", font_size=36, color=YELLOW).to_edge(UP, buff=0.1)
        
        # 将中文和数学公式分开显示，调整位置 - 修正Ω为立体区域
        calc_text = Text("计算：", font_size=24, color=WHITE)
        calc_formula = MathTex(r"\iiint_{\Omega} (x^2 + y^2) \, dV", font_size=24, color=WHITE)
        calc_group = VGroup(calc_text, calc_formula).arrange(RIGHT, buff=0.1)
        
        # 全部使用Text显示中文内容，避免中文在LaTeX中的问题
        domain_text = Text("其中 Ω 为旋转抛物面 z = x² + y²", font_size=24, color=WHITE)
        domain_formula = Text("与平面 z = 4 围成的立体区域", font_size=24, color=WHITE)
        domain_group = VGroup(domain_text, domain_formula).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        
        # 将描述分组放在左上方区域
        problem_desc = VGroup(calc_group, domain_group).arrange(DOWN, buff=0.2).next_to(problem_title, DOWN, buff=0.1).to_edge(LEFT, buff=0.5)
        
        # 显示坐标轴
        self.play(Create(axes), Create(labels), run_time=1.5)
        
        # 添加题目和方程
        self.add_fixed_in_frame_mobjects(problem_title, problem_desc)
        self.play(Write(problem_title), Write(problem_desc), run_time=2)
        
        # 旋转抛物面 z = r^2, 0 ≤ r ≤ 2, 0 ≤ z ≤ 4
        def paraboloid(u, v):
            r = u
            theta = v
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = r**2
            return np.array([x, y, z])
        
        # 创建更美观的表面
        surface = Surface(
            paraboloid,
            u_range=[0, 2],
            v_range=[0, TAU],
            fill_opacity=0.3,
            resolution=(30, 30),
            stroke_width=0.5,
            stroke_color=BLUE_E,
            checkerboard_colors=[BLUE_D, "#3070B0"]
        )
        
        # 显示旋转抛物面
        self.play(Create(surface, run_time=2))
        
        # 旋转相机视角
        self.move_camera(phi=65 * DEGREES, theta=50 * DEGREES)
        self.wait(0.5)
        
        # 创建所有场景元素，但暂不显示
        
        # 定义z_tracker 
        self.z_tracker = ValueTracker(0.1)
        
        # 创建一个随z值变化的半透明截面平面
        section_plane = always_redraw(
            lambda: Surface(
                lambda u, v: np.array([u, v, self.z_tracker.get_value()]),
                u_range=[-2.5, 2.5],
                v_range=[-2.5, 2.5],
                resolution=(2, 2),
                fill_opacity=0.2,
                stroke_width=0.5,
                stroke_color=YELLOW,
                fill_color=YELLOW
            )
        )
        
        # 动态截面 - 使用填充和更突出的边缘
        cross_section = always_redraw(
            lambda: ParametricFunction(
                lambda t: np.array([
                    np.sqrt(self.z_tracker.get_value()) * np.cos(t),
                    np.sqrt(self.z_tracker.get_value()) * np.sin(t),
                    self.z_tracker.get_value()
                ]),
                t_range=[0, TAU],
                color=RED_B,
                stroke_width=4
            )
        )
        
        # 在截面内绘制积分区域 - 使用更美观的填充
        integral_region = always_redraw(
            lambda: Surface(
                lambda u, v: np.array([
                    u * np.cos(v),
                    u * np.sin(v),
                    self.z_tracker.get_value()
                ]),
                u_range=[0, np.sqrt(self.z_tracker.get_value())],
                v_range=[0, TAU],
                fill_opacity=0.4,
                resolution=(20, 20),
                stroke_width=0,
                checkerboard_colors=[RED_D, RED_A]
            )
        )
        
        # 创建左下角的2D截面变化示意图 - 坐标轴更长
        section_frame = Rectangle(height=3.5, width=3.5, color=WHITE)
        section_frame.to_corner(DL, buff=0.2)
        section_axes = Axes(
            x_range=[-2.0, 2.0, 1],
            y_range=[-2.0, 2.0, 1],
            x_length=3.0,  # 增加坐标轴长度
            y_length=3.0,  # 增加坐标轴长度
            axis_config={"color": GREY_B, "include_ticks": True},  # 包含刻度
        ).move_to(section_frame.get_center())
        
        # 添加坐标轴标签
        section_x_label = MathTex("x", font_size=16, color=GREY_B).next_to(section_axes.get_x_axis(), RIGHT)
        section_y_label = MathTex("y", font_size=16, color=GREY_B).next_to(section_axes.get_y_axis(), UP)
        
        # 调整标题位置，确保有足够空间放置截面方程
        section_title = Text("截面示意图", font_size=20, color=YELLOW)
        section_title.next_to(section_frame, UP, buff=0.1)
        section_title.align_to(section_frame, LEFT)
        
        # 截面方程（截面方程）放在标题上方，确保在框内
        section_text = Text("截面方程：z = x² + y² = ", font_size=24, color=YELLOW)
        
        # 将z值单独设置为动态更新的元素
        z_value_label = always_redraw(
            lambda: Text(
                f"{round(self.z_tracker.get_value(), 1)}",
                font_size=24,
                color=YELLOW
            )
        )
        
        # 将文字和动态z值组合在一起
        cross_eq = VGroup(section_text, z_value_label).arrange(RIGHT, buff=0.05)
        cross_eq.next_to(section_title, UP, buff=0.1)
        cross_eq.align_to(section_frame, LEFT)
        
        # 固定z值标签在文字后面
        z_value_label.add_updater(lambda m: m.next_to(section_text, RIGHT, buff=0.05))
        
        # 在小图右侧添加截面范围D(z)的显示
        range_text_title = Text("截面范围D(z):", font_size=20, color=YELLOW)
        range_text_theta = MathTex(r"0 \leq \theta \leq 2\pi", font_size=20, color=WHITE)
        range_text_r = MathTex(r"0 \leq r \leq \sqrt{z}", font_size=20, color=WHITE)
        
        # 将范围说明组合并垂直排列
        range_group = VGroup(range_text_title, range_text_theta, range_text_r).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        range_group.next_to(section_frame, RIGHT, buff=0.3)
        range_group.align_to(section_frame, UP)
        
        # 创建动态更新的2D截面圆
        section_circle = always_redraw(
            lambda: Circle(
                radius=np.sqrt(self.z_tracker.get_value()) * 0.75,  # 缩放以适应框架，但比例更大
                color=RED,
                fill_opacity=0.3,
                fill_color=RED_A
            ).move_to(section_axes.get_center())
        )
        
        # 提示文字 - 放在右侧上方位置
        explanation = Text("先二后一计算法", font_size=28, color=YELLOW).to_edge(RIGHT, buff=0.5).shift(UP * 2)
        
        # 截面变化提示 - 放在右侧说明文字下方
        section_desc = Text("截面随z值变化而变化", font_size=24, color=WHITE).next_to(explanation, DOWN, buff=0.3)
        
        # 积分公式 - 放在"先二后一计算法"下方，但先不显示
        integral_steps = VGroup(
            MathTex(
                r"\begin{aligned}"
                r"\iiint_{\Omega} (x^2 + y^2) \, dV &= \int_{0}^{4} \left( \iint_{D(z)} (x^2 + y^2) \, dxdy \right) dz \\"
                r"&= \int_{0}^{4} \left( \int_{0}^{2\pi} \int_{0}^{\sqrt{z}} r^2 \cdot r \, drd\theta \right) dz \\"
                r"&= \int_{0}^{4} \left( 2\pi \cdot \frac{r^4}{4} \Big|_{0}^{\sqrt{z}} \right) dz \\"
                r"&= \int_{0}^{4} \frac{\pi}{2} \cdot z^2 \, dz \\"
                r"&= \frac{\pi}{2} \cdot \frac{z^3}{3} \Big|_{0}^{4} \\"
                r"&= \frac{\pi}{2} \cdot \frac{64}{3} = \frac{32\pi}{3}"
                r"\end{aligned}",
                font_size=24,
                color=WHITE
            )
        ).next_to(section_desc, DOWN, buff=0.3).to_edge(RIGHT, buff=0.5)
        
        # 最终结果 - 放在中央底部，先不显示
        final_result = MathTex(
            r"\iiint_{\Omega} (x^2 + y^2) \, dV = \frac{32\pi}{3}",
            font_size=36,
            color=YELLOW
        ).to_edge(DOWN, buff=0.3)
        
        # 按照逻辑顺序播放动画
        # 1. 方法介绍
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation), run_time=1)
        self.wait(0.2)
        
        # 2. 截面平面和截面描述
        self.add_fixed_in_frame_mobjects(section_desc)
        self.play(
            Create(section_plane),
            Write(section_desc),
            run_time=1.5
        )
        self.wait(0.2)
        
        # 3. 截面圆和积分区域
        self.play(
            Create(cross_section),
            Create(integral_region),
            run_time=1.5
        )
        self.wait(0.2)
        
        # 4. 2D截面示意图和相关说明 - 修复闪现问题
        # 先只添加框架，不添加动态更新的元素
        self.add_fixed_in_frame_mobjects(section_frame)
        self.play(FadeIn(section_frame), run_time=0.5)
        
        # 添加坐标轴和标签
        self.add_fixed_in_frame_mobjects(section_axes, section_x_label, section_y_label)
        self.play(
            FadeIn(section_axes),
            FadeIn(section_x_label),
            FadeIn(section_y_label),
            run_time=0.5
        )
        
        # 添加标题
        self.add_fixed_in_frame_mobjects(section_title)
        self.play(FadeIn(section_title), run_time=0.5)
        
        # 添加截面方程
        self.add_fixed_in_frame_mobjects(cross_eq)
        self.play(FadeIn(cross_eq), run_time=0.5)
        
        # 添加范围说明
        self.add_fixed_in_frame_mobjects(range_group)
        self.play(FadeIn(range_group), run_time=0.5)
        
        # 最后添加动态更新的圆 - 避免闪现
        self.add_fixed_in_frame_mobjects(section_circle)
        self.play(FadeIn(section_circle), run_time=0.5)
        self.wait(0.3)
        
        # 5. 动态变化z值，显示截面变化
        self.play(
            self.z_tracker.animate.set_value(4),
            run_time=5
        )
        self.wait(0.5)
        
        # 6. 旋转相机角度，准备显示积分计算
        self.move_camera(phi=70 * DEGREES, theta=80 * DEGREES)
        self.wait(0.3)
        
        # 7. 积分计算步骤
        self.add_fixed_in_frame_mobjects(integral_steps)
        self.play(Write(integral_steps), run_time=2.5)
        self.wait(1)
        
        # 8. 旋转展示最终结果
        self.begin_ambient_camera_rotation(rate=0.15)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        
        # 9. 显示最终结果
        self.add_fixed_in_frame_mobjects(final_result)
        self.play(
            FadeOut(integral_steps),
            FadeIn(final_result),
            run_time=1.5
        )
        self.wait(2)

if __name__ == "__main__":
    # 使用更好的渲染设置
    config.frame_rate = 30
    config.pixel_width = 1280
    config.pixel_height = 720
    scene = TripleIntegralScene()
    scene.render()