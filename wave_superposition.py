# -*- coding: utf-8 -*-
from manim import *
import numpy as np

class WaveSuperposition(Scene):
    def construct(self):
        # 设置默认字体
        Text.set_default(font="SimSun")
        
        # 标题
        title = Text("波形叠加演示").scale(0.8)
        title.to_edge(UP, buff=0.3)
        title.shift(RIGHT * 2)  # 将标题向右移动
        self.play(Write(title))
        self.wait(1)

        # 创建三个坐标系，垂直排列
        axes_list = []
        for i in range(3):
            axes = Axes(
                x_range=[-4, 4, 1],  # 扩大范围以适应更大振幅
                y_range=[-4, 4, 1],
                axis_config={"include_tip": False},
                x_length=10,
                y_length=3
            ).scale(0.8)
            axes.shift(LEFT * 2 + (i-1) * DOWN * 2.5)  # 垂直排列
            axes_list.append(axes)
            self.play(Create(axes))

        # 定义波形函数
        def wave(x, amp=1, freq=1, phase=0):
            return amp * np.sin(freq*x + phase)

        # 情况一：同频率不同振幅波形叠加（振幅比3:1）
        wave1_1 = axes_list[0].plot(lambda x: wave(x, amp=3), color=BLUE)  # 振幅3
        wave1_2 = axes_list[0].plot(lambda x: wave(x, amp=1), color=RED)   # 振幅1
        result1 = axes_list[0].plot(
            lambda x: wave(x, amp=3) + wave(x, amp=1), 
            color=GREEN
        )
        
        label1 = Text("同频率不同振幅波形叠加", font="SimSun").scale(0.4)
        label1.next_to(axes_list[0], RIGHT)

        # 情况二：不同振幅反相叠加（振幅比2.5:0.5）
        wave2_1 = axes_list[1].plot(lambda x: wave(x, amp=2.5), color=BLUE)  # 振幅2.5
        wave2_2 = axes_list[1].plot(lambda x: wave(x, amp=0.5, phase=np.pi), color=RED)  # 振幅0.5
        result2 = axes_list[1].plot(
            lambda x: wave(x, amp=2.5) - wave(x, amp=0.5), 
            color=GREEN
        )
        
        label2 = Text("不同振幅反相叠加", font="SimSun").scale(0.4)
        label2.next_to(axes_list[1], RIGHT)

        # 情况三：不同振幅任意相位叠加（振幅比2:0.8）
        wave3_1 = axes_list[2].plot(lambda x: wave(x, amp=2), color=BLUE)  # 振幅2
        wave3_2 = axes_list[2].plot(lambda x: wave(x, amp=0.8, phase=np.pi/3), color=RED)  # 振幅0.8
        result3 = axes_list[2].plot(
            lambda x: wave(x, amp=2) + wave(x, amp=0.8, phase=np.pi/3), 
            color=GREEN
        )
        
        label3 = Text("不同振幅任意相位叠加", font="SimSun").scale(0.4)
        label3.next_to(axes_list[2], RIGHT)

        # 添加波形标签
        for i, (w1, w2, r, label, amps) in enumerate([
            (wave1_1, wave1_2, result1, label1, (3, 1)),
            (wave2_1, wave2_2, result2, label2, (2.5, 0.5)),
            (wave3_1, wave3_2, result3, label3, (2, 0.8))
        ]):
            # 添加图例
            legend1 = Text(f"波形1 (A={amps[0]})", font="SimSun", color=BLUE).scale(0.3)
            legend2 = Text(f"波形2 (A={amps[1]})", font="SimSun", color=RED).scale(0.3)
            legend3 = Text("叠加结果", font="SimSun", color=GREEN).scale(0.3)
            
            legends = VGroup(legend1, legend2, legend3).arrange(DOWN, aligned_edge=LEFT)
            legends.next_to(label, DOWN, buff=0.3)
            
            # 显示动画
            self.play(
                Create(w1),
                Create(w2),
                Write(label),
                Write(legends)
            )
            self.wait(0.5)
            self.play(Create(r))
            self.wait(1)

        self.wait(2) 