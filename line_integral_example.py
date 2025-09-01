from manim import *

class LineIntegralExample(Scene):
    def construct(self):
        # 定义参数化曲线 r(t)
        curve = ParametricFunction(
            lambda t: np.array([
                3 * np.cos(t),
                3 * np.sin(t),
                0
            ]),
            t_range=[0, TAU],
            color=BLUE,
        )

        # 添加标题
        title = Text("第一型曲线积分计算过程").to_edge(UP).scale(0.75)
        self.play(Write(title))

        # 显示曲线
        self.play(Create(curve), run_time=2)

        # 分割曲线成 n 段
        n_segments = 8
        segments = VGroup()
        for i in range(n_segments):
            start_point = curve.point_from_proportion(i / n_segments)
            end_point = curve.point_from_proportion((i + 1) / n_segments)
            segment = Line(start=start_point, end=end_point, color=YELLOW)
            segments.add(segment)

        # 展示分割后的曲线段
        self.play(Create(segments), run_time=2)

        # 近似计算每个小段上的函数值
        approximations = VGroup()
        function_values = [np.linalg.norm(np.array([x, y])) for x, y, _ in segments.get_all_points()[::len(segments)]]
        for segment, value in zip(segments, function_values):
            midpoint = segment.get_midpoint()
            approximation_text = MathTex(f"f({midpoint}) \\approx {value:.2f}").next_to(midpoint, UP)
            approximations.add(approximation_text)

        # 展示近似计算结果
        self.play(Write(approximations), run_time=2)

        # 求和并显示总和
        sum_approximation = sum(function_values)
        total_sum_text = MathTex(f"\\sum f(x_i) \\Delta s_i \\approx {sum_approximation:.2f}").to_edge(DOWN).scale(0.75)
        self.play(Write(total_sum_text), run_time=2)

        # 取极限，当n趋向于无穷大
        limit_text = MathTex(r"\lim_{{n \to \infty}} \sum f(x_i) \Delta s_i = \int_C f ds").next_to(total_sum_text, UP).scale(0.75)
        self.play(TransformMatchingShapes(total_sum_text, limit_text), run_time=2)

        # 结束动画
        self.wait(2)

# 渲染动画
if __name__ == "__main__":
    config.background_color = WHITE
    scene = LineIntegralExample()
    scene.render(preview=True)



