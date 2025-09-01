from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class NestedIntervals(Scene):
    def construct(self):
        # 设置标题
        title = Text("闭区间套定理", font="STSong", font_size=48)
        subtitle = Text("任意一列闭区间套必有唯一公共点", font="STSong", font_size=32)
        subtitle.next_to(title, DOWN)
        
        # 显示标题
        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(1)
        self.play(
            FadeOut(title),
            FadeOut(subtitle)
        )

        # 创建数轴
        number_line = NumberLine(
            x_range=[-2, 2, 1],
            length=12,
            include_numbers=True,
            include_tip=True
        )
        self.play(Create(number_line))
        
        # 定义初始区间
        intervals = []
        left = -1.5
        right = 1.5
        
        # 创建5个嵌套区间
        for i in range(5):
            # 创建区间
            interval = Line(
                start=number_line.n2p(left),
                end=number_line.n2p(right),
                color=BLUE,
                stroke_width=8 - i
            )
            
            # 添加端点
            left_dot = Dot(number_line.n2p(left), color=YELLOW)
            right_dot = Dot(number_line.n2p(right), color=YELLOW)
            
            # 创建区间标签
            label = MathTex(f"[{left:.2f}, {right:.2f}]")
            label.next_to(interval, UP, buff=0.5 + i*0.5)
            
            intervals.append(VGroup(interval, left_dot, right_dot, label))
            
            # 缩小区间
            new_length = (right - left) / 3
            left = left + new_length
            right = right - new_length

        # 逐个显示区间
        for i, interval in enumerate(intervals):
            self.play(Create(interval))
            self.wait(0.5)

        # 添加说明文字
        explanation = VGroup(
            Text("1. 每个区间都是闭区间", font="STSong"),
            Text("2. 后一个区间包含于前一个区间", font="STSong"),
            Text("3. 区间长度趋近于0", font="STSong"),
            Text("4. 存在唯一公共点", font="STSong")
        ).arrange(DOWN, aligned_edge=LEFT)
        explanation.scale(0.6)
        explanation.to_edge(RIGHT)

        # 显示说明文字
        for text in explanation:
            self.play(Write(text))
            self.wait(0.5)

        # 标记公共点
        common_point = Dot(number_line.n2p(0), color=RED)
        common_point_label = MathTex("p").next_to(common_point, DOWN)
        
        self.play(
            Create(common_point),
            Write(common_point_label)
        )
        
        # 添加最终结论
        conclusion = Text(
            "这个点p是所有区间的公共点，\n且随着区间套的继续，\n区间会无限缩小到这一点。",
            font="STSong"
        ).scale(0.6)
        conclusion.to_edge(LEFT)
        
        self.play(Write(conclusion))
        self.wait(2)

def main():
    import os
    os.system("manim -pql nested_intervals.py NestedIntervals")

if __name__ == "__main__":
    main() 