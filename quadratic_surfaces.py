from manim import *

class QuadraticSurfaces(ThreeDScene):
    def construct(self):
        # 设置场景
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        axes = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            z_length=10
        )
        
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 0.5)
        z_label = axes.get_z_axis_label(Tex("z")).shift(RIGHT * 0.5)
        labels = VGroup(x_label, y_label, z_label)
        
        self.play(FadeIn(axes), FadeIn(labels))
        self.wait(1)
        
        # 展示椭球面 x²/a² + y²/b² + z²/c² = 1
        title = Tex("椭球面 (Ellipsoid)").to_corner(UL)
        equation = MathTex(r"\frac{x^2}{a^2} + \frac{y^2}{b^2} + \frac{z^2}{c^2} = 1").next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, equation)
        
        a, b, c = 3, 2, 1
        ellipsoid = ParametricSurface(
            lambda u, v: np.array([
                a * np.cos(u) * np.sin(v),
                b * np.sin(u) * np.sin(v),
                c * np.cos(v)
            ]),
            u_range=[0, 2 * PI],
            v_range=[0, PI],
            resolution=(20, 20),
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=0.5
        )
        
        self.play(FadeIn(ellipsoid))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(ellipsoid))
        
        # 展示单叶双曲面 x²/a² + y²/b² - z²/c² = 1
        title = Tex("单叶双曲面 (Hyperboloid of One Sheet)").to_corner(UL)
        equation = MathTex(r"\frac{x^2}{a^2} + \frac{y^2}{b^2} - \frac{z^2}{c^2} = 1").next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, equation)
        
        a, b, c = 1, 1, 1
        hyperboloid_one_sheet = ParametricSurface(
            lambda u, v: np.array([
                a * np.cosh(u) * np.cos(v),
                b * np.cosh(u) * np.sin(v),
                c * np.sinh(u)
            ]),
            u_range=[-2, 2],
            v_range=[0, 2 * PI],
            resolution=(20, 20),
            checkerboard_colors=[RED_D, RED_E],
            stroke_width=0.5
        )
        
        self.play(FadeIn(hyperboloid_one_sheet))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(hyperboloid_one_sheet))
        
        # 展示双叶双曲面 x²/a² - y²/b² - z²/c² = 1
        title = Tex("双叶双曲面 (Hyperboloid of Two Sheets)").to_corner(UL)
        equation = MathTex(r"\frac{x^2}{a^2} - \frac{y^2}{b^2} - \frac{z^2}{c^2} = 1").next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, equation)
        
        a, b, c = 1, 1, 1
        hyperboloid_two_sheets_1 = ParametricSurface(
            lambda u, v: np.array([
                a * np.cosh(u),
                b * np.sinh(u) * np.cos(v),
                c * np.sinh(u) * np.sin(v)
            ]),
            u_range=[0.1, 2],
            v_range=[0, 2 * PI],
            resolution=(20, 20),
            checkerboard_colors=[GREEN_D, GREEN_E],
            stroke_width=0.5
        )
        
        hyperboloid_two_sheets_2 = ParametricSurface(
            lambda u, v: np.array([
                -a * np.cosh(u),
                b * np.sinh(u) * np.cos(v),
                c * np.sinh(u) * np.sin(v)
            ]),
            u_range=[0.1, 2],
            v_range=[0, 2 * PI],
            resolution=(20, 20),
            checkerboard_colors=[GREEN_D, GREEN_E],
            stroke_width=0.5
        )
        
        self.play(FadeIn(hyperboloid_two_sheets_1), FadeIn(hyperboloid_two_sheets_2))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(hyperboloid_two_sheets_1), FadeOut(hyperboloid_two_sheets_2))
        
        # 展示双曲抛物面 z = x²/a² - y²/b²
        title = Tex("双曲抛物面 (Hyperbolic Paraboloid)").to_corner(UL)
        equation = MathTex(r"z = \frac{x^2}{a^2} - \frac{y^2}{b^2}").next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, equation)
        
        a, b = 1, 1
        hyperbolic_paraboloid = ParametricSurface(
            lambda u, v: np.array([
                u,
                v,
                u**2/a**2 - v**2/b**2
            ]),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(20, 20),
            checkerboard_colors=[YELLOW_D, YELLOW_E],
            stroke_width=0.5
        )
        
        self.play(FadeIn(hyperbolic_paraboloid))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(hyperbolic_paraboloid))
        
        # 展示椭圆抛物面 z = x²/a² + y²/b²
        title = Tex("椭圆抛物面 (Elliptic Paraboloid)").to_corner(UL)
        equation = MathTex(r"z = \frac{x^2}{a^2} + \frac{y^2}{b^2}").next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, equation)
        
        a, b = 1, 1
        elliptic_paraboloid = ParametricSurface(
            lambda u, v: np.array([
                u,
                v,
                u**2/a**2 + v**2/b**2
            ]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            checkerboard_colors=[PURPLE_D, PURPLE_E],
            stroke_width=0.5
        )
        
        self.play(FadeIn(elliptic_paraboloid))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(elliptic_paraboloid))
        
        # 展示椭圆锥面 z² = x²/a² + y²/b²
        title = Tex("椭圆锥面 (Elliptic Cone)").to_corner(UL)
        equation = MathTex(r"z^2 = \frac{x^2}{a^2} + \frac{y^2}{b^2}").next_to(title, DOWN)
        self.add_fixed_in_frame_mobjects(title, equation)
        
        a, b = 1, 1
        elliptic_cone = ParametricSurface(
            lambda u, v: np.array([
                a * u * np.cos(v),
                b * u * np.sin(v),
                u
            ]),
            u_range=[-2, 2],
            v_range=[0, 2 * PI],
            resolution=(20, 20),
            checkerboard_colors=[TEAL_D, TEAL_E],
            stroke_width=0.5
        )
        
        self.play(FadeIn(elliptic_cone))
        self.wait(1)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.play(FadeOut(elliptic_cone))
        
        self.wait(1)
        self.play(FadeOut(axes), FadeOut(labels))
        
if __name__ == "__main__":
    # 命令行运行：manim -pql quadratic_surfaces.py QuadraticSurfaces
    pass 