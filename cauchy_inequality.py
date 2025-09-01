from manim import *
import numpy as np

class CauchyInequalityIntro(Scene):
    def construct(self):
        title = Text("柯西不等式的多种形式", font="SimHei")
        subtitle = Text("Cauchy-Schwarz Inequality", font="Arial").scale(0.8)
        
        title.to_edge(UP)
        subtitle.next_to(title, DOWN)
        
        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(2)
        
        self.clear()
        self.introduce_cauchy()
    
    def introduce_cauchy(self):
        title = Text("柯西不等式是什么？", font="SimHei").to_edge(UP)
        self.play(Write(title))
        
        description = Text(
            "柯西不等式是数学中最重要的不等式之一，\n有多种等价形式，广泛应用于各个数学分支。", 
            font="SimHei"
        ).scale(0.7)
        description.next_to(title, DOWN, buff=1)
        
        self.play(Write(description))
        self.wait(2)
        
        forms = VGroup(
            Text("• 代数形式", font="SimHei"),
            Text("• 向量形式", font="SimHei"),
            Text("• 积分形式", font="SimHei"),
            Text("• 概率形式", font="SimHei")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7)
        forms.next_to(description, DOWN, buff=0.5)
        
        for form in forms:
            self.play(Write(form), run_time=0.5)
        
        self.wait(2)
        self.clear()


class AlgebraicForm(Scene):
    def construct(self):
        title = Text("代数形式", font="SimHei").to_edge(UP)
        self.play(Write(title))
        
        # 基本形式的公式
        formula = MathTex(
            r"\left(\sum_{i=1}^{n} a_i b_i\right)^2 \leq \left(\sum_{i=1}^{n} a_i^2\right) \left(\sum_{i=1}^{n} b_i^2\right)"
        )
        self.play(Write(formula))
        self.wait(2)
        
        # 演示特例 n=2
        self.play(formula.animate.to_edge(UP, buff=1.5))
        example = Text("特例：n=2的情况", font="SimHei").scale(0.7)
        example.next_to(formula, DOWN, buff=0.5)
        self.play(Write(example))
        
        simple_form = MathTex(
            r"(a_1 b_1 + a_2 b_2)^2 \leq (a_1^2 + a_2^2)(b_1^2 + b_2^2)"
        )
        simple_form.next_to(example, DOWN, buff=0.5)
        self.play(Write(simple_form))
        self.wait(2)
        
        # 展开证明思路
        expansion = Text("这可以通过展开左侧，并比较与右侧的差值来证明", font="SimHei").scale(0.7)
        expansion.next_to(simple_form, DOWN, buff=0.5)
        self.play(Write(expansion))
        
        expanded = MathTex(
            r"(a_1 b_1)^2 + 2(a_1 b_1)(a_2 b_2) + (a_2 b_2)^2"
        )
        expanded.next_to(expansion, DOWN, buff=0.5)
        self.play(Write(expanded))
        
        right_side = MathTex(
            r"(a_1^2 + a_2^2)(b_1^2 + b_2^2) = a_1^2 b_1^2 + a_1^2 b_2^2 + a_2^2 b_1^2 + a_2^2 b_2^2"
        )
        right_side.next_to(expanded, DOWN, buff=0.5)
        self.play(Write(right_side))
        
        difference = MathTex(
            r"\text{差值} = (a_1 b_2 - a_2 b_1)^2 \geq 0"
        )
        difference.next_to(right_side, DOWN, buff=0.5)
        self.play(Write(difference))
        self.wait(2)
        
        self.clear()


class VectorForm(Scene):
    def construct(self):
        title = Text("向量形式", font="SimHei").to_edge(UP)
        self.play(Write(title))
        
        formula = MathTex(r"|\vec{a} \cdot \vec{b}| \leq |\vec{a}||\vec{b}|")
        self.play(Write(formula))
        self.wait(2)
        
        # 几何解释
        self.play(formula.animate.to_edge(UP, buff=1.5))
        
        explanation = Text("几何解释：两个向量的点积等于它们长度的乘积乘以夹角的余弦", font="SimHei").scale(0.7)
        explanation.next_to(formula, DOWN, buff=0.5)
        self.play(Write(explanation))
        
        formula2 = MathTex(r"\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta")
        formula2.next_to(explanation, DOWN, buff=0.5)
        self.play(Write(formula2))
        self.wait(1)
        
        implication = MathTex(r"|\cos\theta| \leq 1 \Rightarrow |\vec{a} \cdot \vec{b}| \leq |\vec{a}||\vec{b}|")
        implication.next_to(formula2, DOWN, buff=0.5)
        self.play(Write(implication))
        self.wait(1)
        
        # 几何可视化
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            background_line_style={
                "stroke_opacity": 0.6
            }
        ).scale(0.8)
        plane.next_to(implication, DOWN, buff=0.5)
        self.play(Create(plane))
        
        vector_a = Vector([2, 1], color=BLUE)
        vector_b = Vector([1, 2], color=RED)
        
        vector_a_label = MathTex(r"\vec{a}", color=BLUE).next_to(vector_a.get_end(), RIGHT)
        vector_b_label = MathTex(r"\vec{b}", color=RED).next_to(vector_b.get_end(), RIGHT)
        
        self.play(GrowArrow(vector_a), Write(vector_a_label))
        self.play(GrowArrow(vector_b), Write(vector_b_label))
        
        self.wait(2)
        self.clear()


class IntegralForm(Scene):
    def construct(self):
        title = Text("积分形式", font="SimHei").to_edge(UP)
        self.play(Write(title))
        
        formula = MathTex(
            r"\left(\int_a^b f(x)g(x)dx\right)^2 \leq \int_a^b f^2(x)dx \int_a^b g^2(x)dx"
        )
        self.play(Write(formula))
        self.wait(2)
        
        explanation = Text("这是连续情况下的柯西不等式", font="SimHei").scale(0.7)
        explanation.next_to(formula, DOWN, buff=0.5)
        self.play(Write(explanation))
        
        continuous = Text(
            "可以理解为：函数在L²空间中的内积满足柯西-施瓦茨不等式", 
            font="SimHei"
        ).scale(0.7)
        continuous.next_to(explanation, DOWN, buff=0.5)
        self.play(Write(continuous))
        
        inner_product = MathTex(
            r"\langle f, g \rangle = \int_a^b f(x)g(x)dx"
        )
        inner_product.next_to(continuous, DOWN, buff=0.5)
        self.play(Write(inner_product))
        
        norm_def = MathTex(
            r"\|f\| = \sqrt{\int_a^b f^2(x)dx}"
        )
        norm_def.next_to(inner_product, DOWN, buff=0.5)
        self.play(Write(norm_def))
        
        cauchy = MathTex(
            r"|\langle f, g \rangle| \leq \|f\| \cdot \|g\|"
        )
        cauchy.next_to(norm_def, DOWN, buff=0.5)
        self.play(Write(cauchy))
        
        self.wait(2)
        self.clear()


class ProbabilisticForm(Scene):
    def construct(self):
        title = Text("概率形式", font="SimHei").to_edge(UP)
        self.play(Write(title))
        
        formula = MathTex(
            r"(E[XY])^2 \leq E[X^2] \cdot E[Y^2]"
        )
        self.play(Write(formula))
        self.wait(2)
        
        explanation = Text(
            "对随机变量X和Y，它们协方差的平方不超过各自方差的乘积", 
            font="SimHei"
        ).scale(0.7)
        explanation.next_to(formula, DOWN, buff=0.5)
        self.play(Write(explanation))
        
        covariance = MathTex(
            r"\text{Cov}(X, Y) = E[XY] - E[X]E[Y]"
        )
        covariance.next_to(explanation, DOWN, buff=0.5)
        self.play(Write(covariance))
        
        variance = MathTex(
            r"\text{Var}(X) = E[X^2] - (E[X])^2"
        )
        variance.next_to(covariance, DOWN, buff=0.5)
        self.play(Write(variance))
        
        correlation = MathTex(
            r"\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sqrt{\text{Var}(X) \cdot \text{Var}(Y)}}"
        )
        correlation.next_to(variance, DOWN, buff=0.5)
        self.play(Write(correlation))
        
        bound = MathTex(
            r"|\rho_{X,Y}| \leq 1"
        )
        bound.next_to(correlation, DOWN, buff=0.5)
        self.play(Write(bound))
        
        self.wait(2)
        self.clear()


class ApplicationsScene(Scene):
    def construct(self):
        title = Text("柯西不等式的应用", font="SimHei").to_edge(UP)
        self.play(Write(title))
        
        applications = VGroup(
            Text("• 线性代数：最小二乘法", font="SimHei"),
            Text("• 分析学：Hölder不等式和Minkowski不等式", font="SimHei"),
            Text("• 几何学：三角形不等式", font="SimHei"),
            Text("• 优化理论：凸优化和拉格朗日乘子法", font="SimHei"),
            Text("• 信息论：信息处理不等式", font="SimHei"),
            Text("• 机器学习：核方法和支持向量机", font="SimHei")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7)
        
        applications.next_to(title, DOWN, buff=0.5)
        
        for app in applications:
            self.play(Write(app), run_time=0.5)
        
        self.wait(2)
        
        conclusion = Text(
            "柯西不等式是连接多个数学分支的基础工具", 
            font="SimHei"
        ).scale(0.8)
        conclusion.next_to(applications, DOWN, buff=0.5)
        self.play(Write(conclusion))
        
        self.wait(2)


class CauchySummary(Scene):
    def construct(self):
        title = Text("柯西不等式总结", font="SimHei").to_edge(UP)
        self.play(Write(title))
        
        summary = VGroup(
            Text("• 代数形式：求和的平方 ≤ 平方的求和", font="SimHei"),
            Text("• 向量形式：点积 ≤ 长度的积", font="SimHei"),
            Text("• 积分形式：积分的平方 ≤ 平方的积分", font="SimHei"),
            Text("• 概率形式：期望的平方 ≤ 平方的期望", font="SimHei")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.7)
        
        summary.next_to(title, DOWN, buff=0.5)
        
        for point in summary:
            self.play(Write(point), run_time=0.7)
        
        self.wait(1)
        
        essence = Text(
            "本质：不同形式下内积空间中的柯西-施瓦茨不等式", 
            font="SimHei"
        ).scale(0.8)
        essence.next_to(summary, DOWN, buff=0.5)
        self.play(Write(essence))
        
        self.wait(2)
        
        thanks = Text("谢谢观看！", font="SimHei").scale(1.2)
        thanks.to_edge(DOWN, buff=1)
        self.play(Write(thanks))
        
        self.wait(2)


# 主场景用于展示所有内容
class CauchyInequalityAnimation(Scene):
    def construct(self):
        # 介绍
        intro = CauchyInequalityIntro()
        intro.construct()
        
        # 代数形式
        algebraic = AlgebraicForm()
        algebraic.construct()
        
        # 向量形式
        vector = VectorForm()
        vector.construct()
        
        # 积分形式
        integral = IntegralForm()
        integral.construct()
        
        # 概率形式
        probabilistic = ProbabilisticForm()
        probabilistic.construct()
        
        # 应用
        applications = ApplicationsScene()
        applications.construct()
        
        # 总结
        summary = CauchySummary()
        summary.construct()


class CauchyInequalityVisual(Scene):
    def construct(self):
        # 标题简短呈现
        title = Text("柯西不等式可视化证明", font="PingFang SC").scale(1.2)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # 直接显示向量形式，不再显示代数形式
        vector = MathTex(
            r"|\vec{a} \cdot \vec{b}| \leq |\vec{a}||\vec{b}|"
        ).scale(0.9)
        
        self.play(Write(vector))
        self.wait(1)
        
        # 向量可视化部分
        self.play(vector.animate.to_edge(UP, buff=0.5))
        subtitle = Text("向量形式的几何证明", font="PingFang SC").scale(0.6)
        subtitle.next_to(vector, DOWN, buff=0.2)
        self.play(Write(subtitle))
        
        # 创建坐标平面 - 缩小一点
        plane = NumberPlane(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            background_line_style={"stroke_opacity": 0.4},
            axis_config={"include_numbers": False}
        ).scale(0.7)
        
        self.play(Create(plane))
        
        # 创建两个向量 - 调整向量b的初始位置以显示更合理的夹角
        vec_a = Vector([2, 0], color=BLUE)  # 沿x轴的向量
        vec_b = Vector([1.5, 1], color=RED)  # 45度左右的向量
        
        vec_a_label = MathTex(r"\vec{a}", color=BLUE).scale(0.7).next_to(vec_a.get_end(), RIGHT)
        vec_b_label = MathTex(r"\vec{b}", color=RED).scale(0.7).next_to(vec_b.get_end(), UP+RIGHT)
        
        self.play(GrowArrow(vec_a), Write(vec_a_label))
        self.play(GrowArrow(vec_b), Write(vec_b_label))
        
        # 点积的几何意义
        dot_product_def = MathTex(r"\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta").scale(0.6)
        dot_product_def.to_corner(UL).shift(DOWN*1.5 + RIGHT*0.5)
        self.play(Write(dot_product_def))
        
        # 显示夹角
        angle = Angle(vec_a, vec_b, radius=0.5, color=GREEN)
        angle_label = MathTex(r"\theta", color=GREEN).scale(0.6).move_to(
            angle.point_from_proportion(0.5) + 0.3 * normalize(angle.point_from_proportion(0.5))
        )
        self.play(Create(angle), Write(angle_label))
        
        # 计算向量b在向量a上的投影
        dot_product = np.dot(vec_a.get_end()[:2], vec_b.get_end()[:2])
        a_squared = np.dot(vec_a.get_end()[:2], vec_a.get_end()[:2])
        projection_scalar = dot_product / a_squared
        projection_vector = projection_scalar * np.array([vec_a.get_end()[0], vec_a.get_end()[1], 0])
        
        # 绘制投影向量
        proj_vec = Vector(projection_vector, color=YELLOW)
        proj_vec_label = MathTex(r"\text{proj}_{\vec{a}}\vec{b}", color=YELLOW).scale(0.6)
        proj_vec_label.next_to(proj_vec.get_end(), DOWN)
        
        # 绘制从向量b到投影的虚线
        projection_line = DashedLine(
            vec_b.get_end(), 
            projection_vector,
            color=YELLOW, 
            dash_length=0.1
        )
        
        # 显示投影
        self.play(GrowArrow(proj_vec))
        self.play(Write(proj_vec_label), Create(projection_line))
        
        # 投影证明 - 更紧凑的布局
        proof_step1 = Text("几何证明", font="PingFang SC").scale(0.5)
        proof_step1.next_to(dot_product_def, DOWN, buff=0.3)
        self.play(Write(proof_step1))
        
        # 投影公式
        projection_formula = MathTex(
            r"\text{proj}_{\vec{a}}\vec{b} = \frac{\vec{a} \cdot \vec{b}}{|\vec{a}|^2}\vec{a}"
        ).scale(0.5)
        projection_formula.next_to(proof_step1, DOWN, buff=0.2)
        
        self.play(Write(projection_formula))
        
        # 柯西-施瓦茨不等式的核心
        projection_length = MathTex(
            r"|\text{proj}_{\vec{a}}\vec{b}| = \frac{|\vec{a} \cdot \vec{b}|}{|\vec{a}|} \leq |\vec{b}|"
        ).scale(0.5)
        projection_length.next_to(projection_formula, DOWN, buff=0.2)
        
        self.play(Write(projection_length))
        
        # 最终公式
        final_formula = MathTex(
            r"|\vec{a} \cdot \vec{b}| \leq |\vec{a}||\vec{b}|"
        ).scale(0.6)
        final_formula.next_to(projection_length, DOWN, buff=0.3)
        
        self.play(Write(final_formula))
        
        # 几何论证：向量a与b的夹角变化
        explanation = Text("平行时取等号，垂直时取最小值", font="PingFang SC").scale(0.5)
        explanation.next_to(final_formula, DOWN, buff=0.2).shift(RIGHT*0.5)  # 右移0.5单位
        self.play(Write(explanation))
        
        # 演示不同夹角下的情况 - 使用新的角度范围
        angles = [0, PI/3, PI/2, 2*PI/3]  # 0°, 60°, 90°, 120°
        angle_names = ["0°", "60°", "90°", "120°"]
        original_end_b = vec_b.get_end()
        
        for i, angle_val in enumerate(angles):
            if i > 0:  # 跳过第一个，因为已经画好了
                # 旋转向量b
                new_end = [2 * np.cos(angle_val), 2 * np.sin(angle_val), 0]  # 使用固定长度和指定角度
                new_vec_b = Vector(new_end, color=RED)
                new_angle = Angle(vec_a, new_vec_b, radius=0.5, color=GREEN)
                new_angle_label = MathTex(r"\theta = " + angle_names[i], color=GREEN).scale(0.5)
                new_angle_label.next_to(new_angle, RIGHT, buff=0.2)
                
                # 计算新的投影
                new_dot_product = np.dot(vec_a.get_end()[:2], new_end[:2])
                new_projection_scalar = new_dot_product / a_squared
                new_projection_vector = new_projection_scalar * np.array([vec_a.get_end()[0], vec_a.get_end()[1], 0])
                
                # 创建新的投影向量
                new_proj_vec = Vector(new_projection_vector, color=YELLOW)
                new_proj_vec_label = MathTex(r"\text{proj}_{\vec{a}}\vec{b}", color=YELLOW).scale(0.6)
                new_proj_vec_label.next_to(new_proj_vec.get_end(), DOWN)
                
                # 绘制新的从向量b到投影的虚线
                new_projection_line = DashedLine(
                    new_end, 
                    new_projection_vector,
                    color=YELLOW, 
                    dash_length=0.1
                )
                
                # 更新b向量、角度和投影
                self.play(
                    ReplacementTransform(vec_b, new_vec_b),
                    ReplacementTransform(angle, new_angle),
                    ReplacementTransform(angle_label, new_angle_label),
                    ReplacementTransform(proj_vec, new_proj_vec),
                    ReplacementTransform(proj_vec_label, new_proj_vec_label),
                    ReplacementTransform(projection_line, new_projection_line)
                )
                
                # 更新引用
                vec_b = new_vec_b
                angle = new_angle
                angle_label = new_angle_label
                proj_vec = new_proj_vec
                proj_vec_label = new_proj_vec_label
                projection_line = new_projection_line
                
                # 等待一小段时间让观众观察
                self.wait(0.8)
        
        self.wait(1)
        
        # 最终强调：投影长度不超过向量长度
        key_point = Text("几何本质：投影长度永远不超过原向量长度", font="PingFang SC").scale(0.6)
        key_point.to_edge(DOWN, buff=0.5)
        self.play(Write(key_point))
        self.wait(1.5)
        self.play(FadeOut(key_point))
        
        # 在几何证明结束后，清空所有内容
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
        self.wait(0.5)
        
        # 直接开始代数证明部分
        title = Text("柯西不等式的代数证明", font="PingFang SC").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(title))
        
        # 代数形式
        algebraic_form = MathTex(
            r"\left(\sum_{i=1}^{n} a_i b_i\right)^2 \leq \left(\sum_{i=1}^{n} a_i^2\right) \left(\sum_{i=1}^{n} b_i^2\right)"
        ).scale(0.7)
        algebraic_form.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(algebraic_form))
        
        # 简化为n=2的特殊情况
        special_case = Text("以n=2的特殊情况为例", font="PingFang SC").scale(0.6)
        special_case.next_to(algebraic_form, DOWN, buff=0.3)
        self.play(Write(special_case))
        
        # n=2的代数形式
        simple_form = MathTex(
            r"(a_1 b_1 + a_2 b_2)^2 \leq (a_1^2 + a_2^2)(b_1^2 + b_2^2)"
        ).scale(0.7)
        simple_form.next_to(special_case, DOWN, buff=0.2)
        self.play(Write(simple_form))
        
        # 从向量形式理解代数形式
        connection_title = Text("从向量形式理解代数形式", font="PingFang SC").scale(0.6)
        connection_title.next_to(simple_form, DOWN, buff=0.4)
        self.play(Write(connection_title))
        
        # 左侧列：向量表示
        left_side = VGroup()
        
        vector_def = VGroup(
            MathTex(r"\vec{a} = (a_1, a_2)").scale(0.6),
            MathTex(r"\vec{b} = (b_1, b_2)").scale(0.6)
        ).arrange(DOWN, buff=0.2)
        left_side.add(vector_def)
        
        dot_product = MathTex(
            r"\vec{a} \cdot \vec{b} = a_1b_1 + a_2b_2"
        ).scale(0.6)
        left_side.add(dot_product)
        
        # 修改：分两行显示向量长度，而不是放在一个MathTex中
        vector_length_a = MathTex(r"|\vec{a}| = \sqrt{a_1^2 + a_2^2}").scale(0.6)
        vector_length_b = MathTex(r"|\vec{b}| = \sqrt{b_1^2 + b_2^2}").scale(0.6)
        vector_lengths = VGroup(vector_length_a, vector_length_b).arrange(DOWN, buff=0.1)
        left_side.add(vector_lengths)
        
        left_side.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        left_side.next_to(connection_title, DOWN, buff=0.3).to_edge(LEFT, buff=0.5)
        
        # 右侧列：转换过程
        right_side = VGroup()
        
        vector_ineq = MathTex(
            r"|\vec{a} \cdot \vec{b}| \leq |\vec{a}||\vec{b}|"
        ).scale(0.6)
        right_side.add(vector_ineq)
        
        substitution = MathTex(
            r"|a_1b_1 + a_2b_2| \leq \sqrt{a_1^2 + a_2^2} \cdot \sqrt{b_1^2 + b_2^2}"
        ).scale(0.6)
        right_side.add(substitution)
        
        squared = MathTex(
            r"(a_1b_1 + a_2b_2)^2 \leq (a_1^2 + a_2^2)(b_1^2 + b_2^2)"
        ).scale(0.6)
        right_side.add(squared)
        
        right_side.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right_side.next_to(left_side, RIGHT, buff=0.8).align_to(left_side, UP)
        
        # 显示左侧列
        for item in left_side:
            self.play(Write(item), run_time=0.7)
        
        # 显示右侧列
        for item in right_side:
            self.play(Write(item), run_time=0.7)
        
        self.wait(1)
        
        # 修改说明框的大小，并将其放置在页面底部
        explanation = Text("这表明向量形式与代数形式是完全等价的", font="PingFang SC").scale(0.6)
        
        # 先创建文本，然后基于文本的尺寸设置框的大小
        explanation_box = Rectangle(
            height=explanation.height + 0.3,  # 添加少量边距
            width=explanation.width + 0.5,    # 添加少量边距
            color=YELLOW, 
            fill_opacity=0.1
        )
        
        # 将结论框放置在页面底部
        explanation_group = VGroup(explanation_box, explanation)
        explanation_box.move_to(explanation.get_center())
        explanation_group.to_edge(DOWN, buff=0.5)
        
        self.play(
            Create(explanation_box),
            Write(explanation)
        )
        
        self.wait(2)
        
        # 清场，过渡到总结
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(0.5)
        
        # 最终总结：不同形式本质相同
        final_title = Text("柯西不等式的不同形式", font="PingFang SC").scale(0.8).to_edge(UP, buff=0.3)
        self.play(Write(final_title))
        
        # 展示不同形式 - 改为两列布局
        forms_text = [
            "代数形式:",
            "向量形式:",
            "积分形式:",
            "概率形式:"
        ]
        
        forms_math = [
            r"\left(\sum_{i=1}^{n} a_i b_i\right)^2 \leq \left(\sum_{i=1}^{n} a_i^2\right) \left(\sum_{i=1}^{n} b_i^2\right)",
            r"|\vec{a} \cdot \vec{b}| \leq |\vec{a}||\vec{b}|",
            r"\left(\int_a^b f(x)g(x)dx\right)^2 \leq \int_a^b f^2(x)dx \int_a^b g^2(x)dx",
            r"(E[XY])^2 \leq E[X^2] \cdot E[Y^2]"
        ]
        
        equal_conditions_text = [
            "取等条件：",
            "取等条件：",
            "取等条件：",
            "取等条件："
        ]
        
        equal_conditions_math = [
            r"a_i = \lambda b_i, \forall i \in \{1,2,...,n\}",
            r"\vec{a} \parallel \vec{b}",
            r"f(x) = \lambda g(x)",
            r"X = \lambda Y"
        ]
        
        # 创建左右两列
        left_forms = VGroup()
        right_forms = VGroup()
        
        # 每列包含两个形式
        for i in range(4):
            # 创建文本标题
            text = Text(forms_text[i], font="PingFang SC").scale(0.6)
            
            # 创建公式
            if i == 1:  # 向量形式（简单）
                formula = MathTex(forms_math[i]).scale(0.7)
            else:  # 其他形式
                formula = MathTex(forms_math[i]).scale(0.65)
            
            # 创建取等条件 - 分为中文文本和数学公式
            cond_text = Text(equal_conditions_text[i], font="PingFang SC").scale(0.5).set_color(GREEN)
            cond_math = MathTex(equal_conditions_math[i]).scale(0.5).set_color(GREEN)
            
            # 将文本和公式水平排列
            cond_group = VGroup(cond_text, cond_math).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            
            # 垂直排列标题、公式和取等条件
            item_group = VGroup(
                text,
                formula,
                cond_group
            ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            
            # 将形式分配到左右两列
            if i < 2:
                left_forms.add(item_group)
            else:
                right_forms.add(item_group)
        
        # 垂直排列每列中的内容
        left_forms.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        right_forms.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        
        # 水平排列两列
        both_columns = VGroup(left_forms, right_forms).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        both_columns.next_to(final_title, DOWN, buff=0.4)
        
        # 显示所有形式
        self.play(Write(both_columns), run_time=2.0)
        
        # 修改最后的蓝色框
        essence_title = Text("本质：内积空间中的柯西-施瓦茨不等式", font="PingFang SC").scale(0.65)
        general_form = MathTex(
            r"|\langle u, v \rangle|^2 \leq \langle u, u \rangle \cdot \langle v, v \rangle"
        ).scale(0.7)
        
        # 分离中文和数学公式
        final_condition_text = Text("取等条件：", font="PingFang SC").scale(0.55).set_color(GREEN)
        final_condition_math = MathTex(
            r"u = \lambda v"
        ).scale(0.55).set_color(GREEN)
        final_condition_extra = Text("（线性相关）", font="PingFang SC").scale(0.55).set_color(GREEN)
        
        # 水平排列文本和公式
        final_condition_group = VGroup(
            final_condition_text, 
            final_condition_math, 
            final_condition_extra
        ).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        
        # 垂直排列标题、一般形式和取等条件
        essence_group = VGroup(
            essence_title, 
            general_form, 
            final_condition_group
        ).arrange(DOWN, buff=0.2)
        
        # 根据内容自动调整框框大小
        essence_box = Rectangle(
            height=essence_group.height + 0.4,
            width=essence_group.width + 0.6,
            color=BLUE, 
            fill_opacity=0.1
        )
        
        # 创建组合并移动到页面底部
        essence_box_group = VGroup(essence_box, essence_group)
        essence_box.move_to(essence_group.get_center())
        essence_box_group.to_edge(DOWN, buff=0.3)
        
        self.play(
            Create(essence_box),
            Write(essence_group)
        )
        
        self.wait(3) 