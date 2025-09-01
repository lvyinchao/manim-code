from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class Circulation(ThreeDScene):
    def construct(self):
        # 创建标题
        title = Text("向量场的环流量", font="STSong", font_size=48)
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

        # 创建旋转向量场
        def vector_field_func(point):
            x, y, z = point
            return np.array([-y, x, 0]) / 2

        # 创建向量场（蓝色箭头）- 减少向量数量
        vector_field = VGroup()
        for x in np.linspace(-2, 2, 5):  # 减少为5x5的网格
            for y in np.linspace(-2, 2, 5):
                for z in [0]:
                    point = np.array([x, y, z])
                    vector = vector_field_func(point)
                    arrow = Arrow3D(
                        start=point,
                        end=point + vector,
                        color=BLUE,
                        thickness=0.02
                    )
                    vector_field.add(arrow)

        # 添加向量场说明 - 添加向量符号
        field_label = MathTex(
            "\\vec{F}", 
            tex_template=TexTemplateLibrary.ctex,
            color=BLUE
        ).scale(1.2)
        field_label.shift(LEFT * 3.5)  # 向中间平移

        self.add_fixed_in_frame_mobjects(field_label)
        self.play(Create(vector_field), Write(field_label))
        self.wait(1)

        # 创建圆形路径
        radius = 1.5
        circle = Circle(radius=radius, color=YELLOW)
        circle.shift(OUT*0.01)  # 稍微抬高以便看清
        
        # 创建路径箭头（表示路径方向）
        path_arrows = VGroup()
        n_arrows = 24  # 增加箭头数量
        for i in range(n_arrows):
            angle = i * TAU / n_arrows
            point = np.array([
                radius * np.cos(angle),
                radius * np.sin(angle),
                0.01
            ])
            next_angle = (i + 1) * TAU / n_arrows
            next_point = np.array([
                radius * np.cos(next_angle),
                radius * np.sin(next_angle),
                0.01
            ])
            arrow = Arrow3D(
                start=point,
                end=next_point,
                color=YELLOW,
                thickness=0.02
            )
            path_arrows.add(arrow)

        # 修改路径说明位置
        path_label = Text("闭合路径 C", font="STSong", font_size=30, color=YELLOW)
        path_label.shift(RIGHT * 3.5)  # 向中间平移
        self.add_fixed_in_frame_mobjects(path_label)

        self.play(Create(circle), Create(path_arrows), Write(path_label))
        self.wait(1)

        # 创建移动的点和切向量
        dot = Sphere(radius=0.08, color=RED)
        dot.move_to(circle.point_from_proportion(0))
        
        # 创建切向量（显示做功）
        def get_work_vector(point):
            field_vector = vector_field_func(point)
            return Arrow3D(
                start=point,
                end=point + field_vector,
                color=GREEN,
                thickness=0.03
            )

        work_vector = get_work_vector(circle.point_from_proportion(0))

        # 添加做功说明
        work_label = Text("向量场沿路径做功", font="STSong", font_size=30, color=GREEN)
        work_label.next_to(path_label, DOWN)
        self.add_fixed_in_frame_mobjects(work_label)

        self.play(Create(dot), Create(work_vector), Write(work_label))
        self.wait(1)

        # 创建环流量公式
        circulation_formula = MathTex(
            "\\text{环流量} = \\oint_C \\vec{F} \\cdot d\\vec{r}",
            tex_template=TexTemplateLibrary.ctex
        ).scale(0.8)
        circulation_formula.to_corner(UR)
        
        explanation = Text(
            "环流量表示向量场沿闭合路径的总做功",
            font="STSong",
            font_size=24
        ).next_to(circulation_formula, DOWN+LEFT*0.5)

        self.add_fixed_in_frame_mobjects(circulation_formula, explanation)
        self.play(Write(circulation_formula), Write(explanation))
        self.wait(1)

        # 创建点的运动动画
        def update_dot_and_vector(mob, alpha):
            new_point = circle.point_from_proportion(alpha)
            dot.move_to(new_point)
            new_vector = get_work_vector(new_point)
            work_vector.become(new_vector)

        # 执行动画
        self.play(
            UpdateFromAlphaFunc(dot, update_dot_and_vector),
            run_time=8,
            rate_func=linear
        )
        self.wait(1)

        # 相机旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(2)

def main():
    import os
    os.system("manim -pqh circulation.py Circulation")

if __name__ == "__main__":
    main() 