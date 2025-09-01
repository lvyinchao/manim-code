from manim import *
import numpy as np
import random

class PointSetTopology(Scene):
    def construct(self):
        # 设置标题
        title = Text("平面点集基本概念", font="SimHei")
        title.to_corner(UL)
        self.play(Write(title))
        self.wait(1)
        
        # 创建坐标系
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_tip": True, "include_numbers": False},
            x_length=10,
            y_length=6
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        
        # 显示坐标系
        self.play(Create(axes), Create(axes_labels))
        self.wait(1)
        
        # 定义一个圆形点集（作为我们研究的主要集合）
        circle = Circle(radius=2, color=BLUE)
        circle.move_to(axes.coords_to_point(0, 0))
        
        # 添加圆形到场景
        self.play(Create(circle))
        
        # 添加集合标签
        set_label = MathTex("A", color=BLUE).next_to(circle, UP)
        self.play(Write(set_label))
        
        # 集合定义：平面点集，不显示具体表示
        set_definition = Text("平面点集A", font="SimHei", font_size=24)
        set_definition.to_corner(UR)
        self.play(Write(set_definition))
        self.wait(1)
        
        # 清除定义
        self.play(FadeOut(set_definition))
        
        # ------ 内点演示 ------
        interior_title = Text("内点", font="SimHei", font_size=32)
        interior_title.to_edge(UP)
        # 淡出主标题，显示内点标题
        self.play(FadeOut(title), Write(interior_title))
        
        # 选择集合内的一点
        interior_point = Dot(axes.coords_to_point(0, 0), color=GREEN)
        interior_label = Text("内点", font="SimHei", font_size=24, color=GREEN).next_to(interior_point, UP)
        
        # 添加这个点到场景
        self.play(Create(interior_point), Write(interior_label))
        
        # 创建邻域小圆
        neighborhood = Circle(radius=0.5, color=GREEN, fill_opacity=0.2)
        neighborhood.move_to(interior_point.get_center())
        
        # 显示邻域
        self.play(Create(neighborhood))
        
        # 内点定义
        interior_def = Text("内点：点p存在一个邻域完全包含在集合A中", font="SimHei", font_size=24)
        interior_def.to_edge(DOWN)
        self.play(Write(interior_def))
        self.wait(2)
        
        # 清除内点说明
        self.play(FadeOut(interior_title), FadeOut(interior_def))
        
        # ------ 外点演示 ------
        exterior_title = Text("外点", font="SimHei", font_size=32)
        exterior_title.to_edge(UP)
        self.play(Write(exterior_title))
        
        # 选择集合外的一点
        exterior_point = Dot(axes.coords_to_point(4, 0), color=RED)
        exterior_label = Text("外点", font="SimHei", font_size=24, color=RED).next_to(exterior_point, UP)
        
        # 添加这个点到场景
        self.play(Create(exterior_point), Write(exterior_label))
        
        # 移动邻域到外点
        self.play(
            neighborhood.animate.set_color(RED).move_to(exterior_point.get_center())
        )
        
        # 外点定义
        exterior_def = Text("外点：点p存在一个邻域完全不与集合A相交", font="SimHei", font_size=24)
        exterior_def.to_edge(DOWN)
        self.play(Write(exterior_def))
        self.wait(2)
        
        # 清除外点说明
        self.play(FadeOut(exterior_title), FadeOut(exterior_def))
        
        # ------ 界点演示 ------
        boundary_title = Text("界点", font="SimHei", font_size=32)
        boundary_title.to_edge(UP)
        self.play(Write(boundary_title))
        
        # 选择圆上的一点（界点）
        boundary_point = Dot(axes.coords_to_point(2, 0), color=YELLOW)
        boundary_label = Text("界点", font="SimHei", font_size=24, color=YELLOW).next_to(boundary_point, RIGHT)
        
        # 添加这个点到场景
        self.play(Create(boundary_point), Write(boundary_label))
        
        # 移动邻域到界点
        self.play(
            neighborhood.animate.set_color(YELLOW).move_to(boundary_point.get_center())
        )
        
        # 界点定义
        boundary_def = Text("界点：点p的任何邻域既包含A中的点，又包含不在A中的点", font="SimHei", font_size=24)
        boundary_def.to_edge(DOWN)
        self.play(Write(boundary_def))
        self.wait(2)
        
        # 清除界点说明和邻域
        self.play(FadeOut(boundary_title), FadeOut(boundary_def), FadeOut(neighborhood))
        
        # ------ 分界展示所有点类型 ------
        all_types_title = Text("点的分类总结", font="SimHei", font_size=32)
        all_types_title.to_edge(UP)
        self.play(Write(all_types_title))
        
        # 添加更多示例点
        more_interior_points = [
            Dot(axes.coords_to_point(-1, 0), color=GREEN),
            Dot(axes.coords_to_point(0, 1), color=GREEN),
            Dot(axes.coords_to_point(1, 1), color=GREEN)
        ]
        
        more_exterior_points = [
            Dot(axes.coords_to_point(-3, 0), color=RED),
            Dot(axes.coords_to_point(0, -3), color=RED),
            Dot(axes.coords_to_point(3, 3), color=RED)
        ]
        
        more_boundary_points = [
            Dot(axes.coords_to_point(0, 2), color=YELLOW),
            Dot(axes.coords_to_point(-2, 0), color=YELLOW),
            Dot(axes.coords_to_point(1.414, 1.414), color=YELLOW)  # 约等于√2
        ]
        
        # 添加这些点到场景
        self.play(
            *[Create(p) for p in more_interior_points],
            *[Create(p) for p in more_exterior_points],
            *[Create(p) for p in more_boundary_points]
        )
        
        # 点的分类说明
        points_summary = Text(
            "绿色：内点 (Interior Points)\n"
            "红色：外点 (Exterior Points)\n"
            "黄色：界点 (Boundary Points)",
            font="SimHei",
            font_size=24
        ).to_corner(DR)
        self.play(Write(points_summary))
        self.wait(2)
        
        # 清除分类说明，保留点
        self.play(FadeOut(all_types_title), FadeOut(points_summary))
        
        # 所有点一起淡出，包括聚点（按照要求修改）
        self.play(
            FadeOut(interior_point),
            FadeOut(interior_label),
            FadeOut(exterior_point),
            FadeOut(exterior_label),
            FadeOut(boundary_point),
            FadeOut(boundary_label),
            *[FadeOut(p) for p in more_interior_points],
            *[FadeOut(p) for p in more_exterior_points],
            *[FadeOut(p) for p in more_boundary_points]
        )
        
        # ------ 聚点演示 ------
        accumulation_title = Text("聚点", font="SimHei", font_size=32)
        accumulation_title.to_edge(UP)
        self.play(Write(accumulation_title))
        
        # 选择圆内的一点作为聚点示例（恢复为原来的位置）
        accum_point = Dot(axes.coords_to_point(-1, 1), color=PURPLE)
        accum_label = Text("聚点", font="SimHei", font_size=24, color=PURPLE).next_to(accum_point, UP)
        
        # 添加聚点到场景
        self.play(Create(accum_point), Write(accum_label))
        
        # 创建聚点邻域
        accum_neighborhood = Circle(radius=0.7, color=PURPLE, fill_opacity=0.2)
        accum_neighborhood.move_to(accum_point.get_center())
        self.play(Create(accum_neighborhood))
        
        # 在邻域内添加一系列点
        accum_points = []
        for _ in range(20):
            r = random.uniform(0, 0.6)
            theta = random.uniform(0, 2 * np.pi)
            x = -1 + r * np.cos(theta)
            y = 1 + r * np.sin(theta)
            point = Dot(axes.coords_to_point(x, y), color=BLUE_A, radius=0.03)
            accum_points.append(point)
        
        # 逐渐添加这些点，展示无限多点的概念
        for point in accum_points:
            self.play(Create(point), run_time=0.1)
        
        # 聚点定义
        accum_def = Text("聚点：点p的任何邻域都包含A中无穷多个点", font="SimHei", font_size=24)
        accum_def.to_edge(DOWN)
        self.play(Write(accum_def))
        self.wait(2)
        
        # 清除聚点演示
        self.play(
            FadeOut(accumulation_title),
            FadeOut(accum_def),
            FadeOut(accum_neighborhood),
            FadeOut(accum_point),
            FadeOut(accum_label),
            *[FadeOut(p) for p in accum_points]
        )
        
        # ------ 孤立点演示 ------
        isolated_title = Text("孤立点", font="SimHei", font_size=32)
        isolated_title.to_edge(UP)
        self.play(Write(isolated_title))
        
        # 创建一个新的离散点集B
        set_B_label = MathTex("B", color=ORANGE).next_to(circle, DOWN+LEFT)
        self.play(Write(set_B_label))
        
        # 创建一些孤立点
        isolated_points = [
            Dot(axes.coords_to_point(-3, -2), color=ORANGE),
            Dot(axes.coords_to_point(3, -1), color=ORANGE),
            Dot(axes.coords_to_point(0, -2.5), color=ORANGE)
        ]
        
        # 添加孤立点到场景
        for point in isolated_points:
            self.play(Create(point))
        
        # 为其中一个孤立点添加标签和邻域
        isolated_label = Text("孤立点", font="SimHei", font_size=24, color=ORANGE).next_to(isolated_points[0], UP)
        self.play(Write(isolated_label))
        
        # 创建孤立点邻域
        isolated_neighborhood = Circle(radius=0.5, color=ORANGE, fill_opacity=0.2)
        isolated_neighborhood.move_to(isolated_points[0].get_center())
        self.play(Create(isolated_neighborhood))
        
        # 孤立点定义
        isolated_def = Text("孤立点：点p存在一个邻域，除p外不包含集合中的其他点", font="SimHei", font_size=24)
        isolated_def.to_edge(DOWN)
        self.play(Write(isolated_def))
        self.wait(2)
        
        # 清除孤立点演示
        self.play(
            FadeOut(isolated_title),
            FadeOut(isolated_def),
            FadeOut(isolated_neighborhood),
            FadeOut(isolated_label),
            FadeOut(set_B_label),
            *[FadeOut(p) for p in isolated_points]
        )
        
        # ------ 开集演示 ------
        open_set_title = Text("开集", font="SimHei", font_size=32)
        open_set_title.to_edge(UP)
        self.play(Write(open_set_title))
        
        # 创建一个开圆（不包含边界）
        open_circle = Circle(radius=2, color=GREEN, stroke_width=3)
        open_circle.move_to(axes.coords_to_point(0, 0))
        
        # 添加开集标签
        open_set_label = MathTex("U", color=GREEN).next_to(circle, UP+RIGHT)
        
        # 动画：把原来的圆变成开圆
        dashed_circle = DashedVMobject(circle.copy(), num_dashes=50)
        dashed_circle.set_color(GREEN)
        self.play(
            ReplacementTransform(circle, dashed_circle),
            Write(open_set_label),
            FadeOut(set_label)
        )
        
        # 在场景中添加一些内点来说明开集
        open_set_interior_points = [
            Dot(axes.coords_to_point(0, 0), color=GREEN),
            Dot(axes.coords_to_point(-1, 0), color=GREEN),
            Dot(axes.coords_to_point(1, 1), color=GREEN)
        ]
        
        self.play(*[Create(p) for p in open_set_interior_points])
        
        # 开集定义
        open_set_def = Text("开集：集合中的每个点都是其内点", font="SimHei", font_size=24)
        open_set_def.to_edge(DOWN)
        self.play(Write(open_set_def))
        self.wait(2)
        
        # 清除开集演示
        self.play(
            FadeOut(open_set_title),
            FadeOut(open_set_def),
            *[FadeOut(p) for p in open_set_interior_points]
        )
        
        # ------ 闭集演示 ------
        closed_set_title = Text("闭集", font="SimHei", font_size=32)
        closed_set_title.to_edge(UP)
        self.play(Write(closed_set_title))
        
        # 恢复为完整圆（包含边界）
        closed_circle = Circle(radius=2, color=BLUE)
        closed_circle.move_to(axes.coords_to_point(0, 0))
        
        # 替换开圆为闭圆
        self.play(
            ReplacementTransform(dashed_circle, closed_circle),
            FadeOut(open_set_label),
            Write(set_label)
        )
        
        # 添加界点
        closed_set_boundary_points = [
            Dot(axes.coords_to_point(2, 0), color=YELLOW),
            Dot(axes.coords_to_point(0, 2), color=YELLOW),
            Dot(axes.coords_to_point(-2, 0), color=YELLOW)
        ]
        
        self.play(*[Create(p) for p in closed_set_boundary_points])
        
        # 闭集定义
        closed_set_def = Text("闭集：包含所有聚点的集合", font="SimHei", font_size=24)
        closed_set_def.to_edge(DOWN)
        self.play(Write(closed_set_def))
        self.wait(2)
        
        # 清除闭集演示的标题和定义，但保留图形元素
        self.play(
            FadeOut(closed_set_title),
            FadeOut(closed_set_def)
        )
        
        # 最终结论
        final_title = Text("平面点集基本概念总结", font="SimHei", font_size=32)
        final_title.to_edge(UP)
        self.play(Write(final_title))
        
        # 删除黄色圆圈，直接添加最终总结文字
        final_summary = Text(
            "• 内点、外点、界点构成了平面上所有点的分类\n"
            "• 聚点是极限点或收敛点，邻域内有无穷多点\n"
            "• 孤立点邻域内没有其他点\n"
            "• 开集内每点都是内点\n"
            "• 闭集包含所有聚点",
            font="SimHei",
            font_size=24
        )
        final_summary.to_edge(DOWN)
        self.play(Write(final_summary))
        self.wait(3)

        # 注意：不清除整个场景，保留最后的显示内容
        self.wait(2)


class PointSetRelationships(Scene):
    def construct(self):
        # 设置标题
        title = Text("点集拓扑概念关系", font="SimHei")
        title.to_corner(UL)
        self.play(Write(title))
        self.wait(1)
        
        # 创建图示框架
        frame = Rectangle(height=6, width=10, color=WHITE)
        
        self.play(Create(frame))
        
        # 创建集合A示意图
        set_A_circle = Circle(radius=2, color=BLUE)
        set_A_circle.move_to(ORIGIN)
        
        # 添加集合标签
        set_A_label = MathTex("A", color=BLUE).next_to(set_A_circle, UP)
        
        self.play(
            Create(set_A_circle),
            Write(set_A_label)
        )
        
        # 创建点集概念之间的关系图
        
        # 定义概念节点
        concepts = {
            "int": {"text": "Int(A)\n内部", "pos": UP * 2 + LEFT * 3, "color": GREEN},
            "ext": {"text": "Ext(A)\n外部", "pos": UP * 2 + RIGHT * 3, "color": RED},
            "bdry": {"text": "Bdry(A)\n边界", "pos": DOWN * 2, "color": YELLOW},
            "cl": {"text": "Cl(A)\n闭包", "pos": UP * 0.5 + LEFT * 3, "color": PURPLE},
            "der": {"text": "A'\n导集", "pos": DOWN * 0.5 + LEFT * 3, "color": ORANGE}
        }
        
        # 创建节点
        nodes = {}
        for key, info in concepts.items():
            node = VGroup(
                Circle(radius=0.5, color=info["color"]),
                Text(info["text"], font="SimHei", font_size=20)
            )
            node.move_to(info["pos"])
            nodes[key] = node
        
        # 显示节点
        for key, node in nodes.items():
            self.play(Create(node), run_time=0.7)
        
        # 定义关系
        relations = [
            {"from": "cl", "to": "int", "text": "包含", "pos_adj": RIGHT * 0.5},
            {"from": "cl", "to": "bdry", "text": "包含", "pos_adj": DOWN * 0.5 + RIGHT * 0.5},
            {"from": "cl", "to": "der", "text": "包含", "pos_adj": DOWN * 0.2},
            {"from": "int", "to": "ext", "text": "互斥", "pos_adj": UP * 0.3},
            {"from": "int", "to": "bdry", "text": "互斥", "pos_adj": RIGHT * 0.3},
            {"from": "ext", "to": "bdry", "text": "互斥", "pos_adj": LEFT * 0.3}
        ]
        
        # 创建关系箭头和标签
        arrows = []
        for rel in relations:
            start = nodes[rel["from"]].get_center()
            end = nodes[rel["to"]].get_center()
            
            # 创建箭头
            if rel["text"] == "互斥":
                # 使用虚线和双箭头表示互斥关系
                arrow = DashedLine(
                    start=start,
                    end=end,
                    color=GRAY
                )
            else:
                # 使用实线箭头表示包含关系
                arrow = Arrow(
                    start=start,
                    end=end,
                    color=WHITE,
                    buff=0.6  # 调整箭头与节点的距离
                )
            
            # 创建关系标签
            mid_point = (start + end) / 2 + rel["pos_adj"]
            label = Text(rel["text"], font="SimHei", font_size=18)
            label.move_to(mid_point)
            
            arrows.append(VGroup(arrow, label))
        
        # 显示关系
        for arrow in arrows:
            self.play(Create(arrow), run_time=0.7)
        
        # 添加重要公式
        formulas = [
            {"tex": r"A = \text{Int}(A) \cup \text{Bdry}(A)", "pos": DOWN * 3 + LEFT * 3},
            {"tex": r"\text{Cl}(A) = A \cup A'", "pos": DOWN * 3 + RIGHT * 3},
            {"tex": r"\text{Int}(A) \cap \text{Bdry}(A) = \emptyset", "pos": DOWN * 3.5}
        ]
        
        formula_objs = []
        for f in formulas:
            formula = MathTex(f["tex"])
            formula.move_to(f["pos"])
            formula_objs.append(formula)
            self.play(Write(formula))
        
        # 最后的概念总结
        summary = Text(
            "内点+边界=集合\n"
            "集合+导集=闭包\n"
            "内部、外部、边界两两互斥",
            font="SimHei",
            font_size=24
        )
        summary.to_edge(DOWN)
        
        self.play(
            FadeOut(set_A_circle),
            FadeOut(set_A_label),
            *[FadeOut(node) for node in nodes.values()],
            *[FadeOut(arrow) for arrow in arrows],
            *[FadeOut(formula) for formula in formula_objs],
            FadeOut(frame)
        )
        
        self.play(Write(summary))
        self.wait(3)
        
        # 结束动画
        self.play(FadeOut(summary), FadeOut(title))
        self.wait(1)


# 运行时请使用以下命令：
# manim -pql point_set_topology.py PointSetTopology
# manim -pql point_set_topology.py PointSetRelationships 