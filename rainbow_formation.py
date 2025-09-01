from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class RainbowFormation(Scene):
    def construct(self):
        # 创建标题
        title = Text("彩虹形成原理", font="STSong", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建弧形地面表示地球曲面
        earth_curve = Arc(
            radius=20,
            angle=PI/2,
            start_angle=3*PI/4,
            color=GREEN_E
        ).shift(DOWN*8 + RIGHT*2)
        
        # 添加更多地面纹理
        ground_lines = VGroup(*[
            Line(
                start=earth_curve.point_from_proportion(i/20),
                end=earth_curve.point_from_proportion(i/20) + UP*0.2,
                color=GREEN_E,
                stroke_width=2
            )
            for i in range(21)
        ])

        # 添加地面填充
        ground_fill = VMobject(
            fill_color=GREEN_E,
            fill_opacity=0.2,
            stroke_width=0
        )
        ground_fill.set_points_as_corners([
            earth_curve.get_start(),
            *[earth_curve.point_from_proportion(i/20) for i in range(21)],
            earth_curve.get_end(),
            [-7, -4, 0],
            [7, -4, 0],
        ])

        # 创建观察者
        observer = VGroup(
            Circle(radius=0.2, color=WHITE, fill_opacity=1),  # 头部
            Line([-0.1, -0.4, 0], [0.1, -0.4, 0]),  # 眼睛
        ).move_to([-4, -2.5, 0])
        
        # 创建太阳
        sun = VGroup(
            Circle(radius=0.5, color=YELLOW, fill_opacity=1),
            *[
                Line(
                    start=[0, 0, 0],
                    end=[0.8*np.cos(angle), 0.8*np.sin(angle), 0],
                    color=YELLOW
                )
                for angle in np.linspace(0, 2*PI, 8)
            ]
        ).move_to([4, 2, 0])

        # 显示基本场景
        self.play(
            FadeIn(ground_fill),
            Create(earth_curve),
            Create(ground_lines),
            Create(observer),
            Create(sun)
        )
        self.wait(1)

        # 创建水滴
        waterdrop = Circle(radius=0.5, color=BLUE, fill_opacity=0.3)
        waterdrop.move_to([0, 0, 0])

        # 显示水滴
        self.play(Create(waterdrop))
        self.wait(1)

        # 创建入射光线
        incident_ray = Line(
            start=[4, 2, 0],
            end=[0, 0, 0],
            color=WHITE
        ).set_stroke(width=2)

        # 显示入射光线
        self.play(Create(incident_ray))
        self.wait(1)

        # 创建折射和反射光线
        def create_color_rays(color, offset):
            refracted_ray1 = Line(
                start=[0, 0, 0],
                end=[-0.3, -0.4, 0],
                color=color
            ).set_stroke(width=2)
            
            reflected_ray = Line(
                start=[-0.3, -0.4, 0],
                end=[0.3, -0.4, 0],
                color=color
            ).set_stroke(width=2)
            
            # 不同颜色有不同的折射角度
            refracted_ray2 = Line(
                start=[0.3, -0.4, 0],
                end=[1 + offset*0.1, -1.5 + offset*0.1, 0],
                color=color
            ).set_stroke(width=2)
            
            return VGroup(refracted_ray1, reflected_ray, refracted_ray2)

        # 创建彩虹的七种颜色光线
        rainbow_colors = [RED, ORANGE, YELLOW, GREEN, BLUE, "#4B0082", "#800080"]  # 红橙黄绿蓝靛紫
        color_rays = VGroup(*[
            create_color_rays(color, i) 
            for i, color in enumerate(rainbow_colors)
        ])

        # 显示所有颜色的光线
        self.play(Create(color_rays))
        self.wait(1)

        # 添加说明文字
        labels = VGroup(
            Text("入射光", font="STSong").scale(0.6).next_to(incident_ray, RIGHT),
            Text("折射", font="STSong").scale(0.6).next_to(color_rays[0][0], LEFT),
            Text("反射", font="STSong").scale(0.6).next_to(color_rays[0][1], DOWN),
            Text("出射光", font="STSong").scale(0.6).next_to(color_rays[0][2], RIGHT)
        )

        self.play(Write(labels))
        self.wait(1)

        # 添加角度标注
        angles = VGroup(
            Text("42°(红)", font="STSong", color=RED).scale(0.5),
            Text("40°(紫)", font="STSong", color="#800080").scale(0.5)
        )
        angles[0].next_to(color_rays[0][2], RIGHT)
        angles[1].next_to(color_rays[-1][2], RIGHT)
        self.play(Write(angles))
        self.wait(1)

        # 创建完整的彩虹圆环（但只显示部分）
        def create_rainbow_arc(color, index):
            # 创建完整的圆
            full_circle = Circle(
                radius=3 + index*0.1,
                color=color
            )
            # 将圆移动到观察者位置
            full_circle.move_to(observer.get_center())
            # 创建遮罩以只显示上半部分
            mask = Rectangle(
                width=10,
                height=5,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0
            ).move_to(observer.get_center() + DOWN*2.5)
            
            # 返回圆和遮罩
            return VGroup(full_circle, mask)

        # 创建彩虹弧和遮罩
        rainbow_groups = VGroup(*[
            create_rainbow_arc(color, i)
            for i, color in enumerate(rainbow_colors)
        ])

        # 显示彩虹弧（使用遮罩效果）
        self.play(
            *[Create(group[0]) for group in rainbow_groups],
            *[FadeIn(group[1]) for group in rainbow_groups]
        )
        self.wait(2)

        # 添加地平线说明
        horizon_text = Text(
            "地平线遮挡了彩虹的下半部分",
            font="STSong"
        ).scale(0.5)
        horizon_text.next_to(earth_curve, UP)
        self.play(Write(horizon_text))
        self.wait(1)

        # 更新最终说明
        explanation = Text(
            "彩虹形成于观察者背对太阳方向\n不同波长的光产生不同的折射角\n红光: 42° 紫光: 40°\n实际上彩虹是一个完整的圆环",
            font="STSong"
        ).scale(0.6)
        explanation.to_edge(UP)
        self.play(Write(explanation))
        self.wait(2)

def main():
    import os
    os.system("manim -pql rainbow_formation.py RainbowFormation")

if __name__ == "__main__":
    main() 