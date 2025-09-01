from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class BabylonianMethodAnimation(Scene):
    def construct(self):
        # 标题
        title = Text("巴比伦方法求平方根", font="STSong", font_size=40, color=BLUE)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 显示题目（使用数学公式，一行显示）
        problem_title = Text("题目：", font_size=24, color=YELLOW)
        problem_text = MathTex(r"\text{设 } x_0 > 0, x_{n+1} = \frac{1}{2}(x_n + \frac{a}{x_n}), \text{且 } a > 0, \text{证明 } \lim_{n \to \infty} x_n \text{ 存在并求此极限}", font_size=18, color=WHITE)
        
        problem_group = VGroup(problem_title, problem_text).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        problem_group.to_edge(UP, buff=0.5)
        
        self.play(Write(problem_group))
        self.wait(2)

        # 分析思路（左上角）
        analysis_title = Text("分析思路：", font_size=20, color=GREEN)
        analysis_text1 = Text("1. 证明数列单调有界", font_size=16, color=WHITE)
        analysis_text2 = Text("2. 利用单调有界定理", font_size=16, color=WHITE)
        analysis_text3 = Text("3. 求极限值", font_size=16, color=WHITE)
        
        analysis_group = VGroup(analysis_title, analysis_text1, analysis_text2, analysis_text3)
        analysis_group.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        analysis_group.to_corner(UL, buff=0.3)
        
        self.play(Write(analysis_group))
        self.wait(2)

        # 迭代公式分析（移到分析思路下面）
        formula_title = Text("迭代公式分析：", font_size=20, color=ORANGE)
        formula1 = MathTex(r"x_{n+1} = \frac{1}{2}(x_n + \frac{a}{x_n})", font_size=18)
        formula2 = MathTex(r"= \frac{1}{2}(f(x_n) + g(x_n))", font_size=18)
        
        formula_group = VGroup(formula_title, formula1, formula2)
        formula_group.arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        formula_group.to_corner(UL, buff=0.3).shift(DOWN * 1.5)
        
        self.play(Write(formula_group))
        self.wait(2)

        # 创建坐标系 - 扩大x轴范围
        axes = Axes(
            x_range=[0, 6, 1],  # 从0-4改为0-6
            y_range=[0, 4, 1],
            x_length=8,  # 从6改为8
            y_length=4,
            axis_config={"color": BLUE_B}
        )
        axes.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5)
        
        # 添加标签
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        self.play(Create(axes), Create(x_label), Create(y_label))
        self.wait(1)

        # 绘制函数 f(x) = x 和 g(x) = a/x
        a = 2  # 取 a = 2 作为例子
        x_line = axes.plot(lambda x: x, x_range=[0, 5], color=RED)  # 从0-3改为0-5
        hyperbola = axes.plot(lambda x: a/x, x_range=[0.5, 5], color=GREEN)  # 改为[0.5, 5]
        
        # 添加函数标签 - 增大字体
        f_label = MathTex("f(x) = x", color=RED, font_size=20).next_to(x_line, RIGHT, buff=0.1)
        g_label = MathTex("g(x) = \\frac{a}{x}", color=GREEN, font_size=20).next_to(hyperbola, RIGHT, buff=0.1)
        
        self.play(Create(x_line), Create(hyperbola))
        self.play(Write(f_label), Write(g_label))
        self.wait(1)

        # 开始迭代过程
        x0 = 5.0  # 初始值改为5.0
        iterations = []
        x_values = [x0]
        
        # 在红色直线上标记f(x₀)点
        f_initial_point = Dot(axes.coords_to_point(x0, x0), color=RED, radius=0.06)
        f_initial_label = MathTex("f(x_0)", font_size=14, color=RED).next_to(f_initial_point, UP, buff=0.1)
        
        # 在绿色双曲线上标记g(x₀)点
        g_initial_point = Dot(axes.coords_to_point(x0, a/x0), color=GREEN, radius=0.06)
        g_initial_label = MathTex("g(x_0)", font_size=14, color=GREEN).next_to(g_initial_point, RIGHT, buff=0.1)
        
        self.play(Create(f_initial_point), Write(f_initial_label))
        self.play(Create(g_initial_point), Write(g_initial_label))
        self.wait(1)

        # 执行迭代 - 只显示到x4
        for i in range(4):  # 改为4次迭代
            # 计算下一个值
            x_next = 0.5 * (x_values[-1] + a / x_values[-1])
            x_values.append(x_next)
            
            # 在坐标系中显示迭代过程
            current_x = x_values[-2]
            current_y = x_values[-2]
            
            # 垂直线到双曲线
            vertical_line = DashedLine(
                axes.coords_to_point(current_x, current_y),
                axes.coords_to_point(current_x, a/current_x),
                color=BLUE
            )
            
            # 显示中点计算 - 修正：中点应该是 (x_n, (x_n + a/x_n)/2)
            midpoint_x = current_x
            midpoint_y = (current_x + a/current_x) / 2
            midpoint_point = Dot(axes.coords_to_point(midpoint_x, midpoint_y), color=PURPLE_A, radius=0.05)
            
            # 显示具体的迭代公式
            midpoint_label = MathTex(f"x_{i+1} = \\frac{{1}}{{2}}(x_{i} + \\frac{{a}}{{x_{i}}})", font_size=12, color=PURPLE_A)
            
            # 根据迭代次数调整公式标签位置
            if i == 3:  # x₄的情况，显示在交点下方
                midpoint_label.next_to(midpoint_point, DOWN, buff=0.1)
            else:
                midpoint_label.next_to(midpoint_point, RIGHT)
            
            # 从紫色中点直接连线到x轴上的下一个迭代点位置
            horizontal_line = DashedLine(
                axes.coords_to_point(midpoint_x, midpoint_y),
                axes.coords_to_point(x_next, 0),  # 连线到x轴上的x_{i+1}位置
                color=PURPLE_A
            )
            
            # 在x轴上标记下一个迭代点位置
            x_axis_point = Dot(axes.coords_to_point(x_next, 0), color=YELLOW, radius=0.05)
            x_axis_label = MathTex(f"x_{i+1}", font_size=14, color=YELLOW).next_to(x_axis_point, DOWN, buff=0.1)
            
            # 从x轴上的点向上做垂直线找到f(x_{i+1})和g(x_{i+1})
            vertical_line_to_f = DashedLine(
                axes.coords_to_point(x_next, 0),
                axes.coords_to_point(x_next, x_next),
                color=RED
            )
            
            vertical_line_to_g = DashedLine(
                axes.coords_to_point(x_next, 0),
                axes.coords_to_point(x_next, a/x_next),
                color=GREEN
            )
            
            # 在红色直线上标记f(x_{i+1})点
            f_next_point = Dot(axes.coords_to_point(x_next, x_next), color=RED, radius=0.06)
            f_next_label = MathTex(f"f(x_{i+1})", font_size=14, color=RED)
            
            # 在绿色双曲线上标记g(x_{i+1})点
            g_next_point = Dot(axes.coords_to_point(x_next, a/x_next), color=GREEN, radius=0.06)
            g_next_label = MathTex(f"g(x_{i+1})", font_size=14, color=GREEN)
            
            # 根据迭代次数调整标签位置，避免与交点重叠
            if i == 3:  # x₄的情况
                f_next_label.next_to(f_next_point, LEFT, buff=0.1)
                g_next_label.next_to(g_next_point, LEFT, buff=0.1)
            else:
                f_next_label.next_to(f_next_point, UP, buff=0.1)
                g_next_label.next_to(g_next_point, RIGHT, buff=0.1)
            
            self.play(Create(vertical_line))
            self.wait(0.5)
            self.play(Create(midpoint_point), Write(midpoint_label))
            self.wait(1)
            self.play(Create(horizontal_line))
            self.wait(0.5)
            self.play(Create(x_axis_point), Write(x_axis_label))
            self.wait(0.5)
            self.play(Create(vertical_line_to_f), Create(vertical_line_to_g))
            self.wait(0.5)
            self.play(Create(f_next_point), Write(f_next_label))
            self.play(Create(g_next_point), Write(g_next_label))
            self.wait(1)

        # 显示收敛性证明（移到迭代分析下面）
        proof_title = Text("收敛性证明：", font_size=20, color=PURPLE)
        proof1 = MathTex(r"1. \text{下界性：} x_n \geq \sqrt{a}", font_size=16)
        proof2 = MathTex(r"2. \text{单调性：} x_{n+1} \leq x_n", font_size=16)
        proof3 = MathTex(r"3. \text{极限：} \lim_{n \to \infty} x_n = \sqrt{a}", font_size=16)
        
        proof_group = VGroup(proof_title, proof1, proof2, proof3)
        proof_group.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        proof_group.to_corner(UL, buff=0.3).shift(DOWN * 3.5)
        
        self.play(Write(proof_group))
        self.wait(2)

        # 显示数值结果
        result_title = Text("数值结果：", font_size=24, color=YELLOW)
        result_text = Text(f"a = {a}, x₀ = {x0}", font_size=18, color=WHITE)
        
        result_group = VGroup(result_title, result_text)
        result_group.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        result_group.to_edge(LEFT, buff=0.5).shift(DOWN * 5.5)
        
        self.play(Write(result_group))
        self.wait(2)

        # 最终结论（移到最下面）
        conclusion_title = Text("结论：", font_size=24, color=GREEN)
        conclusion1 = MathTex(r"\lim_{n \to \infty} x_n = \sqrt{a}", font_size=24, color=YELLOW)
        conclusion2 = Text("这是求平方根的巴比伦方法", font_size=20, color=WHITE)
        
        conclusion_group = VGroup(conclusion_title, conclusion1, conclusion2)
        conclusion_group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        conclusion_group.to_corner(DL, buff=0.5)
        
        # 突出显示最终结果
        result_box = SurroundingRectangle(conclusion1, buff=0.2, color=YELLOW)
        
        self.play(Write(conclusion_group))
        self.play(Create(result_box))
        self.wait(3)

if __name__ == "__main__":
    # 使用1080p渲染设置
    config.frame_rate = 30
    config.pixel_width = 1920
    config.pixel_height = 1080
    scene = BabylonianMethodAnimation()
    scene.render() 