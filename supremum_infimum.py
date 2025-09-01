from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class SupremumInfimum(Scene):
    def construct(self):
        # 创建标题
        title = Text("确界原理演示", font="STSong", font_size=48)
        
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建坐标系
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1, 3, 0.5],
            axis_config={"include_tip": True},
            x_length=10,
            y_length=6
        )
        
        x_label = axes.get_x_axis_label("n")
        y_label = axes.get_y_axis_label("x_n")
        
        self.play(Create(axes), Write(x_label), Write(y_label))

        # 创建一个有界但不单调的数列
        def sequence_func(x):
            return 2 + np.sin(x) * np.exp(-x/5)

        # 创建数列点和连线
        x_vals = np.linspace(0, 10, 50)
        points = [axes.coords_to_point(x, sequence_func(x)) for x in x_vals]
        curve = VMobject()
        curve.set_points_smoothly(points)
        curve.set_color(BLUE)
        
        dots = VGroup(*[Dot(point) for point in points[::5]])

        self.play(Create(curve), Create(dots))
        
        # 创建上确界线
        sup_value = 3
        sup_line = DashedLine(
            axes.coords_to_point(0, sup_value),
            axes.coords_to_point(10, sup_value),
            color=RED
        )
        sup_label = MathTex(r"\sup x_n", color=RED).next_to(sup_line, RIGHT)
        
        # 创建下确界线
        inf_value = 1
        inf_line = DashedLine(
            axes.coords_to_point(0, inf_value),
            axes.coords_to_point(10, inf_value),
            color=GREEN
        )
        inf_label = MathTex(r"\inf x_n", color=GREEN).next_to(inf_line, RIGHT)

        # 显示确界
        self.play(
            Create(sup_line),
            Write(sup_label)
        )
        self.play(
            Create(inf_line),
            Write(inf_label)
        )

        # 添加定义说明
        sup_def = Text(
            "上确界：数列的最小上界",
            font="STSong",
            color=RED
        ).scale(0.4)
        inf_def = Text(
            "下确界：数列的最大下界",
            font="STSong",
            color=GREEN
        ).scale(0.4)
        
        definitions = VGroup(sup_def, inf_def).arrange(DOWN, aligned_edge=LEFT)
        definitions.to_corner(UL)
        
        self.play(Write(definitions))
        
        # 演示上界性质
        epsilon = 0.2
        point_above = Dot(axes.coords_to_point(5, sup_value + epsilon), color=RED)
        cross = Cross(point_above, color=RED)
        
        self.play(Create(point_above))
        self.play(Create(cross))
        self.wait(1)
        
        # 演示稠密性质
        for x in [2, 4, 6, 8]:
            point_near = Dot(
                axes.coords_to_point(x, sequence_func(x)),
                color=YELLOW
            )
            self.play(
                Create(point_near),
                FadeOut(point_near),
                run_time=0.5
            )
        
        self.wait(2)

def main():
    import os
    os.system("manim -pql supremum_infimum.py SupremumInfimum")

if __name__ == "__main__":
    main() 