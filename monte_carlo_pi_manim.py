from manim import *
import numpy as np

class MonteCarloPI(Scene):
    def construct(self):
        # 配置参数
        num_points = 500
        radius = 2
        point_radius = 0.02
        
        # 创建坐标系
        axes = Axes(
            x_range=[0, radius, 1],
            y_range=[0, radius, 1],
            x_length=4,
            y_length=4,
            axis_config={
                "include_tip": False,
                "include_numbers": False  # 不使用LaTeX数字
            }
        )
        
        # 添加坐标轴标签
        x_labels = VGroup(*[
            Text(str(i), font_size=20).next_to(
                axes.c2p(i, 0), DOWN
            ) for i in range(radius + 1)
        ])
        
        y_labels = VGroup(*[
            Text(str(i), font_size=20).next_to(
                axes.c2p(0, i), LEFT
            ) for i in range(radius + 1)
        ])
        
        # 创建1/4圆
        arc = Arc(
            radius=radius,
            angle=PI/2,
            color=BLUE,
            stroke_width=2
        )
        
        # 创建正方形
        square = Square(
            side_length=radius*2,
            color=WHITE,
            stroke_width=2
        ).align_to(ORIGIN, DL)
        
        # 创建标题
        title = Text("蒙特卡洛方法估算π", font="SimSun").scale(0.8).to_edge(UP)
        
        # 创建计数器
        points_counter = Text("点数: 0", font="SimSun").to_edge(UR)
        pi_value = Text("π ≈ 0.0000", font="SimSun").next_to(points_counter, DOWN)
        
        # 设置场景
        self.play(
            Write(title),
            Create(axes),
            Write(x_labels),
            Write(y_labels),
            Create(square),
            Create(arc),
            Write(points_counter),
            Write(pi_value)
        )
        
        # 点的存储
        points_inside = []
        points_outside = []
        
        # 添加点的动画
        for i in range(num_points):
            x = np.random.uniform(0, radius)
            y = np.random.uniform(0, radius)
            
            point = axes.c2p(x, y)  # 转换坐标
            dot = Dot(point, radius=point_radius)
            
            if x*x + y*y <= radius*radius:
                dot.set_color(GREEN)
                points_inside.append(dot)
            else:
                dot.set_color(RED)
                points_outside.append(dot)
            
            # 更新计数和π估计值
            total_points = len(points_inside) + len(points_outside)
            pi_estimate = 4 * len(points_inside) / total_points
            
            # 每10个点更新一次动画
            if i % 10 == 0:
                new_counter = Text(f"点数: {total_points}", font="SimSun").to_edge(UR)
                new_pi = Text(f"π ≈ {pi_estimate:.4f}", font="SimSun").next_to(new_counter, DOWN)
                
                self.play(
                    Create(dot),
                    Transform(points_counter, new_counter),
                    Transform(pi_value, new_pi),
                    run_time=0.1
                )
            else:
                self.add(dot)
        
        # 最终结果
        final_text = Text(
            f"最终估计值: {pi_estimate:.4f}\n实际π值: {np.pi:.4f}",
            font="SimSun"
        ).scale(0.6).to_edge(DOWN)
        
        self.play(Write(final_text))
        self.wait(2)

if __name__ == "__main__":
    # 使用命令行运行：manim -pql monte_carlo_pi_manim.py MonteCarloPI
    pass 