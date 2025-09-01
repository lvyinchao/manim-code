import os
import subprocess

def combine_videos():
    # 定义视频文件路径
    point_mass_video = "media/videos/diameter_moment_of_inertia/480p15/PointMassInertiaScene.mp4"
    disk_video = "media/videos/diameter_moment_of_inertia/480p15/DiameterMomentOfInertiaScene.mp4"
    output_video = "media/videos/combined_inertia_scene.mp4"
    file_list = "media/videos/file_list.txt"
    
    # 确保视频文件存在
    if not os.path.exists(point_mass_video):
        print(f"错误：找不到质点场景视频: {point_mass_video}")
        print("首先运行: manim -pql diameter_moment_of_inertia.py PointMassInertiaScene")
        return False
    
    if not os.path.exists(disk_video):
        print(f"错误：找不到圆盘场景视频: {disk_video}")
        print("首先运行: manim -pql diameter_moment_of_inertia.py DiameterMomentOfInertiaScene")
        return False
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_video), exist_ok=True)
    
    # 创建文件列表
    with open(file_list, 'w') as f:
        f.write(f"file '{os.path.abspath(point_mass_video)}'\n")
        f.write(f"file '{os.path.abspath(disk_video)}'\n")
    
    # 使用FFmpeg合并视频
    cmd = [
        'ffmpeg', 
        '-y',  # 覆盖输出文件
        '-f', 'concat',  # 使用concat模式
        '-safe', '0',  # 允许绝对路径
        '-i', file_list,  # 输入文件列表
        '-c', 'copy',  # 直接复制流（不重新编码）
        output_video  # 输出文件
    ]
    
    print("执行命令:", ' '.join(cmd))
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 删除临时文件
    if os.path.exists(file_list):
        os.remove(file_list)
    
    if result.returncode == 0:
        print(f"合并完成! 输出文件: {output_video}")
        
        # 自动打开视频（可选）
        if os.name == 'posix':  # macOS或Linux
            subprocess.call(('open', output_video))
        elif os.name == 'nt':  # Windows
            os.startfile(output_video)
        
        return True
    else:
        print("合并失败!")
        print("错误输出:", result.stderr.decode())
        return False

if __name__ == "__main__":
    print("开始合并转动惯量视频...")
    combine_videos() 