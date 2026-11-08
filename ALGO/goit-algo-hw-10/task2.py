import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

def f(x):
    return x**2

a = 0
b = 2
max_y = f(b)

n_points = 100000

x_random = np.random.uniform(a, b, n_points)
y_random = np.random.uniform(0, max_y, n_points)

points_under = y_random <= f(x_random)

area_rectangle = (b - a) * max_y
integral_mc = area_rectangle * np.sum(points_under) / n_points

integral_exact, error = spi.quad(f, a, b)

print(f"Метод Монте-Карло (n={n_points}): {integral_mc:.6f}")
print(f"Точне значення інтеграла: {integral_exact:.6f}")
print(f"Абсолютна похибка: {abs(integral_exact - integral_mc):.6f}")
print(f"Відносна похибка: {abs(integral_exact - integral_mc)/integral_exact*100:.4f}%")

plt.figure(figsize=(10, 6))
plt.plot(x_random[points_under], y_random[points_under], 'g.', alpha=0.1, label='Точки під кривою')
plt.plot(x_random[~points_under], y_random[~points_under], 'r.', alpha=0.1, label='Точки над кривою')

x = np.linspace(a-0.5, b+0.5, 400)
plt.plot(x, f(x), 'b-', linewidth=2, label='f(x) = x²')

plt.axvline(x=a, color='gray', linestyle='--')
plt.axvline(x=b, color='gray', linestyle='--')
plt.title(f'Метод Монте-Карло для інтеграла f(x) = x² від {a} до {b}')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.legend()
plt.grid(True)
plt.show()