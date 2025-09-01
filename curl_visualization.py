from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class CurlVisualization(ThreeDScene):
    def construct(self):
        # 创建标题
        title = Text("向量场的旋度", font="STSong", font_size=48)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )

        # 设置相机视角
        self.set_camera_orientation(
            phi=70*DEGREES,
            theta=-45*DEGREES
        )

        self.play(Create(axes))
        self.wait(1)

        # 创建旋转向量场（以z轴为轴的旋转场）
        def vector_field_func(point):
            x, y, z = point
            return np.array([-y, x, 0]) / 2

        # 创建向量场
        vector_field = VGroup()
        for x in np.linspace(-2, 2, 5):
            for y in np.linspace(-2, 2, 5):
                for z in [0]:  # 只在z=0平面创建向量
                    point = np.array([x, y, z])
                    vector = vector_field_func(point)
                    arrow = Arrow3D(
                        start=point,
                        end=point + vector,
                        color=BLUE,
                        thickness=0.02
                    )
                    vector_field.add(arrow)

        self.play(Create(vector_field))
        self.wait(1)

        # 创建测试圆盘
        radius = 0.5
        test_points = [(1.5, 0, 0), (-1.5, 0, 0), (0, 1.5, 0), (0, -1.5, 0)]
        discs = VGroup()
        disc_vectors = VGroup()
        
        for center in test_points:
            # 创建圆盘
            disc = Surface(
                lambda u, v: np.array([
                    center[0] + radius * u * np.cos(v),
                    center[1] + radius * u * np.sin(v),
                    center[2]
                ]),
                u_range=[0, 1],
                v_range=[0, TAU],
                resolution=(8, 16),
                checkerboard_colors=[RED_D, RED_E],
                fill_opacity=0.3
            )
            discs.add(disc)

            # 在圆盘周围添加向量
            for theta in np.linspace(0, TAU, 8):
                point = np.array([
                    center[0] + radius * np.cos(theta),
                    center[1] + radius * np.sin(theta),
                    center[2]
                ])
                vector = vector_field_func(point)
                arrow = Arrow3D(
                    start=point,
                    end=point + vector,
                    color=YELLOW,
                    thickness=0.02
                )
                disc_vectors.add(arrow)

        self.play(Create(discs), Create(disc_vectors))
        self.wait(1)

        # 添加旋转动画
        def rotate_disc(disc, angle, center):
            disc.rotate(angle, axis=OUT, about_point=center)

        # 创建说明文字
        curl_formula = MathTex(
            "\\text{curl}\\,\\vec{F} = \\nabla \\times \\vec{F} = \\begin{vmatrix} "
            "\\mathbf{i} & \\mathbf{j} & \\mathbf{k} \\\\ "
            "\\frac{\\partial}{\\partial x} & \\frac{\\partial}{\\partial y} & \\frac{\\partial}{\\partial z} \\\\ "
            "F_x & F_y & F_z"
            "\\end{vmatrix}"
        ).scale(0.7).to_corner(UL)

        explanation = Text(
            "旋度表示向量场在该点的旋转趋势",
            font="STSong",
            font_size=24
        ).next_to(curl_formula, DOWN)

        self.add_fixed_in_frame_mobjects(curl_formula, explanation)
        self.play(Write(curl_formula), Write(explanation))

        # 添加旋转动画
        self.play(
            *[Rotate(disc, angle=2*PI, axis=OUT, about_point=np.array(center)) 
              for disc, center in zip(discs, test_points)],
            run_time=4,
            rate_func=linear
        )
        self.wait(2)

        # 显示旋度大小的说明
        curl_magnitude = MathTex(
            "\\text{旋度大小} = \\lim_{\\Delta S \\to 0} \\frac{\\oint_C \\vec{F} \\cdot d\\vec{r}}{\\Delta S}"
        ).scale(0.7).next_to(explanation, DOWN)
        
        self.add_fixed_in_frame_mobjects(curl_magnitude)
        self.play(Write(curl_magnitude))
        self.wait(2)

        # 最后的旋转动画
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(2)

def main():
    import os
    os.system("manim -pqh curl_visualization.py CurlVisualization")

if __name__ == "__main__":
    main() 