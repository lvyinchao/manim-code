from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class SphereFluxProblem(ThreeDScene):
    def construct(self):
        # 创建标题
        title = Text("流体通过球面的流量计算", font="STSong", font_size=40)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 设置相机视角
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES, zoom=0.8)

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
            axis_config={"color": BLUE_B}
        )
        labels = axes.get_axis_labels(
            x_label=MathTex("x", color=BLUE_B),
            y_label=MathTex("y", color=BLUE_B),
            z_label=MathTex("z", color=BLUE_B)
        )

        # 显示题目
        problem_title = Text("题目：", font_size=24, color=YELLOW).to_edge(UP, buff=0.1).to_edge(LEFT, buff=0.5)
        problem_text1 = Text("设某流体的流速为", font_size=20, color=WHITE)
        problem_formula1 = MathTex(r"\vec{v} = (k, y, 0)", font_size=20, color=WHITE)
        problem_line1 = VGroup(problem_text1, problem_formula1).arrange(RIGHT, buff=0.1)
        
        problem_text2 = Text("求单位时间内从球面", font_size=20, color=WHITE)
        problem_formula2 = MathTex(r"x^2 + y^2 + z^2 = 4", font_size=20, color=WHITE)
        problem_text3 = Text("的内部流过球面的流量", font_size=20, color=WHITE)
        problem_line2 = VGroup(problem_text2, problem_formula2, problem_text3).arrange(RIGHT, buff=0.1)
        
        problem_desc = VGroup(problem_line1, problem_line2).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        problem_group = VGroup(problem_title, problem_desc).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        problem_group.to_edge(UP, buff=0.1).to_edge(LEFT, buff=0.5)

        self.add_fixed_in_frame_mobjects(problem_group)
        self.play(Write(problem_group))
        self.wait(2)

        # 显示坐标轴
        self.play(Create(axes), Create(labels))
        self.wait(1)

        # 创建球面 x² + y² + z² = 4
        sphere = Surface(
            lambda u, v: np.array([
                2 * np.sin(u) * np.cos(v),
                2 * np.sin(u) * np.sin(v),
                2 * np.cos(u)
            ]),
            u_range=[0, PI],
            v_range=[0, TAU],
            resolution=(20, 20),
            fill_opacity=0.3,
            stroke_width=1,
            stroke_color=BLUE_E,
            checkerboard_colors=[BLUE_D, BLUE_C]
        )

        # 显示球面
        self.play(Create(sphere))
        self.wait(1)

        # 创建向量场 v = (k, y, 0)，简化为k=1的情况
        def vector_field_func(point):
            x, y, z = point
            return np.array([1, y * 0.5, 0])  # 缩放y分量以便可视化

        # 在球面周围显示向量场
        vector_field = VGroup()
        for theta in np.linspace(0, TAU, 12):
            for phi in np.linspace(0, PI, 6):
                if phi == 0 or phi == PI:  # 跳过极点
                    continue
                # 球面上的点
                x = 2 * np.sin(phi) * np.cos(theta)
                y = 2 * np.sin(phi) * np.sin(theta)
                z = 2 * np.cos(phi)
                point = np.array([x, y, z])
                
                # 计算向量场
                field_vector = vector_field_func(point)
                # 归一化并缩放
                if np.linalg.norm(field_vector) > 0:
                    field_vector = field_vector / np.linalg.norm(field_vector) * 0.8
                
                arrow = Arrow3D(
                    start=point,
                    end=point + field_vector,
                    color=RED,
                    thickness=0.02
                )
                vector_field.add(arrow)

        # 显示向量场
        self.play(Create(vector_field))
        self.wait(1)

        # 添加向量场标识
        field_label = Text("流速场", font="STSong", font_size=24, color=RED)
        field_formula = MathTex(r"\vec{v} = (k, y, 0)", font_size=20, color=RED)
        field_group = VGroup(field_label, field_formula).arrange(DOWN, buff=0.1)
        field_group.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(field_group)
        self.play(Write(field_group))
        self.wait(1)

        # 显示法向量
        normal_vectors = VGroup()
        for theta in np.linspace(0, TAU, 8):
            for phi in np.linspace(PI/4, 3*PI/4, 3):
                # 球面上的点
                x = 2 * np.sin(phi) * np.cos(theta)
                y = 2 * np.sin(phi) * np.sin(theta)
                z = 2 * np.cos(phi)
                point = np.array([x, y, z])
                
                # 法向量（向外）
                normal = point / 2  # 单位法向量
                
                arrow = Arrow3D(
                    start=point,
                    end=point + normal,
                    color=YELLOW,
                    thickness=0.03
                )
                normal_vectors.add(arrow)

        self.play(Create(normal_vectors))
        
        # 添加法向量标识
        normal_label = Text("法向量", font="STSong", font_size=24, color=YELLOW)
        normal_formula = MathTex(r"\vec{n} = \frac{(x,y,z)}{2}", font_size=20, color=YELLOW)
        normal_group = VGroup(normal_label, normal_formula).arrange(DOWN, buff=0.1)
        normal_group.next_to(field_group, DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(normal_group)
        self.play(Write(normal_group))
        self.wait(2)

        # 移动相机以便更好地显示计算过程
        self.move_camera(phi=60 * DEGREES, theta=45 * DEGREES)
        self.wait(1)

        # 显示通量公式
        flux_title = Text("通量计算：", font="STSong", font_size=24, color=YELLOW)
        flux_formula1 = MathTex(r"\Phi = \iint_S \vec{v} \cdot \vec{n} \, dS", font_size=22)
        flux_step1 = MathTex(r"= \iint_S (k, y, 0) \cdot \frac{(x,y,z)}{2} \, dS", font_size=22)
        flux_step2 = MathTex(r"= \iint_S \left(\frac{kx}{2} + \frac{y^2}{2}\right) dS", font_size=22)

        flux_calc = VGroup(flux_title, flux_formula1, flux_step1, flux_step2)
        flux_calc.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        flux_calc.to_edge(LEFT, buff=0.5).shift(DOWN * 2)
        
        self.add_fixed_in_frame_mobjects(flux_calc)
        self.play(Write(flux_title))
        self.wait(1)
        self.play(Write(flux_formula1))
        self.wait(1)
        self.play(Write(flux_step1))
        self.wait(1)
        self.play(Write(flux_step2))
        self.wait(2)

        # 使用球坐标系计算
        coord_title = Text("使用球坐标系：", font="STSong", font_size=24, color=GREEN)
        coord_formula1 = MathTex(r"x = 2\sin\phi\cos\theta", font_size=20)
        coord_formula2 = MathTex(r"y = 2\sin\phi\sin\theta", font_size=20)
        coord_formula3 = MathTex(r"z = 2\cos\phi", font_size=20)
        coord_formula4 = MathTex(r"dS = 4\sin\phi \, d\phi \, d\theta", font_size=20)

        coord_group = VGroup(coord_title, coord_formula1, coord_formula2, coord_formula3, coord_formula4)
        coord_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        coord_group.to_edge(RIGHT, buff=0.5).shift(DOWN * 1)

        self.add_fixed_in_frame_mobjects(coord_group)
        for item in coord_group:
            self.play(Write(item))
            self.wait(0.5)

        # 展示积分计算
        integral_title = Text("积分计算：", font="STSong", font_size=24, color=ORANGE)
        integral_step1 = MathTex(
            r"\Phi = \int_0^{2\pi} \int_0^{\pi} \left(\frac{k \cdot 2\sin\phi\cos\theta}{2} + \frac{(2\sin\phi\sin\theta)^2}{2}\right) \cdot 4\sin\phi \, d\phi \, d\theta",
            font_size=16
        )
        integral_step2 = MathTex(
            r"= \int_0^{2\pi} \int_0^{\pi} (2k\sin\phi\cos\theta + 8\sin^3\phi\sin^2\theta) \sin\phi \, d\phi \, d\theta",
            font_size=16
        )
        integral_step3 = MathTex(
            r"= \int_0^{2\pi} \cos\theta \, d\theta \int_0^{\pi} 2k\sin^2\phi \, d\phi + \int_0^{2\pi} \sin^2\theta \, d\theta \int_0^{\pi} 8\sin^4\phi \, d\phi",
            font_size=16
        )

        integral_group = VGroup(integral_title, integral_step1, integral_step2, integral_step3)
        integral_group.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        integral_group.to_edge(DOWN, buff=0.5)

        self.add_fixed_in_frame_mobjects(integral_group)
        for item in integral_group:
            self.play(Write(item))
            self.wait(1)

        # 计算结果
        result_title = Text("计算结果：", font="STSong", font_size=24, color=YELLOW)
        result_step1 = MathTex(r"\int_0^{2\pi} \cos\theta \, d\theta = 0", font_size=20)
        result_step2 = MathTex(r"\int_0^{2\pi} \sin^2\theta \, d\theta = \pi", font_size=20)
        result_step3 = MathTex(r"\int_0^{\pi} \sin^4\phi \, d\phi = \frac{3\pi}{8}", font_size=20)
        result_final = MathTex(r"\Phi = 0 + \pi \cdot 8 \cdot \frac{3\pi}{8} = 3\pi^2", font_size=24, color=YELLOW)

        result_group = VGroup(result_title, result_step1, result_step2, result_step3, result_final)
        result_group.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        result_group.to_corner(DL, buff=0.5)

        self.add_fixed_in_frame_mobjects(result_group)
        for item in result_group[:-1]:
            self.play(Write(item))
            self.wait(0.8)
        
        # 突出显示最终结果
        result_box = SurroundingRectangle(result_final, buff=0.2, color=YELLOW)
        self.add_fixed_in_frame_mobjects(result_box)
        self.play(Write(result_final), Create(result_box))
        self.wait(2)

        # 相机旋转展示
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(2)

if __name__ == "__main__":
    # 使用更好的渲染设置
    config.frame_rate = 30
    config.pixel_width = 1280
    config.pixel_height = 720
    scene = SphereFluxProblem()
    scene.render() 