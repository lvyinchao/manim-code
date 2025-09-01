from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class GradientConcept(ThreeDScene):
    def create_derivative_value_tracker(self):
        """创建方向导数值的显示区域"""
        tracker = VGroup()
        # 将显示区域放在右侧
        tracker.arrange(DOWN, buff=0.1)
        tracker.to_edge(RIGHT, buff=0.5)
        return tracker

    def construct(self):
        # 创建标题
        title = Text(
            "方向导数与梯度",
            font="STSong",
            font_size=48
        )
        
        # 显示标题
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(2)
        
        # 淡出标题
        self.play(FadeOut(title))
        
        # 创建3D坐标系
        self.axes = ThreeDAxes(
            x_range=[-1, 1, 0.5],
            y_range=[-1, 1, 0.5],
            z_range=[0, 2, 0.5],
            x_length=4,  # 缩小坐标轴长度
            y_length=4,
            z_length=3,
            axis_config={"color": GREY, "include_ticks": False}
        )
        
        # 创建函数曲面 z = -x² - y² + 2
        surface = Surface(
            lambda u, v: self.axes.c2p(u, v, -u**2 - v**2 + 2),  # 降低最高点
            u_range=[-1, 1],
            v_range=[-1, 1],
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.6
        )
        
        # 设置初始视角
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        self.add(self.axes, surface)
        
        # 选择基准点 P(0.5,0.5,0)
        P = [0.5, 0.5, 0]
        P_surface = [0.5, 0.5, 1.5]  # z = -0.5² - 0.5² + 2 = 1.5
        point_P = Dot3D(self.axes.c2p(*P), color=RED, radius=0.05)  # 缩小点的大小
        point_P_surface = Dot3D(self.axes.c2p(*P_surface), color=RED)
        
        # 显示基准点
        self.play(
            Create(point_P),
            Create(point_P_surface),
            Create(Line(
                self.axes.c2p(*P),
                self.axes.c2p(*P_surface),
                color=YELLOW
            ))
        )
        
        # 创建多个方向的切线
        angles = np.linspace(0, 2*np.pi, 8)  # 8个不同方向
        directions = []
        tangent_lines = []
        direction_vectors = []  # 存储底面上的方向向量
        
        for angle in angles:
            # 计算方向向量
            direction = [np.cos(angle), np.sin(angle), 0]
            directions.append(direction)
            
            # 计算方向导数
            directional_derivative = -2*P[0]*direction[0] - 2*P[1]*direction[1]
            
            # 创建切线和方向向量
            tangent = self.create_tangent_line(
                P_surface,
                direction,
                directional_derivative,
                length=2
            )
            direction_vector = Arrow3D(
                start=self.axes.c2p(*P),
                end=self.axes.c2p(*(np.array(P) + 0.3*np.array(direction))),  # 缩放方向向量长度
                color=RED,
                thickness=0.03  # 稍细一些
            )
            tangent_lines.append(tangent)
            direction_vectors.append(direction_vector)
        
        # 逐个显示不同方向的切线和方向向量
        for tangent, vector in zip(tangent_lines, direction_vectors):
            self.play(
                Create(tangent),
                Create(vector),
                run_time=1
            )
            self.wait(0.5)
        
        # 创建说明文字
        explanation = Text(
            "不同方向的切线斜率表示\n沿不同方向的方向导数值",
            font="STSong",
            line_spacing=1.5
        ).scale(0.5)
        explanation.to_edge(RIGHT, buff=0.5).to_edge(UP, buff=1)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(1)
        
        # 创建方向导数计算公式
        formula = MathTex(
            "\\frac{\\partial f}{\\partial l} = ",
            "\\frac{\\partial f}{\\partial x}\\cos\\theta + ",
            "\\frac{\\partial f}{\\partial y}\\sin\\theta"
        ).scale(0.6)
        formula.to_edge(RIGHT, buff=0.5).shift(UP)
        self.add_fixed_in_frame_mobjects(formula)
        self.play(Write(formula))
        self.wait(1)
        
        # 计算梯度向量
        gradient = [2*P[0], 2*P[1], 0]
        gradient_arrow = Arrow3D(
            start=self.axes.c2p(*P),
            end=self.axes.c2p(*(np.array(P) + 0.5*np.array(gradient))),
            color=YELLOW,
            thickness=0.05
        )
        
        # 突出显示最大方向导数（梯度方向）
        self.play(
            Create(gradient_arrow),
            *[tangent.animate.set_opacity(0.3) for tangent in tangent_lines],
            *[vector.animate.set_opacity(0.3) for vector in direction_vectors],
            run_time=2
        )
        
        # 添加梯度标签
        gradient_label = MathTex("\\text{grad }f").next_to(gradient_arrow, RIGHT)
        self.play(Write(gradient_label))
        
        # 显示结论
        conclusion = VGroup(
            Text(
                "方向导数最大的方向是梯度的方向",
                font="STSong",
                font_size=24
            ),
            Text(
                "方向导数的最大值是梯度的模",
                font="STSong",
                font_size=24
            )
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(2)
        
    def create_tangent_line(self, point, direction, derivative, length=2):
        """创建切线"""
        direction = np.array(direction)
        direction = direction / np.linalg.norm(direction)
        
        # 计算曲面上的切向量
        # 对于f(x,y)=-x²-y²+2, 在点(x₀,y₀)处
        x0, y0 = point[0], point[1]
        dx = -2*x0  # ∂f/∂x = -2x
        dy = -2*y0  # ∂f/∂y = -2y
        
        # 计算方向导数
        dir_derivative = dx*direction[0] + dy*direction[1]
        
        # 构造切向量 (注意z分量是方向导数)
        tangent = np.array([
            direction[0],
            direction[1],
            dir_derivative
        ])
        # 归一化切向量
        tangent = tangent / np.linalg.norm(tangent)
        
        # 创建射线（只向一个方向延伸）
        end = np.array(point) + length * tangent
        
        return Line(
            self.axes.c2p(*point),  # 从曲面上的点开始
            self.axes.c2p(*end),
            color=RED,
            stroke_width=3
        )

    def color_from_direction(self, direction, gradient):
        """根据方向与梯度的夹角确定颜色"""
        cos_theta = np.dot(direction[:2], gradient[:2]) / (
            np.linalg.norm(direction[:2])*np.linalg.norm(gradient[:2]))
        return interpolate_color(BLUE, RED, (cos_theta + 1)/2) 