from manim import *

class Simple3DScene(ThreeDScene):
    def construct(self):
        # 设置相机角度
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        # 创建一个简单的立方体
        cube = Cube(side_length=2, fill_opacity=0.7)
        
        # 添加坐标轴
        axes = ThreeDAxes()
        
        # 添加标签
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("z")
        
        # 显示所有对象
        self.add(axes, x_label, y_label, z_label)
        self.add(cube)
        
        # 旋转动画
        self.begin_ambient_camera_rotation(rate=0.5)
        self.wait(4)
        self.stop_ambient_camera_rotation() 