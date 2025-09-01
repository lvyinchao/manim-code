from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class SimpleSphereFLux(ThreeDScene):
    def construct(self):
        # 简洁标题
        title = Text("球面流量计算", font="STSong", font_size=36)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 设置相机视角
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES, zoom=0.9)

        # 简化的坐标系
        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-2.5, 2.5, 1],
            z_range=[-2.5, 2.5, 1],
            x_length=5,
            y_length=5,
            z_length=5,
            axis_config={"color": BLUE_B}
        )

        # 创建球面 x² + y² + z² = 4
        sphere = Surface(
            lambda u, v: np.array([
                2 * np.sin(u) * np.cos(v),
                2 * np.sin(u) * np.sin(v),
                2 * np.cos(u)
            ]),
            u_range=[0, PI],
            v_range=[0, TAU],
            resolution=(15, 15),
            fill_opacity=0.4,
            stroke_width=1,
            stroke_color=BLUE_E,
            fill_color=BLUE_D
        )

        # 题目：简洁显示
        problem = VGroup(
            Text("流速：", font="STSong", font_size=20, color=WHITE),
            MathTex(r"\vec{v} = (k, y, 0)", font_size=20, color=RED),
            Text("  球面：", font="STSong", font_size=20, color=WHITE),
            MathTex(r"x^2+y^2+z^2=4", font_size=20, color=BLUE)
        ).arrange(RIGHT, buff=0.2).to_edge(UP, buff=0.5)

        self.add_fixed_in_frame_mobjects(problem)
        self.play(Write(problem), Create(axes), Create(sphere))
        self.wait(1)

        # 显示几个代表性的向量场箭头
        vectors = VGroup()
        for i in range(8):
            theta = i * TAU / 8
            phi = PI/3
            x = 2 * np.sin(phi) * np.cos(theta)
            y = 2 * np.sin(phi) * np.sin(theta)
            z = 2 * np.cos(phi)
            point = np.array([x, y, z])
            
            # 流速向量 (k, y, 0)，k取1
            field_vector = np.array([0.8, y * 0.3, 0])
            
            arrow = Arrow3D(
                start=point,
                end=point + field_vector,
                color=RED,
                thickness=0.03
            )
            vectors.add(arrow)

        self.play(Create(vectors))
        self.wait(1)

        # 显示法向量
        normals = VGroup()
        for i in range(8):
            theta = i * TAU / 8
            phi = PI/3
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
            normals.add(arrow)

        self.play(Create(normals))
        self.wait(1)

        # 添加向量标识
        vector_labels = VGroup(
            Text("流速", font="STSong", font_size=18, color=RED),
            MathTex(r"\vec{v}", font_size=18, color=RED),
            Text("法向量", font="STSong", font_size=18, color=YELLOW),
            MathTex(r"\vec{n}", font_size=18, color=YELLOW)
        ).arrange(RIGHT, buff=0.3).to_corner(DR, buff=0.3)
        
        self.add_fixed_in_frame_mobjects(vector_labels)
        self.play(Write(vector_labels))
        self.wait(1)

        # 关键公式：通量
        flux_formula = MathTex(
            r"\Phi = \iint_S \vec{v} \cdot \vec{n} \, dS",
            font_size=28,
            color=YELLOW
        ).to_corner(UR, buff=0.5)
        
        self.add_fixed_in_frame_mobjects(flux_formula)
        self.play(Write(flux_formula))
        self.wait(1)

        # 计算步骤：只显示关键步骤
        step1 = MathTex(
            r"= \iint_S (k, y, 0) \cdot \frac{(x,y,z)}{2} \, dS",
            font_size=22
        ).next_to(flux_formula, DOWN, buff=0.3)
        
        step2 = MathTex(
            r"= \iint_S \left(\frac{kx + y^2}{2}\right) dS",
            font_size=22
        ).next_to(step1, DOWN, buff=0.2)
        
        self.add_fixed_in_frame_mobjects(step1, step2)
        self.play(Write(step1))
        self.wait(0.8)
        self.play(Write(step2))
        self.wait(1)

        # 球坐标转换：关键信息
        coord_info = VGroup(
            Text("球坐标：", font="STSong", font_size=20, color=GREEN),
            MathTex(r"x=2\sin\phi\cos\theta,\, y=2\sin\phi\sin\theta", font_size=18),
            MathTex(r"dS = 4\sin\phi \, d\phi d\theta", font_size=18, color=GREEN)
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        coord_info.to_edge(LEFT, buff=0.5).shift(DOWN * 1.5)
        
        self.add_fixed_in_frame_mobjects(coord_info)
        self.play(Write(coord_info))
        self.wait(1)

        # 积分计算：直接显示结果
        calculation = VGroup(
            Text("计算：", font="STSong", font_size=20, color=ORANGE),
            MathTex(r"\int_0^{2\pi} \cos\theta \, d\theta = 0", font_size=18),
            MathTex(r"\int_0^{2\pi} \sin^2\theta \, d\theta = \pi", font_size=18),
            MathTex(r"\int_0^{\pi} \sin^4\phi \, d\phi = \frac{3\pi}{8}", font_size=18)
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        calculation.next_to(coord_info, DOWN, buff=0.5)
        
        self.add_fixed_in_frame_mobjects(calculation)
        for item in calculation:
            self.play(Write(item), run_time=0.6)

        self.wait(1)

        # 最终结果：突出显示
        result = MathTex(
            r"\Phi = 3\pi^2",
            font_size=36,
            color=YELLOW
        ).to_edge(DOWN, buff=0.8)
        
        result_box = SurroundingRectangle(result, buff=0.3, color=YELLOW, stroke_width=3)
        
        self.add_fixed_in_frame_mobjects(result, result_box)
        self.play(
            Write(result),
            Create(result_box),
            run_time=1.5
        )
        
        # 相机旋转展示
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(1)

if __name__ == "__main__":
    config.frame_rate = 30
    config.pixel_width = 1280
    config.pixel_height = 720
    scene = SimpleSphereFLux()
    scene.render() 