import numpy as np
from scipy import integrate
import sympy as sp

print("=== 体积计算验证 ===")
print()

# 题目：计算由 z = x² + y² 和 z = x + y 围成的立体体积

print("1. 找交线：x² + y² = x + y")
print("   即：x² - x + y² - y = 0")
print("   配方：(x - 1/2)² - 1/4 + (y - 1/2)² - 1/4 = 0")
print("   简化：(x - 1/2)² + (y - 1/2)² = 1/2")
print("   这是圆心在(1/2, 1/2)，半径为√(1/2)的圆")
print()

# 检查上下限关系
print("2. 检查z的上下限关系：")
# 在交线上的点
x_test, y_test = 0.5 + np.sqrt(0.5)*np.cos(0), 0.5 + np.sqrt(0.5)*np.sin(0)
z1 = x_test**2 + y_test**2  # 抛物面
z2 = x_test + y_test        # 平面
print(f"   测试点：({x_test:.3f}, {y_test:.3f})")
print(f"   抛物面：z = {z1:.3f}")
print(f"   平面：z = {z2:.3f}")

# 在圆心处
x_center, y_center = 0.5, 0.5
z1_center = x_center**2 + y_center**2
z2_center = x_center + y_center
print(f"   圆心：({x_center}, {y_center})")
print(f"   抛物面：z = {z1_center}")
print(f"   平面：z = {z2_center}")
print(f"   平面在上方：{z2_center > z1_center}")
print()

print("3. 设置三重积分：")
print("   V = ∫∫∫ dV = ∫∫_D ∫_{x²+y²}^{x+y} dz dx dy")
print("   = ∫∫_D (x + y - x² - y²) dx dy")
print()

print("4. 极坐标变换：")
print("   x = 1/2 + r cos θ")
print("   y = 1/2 + r sin θ")
print("   雅可比行列式：r")
print("   积分区域：0 ≤ r ≤ √(1/2), 0 ≤ θ ≤ 2π")
print()

print("5. 计算被积函数 f(r,θ) = x + y - x² - y²：")

# 符号计算
r, theta = sp.symbols('r theta', real=True, positive=True)
x = sp.Rational(1,2) + r * sp.cos(theta)
y = sp.Rational(1,2) + r * sp.sin(theta)

f = x + y - x**2 - y**2
f_expanded = sp.expand(f)
print(f"   f(r,θ) = {f_expanded}")

# 简化
f_simplified = sp.simplify(f_expanded)
print(f"   简化后：f(r,θ) = {f_simplified}")
print()

print("6. 验证我们动画中的表达式：")
# 动画中的表达式
print("   动画中：f(r,θ) = 1 + r cos θ + r sin θ - r²/2")
f_animation = 1 + r*sp.cos(theta) + r*sp.sin(theta) - r**2/2
print(f"   符号形式：{f_animation}")
print(f"   是否相等：{sp.simplify(f_simplified - f_animation) == 0}")
print()

if sp.simplify(f_simplified - f_animation) != 0:
    print("❌ 发现错误！让我重新计算...")
    print(f"   正确的 f(r,θ) = {f_simplified}")
    
    # 手工展开验证
    print("\n   手工验证：")
    x_expr = sp.Rational(1,2) + r * sp.cos(theta)
    y_expr = sp.Rational(1,2) + r * sp.sin(theta)
    
    print(f"   x = {x_expr}")
    print(f"   y = {y_expr}")
    print(f"   x² = {sp.expand(x_expr**2)}")
    print(f"   y² = {sp.expand(y_expr**2)}")
    print(f"   x + y = {x_expr + y_expr}")
    print(f"   x² + y² = {sp.expand(x_expr**2 + y_expr**2)}")
    print(f"   x + y - x² - y² = {sp.expand((x_expr + y_expr) - (x_expr**2 + y_expr**2))}")

print()
print("7. 数值验证积分：")

def integrand(r, theta):
    """正确的被积函数"""
    return r * (1 + r*np.cos(theta) + r*np.sin(theta) - r**2)

# 数值积分
result, error = integrate.dblquad(
    lambda r, theta: integrand(r, theta),
    0, 2*np.pi,  # theta 范围
    lambda theta: 0, lambda theta: np.sqrt(0.5)  # r 范围
)

print(f"   数值积分结果：{result:.6f}")
print(f"   π/12 ≈ {np.pi/12:.6f}")
print(f"   相对误差：{abs(result - np.pi/12)/(np.pi/12)*100:.2f}%")
print()

print("8. 解析积分验证：")
# 符号积分
r_max = sp.sqrt(sp.Rational(1,2))
integral = sp.integrate(
    r * f_simplified,
    (r, 0, r_max),
    (theta, 0, 2*sp.pi)
)
integral_value = sp.simplify(integral)
print(f"   解析积分结果：{integral_value}")
print(f"   π/12 = {sp.pi/12}")
print(f"   是否等于 π/12：{sp.simplify(integral_value - sp.pi/12) == 0}") 