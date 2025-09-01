from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class FluidCurl(ThreeDScene):
    def construct(self):
        # 创建标题
        title = Text("流体的旋度", font="STSong", font_size=48)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )

        # 设置相机视角
        self.set_camera_orientation(
            phi=70*DEGREES,
            theta=-45*DEGREES
        )

        self.play(Create(axes))
        self.wait(1)

        # 创建流体粒子（用小球表示）
        particles = VGroup()
        particle_traces = VGroup()  # 存储粒子轨迹
        n_particles = 30
        radius = 2

        for i in range(n_particles):
            angle = i * TAU / n_particles
            pos = np.array([
                radius * np.cos(angle),
                radius * np.sin(angle),
                0
            ])
            particle = Sphere(radius=0.1, fill_opacity=0.8)
            particle.set_color(BLUE)
            particle.move_to(pos)
            particles.add(particle)
            
            # 为每个粒子创建轨迹
            trace = VMobject(stroke_color=BLUE_A, stroke_opacity=0.3)
            trace.set_points_as_corners([pos, pos])
            particle_traces.add(trace)

        self.play(Create(particles), Create(particle_traces))

        # 创建浮标（用于显示局部旋转）
        paddles = VGroup()
        paddle_centers = [
            (1.5, 0, 0),
            (-1.5, 0, 0),
            (0, 1.5, 0),
            (0, -1.5, 0)
        ]

        for center in paddle_centers:
            # 创建十字形浮标
            paddle = VGroup()
            # 水平杆
            horizontal = Line(
                start=np.array([center[0]-0.3, center[1], center[2]]),
                end=np.array([center[0]+0.3, center[1], center[2]]),
                color=RED
            )
            # 垂直杆
            vertical = Line(
                start=np.array([center[0], center[1]-0.3, center[2]]),
                end=np.array([center[0], center[1]+0.3, center[2]]),
                color=RED
            )
            paddle.add(horizontal, vertical)
            paddles.add(paddle)

        self.play(Create(paddles))

        # 创建说明文字
        curl_def = MathTex(
            "\\text{curl}\\,\\vec{v} = \\nabla \\times \\vec{v} = 2\\vec{\\omega}",
            tex_template=TexTemplateLibrary.ctex
        ).scale(0.7).to_corner(UL)

        explanation = Text(
            "旋度是流体局部旋转角速度的两倍",
            font="STSong",
            font_size=24
        ).next_to(curl_def, DOWN)

        self.add_fixed_in_frame_mobjects(curl_def, explanation)
        self.play(Write(curl_def), Write(explanation))

        # 添加动画
        def update_particles(particles, dt):
            for i, particle in enumerate(particles):
                # 获取当前位置
                pos = particle.get_center()
                # 计算新位置（旋转运动）
                angle = dt * 0.5  # 角速度
                x, y, z = pos
                new_x = x * np.cos(angle) - y * np.sin(angle)
                new_y = x * np.sin(angle) + y * np.cos(angle)
                new_pos = np.array([new_x, new_y, z])
                particle.move_to(new_pos)
                
                # 更新轨迹
                trace = particle_traces[i]
                points = trace.get_points()
                points = np.vstack([points, [new_pos]])
                if len(points) > 50:  # 限制轨迹长度
                    points = points[-50:]
                trace.set_points_as_corners(points)

        # 创建浮标旋转动画
        paddle_rotations = [
            Rotate(paddle, angle=TAU, axis=OUT, about_point=np.array(center), rate_func=linear)
            for paddle, center in zip(paddles, paddle_centers)
        ]

        # 开始动画
        particles.add_updater(update_particles)
        self.play(*paddle_rotations, run_time=8)
        
        # 添加涡量公式
        vorticity = MathTex(
            "\\vec{\\omega} = \\frac{1}{2}\\text{curl}\\,\\vec{v}",
            tex_template=TexTemplateLibrary.ctex
        ).scale(0.7).next_to(explanation, DOWN)
        
        self.add_fixed_in_frame_mobjects(vorticity)
        self.play(Write(vorticity))

        # 相机旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()

        # 移除粒子更新器
        particles.remove_updater(update_particles)
        self.wait(2)

def main():
    import os
    os.system("manim -pqh fluid_curl.py FluidCurl")

if __name__ == "__main__":
    main() 