from manim import *

class ThreePlanesShape(ThreeDScene):
    def construct(self):
        # 设置场景和相机
        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        
        # 创建坐标轴
        axes = ThreeDAxes(
            x_range=[-1, 3, 1],
            y_range=[-1, 3, 1],
            z_range=[-1, 3, 1],
            x_length=4,
            y_length=4,
            z_length=4
        )
        
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 0.5)
        z_label = axes.get_z_axis_label(Tex("z")).shift(RIGHT * 0.5)
        labels = VGroup(x_label, y_label, z_label)
        
        # 添加平面标题 - 使用Text而不是Tex来支持中文
        title = Text("三平面围成的图形", font_size=36).to_corner(UL)
        equations = MathTex(r"z=y,\ y=x,\ x=1").next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, equations)
        
        # 显示坐标系
        self.play(FadeIn(axes), FadeIn(labels))
        self.wait(1)
        
        # 创建三个平面
        # 平面 z = y (范围有限制)
        z_equals_y_plane = Surface(
            lambda u, v: np.array([u, v, v]),
            u_range=[0, 1],  # x从0到1
            v_range=[0, 1],  # y和z从0到1
            resolution=(20, 20),
            fill_opacity=0.6,
            fill_color=BLUE_C,
            stroke_width=0.5,
            stroke_color=BLUE_A
        )
        
        # 修正平面 y = x (范围有限制)
        # 正确参数化：取点(t,t,z)，其中t从0到1，z从0到1
        y_equals_x_plane = Surface(
            lambda u, v: np.array([u, u, v]),
            u_range=[0, 1],  # x=y=u，从0到1
            v_range=[0, 1],  # z从0到1
            resolution=(20, 20),
            fill_opacity=0.6,
            fill_color=GREEN_C,
            stroke_width=0.5,
            stroke_color=GREEN_A
        )
        
        # 平面 x = 1 (范围有限制)
        x_equals_1_plane = Surface(
            lambda u, v: np.array([1, u, v]),
            u_range=[0, 1],  # y从0到1
            v_range=[0, 1],  # z从0到1
            resolution=(20, 20),
            fill_opacity=0.6,
            fill_color=RED_C,
            stroke_width=0.5,
            stroke_color=RED_A
        )
        
        # 创建三个平面的交线
        # 线 x=1, y=1, z=y (即 z=1)
        line1 = Line3D(
            start=np.array([1, 1, 0]),
            end=np.array([1, 1, 1]),
            color=YELLOW,
            thickness=0.05
        )
        
        # 线 y=x, x=1 (即 y=1), z可变
        line2 = Line3D(
            start=np.array([1, 1, 0]),
            end=np.array([1, 1, 1]),
            color=YELLOW,
            thickness=0.05
        )
        
        # 线 y=x, z=y (即 z=x), x可变
        line3 = Line3D(
            start=np.array([0, 0, 0]),
            end=np.array([1, 1, 1]),
            color=YELLOW,
            thickness=0.05
        )
        
        # 交点 (1,1,1)
        intersection_point = Sphere(
            radius=0.05,
            color=YELLOW
        ).move_to([1, 1, 1])
        
        # 原点 (0,0,0)
        origin_point = Sphere(
            radius=0.05,
            color=YELLOW
        ).move_to([0, 0, 0])
        
        # 显示三个平面
        self.play(FadeIn(z_equals_y_plane))
        self.play(FadeIn(y_equals_x_plane))
        self.play(FadeIn(x_equals_1_plane))
        
        # 添加平面方程说明
        plane1_text = Tex("$z=y$", color=BLUE_A).to_corner(UR).shift(DOWN * 0.5)
        plane2_text = Tex("$y=x$", color=GREEN_A).next_to(plane1_text, DOWN)
        plane3_text = Tex("$x=1$", color=RED_A).next_to(plane2_text, DOWN)
        
        self.add_fixed_in_frame_mobjects(plane1_text, plane2_text, plane3_text)
        
        # 添加交线和交点
        self.play(FadeIn(line3))
        self.play(FadeIn(intersection_point))
        self.play(FadeIn(origin_point))
        
        # 旋转相机以便从不同角度查看该图形
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # 移除单独的平面，展示完整的立体
        self.play(
            FadeOut(z_equals_y_plane),
            FadeOut(y_equals_x_plane),
            FadeOut(x_equals_1_plane),
            FadeOut(line3),
            FadeOut(intersection_point),
            FadeOut(origin_point)
        )
        
        # 创建四面体的顶点
        v0 = np.array([0, 0, 0])  # 原点
        v1 = np.array([1, 1, 1])  # 三平面交点
        v2 = np.array([1, 1, 0])  # x=1, y=1, z=0
        v3 = np.array([1, 0, 0])  # x=1, y=0, z=0
        
        # 创建四面体的面
        face_group = VGroup()
        
        # 创建面1 (对应y=x平面) - 顶点顺序为 v0, v2, v1
        # 使用triangle方法创建三角形
        face1 = Triangle3D(
            v0, v2, v1,
            fill_color=GREEN_D,
            fill_opacity=0.7,
            stroke_width=1,
            stroke_color=WHITE
        )
        face_group.add(face1)
        
        # 创建面2 (对应x=1平面) - 顶点顺序为 v0, v3, v2
        face2 = Triangle3D(
            v0, v3, v2,
            fill_color=RED_D,
            fill_opacity=0.7,
            stroke_width=1,
            stroke_color=WHITE
        )
        face_group.add(face2)
        
        # 创建面3 (对应z=y平面) - 顶点顺序为 v0, v1, v3
        face3 = Triangle3D(
            v0, v1, v3,
            fill_color=BLUE_D,
            fill_opacity=0.7,
            stroke_width=1,
            stroke_color=WHITE
        )
        face_group.add(face3)
        
        # 创建面4 (外部面) - 顶点顺序为 v1, v2, v3
        face4 = Triangle3D(
            v1, v2, v3,
            fill_color=PURPLE_D,
            fill_opacity=0.7,
            stroke_width=1,
            stroke_color=WHITE
        )
        face_group.add(face4)
        
        # 创建边
        edges = [
            [v0, v1],  # 边0-1
            [v0, v2],  # 边0-2
            [v0, v3],  # 边0-3
            [v1, v2],  # 边1-2
            [v1, v3],  # 边1-3
            [v2, v3],  # 边2-3
        ]
        
        edge_group = VGroup()
        for edge in edges:
            start_point = edge[0]
            end_point = edge[1]
            line = Line3D(
                start=start_point,
                end=end_point,
                color=WHITE,
                thickness=0.03
            )
            edge_group.add(line)
        
        # 显示多面体 - 使用Text替换Tex
        new_title = Text("三平面围成的四面体", font_size=36).to_corner(UL)
        self.remove_fixed_in_frame_mobjects(title)
        self.add_fixed_in_frame_mobjects(new_title)
        
        # 先显示面，再显示边，让边更明显
        self.play(FadeIn(face_group))
        self.play(FadeIn(edge_group))
        
        # 添加顶点
        vertex_group = VGroup()
        for point in [v0, v1, v2, v3]:
            vertex = Sphere(
                radius=0.04,
                color=YELLOW
            ).move_to(point)
            vertex_group.add(vertex)
            
        self.play(FadeIn(vertex_group))
        
        # 旋转相机以便查看立体图形
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # 添加文字说明 - 将中文部分和公式分开处理
        explanation_text = Text("这是由", font_size=30).to_edge(DOWN).shift(LEFT * 2.5)
        explanation_formula = MathTex(r"z=y,\ y=x,\ x=1").next_to(explanation_text, RIGHT)
        explanation_text2 = Text("三个平面围成的四面体", font_size=30).next_to(explanation_formula, RIGHT)
        
        self.add_fixed_in_frame_mobjects(explanation_text, explanation_formula, explanation_text2)
        
        self.wait(2)
        
        # 结束动画
        self.play(
            FadeOut(face_group), 
            FadeOut(edge_group), 
            FadeOut(vertex_group), 
            FadeOut(axes), 
            FadeOut(labels)
        )
        
if __name__ == "__main__":
    # 命令行运行：manim -pql three_planes.py ThreePlanesShape
    pass

# 定义 Triangle3D 类，因为manim可能没有内置
class Triangle3D(VGroup):
    def __init__(self, p1, p2, p3, **kwargs):
        super().__init__(**kwargs)
        
        # 创建三角形的三条边
        lines = VGroup(
            Line3D(p1, p2, **kwargs),
            Line3D(p2, p3, **kwargs),
            Line3D(p3, p1, **kwargs)
        )
        
        # 创建三角形的面
        # 使用Surface创建填充的三角形面
        triangle = Surface(
            lambda u, v: p1 * (1 - u - v) + p2 * u + p3 * v,
            u_range=[0, 1],
            v_range=[0, 1 - 1e-6],
            resolution=(8, 8),
            **kwargs
        )
        
        self.add(triangle, lines) 