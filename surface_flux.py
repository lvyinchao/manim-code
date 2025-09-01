from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class SurfaceFlux(ThreeDScene):
    def construct(self):
        # 创建标题
        title = Text("向量场通量的计算", font="STSong", font_size=48)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建3D坐标系
        left_axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 2, 1],
            x_length=4,  # 缩小左侧坐标系
            y_length=4,
            z_length=4
        ).shift(LEFT * 3)  # 向左移动

        right_axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[0, 2, 1],
            x_length=4,  # 右侧坐标系大小相同
            y_length=4,
            z_length=4
        ).shift(RIGHT * 3)  # 向右移动

        # 设置一个稍微倾斜的固定视角，便于同时观察平面和曲面
        self.set_camera_orientation(
            phi=75*DEGREES,  # 稍微抬高视角
            theta=270*DEGREES  # 旋转270度（相当于-90度），从另一侧观察
        )

        # 显示坐标系
        self.play(Create(left_axes), Create(right_axes))
        self.wait(2)

        # 第一部分：平面通量演示
        # 创建平面 z = 1
        plane = Surface(
            lambda u, v: left_axes.c2p(u, v, 0),  # 改为z=0平面
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(10, 10),
            fill_opacity=0.5,
            color=BLUE
        )
        
        self.play(Create(plane))
        self.wait(1)

        # 创建平面上的法向量场（只显示几个代表性向量）
        normal_vectors = VGroup()
        for u, v in [(-0.8, -0.8), (-0.8, 0.8), (0.8, -0.8), (0.8, 0.8), (0, 0)]:
            point = left_axes.c2p(u, v, 0)  # 改为z=0平面上的点
            normal = np.array([0, 0, 1])
            vector = Arrow3D(
                start=point,
                end=point + normal * 0.5,
                color=YELLOW,
                thickness=0.02
            )
            normal_vectors.add(vector)

        # 显示法向量场
        self.play(
            Create(normal_vectors),
            run_time=1
        )
        self.wait(2)

        # 显示法向量标注
        normal_text = MathTex(
            "\\text{法向量}\\,\\vec{n}",
            color=YELLOW
        ).scale(0.6).to_corner(UL)
        self.add_fixed_in_frame_mobjects(normal_text)
        self.play(Write(normal_text))
        self.wait(1)

        # 创建向量场 F = (0, 0, z)
        def get_vector_field(u, v, z):
            return np.array([1, 1, 1])  # 统一方向的向量场，指向(1,1,1)

        field_vectors = VGroup()
        for u, v in [(-0.8, -0.8), (-0.8, 0.8), (0.8, -0.8), (0.8, 0.8), (0, 0)]:
            point = left_axes.c2p(u, v, 0)
            field = get_vector_field(u, v, 0)
            # 归一化向量场
            norm = np.linalg.norm(field)
            if norm > 0:
                field = field / norm * 0.5
            vector = Arrow3D(
                start=point,
                end=point + field,
                color=RED,
                thickness=0.03
            )
            vector.set_fill(RED, opacity=0.8)
            field_vectors.add(vector)

        # 显示向量场
        self.play(
            *[Create(vec) for vec in field_vectors],
            run_time=1
        )
        self.wait(2)

        # 显示向量场标注
        field_desc = MathTex(
            "\\text{向量场}\\,\\vec{F}",
            color=RED
        ).scale(0.6).next_to(normal_text, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(field_desc)
        self.play(Write(field_desc))
        self.wait(1)

        # 显示平面通量计算公式
        flux_formula = MathTex(
            "\\text{通量}\\Phi = \\vec{F} \\cdot \\vec{n} \\, S"
        ).scale(0.6).next_to(field_desc, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(flux_formula)
        self.play(Write(flux_formula))
        self.wait(1)

        # 第二部分：曲面通量演示
        # 创建抛物面 z = 0.1(x² + y²)
        surface = Surface(
            lambda u, v: right_axes.c2p(u, v, 0.1*(u**2 + v**2)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(10, 10),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.7
        )
        self.play(Create(surface))
        self.wait(1)

        # 定义法向量计算函数
        def get_normal_vector(u, v):
            # 计算曲面在点(u,v)处的法向量
            tangent_u = np.array([1, 0, 0.2*u])  # 修改系数
            tangent_v = np.array([0, 1, 0.2*v])
            normal = np.cross(tangent_u, tangent_v)
            normal = normal / np.linalg.norm(normal)
            return normal

        # 定义向量场函数
        def get_vector_field(u, v):
            point = np.array([u, v, 0.1*(u**2 + v**2)])  # 修改系数
            return point

        # 创建法向量场
        normal_vectors = VGroup()
        for u, v in [(-0.8, -0.8), (-0.8, 0.8), (0.8, -0.8), (0.8, 0.8), (0, 0)]:
            point = right_axes.c2p(u, v, 0.1*(u**2 + v**2))
            normal = get_normal_vector(u, v)
            vector = Arrow3D(
                start=point,
                end=point + normal * 0.5,
                color=YELLOW,
                thickness=0.03
            )
            vector.set_fill(YELLOW, opacity=0.8)
            normal_vectors.add(vector)

        # 修改显示法向量场的方式
        self.play(
            *[Create(vec) for vec in normal_vectors],
            run_time=1
        )
        self.wait(0.3)

        # 创建向量场（同样减少向量数量）
        field_vectors = VGroup()
        for u, v in [(-0.8, -0.8), (-0.8, 0.8), (0.8, -0.8), (0.8, 0.8), (0, 0)]:
            point = right_axes.c2p(u, v, 0.1*(u**2 + v**2))
            field = get_vector_field(u, v)
            # 归一化向量场，避免太长
            norm = np.linalg.norm(field)
            if norm > 0:
                field = field / norm * 0.5
            vector = Arrow3D(
                start=point,
                end=point + field,
                color=RED,
                thickness=0.03
            )
            # 设置向量的填充不透明度
            vector.set_fill(RED, opacity=0.8)
            field_vectors.add(vector)

        # 修改显示向量场的方式
        self.play(
            *[Create(vec) for vec in field_vectors],
            run_time=1
        )
        self.wait(2)

        # 添加向量场说明
        field_desc = MathTex(
            "\\text{法向量}\\,\\vec{n}",
            color=YELLOW
        ).scale(0.7).to_corner(UR)
        self.add_fixed_in_frame_mobjects(field_desc)
        
        field_desc2 = MathTex(
            "\\text{向量场}\\,\\vec{F}",
            color=RED
        ).scale(0.7).next_to(field_desc, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(field_desc2)
        
        self.play(
            Write(field_desc),
            Write(field_desc2)
        )
        self.wait(1)

        # 添加微元演示
        micro_u, micro_v = 1.0, 1.0  # 选择曲面上更倾斜的位置
        du, dv = 0.2, 0.2  # 微元大小

        # 创建放大的微元框架
        micro_frame = ThreeDAxes(
            x_range=[-0.5, 0.5, 0.2],
            y_range=[-0.5, 0.5, 0.2],
            z_range=[0, 0.5, 0.1],
            x_length=2,
            y_length=2,
            z_length=1
        ).shift(DOWN * 6).set_opacity(0)
        
        # 获取原曲面上微元中心点的坐标
        original_point = right_axes.c2p(micro_u, micro_v, 0.1*(micro_u**2 + micro_v**2))
        
        # 创建并显示放大框和连接线
        zoom_box = Rectangle(
            height=1,
            width=1,
            color=YELLOW
        ).set_fill(BLACK, opacity=0.1)
        zoom_box.move_to(original_point)
        
        zoom_lines = VGroup(
            Line(
                original_point,
                micro_frame.get_origin(),
                color=YELLOW,
                stroke_width=0.5
            )
        )

        # 计算微元处的法向量，用于确定微元的倾斜角度
        normal = get_normal_vector(micro_u, micro_v)
        # 计算微元平面的旋转矩阵
        z_axis = np.array([0, 0, 1])
        rotation_axis = np.cross(z_axis, normal)
        rotation_angle = np.arccos(np.dot(z_axis, normal))
        
        # 旋转微元框架
        if np.linalg.norm(rotation_axis) > 1e-6:  # 避免零向量
            rotation_axis = rotation_axis / np.linalg.norm(rotation_axis)
            micro_frame.rotate(angle=rotation_angle, axis=rotation_axis)

        # 在原曲面上标记微元区域
        highlight_box = Surface(
            lambda u, v: right_axes.c2p(
                micro_u + u*du, micro_v + v*du, 
                0.1*((micro_u + u*du)**2 + (micro_v + v*du)**2)
            ),
            u_range=[-0.5, 0.5],
            v_range=[-0.5, 0.5],
            resolution=(2, 2),
            fill_opacity=0.3,
            color=YELLOW
        )

        self.play(
            Create(zoom_box),
            Create(zoom_lines),
            Create(highlight_box)
        )
        self.wait(1)

        # 创建微元区域（保持与原曲面相同的倾斜角度）
        micro_surface = Surface(
            lambda u, v: micro_frame.c2p(
                u, v, 
                0  # 在旋转后的坐标系中，微元近似为平面
            ),
            u_range=[-0.5, 0.5],
            v_range=[-0.5, 0.5],
            resolution=(2, 2),
            fill_opacity=0.8,
            color=YELLOW_A
        )

        self.play(
            Create(micro_surface)
        )
        self.wait(1)

        # 在微元上显示向量场和法向量
        center_point = micro_frame.c2p(0, 0, 0)
        micro_normal = Arrow3D(
            start=center_point,
            end=center_point + normal * 1,
            color=YELLOW,
            thickness=0.03
        )

        field = get_vector_field(micro_u, micro_v)
        field = field / np.linalg.norm(field) * 1
        micro_field = Arrow3D(
            start=center_point,
            end=center_point + field,
            color=RED,
            thickness=0.03
        )

        self.play(
            Create(micro_normal),
            Create(micro_field)
        )
        self.wait(2)

        # 添加说明文字
        micro_text = Text(
            "曲面微元可近似为平面",
            font="STSong",
            font_size=24
        ).shift(DOWN * 2.5+RIGHT*3.5)
        self.add_fixed_in_frame_mobjects(micro_text)

        # 显示平面近似
        self.play(
            Write(micro_text),
            run_time=1
        )
        self.wait(2)

        # 显示微元通量计算公式和最后的结论（在同一行）
        micro_flux_formula = MathTex(
            "d\\Phi = \\vec{F} \\cdot \\vec{n} \\, dS"
        ).scale(0.6).shift(DOWN * 3.5).shift(LEFT * 2)  # 放在左侧
        self.add_fixed_in_frame_mobjects(micro_flux_formula)
        self.play(Write(micro_flux_formula))
        self.wait(2)

        

        # 最后的结论
        conclusion = MathTex(
            "\\text{通量} = \\iint_S \\vec{F} \\cdot \\vec{n} \\, dS"
        ).scale(0.6).shift(DOWN * 3.5).shift(RIGHT * 2)  # 放在右侧
        self.add_fixed_in_frame_mobjects(conclusion)
        self.play(Write(conclusion))
        self.wait(3)

        # 最后多等待一会，让观众有时间观察
        self.wait(1)

def main():
    import os
    os.system("manim -pqh surface_flux.py SurfaceFlux")

if __name__ == "__main__":
    main() 