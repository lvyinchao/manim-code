import sympy as sp
import numpy as np

print("=== 详细计算验证 ===")
print()

# 定义符号
r, theta = sp.symbols('r theta', real=True)

print("步骤1: 极坐标变换")
print("x = 1/2 + r cos θ")
print("y = 1/2 + r sin θ")
print()

x = sp.Rational(1,2) + r * sp.cos(theta)
y = sp.Rational(1,2) + r * sp.sin(theta)

print("步骤2: 计算被积函数 f = x + y - x² - y²")

# 计算每一项
x_plus_y = x + y
x_squared = sp.expand(x**2)
y_squared = sp.expand(y**2)
x2_plus_y2 = sp.expand(x**2 + y**2)

print(f"x + y = {x_plus_y}")
print(f"x² = {x_squared}")
print(f"y² = {y_squared}")
print(f"x² + y² = {x2_plus_y2}")
print()

f = x_plus_y - x2_plus_y2
f_simplified = sp.simplify(f)
print(f"f = x + y - x² - y² = {f_simplified}")
print()

print("步骤3: 设置极坐标积分")
print("V = ∫₀²π ∫₀^√(1/2) r · f(r,θ) dr dθ")
print(f"  = ∫₀²π ∫₀^√(1/2) r · ({f_simplified}) dr dθ")
print()

# 计算内层积分（对r）
print("步骤4: 计算内层积分 ∫₀^√(1/2) r · (1/2 - r²) dr")
integrand_r = r * f_simplified
print(f"被积函数: {integrand_r}")

# 计算不定积分
antiderivative = sp.integrate(integrand_r, r)
print(f"不定积分: {antiderivative}")

# 计算定积分
r_upper = sp.sqrt(sp.Rational(1,2))
inner_integral = sp.integrate(integrand_r, (r, 0, r_upper))
inner_simplified = sp.simplify(inner_integral)
print(f"定积分 [0, √(1/2)]: {inner_simplified}")
print()

print("步骤5: 计算外层积分 ∫₀²π (1/8) dθ")
print(f"内层积分结果: {inner_simplified}")
print("注意：这个结果不依赖于θ，所以外层积分就是:")
print(f"V = ∫₀²π {inner_simplified} dθ = {inner_simplified} · 2π")

final_result = inner_simplified * 2 * sp.pi
final_simplified = sp.simplify(final_result)
print(f"V = {final_simplified}")
print()

print("步骤6: 数值验证")
print(f"V = {final_simplified} = {float(final_simplified):.6f}")
print(f"π/8 = {float(sp.pi/8):.6f}")
print(f"π/12 = {float(sp.pi/12):.6f}")
print()

print("结论：")
print(f"✅ 正确答案是 V = π/8")
print(f"❌ 之前的 π/12 是错误的") 