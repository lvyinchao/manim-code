from manim import *
import numpy as np

class TorusVolumeIntegral(ThreeDScene):
    def construct(self):
        # 在开始添加标题
        title = Text("直角坐标计算二重积分", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        self.wait(1)

        # 设置相机角度（初始视角旋转180度）
        self.set_camera_orientation(
            phi=65 * DEGREES, 
            theta=(30 + 260) * DEGREES  # 增加180度
        )
        
        # 创建3D坐标系并向左移动
        axes = ThreeDAxes(
            x_range=[0, 4],
            y_range=[0, 2],
            z_range=[0, 4],
            x_length=6,
            y_length=6,
            z_length=4,
            axis_config={
                "color": GREY,
                "include_numbers": False  # 移除数字标识
            }
        ).shift(LEFT * 2)  # 向左移动3个单位

        # 添加坐标轴标签
        x_label = MathTex("x").next_to(axes.x_axis.get_end(), RIGHT)
        y_label = MathTex("y").next_to(axes.y_axis.get_end(), UP)
        z_label = MathTex("z").next_to(axes.z_axis.get_end(), OUT)
        axes_labels = VGroup(x_label, y_label, z_label)

        # 显示坐标系和标签
        self.play(Create(axes))
        self.play(Write(axes_labels))
        self.wait(1)

        # 创建底面区域的边界曲线
        def curve1(x): return np.sqrt(x)  # y = √x
        def curve2(x): return (1/5)*(x-1)**2  # y = (1/5)(x-1)²
        
        x_vals = np.linspace(1, 3, 100)
        curve1_points = [[x, curve1(x), 0] for x in x_vals]
        curve2_points = [[x, curve2(x), 0] for x in x_vals]
        
        # 创建完整的底面区域轮廓
        region_points = [
            *curve1_points,  # 上边界：y = √x
            [3, curve2(3), 0],  # 右边界：x = 3
            *curve2_points[::-1],  # 下边界：y = (1/5)(x-1)²
            [1, curve2(1), 0],  # 左边界：x = 1
        ]
        
        # 创建底面
        region = Polygon(
            *[axes.c2p(*p) for p in region_points],
            color=BLUE,
            fill_opacity=0.3
        )

        # 创建高度函数
        def height_func(x, y):
            return 2 - (1/10)*(x**2 + y**2)

        # 创建立体图形（包括顶面和侧面）
        # 顶面
        def param_surface(u, v):
            x = u
            y = v * curve1(x) + (1-v) * curve2(x)
            return axes.c2p(x, y, height_func(x, y))

        top_surface = Surface(
            param_surface,
            u_range=[1, 3],
            v_range=[0, 1],
            resolution=(30, 30),
            fill_opacity=0.7,
            fill_color=BLUE,
            stroke_color=WHITE,
            stroke_width=0.5
        )

        # 添加曲面方程标注
        surface_equation = MathTex(
            r"z=f(x,y)",
            font_size=32,
            color=BLUE
        ).move_to(
            axes.c2p(2, 1, height_func(2, 1) + 0.5)  # 将标注放在曲面上方
        )
        self.play(Write(surface_equation))

        # 创建所有侧面
        side_surfaces = VGroup()
        
        # 前侧面（x=1）
        front_surface = Surface(
            lambda u, v: axes.c2p(
                1,  # x固定为1
                u,  # y从下边界到上边界
                v * height_func(1, u)  # z从0到对应高度
            ),
            u_range=[curve2(1), curve1(1)],
            v_range=[0, 1],  # 使用参数v来控制高度
            fill_opacity=0,  # 完全透明
            fill_color=BLUE_E,
            stroke_color=BLUE_E,
            stroke_width=2
        )
        
        # 后侧面（x=3）
        back_surface = Surface(
            lambda u, v: axes.c2p(
                3,  # x固定为3
                u,  # y从下边界到上边界
                v * height_func(3, u)  # z从0到对应高度
            ),
            u_range=[curve2(3), curve1(3)],
            v_range=[0, 1],  # 使用参数v来控制高度
            fill_opacity=0,  # 完全透明
            fill_color=BLUE_E,
            stroke_color=BLUE_E,
            stroke_width=2
        )

        # 上边界曲面（y = √x）
        upper_surface = Surface(
            lambda u, v: axes.c2p(
                u,
                curve1(u),
                v * height_func(u, curve1(u))
            ),
            u_range=[1, 3],
            v_range=[0, 1],
            fill_opacity=0,  # 完全透明
            fill_color=BLUE_E,
            stroke_color=BLUE_E,
            stroke_width=2
        )

        # 下边界曲面（y = (1/5)(x-1)²）
        lower_surface = Surface(
            lambda u, v: axes.c2p(
                u,
                curve2(u),
                v * height_func(u, curve2(u))
            ),
            u_range=[1, 3],
            v_range=[0, 1],
            fill_opacity=0,  # 完全透明
            fill_color=BLUE_E,
            stroke_color=BLUE_E,
            stroke_width=2
        )

        # 底面
        bottom_surface = Surface(
            lambda u, v: axes.c2p(
                u,
                v * curve1(u) + (1-v) * curve2(u),
                0
            ),
            u_range=[1, 3],
            v_range=[0, 1],
            fill_opacity=0,  # 完全透明
            fill_color=BLUE,
            stroke_color=BLUE,
            stroke_width=2
        )

        side_surfaces.add(front_surface, back_surface, upper_surface, lower_surface, bottom_surface)

        # 添加边界函数标注
        boundary_labels = VGroup(
            # 上边界标注
            MathTex(r"y=\varphi_2(x)", font_size=32).next_to(
                axes.c2p(2, curve1(2), 0),
                UP,
                buff=0.2
            ),
            # 下边界标注
            MathTex(r"y=\varphi_1(x)", font_size=32).next_to(
                axes.c2p(2, curve2(2), 0),
                DOWN,
                buff=0.2
            )
        )

        # 添加x=a和x=b的边界标注
        x_boundary_labels = VGroup(
            MathTex(r"x=a", font_size=32).next_to(
                axes.c2p(1, 0, 0),
                DOWN,
                buff=0.2
            ),
            MathTex(r"x=b", font_size=32).next_to(
                axes.c2p(3, 0, 0),
                DOWN,
                buff=0.2
            )
        )

        # 修改显示顺序
        # 1. 显示顶面
        self.play(Create(top_surface))
        self.wait(1)

        # 2. 显示底面
        self.play(Create(bottom_surface))
        self.wait(1)

        # 3. 显示边界函数标注
        self.play(
            Write(boundary_labels),
            Write(x_boundary_labels)
        )
        self.wait(1)

        # 4. 显示侧面
        self.play(
            Create(front_surface),
            Create(back_surface),
            Create(upper_surface),
            Create(lower_surface)
        )
        self.wait(1)

        # 创建切片平面（x=2和x=2.1）
        def create_slice_plane(x_val):
            y_min = curve2(x_val)
            y_max = curve1(x_val)
            
            # 创建填充面
            slice_plane = Surface(
                lambda u, v: axes.c2p(
                    x_val,
                    u,
                    v * height_func(x_val, u)
                ),
                u_range=[y_min, y_max],
                v_range=[0, 1],
                fill_opacity=0.8,
                stroke_width=0
            )
            
            # 创建完整边界
            slice_border = VGroup(
                # 上边界曲线
                ParametricFunction(
                    lambda t: axes.c2p(
                        x_val,
                        t,
                        height_func(x_val, t)
                    ),
                    t_range=[y_min, y_max],
                    color=YELLOW,
                    stroke_width=2
                ),
                # 下边界（底部）
                ParametricFunction(
                    lambda t: axes.c2p(x_val, t, 0),
                    t_range=[y_min, y_max],
                    color=YELLOW,
                    stroke_width=2
                ),
                # 左边界
                Line(
                    axes.c2p(x_val, y_min, 0),
                    axes.c2p(x_val, y_min, height_func(x_val, y_min)),
                    color=YELLOW,
                    stroke_width=2
                ),
                # 右边界
                Line(
                    axes.c2p(x_val, y_max, 0),
                    axes.c2p(x_val, y_max, height_func(x_val, y_max)),
                    color=YELLOW,
                    stroke_width=2
                )
            )
            
            return VGroup(slice_plane, slice_border)

        # 创建两个切片
        slice_1 = create_slice_plane(2.0)
        slice_1[0].set_fill(color=YELLOW)  # 设置填充颜色
        slice_2 = create_slice_plane(2.1)
        slice_2[0].set_fill(color=YELLOW)  # 设置填充颜色

        # 显示立体图形和切片
        # self.play(
        #     Create(top_surface),
        #     Create(side_surfaces)
        # )
        #self#.wait(1)
        
        self.play(
            Create(slice_1),
            Create(slice_2)
        )
        self.wait(1)

        # 修改右侧2D截面显示
        section_axes = Axes(
            x_range=[0, 4],
            y_range=[0, 4],
            x_length=3,
            y_length=4,
            axis_config={
                "color": GREY,
                "include_numbers": False  # 移除数字标识
            }
        ).shift(RIGHT * 4)

        # 添加2D坐标轴标签
        section_x_label = MathTex("y").next_to(section_axes.x_axis.get_end(), RIGHT)
        section_y_label = MathTex("z").next_to(section_axes.y_axis.get_end(), UP)
        section_labels = VGroup(section_x_label, section_y_label)

        # 固定2D坐标系、标签和截面在屏幕上
        self.add_fixed_in_frame_mobjects(section_axes, section_labels)

        # 显示2D坐标系和标签
        self.play(
            Create(section_axes),
            Write(section_labels)
        )

        # 在新坐标系中绘制完整截面
        def create_section_curve(x_val):
            y_min = curve2(x_val)
            y_max = curve1(x_val)
            
            # 计算z的范围
            z_max = height_func(x_val, y_min)  # 计算最大高度
            
            return VGroup(
                # 主曲线（y-z平面上的曲线）
                ParametricFunction(
                    lambda t: section_axes.c2p(
                        t,  # y坐标作为横坐标
                        height_func(x_val, t)  # z坐标作为纵坐标
                    ),
                    t_range=[y_min, y_max],
                    color=YELLOW,
                    stroke_width=2
                ),
                # 底边（y轴上的线段）
                Line(
                    section_axes.c2p(y_min, 0),  # 从最小y值开始
                    section_axes.c2p(y_max, 0),  # 到最大y值结束
                    color=YELLOW,
                    stroke_width=2
                ),
                # 左边界（垂直线）
                Line(
                    section_axes.c2p(y_min, 0),
                    section_axes.c2p(y_min, height_func(x_val, y_min)),
                    color=YELLOW,
                    stroke_width=2
                ),
                # 右边界（垂直线）
                Line(
                    section_axes.c2p(y_max, 0),
                    section_axes.c2p(y_max, height_func(x_val, y_max)),
                    color=YELLOW,
                    stroke_width=2
                )
            )

        # 定义切片位置和边界
        x_val = 2.0
        y_min = curve2(x_val)  # φ₁(x₀)
        y_max = curve1(x_val)  # φ₂(x₀)

        # 创建x=2处的截面曲线
        section_curve = create_section_curve(2.0)
        self.add_fixed_in_frame_mobjects(section_curve)

        # 显示截面
        self.play(Create(section_curve))

        # 添加z=f(x₀,y)标注
        section_equation = MathTex(
            r"z=f(x_0,y)",
            font_size=28,
            color=YELLOW
        ).move_to(
            section_axes.c2p(
                (y_min + y_max)/2,  # y坐标取中点
                height_func(x_val, (y_min + y_max)/2) + 0.5  # 曲线上方0.5个单位
            )
        )
        self.add_fixed_in_frame_mobjects(section_equation)
        self.play(Write(section_equation))

        # 添加φ₁(x₀)和φ₂(x₀)标注
        phi_labels = VGroup(
            # φ₁(x₀)标注
            MathTex(r"\varphi_1(x_0)", font_size=20).next_to(
                section_axes.c2p(y_min, 0),
                LEFT,
                buff=0.1
            ),
            # φ₂(x₀)标注
            MathTex(r"\varphi_2(x_0)", font_size=20).next_to(
                section_axes.c2p(y_max, 0),
                LEFT,
                buff=0.1
            )
        )
        self.add_fixed_in_frame_mobjects(phi_labels)
        self.play(Write(phi_labels))

        # 修改标注文字
        section_label = VGroup(
            MathTex(r"x=x_0", font_size=24),
            Text("处的截面", font="SimSun", font_size=24)
        ).arrange(RIGHT, buff=0.1).next_to(section_axes, UP)
        self.add_fixed_in_frame_mobjects(section_label)
        self.play(Write(section_label))

        # 在切片内添加A(x₀)标注
        area_label = MathTex(
            r"A(x_0)",
            font_size=28,
            color=YELLOW
        ).move_to(
            section_axes.c2p(
                (y_min + y_max)/2,  # y坐标取中点
                height_func(x_val, (y_min + y_max)/2)/2  # z坐标取高度的一半
            )
        )
        self.add_fixed_in_frame_mobjects(area_label)
        self.play(Write(area_label))

        # 添加面积计算公式
        area_formula = MathTex(
            r"A(x_0) = \int_{\varphi_1(x_0)}^{\varphi_2(x_0)} f(x_0,y)dy",
            font_size=28
        ).next_to(section_axes, DOWN, buff=0.5)  # 在坐标系下方显示
        self.add_fixed_in_frame_mobjects(area_formula)
        self.play(Write(area_formula))

        # 修改积分公式为两行
        conversion_formulas = VGroup(
            # 第一行：二重积分
            MathTex(
                r"\iint_D f(x,y)dxdy",
                font_size=32
            ),
            # 第二行：等号和累次积分
            VGroup(
                MathTex(r"=", font_size=32),
                MathTex(
                    r"\int_a^b \left(\int_{\varphi_1(x)}^{\varphi_2(x)} f(x,y)dy\right)dx",
                    font_size=32
                )
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.3).to_corner(DL)

        # 显示转换公式
        self.add_fixed_in_frame_mobjects(conversion_formulas)
        self.play(Write(conversion_formulas[0]))
        self.wait(0.5)
        self.play(Write(conversion_formulas[1]))
        self.wait(1)

        # 最后等待几秒
        self.wait(3) 