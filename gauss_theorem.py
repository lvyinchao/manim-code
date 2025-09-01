from manim import *
import numpy as np

config.tex_template = TexTemplateLibrary.ctex
config.tex_template.add_to_preamble(r"\setCJKmainfont{STSong}")

class GaussTheorem(ThreeDScene):
    def construct(self):
        # 创建标题
        title = Text("高斯公式与散度", font="STSong", font_size=48)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 2, 1],
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

        # 创建一个球体（作为闭合曲面）
        sphere = Surface(
            lambda u, v: np.array([
                np.cos(u) * np.cos(v),
                np.cos(u) * np.sin(v),
                np.sin(u)
            ]),
            u_range=[-PI/2, PI/2],
            v_range=[0, 2*PI],
            resolution=(20, 40),
            checkerboard_colors=[BLUE_D, BLUE_E],
            fill_opacity=0.3
        )
        
        self.play(Create(sphere))
        self.wait(1)

        # 创建向外的法向量场
        normal_vectors = VGroup()
        points = [
            (0, 0, 1),    # 顶部
            (0, 0, -1),   # 底部
            (1, 0, 0),    # 右
            (-1, 0, 0),   # 左
            (0, 1, 0),    # 前
            (0, -1, 0),   # 后
        ]
        
        for point in points:
            normal = np.array(point)  # 球面上的点就是其法向量方向
            vector = Arrow3D(
                start=normal,
                end=normal * 1.5,  # 延长法向量
                color=YELLOW,
                thickness=0.03
            )
            normal_vectors.add(vector)

        # 修改向量场为从一个偏移点发出
        source_point = np.array([0.3, 0.3, 0.3])  # 源点位置
        field_vectors = VGroup()
        for point in points:
            start = np.array(point) * 0.3
            # 计算从源点到表面点的方向
            direction = np.array(point) - source_point
            # 归一化并设置长度
            direction = direction / np.linalg.norm(direction) * 1.5
            end = start + direction
            
            vector = Arrow3D(
                start=start,
                end=end,
                color=RED,
                thickness=0.03
            )
            field_vectors.add(vector)

        
        # 创建点M处的向量场箭头（将在收缩后显示）
        point_vectors = VGroup()
        for direction in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), 
                         (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            direction = np.array(direction)
            vector = Arrow3D(
                start=source_point,
                end=source_point + direction * 0.5,  # 较短的箭头
                color=RED,
                thickness=0.02
            )
            point_vectors.add(vector)

        # 修改等待时间
        self.play(Create(normal_vectors))
        self.wait(1.5)  # 增加等待时间
        self.play(Create(field_vectors))
        self.wait(2)    # 增加等待时间

        # 添加说明文字（右移1.5个单位）
        field_desc = MathTex(
            "\\text{向量场}\\,\\vec{F}",
            color=RED
        ).scale(0.7).to_corner(UL).shift(RIGHT*1.8)
        normal_desc = MathTex(
            "\\text{法向量}\\,\\vec{n}",
            color=YELLOW
        ).scale(0.7).next_to(field_desc, DOWN, buff=0.3)

        # 高斯公式
        gauss_formula = MathTex(
            "\\oiint_S \\vec{F} \\cdot \\vec{n} \\, dS = \\iiint_V (\\frac{\\partial F_x}{\\partial x} + \\frac{\\partial F_y}{\\partial y} + \\frac{\\partial F_z}{\\partial z}) \\, dV"
        ).scale(0.6).next_to(normal_desc, DOWN, buff=0.5)

        # 单位体积通量
        avg_div_formula = MathTex(
            "\\frac{1}{V} \\oiint_S \\vec{F} \\cdot \\vec{n} \\, dS = \\text{单位体积发出的通量}"
        ).scale(0.6).next_to(gauss_formula, DOWN, buff=0.3)

        # 极限公式（先不创建，等到需要时再创建）

        # 散度定义
        div_definition = MathTex(
            "\\text{div}\\,\\vec{F}(M) = \\lim_{V \\to 0} \\frac{1}{V} \\oiint_S \\vec{F} \\cdot \\vec{n} \\, dS"
        ).scale(0.6)  # 位置稍后设置

        # 物理解释
        explanation = Text(
            "散度表示向量场在点M处的发散强度",
            font="STSong",
            font_size=24
        )  # 位置稍后设置

        # 分别显示左边的文字说明
        self.add_fixed_in_frame_mobjects(field_desc)
        self.play(Write(field_desc))
        self.wait(1)    # 增加等待时间
        
        self.add_fixed_in_frame_mobjects(normal_desc)
        self.play(Write(normal_desc))
        self.wait(1)    # 增加等待时间

        # 显示高斯公式
        self.add_fixed_in_frame_mobjects(gauss_formula)
        self.play(Write(gauss_formula))
        self.wait(2)    # 增加等待时间

        # 显示单位体积通量
        self.add_fixed_in_frame_mobjects(avg_div_formula)
        self.play(Write(avg_div_formula))
        self.wait(2)    # 增加等待时间

        # 创建点M（最终收缩的目标点）
        point_M = Dot3D(source_point, color=YELLOW)
        point_M_label = MathTex("M").next_to(point_M, UP+RIGHT, buff=0.1)
        self.add_fixed_in_frame_mobjects(point_M_label)

        # 修改收缩动画，从源点位置开始收缩
        shrink_sphere = sphere.copy()
        shrink_vectors = field_vectors.copy()
        shrink_normals = normal_vectors.copy()
        
        # 直接淡出原始对象并显示新对象
        self.play(
            ReplacementTransform(sphere, shrink_sphere),
            ReplacementTransform(field_vectors, shrink_vectors),
            ReplacementTransform(normal_vectors, shrink_normals)
        )
        self.wait(1)    # 增加等待时间

        # 添加收缩更新函数
        def shrink_updater(mob, alpha):
            scale = 1 - alpha
            if scale > 0:
                if mob == shrink_sphere:
                    shrink_sphere.scale(scale, about_point=source_point)
                elif mob == shrink_vectors:
                    shrink_vectors.scale(scale, about_point=source_point)
                elif mob == shrink_normals:
                    shrink_normals.scale(scale, about_point=source_point)

        # 在收缩动画之前创建极限公式
        limit_formula = MathTex(
            "\\lim_{V \\to 0} \\frac{1}{V} \\oiint_S \\vec{F} \\cdot \\vec{n} \\, dS = \\text{div}\\,\\vec{F}(M)"
        ).scale(0.6).next_to(avg_div_formula, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(limit_formula)

        # 执行收缩动画
        self.play(
            UpdateFromAlphaFunc(shrink_sphere, shrink_updater),
            UpdateFromAlphaFunc(shrink_vectors, shrink_updater),
            UpdateFromAlphaFunc(shrink_normals, shrink_updater),
            Write(limit_formula),
            FadeIn(point_M),
            Write(point_M_label),
            run_time=3   # 增加收缩动画时间
        )
        self.wait(1)

        # 显示点M处的向量场
        self.play(Create(point_vectors))
        self.wait(1.5)

        # 显示散度定义
        div_definition.next_to(limit_formula, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(div_definition)
        self.play(Write(div_definition))
        self.wait(2)    # 增加等待时间

        # 显示物理解释
        explanation.next_to(div_definition, DOWN, buff=0.3)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        self.wait(2)    # 增加等待时间

        # 最后的等待时间
        self.wait(4)    # 增加最后的等待时间

def main():
    import os
    os.system("manim -pqh gauss_theorem.py GaussTheorem")

if __name__ == "__main__":
    main() 