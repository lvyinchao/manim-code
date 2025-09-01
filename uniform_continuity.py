from manim import *
import numpy as np

class UniformContinuityDemo(Scene):
    def construct(self):
        # 添加标题
        title = Text("函数的一致连续性", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建坐标系
        axes = Axes(
            x_range=[0, 3],
            y_range=[0, 2],
            axis_config={"color": GREY},
            x_length=10,
            y_length=6
        ).add_coordinates()

        # 添加坐标轴标签
        labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(Create(axes), Write(labels))
        self.wait(1)

        # 创建函数图像 f(x) = sin(x)
        def f(x): return np.sin(x)
        graph = axes.plot(f, color=BLUE)
        graph_label = MathTex(r"f(x)=\sin(x)").next_to(graph, UR)
        
        self.play(Create(graph), Write(graph_label))
        self.wait(1)

        # 创建两个点和它们的垂直线
        x1, x2 = 0.5, 1.2
        point1 = Dot(axes.c2p(x1, f(x1)), color=RED)
        point2 = Dot(axes.c2p(x2, f(x2)), color=RED)
        
        v_line1 = axes.get_vertical_line(axes.c2p(x1, f(x1)), color=YELLOW)
        v_line2 = axes.get_vertical_line(axes.c2p(x2, f(x2)), color=YELLOW)

        # 添加x轴上的点
        x1_dot = Dot(axes.c2p(x1, 0), color=RED)
        x2_dot = Dot(axes.c2p(x2, 0), color=RED)

        # 创建水平和垂直距离的标注
        x_brace = BraceBetweenPoints(
            axes.c2p(x1, 0),
            axes.c2p(x2, 0),
            color=GREEN,
            direction=DOWN
        )
        x_text = MathTex(r"|x_1-x_2|<\delta", color=GREEN).next_to(x_brace, DOWN)

        y_brace = BraceBetweenPoints(
            axes.c2p(x2, f(x1)),
            axes.c2p(x2, f(x2)),
            color=BLUE,
            direction=RIGHT
        )
        y_text = MathTex(r"|f(x_1)-f(x_2)|<\epsilon", color=BLUE).next_to(y_brace, RIGHT)

        # 添加两点之间的连线和距离标注
        line_between_points = DashedLine(
            axes.c2p(x1, f(x1)),
            axes.c2p(x2, f(x2)),
            color=YELLOW
        )
        
        # 计算两点之间的实际距离
        distance_text = MathTex(
            r"\sqrt{(x_1-x_2)^2 + (f(x_1)-f(x_2))^2}",
            color=YELLOW,
            font_size=24
        ).next_to(line_between_points.get_center(), UP, buff=0.2)

        # 显示点和线
        self.play(
            Create(point1),
            Create(point2),
            Create(x1_dot),
            Create(x2_dot),
            Create(v_line1),
            Create(v_line2),
            Create(line_between_points),
            Write(distance_text)
        )
        self.wait(1)

        # 显示距离标注
        self.play(
            Create(x_brace),
            Write(x_text)
        )
        self.play(
            Create(y_brace),
            Write(y_text)
        )
        self.wait(1)

        # 创建一致连续性的定义
        definition = VGroup(
            Text("一致连续性定义：", font="SimSun", font_size=24),
            MathTex(r"\forall \epsilon > 0, \exists \delta > 0, \forall x_1,x_2 \in D:"),
            MathTex(r"|x_1-x_2|<\delta \Rightarrow |f(x_1)-f(x_2)|<\epsilon")
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DL)

        self.play(Write(definition))
        self.wait(1)

        # 动画演示：移动点并保持距离关系
        def update_points(t):
            new_x1 = 0.5 + 0.8*t  # 减小移动距离
            new_x2 = 1.2 + 0.8*t - 0.9*t  # 增加收敛速度，确保最终在ε带内
            
            # 更新点的位置
            point1.move_to(axes.c2p(new_x1, f(new_x1)))
            point2.move_to(axes.c2p(new_x2, f(new_x2)))
            x1_dot.move_to(axes.c2p(new_x1, 0))
            x2_dot.move_to(axes.c2p(new_x2, 0))
            
            # 更新垂直线
            v_line1.become(axes.get_vertical_line(axes.c2p(new_x1, f(new_x1)), color=YELLOW))
            v_line2.become(axes.get_vertical_line(axes.c2p(new_x2, f(new_x2)), color=YELLOW))
            
            # 更新距离标注位置
            distance_text.next_to(line_between_points.get_center(), UP, buff=0.2)
            
            # 更新距离标注
            x_brace.become(BraceBetweenPoints(
                axes.c2p(new_x1, 0),
                axes.c2p(new_x2, 0),
                color=GREEN,
                direction=DOWN
            ))
            y_brace.become(BraceBetweenPoints(
                axes.c2p(new_x2, f(new_x1)),
                axes.c2p(new_x2, f(new_x2)),
                color=BLUE,
                direction=RIGHT
            ))

        # 创建动画
        self.play(
            UpdateFromAlphaFunc(
                VGroup(
                    point1, point2, x1_dot, x2_dot, 
                    v_line1, v_line2, x_brace, y_brace,
                    line_between_points, distance_text
                ),
                lambda mob, alpha: update_points(1.5 * alpha)
            ),
            run_time=3,
            rate_func=there_and_back
        )
        self.wait(2)

class UniformContinuityComparison(Scene):
    def construct(self):
        # 添加标题
        title = Text("一致连续与非一致连续函数对比", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建两个子坐标系
        left_axes = Axes(
            x_range=[0, 3],
            y_range=[0, 2],
            axis_config={"color": GREY},
            x_length=5,
            y_length=4
        ).shift(LEFT * 3.5)

        right_axes = Axes(
            x_range=[0.2, 3],
            y_range=[0, 5],
            axis_config={"color": GREY},
            x_length=5,
            y_length=4
        ).shift(RIGHT * 3.5)

        # 添加坐标轴标签
        left_labels = left_axes.get_axis_labels(x_label="x", y_label="y")
        right_labels = right_axes.get_axis_labels(x_label="x", y_label="y")
        
        self.play(
            Create(left_axes), Write(left_labels),
            Create(right_axes), Write(right_labels)
        )
        self.wait(1)

        # 创建函数图像
        def f1(x): return np.sin(x)  # 一致连续函数
        def f2(x): return 1/x        # 非一致连续函数

        graph1 = left_axes.plot(f1, color=BLUE)
        graph2 = right_axes.plot(f2, color=RED, x_range=[0.2, 3])

        graph1_label = MathTex(r"f(x)=\sin(x)", color=BLUE).next_to(left_axes, UP)
        graph2_label = MathTex(r"g(x)=\frac{1}{x}", color=RED).next_to(right_axes, UP)
        
        self.play(
            Create(graph1), Write(graph1_label),
            Create(graph2), Write(graph2_label)
        )
        self.wait(1)

        # 在左图（sin函数）上创建两个点和垂直线
        x1, x2 = 0.5, 1.2
        left_point1 = Dot(left_axes.c2p(x1, f1(x1)), color=BLUE)
        left_point2 = Dot(left_axes.c2p(x2, f1(x2)), color=BLUE)
        
        # 添加垂直辅助线
        left_v_line1 = left_axes.get_vertical_line(left_axes.c2p(x1, f1(x1)), color=YELLOW)
        left_v_line2 = left_axes.get_vertical_line(left_axes.c2p(x2, f1(x2)), color=YELLOW)

        # 修改左图的标注
        left_delta = BraceBetweenPoints(
            left_axes.c2p(x1, 0),
            left_axes.c2p(x2, 0),
            color=GREEN,
            direction=DOWN
        )
        left_delta_text = MathTex(r"\delta", color=GREEN).next_to(left_delta, DOWN)

        # 修改垂直距离标注，使用函数值差异
        left_v_brace = BraceBetweenPoints(
            left_axes.c2p(x2, f1(x1)),
            left_axes.c2p(x2, f1(x2)),
            color=BLUE,
            direction=RIGHT
        )
        left_v_text = MathTex(r"f(x_1)-f(x_2)", color=BLUE, font_size=24).next_to(
            left_v_brace, RIGHT, buff=0.1
        )

        # 在右图（1/x函数）上创建两个点和垂直线
        x3, x4 = 0.5, 0.8
        right_point1 = Dot(right_axes.c2p(x3, f2(x3)), color=RED)
        right_point2 = Dot(right_axes.c2p(x4, f2(x4)), color=RED)
        
        # 添加垂直辅助线
        right_v_line1 = right_axes.get_vertical_line(right_axes.c2p(x3, f2(x3)), color=YELLOW)
        right_v_line2 = right_axes.get_vertical_line(right_axes.c2p(x4, f2(x4)), color=YELLOW)

        # 修改右图的标注
        right_delta = BraceBetweenPoints(
            right_axes.c2p(x3, 0),
            right_axes.c2p(x4, 0),
            color=GREEN,
            direction=DOWN
        )
        right_delta_text = MathTex(r"\delta", color=GREEN).next_to(right_delta, DOWN)

        # 修改垂直距离标注，使用函数值差异
        right_v_brace = BraceBetweenPoints(
            right_axes.c2p(x4, f2(x3)),
            right_axes.c2p(x4, f2(x4)),
            color=BLUE,
            direction=RIGHT
        )
        right_v_text = MathTex(r"g(x_1)-g(x_2)", color=BLUE, font_size=24).next_to(
            right_v_brace, RIGHT, buff=0.1
        )

        # 显示点、线和标注
        self.play(
            Create(VGroup(
                left_point1, left_point2, 
                left_v_line1, left_v_line2
            )),
            Create(VGroup(
                right_point1, right_point2,
                right_v_line1, right_v_line2
            ))
        )
        self.play(
            Create(left_delta), Write(left_delta_text),
            Create(left_v_brace), Write(left_v_text),
            Create(right_delta), Write(right_delta_text),
            Create(right_v_brace), Write(right_v_text)
        )
        self.wait(1)

        # 添加固定的ε水平线（左图）
        epsilon_value = 0.2  # 设置一个固定的ε值
        left_epsilon_line1 = DashedLine(
            left_axes.c2p(0, 0.8),  # 降低水平线的位置
            left_axes.c2p(3, 0.8),
            color=BLUE_A
        )
        left_epsilon_line2 = DashedLine(
            left_axes.c2p(0, 0.8 + epsilon_value),
            left_axes.c2p(3, 0.8 + epsilon_value),
            color=BLUE_A
        )
        left_epsilon_brace = BraceBetweenPoints(
            left_axes.c2p(2.8, 0.8),
            left_axes.c2p(2.8, 0.8 + epsilon_value),
            color=BLUE_A,
            direction=RIGHT
        )
        left_epsilon_text = MathTex(r"\epsilon", color=BLUE_A).next_to(left_epsilon_brace, RIGHT)

        # 添加固定的ε水平线（右图）
        right_epsilon_line1 = DashedLine(
            right_axes.c2p(0.2, 1.5),  # 调整右图水平线位置
            right_axes.c2p(3, 1.5),
            color=BLUE_A
        )
        right_epsilon_line2 = DashedLine(
            right_axes.c2p(0.2, 1.5 + epsilon_value),
            right_axes.c2p(3, 1.5 + epsilon_value),
            color=BLUE_A
        )
        right_epsilon_brace = BraceBetweenPoints(
            right_axes.c2p(2.8, 1.5),
            right_axes.c2p(2.8, 1.5 + epsilon_value),
            color=BLUE_A,
            direction=RIGHT
        )
        right_epsilon_text = MathTex(r"\epsilon", color=BLUE_A).next_to(right_epsilon_brace, RIGHT)

        # 显示ε线和标注
        self.play(
            Create(left_epsilon_line1), Create(left_epsilon_line2),
            Create(left_epsilon_brace), Write(left_epsilon_text),
            Create(right_epsilon_line1), Create(right_epsilon_line2),
            Create(right_epsilon_brace), Write(right_epsilon_text)
        )
        self.wait(1)

        # 修改动画更新函数
        def update_points(t):
            # 更新左侧点（sin函数）- 让两点最终重合
            new_x1 = 0.5 + 0.8*t  # 第一个点向右移动
            new_x2 = new_x1 + 0.7*(1-t)  # 第二个点逐渐靠近第一个点，最后重合

            left_point1.move_to(left_axes.c2p(new_x1, f1(new_x1)))
            left_point2.move_to(left_axes.c2p(new_x2, f1(new_x2)))
            
            # 更新左侧垂直线和δ标注
            left_v_line1.become(left_axes.get_vertical_line(left_axes.c2p(new_x1, f1(new_x1)), color=YELLOW))
            left_v_line2.become(left_axes.get_vertical_line(left_axes.c2p(new_x2, f1(new_x2)), color=YELLOW))
            
            left_delta.become(BraceBetweenPoints(
                left_axes.c2p(new_x1, 0),
                left_axes.c2p(new_x2, 0),
                color=GREEN,
                direction=DOWN
            ))
            left_delta_text.next_to(left_delta, DOWN)

            # 更新左侧垂直花括号和标注
            left_v_brace.become(BraceBetweenPoints(
                left_axes.c2p(new_x2, f1(new_x1)),
                left_axes.c2p(new_x2, f1(new_x2)),
                color=BLUE,
                direction=RIGHT
            ))
            left_v_text.next_to(left_v_brace, RIGHT, buff=0.1)

            # 更新右侧点（1/x函数）
            new_x3 = 0.5 - 0.25*t  # 第一个点向左移动
            new_x4 = 0.8 - 0.45*t  # 第二个点移动更快，使得两点逐渐靠近

            # 确保x值不会太接近0
            new_x3 = max(0.2, new_x3)
            new_x4 = max(0.25, new_x4)
            
            right_point1.move_to(right_axes.c2p(new_x3, f2(new_x3)))
            right_point2.move_to(right_axes.c2p(new_x4, f2(new_x4)))
            
            # 更新右侧垂直线
            right_v_line1.become(right_axes.get_vertical_line(right_axes.c2p(new_x3, f2(new_x3)), color=YELLOW))
            right_v_line2.become(right_axes.get_vertical_line(right_axes.c2p(new_x4, f2(new_x4)), color=YELLOW))
            
            # 更新右侧δ标注
            right_delta.become(BraceBetweenPoints(
                right_axes.c2p(new_x3, 0),
                right_axes.c2p(new_x4, 0),
                color=GREEN,
                direction=DOWN
            ))
            right_delta_text.next_to(right_delta, DOWN)

            # 更新右侧垂直花括号和函数值差标注
            right_v_brace.become(BraceBetweenPoints(
                right_axes.c2p(new_x4, f2(new_x3)),
                right_axes.c2p(new_x4, f2(new_x4)),
                color=BLUE,
                direction=RIGHT
            ))
            right_v_text.next_to(right_v_brace, RIGHT, buff=0.1)
            
            # 更新右侧水平虚线位置
            min_y = min(f2(new_x3), f2(new_x4))  # 获取较小的y值
            right_epsilon_line1.become(DashedLine(
                right_axes.c2p(0.2, min_y),
                right_axes.c2p(3, min_y),
                color=BLUE_A
            ))
            right_epsilon_line2.become(DashedLine(
                right_axes.c2p(0.2, min_y + epsilon_value),
                right_axes.c2p(3, min_y + epsilon_value),
                color=BLUE_A
            ))
            right_epsilon_brace.become(BraceBetweenPoints(
                right_axes.c2p(2.8, min_y),
                right_axes.c2p(2.8, min_y + epsilon_value),
                color=BLUE_A,
                direction=RIGHT
            ))
            right_epsilon_text.next_to(right_epsilon_brace, RIGHT)

        # 修改动画组，添加右侧水平虚线到更新组
        self.play(
            UpdateFromAlphaFunc(
                VGroup(
                    left_point1, left_point2,
                    left_v_line1, left_v_line2,
                    left_delta, left_delta_text,
                    left_v_brace, left_v_text,
                    right_point1, right_point2,
                    right_v_line1, right_v_line2,
                    right_delta, right_delta_text,
                    right_v_brace, right_v_text,
                    right_epsilon_line1, right_epsilon_line2,  # 添加右侧水平虚线
                    right_epsilon_brace, right_epsilon_text    # 添加右侧epsilon标注
                ),
                lambda mob, alpha: update_points(alpha)
            ),
            run_time=4,
            rate_func=linear
        )

        # 修改结论文字和位置
        conclusion = Text(
            "一致连续函数中，对于任意给定的ε，总能找到足够小的δ，\n" + 
            "使得任意两点距离小于δ时，函数值之差小于ε；而非一致连续函数在某些区域无法做到这一点。",
            font="SimSun",
            font_size=18,  # 减小字体
            line_spacing=1.2
        ).next_to(
            VGroup(left_axes, right_axes),  # 相对于两个坐标系
            DOWN,  # 在坐标系下方
            buff=1.0  # 增加与坐标系的距离
        )
        
        self.play(Write(conclusion))
        self.wait(2) 