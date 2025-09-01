from manim import *
import numpy as np

# 在文件开头添加全局配置
config.tex_template = TexTemplateLibrary.ctex
config.tex_template.font_size = 24
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")  # 使用华文宋体

class GreensTheorem(Scene):
    def construct(self):
        # 创建更醒目的标题
        title = Text("格林公式直观演示", font="Source Han Serif SC", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-2, 2],
            axis_config={"color": GREY},
            x_length=7,
            y_length=5
        )
        self.play(Create(axes))
        self.wait(1)

        # 创建闭合区域（椭圆）
        region = ParametricFunction(
            lambda t: axes.c2p(2*np.cos(t), np.sin(t)),
            t_range=[0, 2*PI],
            color=BLUE
        )
        boundary = region.copy().set_color(YELLOW)
        
        self.play(Create(region))
        self.wait(1)

        # 添加边界方向指示
        moving_dot = Dot(color=RED).move_to(region.get_start())
        self.play(Create(moving_dot))
        self.play(MoveAlongPath(moving_dot, boundary), run_time=3, rate_func=linear)
        self.remove(moving_dot)
        self.wait(1)

        # 创建向量场 P = -y, Q = x
        def vector_field(point):
            x, y = axes.p2c(point)
            return Vector([y, -x], color=GREEN).shift(point)
        
        field = VGroup(*[vector_field(axes.c2p(x,y)) 
                       for x in np.arange(-2, 2.5, 0.5)
                       for y in np.arange(-1, 1.5, 0.5)])
        
        self.play(Create(field))
        self.wait(1)

        # 优化向量场展示
        field_creation = LaggedStart(
            *[GrowArrow(vec) for vec in field],
            run_time=3,
            lag_ratio=0.1
        )
        self.play(field_creation)
        self.wait(1)

        # 分步展示格林公式
        formula = VGroup(
            MathTex(r"\oint_C", color=RED),
            MathTex(r"P\,dx + Q\,dy", color=GREEN),
            MathTex(r"=", color=WHITE),
            MathTex(r"\iint_D", color=BLUE),
            MathTex(r"\left( \frac{\partial Q}{\partial x}", color=GREEN),
            MathTex(r"-", color=WHITE),
            MathTex(r"\frac{\partial P}{\partial y} \right)", color=GREEN),
            MathTex(r"dA", color=BLUE)
        ).arrange(RIGHT).to_edge(DOWN)

        # 分步动画展示公式
        self.play(Write(formula[0]))  # 展示环积分符号
        self.wait(0.5)
        self.play(Write(formula[1]))  # 展示积分项
        self.wait(1)
        self.play(Write(formula[2:4]))  # 展示等号和二重积分符号
        self.wait(0.5)
        self.play(Write(formula[4:]))  # 展示偏导部分
        self.wait(2)

        # 添加公式注释框
        formula_box = SurroundingRectangle(formula, color=YELLOW, buff=0.2)
        self.play(Create(formula_box))
        self.wait(1)

        # 优化示例展示（分步显示）
        example_steps = VGroup(
            VGroup(
                Text("步骤1: 定义向量场", font="STSong"),
                MathTex("P = -y,\\ Q = x")
            ),
            VGroup(
                Text("步骤2: 计算旋度", font="STSong"),
                MathTex(r"\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = 2")
            ),
            VGroup(
                Text("步骤3: 应用公式", font="STSong"),
                MathTex(r"\oint_C -y\,dx + x\,dy = 2 \times \text{面积}")
            )
        )

        # 分步显示示例
        current_step = example_steps[0].copy()
        self.play(FadeIn(current_step))
        self.wait(1)
        
        for step in example_steps[1:]:
            self.play(Transform(current_step, step))
            self.wait(1)

        # 动态展示面积计算
        area_text = Text("椭圆面积:", font="Source Han Serif SC", font_size=24)
        self.play(Write(area_text))
        self.wait(1)

        # 面积公式展示
        area_equation = VGroup(
            Text("椭圆面积 = π·a·b = ", font="Source Han Serif SC"),
            MathTex(r"\pi \cdot 2 \cdot 1 = 2\pi")
        ).arrange(RIGHT)
        self.play(Write(area_equation))
        self.wait(2)

    def check_font_exists(self, font_name):
        try:
            Text("test", font=font_name)
            return True
        except:
            return False

def main():
    import os
    os.system("manim -pqh greens_theorem.py GreensTheorem")

if __name__ == "__main__":
    main() 