from manim import *

class DoubleIntegralScene(ThreeDScene):
    def construct(self):
        # Set up the axes and the grid
        axes = ThreeDAxes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            z_range=[0, 15],
            axis_config={"color": BLUE},
        )

        # Create the surface for f(x, y) = x^2 + y^2
        surface = Surface(
            lambda u, v: axes.c2p(u, v, u**2 + v**2),  # f(x, y) = x^2 + y^2
            u_range=[-2, 2],
            v_range=[-2, 2],
            checkerboard_colors=[BLUE_D, BLUE_E],
        )

        # Add the axes and the surface to the scene
        self.play(Create(axes))
        self.play(Create(surface))

        # Highlight the region of integration (a rectangle for simplicity)
        rect = Rectangle(
            width=4, height=4, color=RED, fill_opacity=0.3
        ).move_to(axes.c2p(0, 0, 0))

        self.play(Create(rect))

        # Show small squares (approximation of Riemann sum)
        self.show_riemann_sum(axes, rect)

        # Fade out surface and axes to focus on sum approximation
        self.play(FadeOut(surface), FadeOut(axes))

        # Show the sum becoming more precise (with smaller rectangles)
        self.show_limit_of_riemann_sum(axes, rect)

    def show_riemann_sum(self, axes, rect):
        # Create a grid of small squares for the approximation
        squares = VGroup()
        for i in range(-1, 2):
            for j in range(-1, 2):
                square = Square(side_length=1, color=WHITE, fill_opacity=0.5).move_to(
                    axes.c2p(i, j, 0)
                )
                squares.add(square)
        
        self.play(Create(squares))
        
        # Animate the height of squares based on the function f(x, y) = x^2 + y^2
        for square in squares:
            x, y, z = square.get_center()
            height = x**2 + y**2
            square.generate_target()
            square.target = square.copy().shift(UP * height)  # Shift the square to the correct height
            self.play(MoveToTarget(square))
        
        # Sum approximation visual (use a label for simplicity)
        self.play(Write(Text("Sum Approximation").next_to(squares, UP)))

    def show_limit_of_riemann_sum(self, axes, rect):
        # Now create smaller rectangles (approaching infinitesimal width/height)
        small_squares = VGroup()
        for i in range(-5, 6):
            for j in range(-5, 6):
                small_square = Square(side_length=0.4, color=WHITE, fill_opacity=0.5).move_to(
                    axes.c2p(i * 0.4, j * 0.4, 0)
                )
                small_squares.add(small_square)
        
        self.play(Create(small_squares))

        # Animate the heights of these small squares
        for small_square in small_squares:
            x, y, z = small_square.get_center()
            height = x**2 + y**2
            small_square.generate_target()
            small_square.target = small_square.copy().shift(UP * height)  # Move to the height position
            self.play(MoveToTarget(small_square))
        
        # Fade in the idea of the limit
        self.play(Write(Text("Limit as Δx, Δy -> 0").next_to(small_squares, UP)))
        
        # Show final animation (integral result)
        self.play(FadeOut(small_squares))

        # Display the result
        result_text = Text("Double Integral Result: Volume", font_size=36).shift(UP * 3)
        self.play(Write(result_text))

