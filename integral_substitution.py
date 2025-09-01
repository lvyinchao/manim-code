from manim import *
import numpy as np

class IntegralSubstitution(Scene):
    def construct(self):
        # 添加标题
        title = Text("二重积分的换元法（极坐标变换）", font="SimSun", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # 创建两个坐标系，左边xy平面，右边rθ平面
        xy_axes = Axes(
            x_range=[-2, 2],
            y_range=[-2, 2],
            axis_config={"color": GREY},
            x_length=4,
            y_length=4,
        ).shift(LEFT * 4)

        rt_axes = Axes(
            x_range=[0, 1.2],  # r的范围
            y_range=[0, 2*np.pi],  # θ的范围
            axis_config={"color": GREY},
            x_length=4,
            y_length=4,
        ).shift(RIGHT * 4)

        # 添加坐标轴标签
        xy_labels = VGroup(
            xy_axes.get_x_axis_label("x", direction=DOWN),
            xy_axes.get_y_axis_label("y")
        )
        rt_labels = VGroup(
            rt_axes.get_x_axis_label("r", direction=DOWN),
            rt_axes.get_y_axis_label(r"\theta")
        )

        # 显示坐标系和标签
        self.play(
            Create(xy_axes), Create(rt_axes),
            Write(xy_labels), Write(rt_labels)
        )
        self.wait(1)

        # 添加坐标值标注
        xy_axes.add_coordinates()  # 添加xy平面的坐标值
        
        # 为rθ平面添加自定义坐标值
        r_numbers = VGroup()
        r_values = [0, 0.5, 1]
        
        for value in r_values:
            tex = MathTex(str(value), font_size=24)
            tex.next_to(rt_axes.x_axis.n2p(value), DOWN)
            r_numbers.add(tex)
        
        # 为θ轴添加特殊标注
        theta_numbers = VGroup()
        theta_values = [0, np.pi, 2*np.pi]
        theta_labels = ["0", r"\pi", r"2\pi"]
        
        for value, label in zip(theta_values, theta_labels):
            tex = MathTex(label, font_size=24)
            tex.next_to(rt_axes.y_axis.n2p(value), LEFT)
            theta_numbers.add(tex)
        
        self.play(Write(VGroup(r_numbers, theta_numbers)))

        # 在xy平面创建一个圆形区域
        xy_region = Circle(radius=1, color=BLUE, fill_opacity=0.3)
        xy_region.move_to(xy_axes.c2p(0, 0))

        # 添加圆的范围标注
        radius_line = Line(
            xy_axes.c2p(0, 0),
            xy_axes.c2p(1, 0),
            color=WHITE
        )
        radius_label = MathTex("r=1", font_size=24).next_to(radius_line, DOWN, buff=0.1)
        
        # 显示区域和标注
        self.play(Create(xy_region))
        self.play(Create(radius_line), Write(radius_label))
        self.wait(1)

        # 创建网格点来显示变换
        n_r = 8  # r方向的点数
        n_theta = 16  # θ方向的点数
        dots_xy = VGroup()
        dots_rt = VGroup()
        
        for i in range(n_r + 1):
            r = i / n_r
            for j in range(n_theta):
                theta = j * 2 * np.pi / n_theta
                # xy平面上的点
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                dot_xy = Dot(
                    xy_axes.c2p(x, y),
                    color=BLUE,
                    radius=0.02
                )
                dots_xy.add(dot_xy)
                
                # rθ平面上的点
                dot_rt = Dot(
                    rt_axes.c2p(r, theta),
                    color=RED,
                    radius=0.02
                )
                dots_rt.add(dot_rt)

        self.play(Create(dots_xy))
        self.wait(1)

        # 在rθ平面创建变换后的矩形区域
        # 计算矩形的实际尺寸
        r_range = rt_axes.x_range[1] - rt_axes.x_range[0]  # r的范围长度
        theta_range = rt_axes.y_range[1] - rt_axes.y_range[0]  # θ的范围长度
        
        # 创建矩形，使用坐标轴的比例
        rt_region = Rectangle(
            width=rt_axes.get_x_axis().get_unit_size() * 1,  # r从0到1
            height=rt_axes.get_y_axis().get_unit_size() * 2*np.pi,  # θ从0到2π
            color=RED,
            fill_opacity=0.3
        )
        
        # 将矩形的左下角对齐到原点，然后向右移动到r=0的位置
        rt_region.align_to(rt_axes.c2p(0, 0), DL)
        
        # 添加范围标注（不使用花括号）
        r_text = MathTex("0 \leq r \leq 1", font_size=24).next_to(
            rt_region, 
            DOWN, 
            buff=0.5  # 增加下方间距
        )
        theta_text = MathTex("0 \leq \\theta \leq 2\pi", font_size=24).next_to(
            rt_region, 
            RIGHT
        )

        # 显示变换过程和标注
        self.play(
            Transform(dots_xy.copy(), dots_rt),
            Create(rt_region)
        )
        self.play(
            Write(r_text),
            Write(theta_text)
        )
        self.wait(1)

        # 添加变换公式
        transform_formula = MathTex(
            r"\begin{cases} x &= r\cos\theta \\ y &= r\sin\theta \end{cases}",
            font_size=32
        ).next_to(title, DOWN)
        
        self.play(Write(transform_formula))
        self.wait(1)

        # 添加雅可比行列式
        jacobian = MathTex(
            r"J = \begin{vmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix} = r",
            font_size=32
        ).next_to(transform_formula, DOWN)
        
        self.play(Write(jacobian))
        self.wait(1)

        # 添加换元公式
        integral_formula = MathTex(
            r"\iint_D f(x,y)dxdy = \iint_{D'} f(r\cos\theta,r\sin\theta)r\,drd\theta",
            font_size=32
        ).to_edge(DOWN)
        
        self.play(Write(integral_formula))
        self.wait(2) 