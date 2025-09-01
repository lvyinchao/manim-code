from manim import *
import numpy as np

class DoubleIntegralConversion(Scene):
    def construct(self):
        # 添加标题
        title = Text("二重积分转化为累次积分", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[-1, 4],
            y_range=[-1, 4],
            axis_config={"color": GREY},
            x_length=5,
            y_length=5
        ).add_coordinates()
        axes.shift(LEFT * 2)

        # 创建积分区域（以一个简单的矩形为例）
        x1, x2 = 0, 3
        y1, y2 = 1, 3
        region = Rectangle(
            width=(x2-x1) * axes.get_x_axis().unit_size,
            height=(y2-y1) * axes.get_y_axis().unit_size,
            color=BLUE,
            fill_opacity=0.3
        )
        region.move_to(
            axes.c2p((x1+x2)/2, (y1+y2)/2)
        )

        # 显示坐标系和区域
        self.play(Create(axes))
        self.play(Create(region))
        self.wait(1)

        # 显示原始二重积分
        original_integral = MathTex(
            r"\iint_D f(x,y)dxdy",
            font_size=32
        ).to_corner(UR)
        self.play(Write(original_integral))
        self.wait(1)

        # 先x后y的转化
        # 创建垂直扫描线
        scan_line_x = Line(
            axes.c2p(1, y1),
            axes.c2p(1, y2),
            color=YELLOW
        )
        
        # 动画展示扫描过程
        self.play(Create(scan_line_x))
        self.play(
            scan_line_x.animate.shift(RIGHT * 2 * axes.get_x_axis().unit_size),
            run_time=2
        )
        self.wait(1)

        # 显示先x后y的累次积分
        xy_integral = MathTex(
            r"\int_{y_1}^{y_2} \left(\int_{x_1}^{x_2} f(x,y)dx\right)dy",
            font_size=32
        ).next_to(original_integral, DOWN)
        self.play(Write(xy_integral))
        self.wait(1)

        # 清除扫描线
        self.play(FadeOut(scan_line_x))

        # 先y后x的转化
        # 创建水平扫描线
        scan_line_y = Line(
            axes.c2p(x1, 2),
            axes.c2p(x2, 2),
            color=RED
        )

        # 动画展示扫描过程
        self.play(Create(scan_line_y))
        self.play(
            scan_line_y.animate.shift(UP * axes.get_y_axis().unit_size),
            run_time=2
        )
        self.wait(1)

        # 显示先y后x的累次积分
        yx_integral = MathTex(
            r"\int_{x_1}^{x_2} \left(\int_{y_1}^{y_2} f(x,y)dy\right)dx",
            font_size=32
        ).next_to(xy_integral, DOWN)
        self.play(Write(yx_integral))
        self.wait(1)

        # 添加边界标注
        x1_label = MathTex("x_1", font_size=24).next_to(axes.c2p(x1, 0), DOWN)
        x2_label = MathTex("x_2", font_size=24).next_to(axes.c2p(x2, 0), DOWN)
        y1_label = MathTex("y_1", font_size=24).next_to(axes.c2p(0, y1), LEFT)
        y2_label = MathTex("y_2", font_size=24).next_to(axes.c2p(0, y2), LEFT)

        self.play(
            Write(VGroup(x1_label, x2_label, y1_label, y2_label))
        )

        # 添加说明文字
        explanation = Text(
            "积分顺序的选择取决于积分区域的形状和被积函数",
            font="SimSun",
            font_size=24
        ).to_edge(DOWN)
        self.play(Write(explanation))
        self.wait(2) 