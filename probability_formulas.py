# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class TotalProbabilityFormula(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("全概率公式").scale(0.8)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))
        self.wait(1)

        # 创建全概率公式
        total_prob = VGroup(
            MathTex(r"P(A) = \sum_{i=1}^n P(B_i)P(A|B_i)", color=BLUE),
            Text("全概率公式", font="SimSun", color=BLUE).scale(0.6)
        ).arrange(DOWN, buff=0.3)
        total_prob.shift(UP * 2)

        # 显示公式
        self.play(Write(total_prob))
        self.wait(1)

        # 创建样本空间的矩形
        rect = Rectangle(width=6, height=4, color=WHITE)
        rect.shift(DOWN * 0.5)
        
        # 创建水平分割线
        lines = VGroup()
        n_divisions = 3
        for i in range(1, n_divisions):
            line = Line(
                rect.get_left() + RIGHT * i * rect.width/n_divisions,
                rect.get_right() + LEFT * (n_divisions-i) * rect.width/n_divisions,
                color=GREEN
            )
            lines.add(line)
        
        # B_i的标签
        b_labels = VGroup()
        for i in range(n_divisions):
            label = MathTex(f"B_{i+1}", color=GREEN).scale(0.8)
            label.move_to(rect.get_left() + RIGHT * (i + 0.5) * rect.width/n_divisions)
            b_labels.add(label)

        # 显示样本空间和分割
        self.play(Create(rect))
        self.play(Create(lines), Write(b_labels))
        
        # 添加说明文字
        explanation1 = Text(
            "{B₁, B₂, B₃}构成完备事件组",
            font="SimSun"
        ).scale(0.6)
        explanation1.next_to(rect, UP, buff=0.3)
        
        explanation2 = VGroup(
            Text("• B₁∪B₂∪B₃ = Ω（互斥完备）", font="SimSun"),
            Text("• P(B₁) + P(B₂) + P(B₃) = 1", font="SimSun")
        ).arrange(DOWN, aligned_edge=LEFT).scale(0.5)
        explanation2.next_to(rect, DOWN, buff=0.3)
        
        self.play(Write(explanation1))
        self.play(Write(explanation2))
        self.wait(1)

        # 显示事件A的区域（用不同颜色表示在不同B_i中的部分）
        a_parts = VGroup()
        colors = [RED_A, RED_B, RED_C]
        for i in range(n_divisions):
            part = Rectangle(
                width=rect.width/n_divisions * 0.6,
                height=rect.height * 0.4,
                color=colors[i],
                fill_opacity=0.3
            )
            part.move_to(rect.get_left() + RIGHT * (i + 0.5) * rect.width/n_divisions)
            a_parts.add(part)
            
            # 添加P(A|B_i)的标签
            label = MathTex(f"P(A|B_{i+1})", color=colors[i]).scale(0.6)
            label.next_to(part, UP, buff=0.2)
            a_parts.add(label)

        self.play(Create(a_parts))
        
        # 添加最终解释
        final_explanation = Text(
            "事件A在不同B_i中的条件概率P(A|B_i)与P(B_i)的加权和即为P(A)",
            font="SimSun"
        ).scale(0.5)
        final_explanation.to_edge(DOWN, buff=0.5)
        
        self.play(Write(final_explanation))
        self.wait(2) 