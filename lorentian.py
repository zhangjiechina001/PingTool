import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# 洛伦兹分布函数
def lorentzian_fun(x, x0, gamma):
    return 1 / (1 + ((x - x0) / (gamma / 2)) ** 2)

# 生成模拟数据
x_data = np.linspace(0, 10, 100)
y_data = lorentzian_fun(x_data, 5, 2) + np.random.normal(scale=0.1, size=len(x_data))

# 进行洛伦兹拟合
initial_params = [4, 0.8]  # 初始参数值
fit_params, _ = curve_fit(lorentzian_fun, x_data, y_data, p0=initial_params)

# 绘制拟合结果
plt.scatter(x_data, y_data, label='Data')
plt.plot(x_data, lorentzian_fun(x_data, *fit_params), label='Fit')
plt.legend()
plt.show()

print("Fit parameters:")
print("Center:", fit_params[0])
print("Half Width at Half Maximum (HWHM):", fit_params[1])
