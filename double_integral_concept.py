from manim import *

class DoubleIntegralConcept(ThreeDScene):
    def construct(self):
        # 先显示标题
        title = Text("曲顶柱体的体积计算", font="SimSun").scale(0.8)
        title.to_corner(UR, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))

        self.wait(1)  # 给观众时间阅读标题

        # 创建3D坐标系
        axes = ThreeDAxes(
            x_range=[0, 2, 0.5],
            y_range=[0, 2, 0.5],
            z_range=[0, 4, 1],
            x_length=6,
            y_length=6,
            z_length=4
        ).shift(RIGHT* 4)  # 将坐标系向下平移2个单位

        # 定义函数 z = f(x, y) = x^2 + y^2
        def func(x, y):
            return x**2 + y**2

        # 创建曲面
        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[0, 2],
            v_range=[0, 2],
            resolution=(20, 20),
            fill_color=BLUE,
            fill_opacity=0.6,
            should_make_jagged=True
        )

        # 创建底部投影区域
        projection = Surface(
            lambda u, v: axes.c2p(u, v, 0),
            u_range=[0, 2],
            v_range=[0, 2],
            fill_color=GREEN,
            fill_opacity=0.3,
            should_make_jagged=True
        )

        # 设置网格参数
        dx = dy = 0.2  # 网格大小改为0.2
        nx = ny = int(2 / dx)  # 计算网格数量
        
        # 创建网格线
        grid_lines = VGroup()
        
        # x方向的网格线
        for i in range(nx + 1):
            x = i * dx
            line = Line(
                start=axes.c2p(x, 0, 0),
                end=axes.c2p(x, 2, 0),
                color=WHITE,
                stroke_width=2
            )
            grid_lines.add(line)
            
        # y方向的网格线
        for j in range(ny + 1):
            y = j * dy
            line = Line(
                start=axes.c2p(0, y, 0),
                end=axes.c2p(2, y, 0),
                color=WHITE,
                stroke_width=2
            )
            grid_lines.add(line)

        # 创建坐标轴标签
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        labels = VGroup(x_label, y_label, z_label)

        # 设置相机角度
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        
        # 显示坐标系和标签
        self.play(
            Create(axes),
            Create(labels),
            run_time=1
        )

        # 显示曲面和投影
        self.play(
            Create(surface),
            Create(projection),
            Create(grid_lines),
            run_time=2
        )
        self.wait(1)

        # 创建完整的曲顶柱体
        full_prism = VGroup()
        
        # 创建四个竖直面
        vertices = [
            [0, 0, 0],
            [2, 0, 0],
            [2, 2, 0],
            [0, 2, 0]
        ]
        for i in range(4):
            start = vertices[i]
            end = vertices[(i+1)%4]
            points = []
            # 底边两点
            points.append(axes.c2p(*start))
            points.append(axes.c2p(*end))
            # 上边两点（对应曲面上的点）
            points.append(axes.c2p(end[0], end[1], func(end[0], end[1])))
            points.append(axes.c2p(start[0], start[1], func(start[0], start[1])))
            
            side = Polygon(
                *[np.array(p) for p in points],
                fill_color=YELLOW,
                fill_opacity=0.3,
                stroke_width=1,
                stroke_color=WHITE
            )
            full_prism.add(side)

        # 显示完整曲顶柱体
        self.play(
            Create(full_prism),
            run_time=1
        )
        self.wait(1)

        # 淡出完整曲顶柱体，准备显示分割的小柱体
        self.play(
            FadeOut(full_prism),
            run_time=1
        )

        # 创建并显示小柱体
        columns = VGroup()
        
        for i in range(nx):
            for j in range(ny):
                x = i * dx
                y = j * dy
                
                # 计算底面中心点的高度
                center_x = x + dx/2
                center_y = y + dy/2
                height = func(center_x, center_y)  # 使用中心点的函数值
                
                # 创建柱体
                column = Prism(
                    dimensions=[0.6, 0.6, height],
                    fill_color=YELLOW,
                    fill_opacity=0.1,
                    stroke_width=1,
                    stroke_color=WHITE
                )
                
                # 调整柱体位置
                column.move_to(
                    axes.c2p(x + dx/2, y + dy/2, height/2),
                    aligned_edge=ORIGIN
                )
                columns.add(column)

                # 添加顶面 - 使用中心点高度
                top_vertices = [
                    axes.c2p(x, y, height),
                    axes.c2p(x + dx, y, height),
                    axes.c2p(x + dx, y + dy, height),
                    axes.c2p(x, y + dy, height)
                ]
                top_face = Polygon(
                    *[np.array(v) for v in top_vertices],
                    fill_color=BLUE,
                    fill_opacity=0.4,
                    stroke_width=1
                )
                columns.add(top_face)

        # 分批显示小柱体 - 减少批次以使显示更连续
        n_batches = 3  # 减少批次数量
        columns_list = [columns[i::n_batches] for i in range(n_batches)]
        for batch in columns_list:
            self.play(
                Create(batch),
                run_time=0.8  # 增加运行时间使动画更流畅
            )

        # 在右侧创建一个单独的示例柱体
        # 选择一个合适的位置（比如x=1, y=1附近的柱体）
        sample_x = dx * 5
        sample_y = dy * 5
        sample_center_x = sample_x + dx/2
        sample_center_y = sample_y + dy/2
        sample_height = func(sample_center_x, sample_center_y)

        # 创建一个新的坐标系用于示例 - 位置调整到y轴延长线上
        sample_axes = ThreeDAxes(
            x_range=[-0.5, 1.5, 0.5],
            y_range=[-0.5, 1.5, 0.5],
            z_range=[0, 4, 1],
            x_length=3,
            y_length=3,
            z_length=4
        ).shift(LEFT * 1 + UP * 4)  # 调整位置到y轴延长线上

        # 创建示例柱体
        sample_column = Prism(
            dimensions=[0.6, 0.6, sample_height],
            fill_color=YELLOW,
            fill_opacity=0.3,
            stroke_width=2,  # 示例柱体的边界线可以稍粗一些
            stroke_color=WHITE
        ).move_to(sample_axes.c2p(0.5, 0.5, sample_height/2))

        # 创建穿过柱体的曲面部分
        sample_surface = Surface(
            lambda u, v: sample_axes.c2p(
                u, v, 
                func(sample_x + u*dx, sample_y + v*dy)
            ),
            u_range=[0.3, 0.7],
            v_range=[0.3, 0.7],
            resolution=(20, 20),
            fill_color=BLUE,
            fill_opacity=0.8
        )

        # 添加连接线，表示这是放大的部分
        start_point = axes.c2p(sample_x, sample_y, func(sample_x, sample_y))
        end_point = sample_axes.c2p(0.6, 0.6, 0)
        connection_line = DashedLine(
            start_point,
            end_point,
            dash_length=0.1,
            color=RED  # 改为红色
        )
        self.play(Create(connection_line))

        # 添加示例图形
        self.play(
            Create(sample_axes),
            run_time=1
        )
        self.play(
            Create(sample_column),
            Create(sample_surface),
            run_time=1
        )

        # 添加说明标签
        sample_label = Text("局部放大", font="SimSun").scale(0.6)
        sample_label.next_to(sample_axes, UP, buff=0.2)
        self.add_fixed_in_frame_mobjects(sample_label)
        self.play(Write(sample_label))

        # 在示例坐标系底面添加dσ符号
        d_sigma = MathTex(r"d\sigma_i").scale(0.6)
        d_sigma.move_to(
            sample_axes.c2p(0.5, 0.5, 0)  # 放在xy平面上
        )
        
        # 添加小柱体体积计算公式 - 放在xoy平面上
        volume_formula = MathTex(
            r"dV = f(\xi_i, \zeta_i)d\sigma"
        ).scale(0.9)
        
        # 将公式放在xoy平面上，不再旋转
        volume_formula.move_to(
            sample_axes.c2p(0.8, 0.3, 0)  # 放在xoy平面上，调整位置避免重叠
        )

        # 显示公式
        self.play(
            Write(d_sigma),
            Write(volume_formula),
            run_time=1
        )

        self.wait(1)  # 给观众一些时间阅读公式

        # 开始相机旋转
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(8)
        self.stop_ambient_camera_rotation()

        self.wait(2) 

        # 移除之前的fixed_in_frame设置
        # self.add_fixed_in_frame_mobjects(d_sigma, volume_formula) 

        # 停止相机旋转后，显示二重积分定义式
        integral_formula = MathTex(
            r"V = \iint_D f(x,y)\,d\sigma = \lim_{||T||\to 0} \sum_{i=1}^n f(\xi_i, \zeta_i)\Delta \sigma_i",
        ).scale(0.7)
        
        # 将公式放在屏幕底部并向右平移
        integral_formula.to_edge(DOWN, buff=0.5).shift(RIGHT * 3)
        
        # 添加为固定在屏幕上的元素
        self.add_fixed_in_frame_mobjects(integral_formula)
        
        # 渐变显示公式
        self.play(
            FadeIn(integral_formula),
            run_time=2
        )

        self.wait(2) 