from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class StokesTheorem(ThreeDScene):
    def construct(self):
        # 创建标题
        title = Text("斯托克斯公式演示", font="STSong", font_size=48)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-1, 3, 1],
            x_length=6,
            y_length=6,
            z_length=4
        )

        # 设置相机视角
        self.set_camera_orientation(
            phi=70*DEGREES,
            theta=-45*DEGREES
        )

        self.play(Create(axes))
        self.wait(1)

        # 创建曲面（抛物面）
        surface = Surface(
            lambda u, v: np.array([u, v, 0.5*(u**2 + v**2)]),
            u_range=[-1, 1],
            v_range=[-1, 1],
            resolution=(20, 20),
            fill_color=BLUE,
            fill_opacity=0.3  # 降低透明度以便看清向量场
        )

        # 创建边界曲线
        def param_curve(t):
            x = np.cos(t)
            y = np.sin(t)
            z = 0.5*(x**2 + y**2)
            return np.array([x, y, z])

        boundary = ParametricFunction(
            param_curve,
            t_range=[0, TAU],
            color=YELLOW
        )

        # 显示曲面和边界
        self.play(Create(surface))
        self.play(Create(boundary))
        self.wait(1)

        # 创建向量场 F = (-y, x, z/2)
        def vector_field_func(point):
            x, y, z = point
            return np.array([-y, x, z/2]) / 2

        # 在曲面上创建向量场
        vector_field = VGroup()
        n_points = 6  # 每个方向上的点数
        for u in np.linspace(-0.9, 0.9, n_points):
            for v in np.linspace(-0.9, 0.9, n_points):
                if u**2 + v**2 <= 0.9:  # 只在边界内显示向量场
                    point = np.array([u, v, 0.5*(u**2 + v**2)])
                    vector = vector_field_func(point)
                    arrow = Arrow3D(
                        start=point,
                        end=point + vector,
                        color=BLUE,
                        thickness=0.02
                    )
                    vector_field.add(arrow)

        # 显示向量场
        self.play(Create(vector_field))
        self.wait(1)

        # # 添加向量场说明
        # field_text = Text("向量场 F = (-y, x, z/2)", font="STSong", color=BLUE).scale(0.6)
        # field_text.to_corner(UL)
        # self.add_fixed_in_frame_mobjects(field_text)
        # self.play(Write(field_text))

        # 创建移动的点和向量
        dot = Sphere(radius=0.05, color=RED)
        dot.move_to(param_curve(0))

        # 创建切向量
        def get_work_vector(t):
            point = param_curve(t)
            x, y, z = point
            field_vector = np.array([-y, x, z/2]) / 2
            return Arrow3D(
                start=point,
                end=point + field_vector,
                color=GREEN,
                thickness=0.02
            )

        work_vector = get_work_vector(0)

        # 添加环流说明
        circulation_text = Text("沿边界曲线的环流", font="STSong", color=GREEN).scale(0.6)
        circulation_text.to_corner(UL)  # 改为左上角
        self.add_fixed_in_frame_mobjects(circulation_text)

        # 显示点和向量
        self.play(Create(dot), Create(work_vector))
        self.play(Write(circulation_text))

        # 创建环流动画
        def update_dot_and_vector(mob, alpha):
            point = param_curve(alpha * TAU)
            dot.move_to(point)
            new_vector = get_work_vector(alpha * TAU)
            work_vector.become(new_vector)

        # 执行环流动画
        self.play(
            UpdateFromAlphaFunc(dot, update_dot_and_vector),
            run_time=6,
            rate_func=linear
        )
        self.wait(1)

        # 显示斯托克斯公式
        stokes_formula = MathTex(
            r"\oint_C \vec{F} \cdot d\vec{r} = \iint_S (\nabla \times \vec{F}) \cdot d\vec{S}"
        ).scale(0.8)
        stokes_formula.to_corner(UR)
        self.add_fixed_in_frame_mobjects(stokes_formula)
        self.play(Write(stokes_formula))

        # 显示旋度向量
        curl_vector = Arrow3D(
            start=np.array([0, 0, 0.5]),
            end=np.array([0, 0, 1.5]),
            color=RED,
            thickness=0.03
        )

        # 显示旋度
        self.play(Create(curl_vector))
        self.wait(1)

        # 相机旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(2)

def main():
    import os
    os.system("manim -pql stokes_theorem.py StokesTheorem")

if __name__ == "__main__":
    main() 