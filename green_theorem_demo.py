from manim import *
import numpy as np

class GreenTheoremDemo(Scene):
    def construct(self):
        # 显示标题
        title = Text("格林公式演示", font_size=36)
        self.play(Write(title))
        self.wait()
        self.play(FadeOut(title))
        
        # 显示格林公式
        formula = MathTex(
            r"\oint_C P\,dx + Q\,dy = \iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dx\,dy",
            font_size=36
        )
        self.play(Write(formula))
        self.wait()
        
        # 创建坐标系
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            axis_config={"color": BLUE}
        )
        self.play(Create(axes))
        
        # 创建边界曲线C（椭圆）
        curve = ParametricFunction(
            lambda t: np.array([2*np.cos(t), np.sin(t), 0]),
            t_range=[0, 2*PI],
            color=RED
        )
        self.play(Create(curve))
        
        # 创建填充区域D
        points = [
            np.array([2*np.cos(t), np.sin(t), 0])
            for t in np.linspace(0, 2*PI, 100)
        ]
        region = Polygon(*points, color=BLUE_E, fill_opacity=0.3)
        self.play(FadeIn(region))
        
        # 创建向量场
        def vector_field_func(pos):
            x, y = pos[:2]
            return np.array([-y, x, 0])
        
        vector_field = ArrowVectorField(
            vector_field_func,
            x_range=[-2.5, 2.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            length_func=lambda x: 0.5,
            color=GREEN
        )
        self.play(Create(vector_field))
        
        # 计算旋度
        curl = MathTex(
            r"\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} = 1 - (-1) = 2",
            font_size=32
        ).to_edge(UP)
        self.play(Write(curl))
        
        # 显示曲线积分
        line_integral = MathTex(
            r"\oint_C -y\,dx + x\,dy",
            font_size=32
        ).next_to(curl, DOWN)
        self.play(Write(line_integral))
        
        # 显示二重积分
        double_integral = MathTex(
            r"\iint_D 2\,dx\,dy = 2 \times \text{Area}(D) = 2\pi",
            font_size=32
        ).next_to(line_integral, DOWN)
        self.play(Write(double_integral))
        
        # 添加说明文字
        explanation = Text(
            "格林公式将曲线积分与二重积分联系起来",
            font_size=24
        ).to_edge(DOWN)
        self.play(Write(explanation))
        
        self.wait(2)
        
        # 淡出所有元素
        self.play(*[FadeOut(mob) for mob in self.mobjects]) 