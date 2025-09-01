from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class DirectionalDerivative(ThreeDScene):
    def create_vertical_plane(self, direction_vector, base_point):
        """创建过方向向量且垂直于底面的平面"""
        u_vec = np.array(direction_vector) / np.linalg.norm(direction_vector)
        base = np.array(base_point)
        
        return Surface(
            lambda u, v: [
                base[0] + u * u_vec[0],
                base[1] + u * u_vec[1],
                base[2] + v
            ],
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(1, 1),
            color=RED,
            fill_opacity=0.3,
            stroke_opacity=0
        )

    def create_secant(self, p1, p2):
        """创建曲面上的割线"""
        t_values = np.linspace(-3, 3, 400)
        points = []
        for t in t_values:
            x = p1[0] + t*(p2[0]-p1[0])
            y = p1[1] + t*(p2[1]-p1[1])
            if abs(x) > 3 or abs(y) > 3:
                continue
            z = x**2 + y**2
            points.append(self.axes.c2p(x, y, z))
        return VMobject().set_points_smoothly(points).set_style(
            stroke_color=YELLOW,
            stroke_width=8,
            stroke_opacity=1
        )

    def create_tangent_line(self, point, direction, length=6):
        """创建直线切线"""
        direction = np.array(direction) / np.linalg.norm(direction)
        p = np.array(point)
        
        z_change = 2 * (p[0]*direction[0] + p[1]*direction[1])
        tangent = np.array([direction[0], direction[1], z_change])
        tangent = tangent / np.linalg.norm(tangent)
        
        start = p - length * tangent
        end = p + length * tangent
        
        return Line(
            self.axes.c2p(*start),
            self.axes.c2p(*end),
            color=WHITE,
            stroke_width=6
        )

    def construct(self):
        # 创建3D坐标系
        self.axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 8, 2],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={"color": GREY, "include_ticks": False}
        ).add_coordinates()

        # 创建标题
        title = Text("方向导数的几何意义", font="STSong")
        title.scale(0.6).to_corner(UP+LEFT)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)

        # 创建函数曲面
        surface = Surface(
            lambda u, v: self.axes.c2p(u, v, u**2 + v**2),
            u_range=[-2, 2], v_range=[-2, 2],
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.8
        )

        # 设置固定视角
        self.set_camera_orientation(phi=60*DEGREES, theta=-40*DEGREES)
        self.stop_ambient_camera_rotation()

        # 显示坐标系和曲面
        self.play(Create(self.axes), Create(surface))
        self.wait(1)

        # 创建底面上的点P(1,1)
        P = (1, 1, 0)
        P_surface = (1, 1, 2)
        point_P = Dot3D(self.axes.c2p(*P), color=RED)
        point_P_surface = Dot3D(self.axes.c2p(*P_surface), color=RED)
        vertical_line = Line(self.axes.c2p(*P), self.axes.c2p(*P_surface), color=YELLOW)

        # 创建曲面方程和基准点标记
        surface_equation = MathTex(
            "z = f(x,y)",
            color=WHITE
        ).to_corner(UP+RIGHT)
        self.add_fixed_in_frame_mobjects(surface_equation)
        self.play(Write(surface_equation))

        # 创建基准点标记
        P0_label = MathTex(
            "P_0(x_0,y_0)",
            color=RED
        ).scale(0.6).next_to(
            self.axes.c2p(*P),  # 使用三维坐标定位
            UR,  # 改为右上方向
            buff=0.2
        ).shift(LEFT*0.3 + DOWN*2)  # 微调位置
        self.add_fixed_in_frame_mobjects(P0_label)

        # 显示基准点和标记
        self.play(Create(point_P))
        self.wait(0.5)

        # 创建方向向量
        angle = 30*DEGREES
        u_vec = [np.cos(angle), np.sin(angle), 0]
        vector_scale = 0.8
        direction_arrow = Arrow3D(
            start=self.axes.c2p(*P),
            end=self.axes.c2p(*(np.array(P) + vector_scale * np.array(u_vec))),
            color=GREEN
        )

        # 显示方向向量
        self.play(Create(direction_arrow))
        self.wait(0.1)  # 确保箭头已渲染

        # 修改方向向量标记的位置
        # 将标签直接附加在箭头末端
        direction_label = MathTex(
            "\\vec{l}",
            color=GREEN
        ).scale(0.7).next_to(
            direction_arrow.get_end(),  # 使用箭头末端坐标
            UR,  # 右上方向
            buff=0.1
        ).shift(LEFT*0.2 + DOWN*2)  # 微调位置

        # 确保标签位于底面
        direction_label.move_to(
            self.axes.c2p(
                *(np.array(P) + vector_scale * np.array(u_vec))[:2],  # 取x,y坐标
                0  # z坐标强制为0
            )
        ).shift(RIGHT*0.3 + DOWN*2)  # 最终微调

        # 确保标记固定在底面
        self.add_fixed_in_frame_mobjects(direction_label)
        self.play(Write(direction_label))
        self.wait(1)

        # 计算Ph点坐标（使用第一个h值）
        h = 0.8  # 使用固定值
        Ph = np.array(P) + h * vector_scale * np.array(u_vec)
        Ph_clipped = np.clip(Ph[:2], -1.8, 1.8)
        Ph_surface = (*Ph_clipped, Ph_clipped[0]**2 + Ph_clipped[1]**2)

        # 创建几何元素
        points = {
            "P": P,
            "Ph": (*Ph_clipped, 0),
            "P_surface": P_surface,
            "Ph_surface": Ph_surface
        }

        # 创建点和线
        ph_point = Dot3D(
            self.axes.c2p(*points["Ph"]), 
            color=PINK,  # 改为更醒目的颜色
            radius=0.08  # 稍微加大点的大小
        )
        ph_surface_point = Dot3D(self.axes.c2p(*points["Ph_surface"]), color=GREEN)
        ph_line = Line(
            self.axes.c2p(*points["Ph"]), 
            self.axes.c2p(*points["Ph_surface"]), 
            color=YELLOW
        )

        # 创建移动点标记
        Ph_label = MathTex(
            "P(x_0+\\rho\\cos\\alpha, y_0+\\rho\\sin\\alpha)",
            color=PINK
        ).scale(0.6).next_to(
            self.axes.c2p(*points["Ph"]),  # 使用三维坐标定位
            UR,  # 保持右上方向
            buff=0.2
        ).shift(LEFT*0.5+DOWN*2)  # 向左微调避免超出屏幕
        self.add_fixed_in_frame_mobjects(Ph_label)

        # 显示移动点和标记
        self.play(Create(ph_point))
        self.wait(0.5)

        # 3. 显示曲面上对应的点和垂线
        self.play(
            Create(point_P_surface),
            Create(ph_surface_point),
            Create(vertical_line),
            Create(ph_line),
            run_time=1
        )
        self.wait(1)

        # 4. 显示垂直平面
        vertical_plane = self.create_vertical_plane(u_vec, P)
        self.play(Create(vertical_plane))
        self.wait(0.5)

        # 5. 显示交线
        intersection_curve = self.create_secant(
            (P[0] - 3*u_vec[0], P[1] - 3*u_vec[1], 0),
            (P[0] + 3*u_vec[0], P[1] + 3*u_vec[1], 0)
        ).set_color(YELLOW_A)  # 使用更亮的黄色
        self.play(Create(intersection_curve))
        self.wait(0.1)

        # 创建rho标记
        t = 0.5  # 中点参数
        mid_x = (1 - t)*P[0] + t*points["Ph"][0]
        mid_y = (1 - t)*P[1] + t*points["Ph"][1]
        mid_z = 0
        rho_mid = self.axes.c2p(mid_x, mid_y, mid_z)

        rho_label = MathTex(
            "\\rho",
            color=YELLOW
        ).scale(0.8).next_to(
            rho_mid,
            RIGHT*0.5+ DOWN*0.5, 
            buff=0.2
        )
        self.add_fixed_in_frame_mobjects(rho_label)

        # 创建曲面上的连线
        surface_line = Line(
            self.axes.c2p(*P_surface),
            self.axes.c2p(*points["Ph_surface"]),
            color=BLUE_C,
            stroke_width=4
        )

        # 调整动画顺序
        # 6. 显示rho标记和曲面连线
        self.play(Write(rho_label))
        self.play(Create(surface_line))
        self.wait(1)

        # 7. 显示切线
        final_tangent = self.create_tangent_line(
            P_surface,
            u_vec,
            length=6
        )
        self.play(Create(final_tangent))
        self.wait(1)

        # 修改旋转方向
        current_theta = self.camera.theta
        self.move_camera(
            theta=current_theta + 90 * DEGREES,  # 改为顺时针旋转
            run_time=2
        )
        self.wait(1)

        # 创建方向导数定义
        definition = VGroup(
            MathTex("\\text{方向导数:}"),
            MathTex(
                "f'_l(x_0,y_0) = \\lim_{\\rho \\to 0} \\frac{f(x_0+\\rho\\cos\\alpha, y_0+\\rho\\sin\\alpha) - f(x_0,y_0)}{\\rho}"
            )
        ).arrange(RIGHT, buff=0.5)
        definition.scale(0.8).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(definition)

        # 显示定义
        self.play(Write(definition))
        self.wait(1)

        # 添加结论说明
        conclusion = Text(
            "函数f在P₀点沿方向l的方向导数为图中白色切线的斜率",
            font="STSong",
            font_size=24  # 缩小字体大小
        ).scale(0.8).next_to(definition, DOWN, buff=0.2)  # 添加缩放和调整间距
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(2)

def main():
    import os
    os.system("manim -pqh directional_derivative.py DirectionalDerivative")

if __name__ == "__main__":
    main() 