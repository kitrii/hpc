import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

# Параметры
num_points = 1000000  # Число точек для генерации

# Подготовка OpenCL-контекста
platforms = cl.get_platforms()
devices = platforms[0].get_devices()
ctx = cl.Context(devices)
queue = cl.CommandQueue(ctx)

# Генерация случайных точек
np.random.seed(42)
x_vals = np.random.uniform(-1, 1, num_points).astype(np.float32)
y_vals = np.random.uniform(-1, 1, num_points).astype(np.float32)

# Буферы OpenCL
mf = cl.mem_flags
x_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=x_vals)
y_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=y_vals)
inside_circle_buf = cl.Buffer(ctx, mf.WRITE_ONLY, num_points * np.float32(0).nbytes)

# Шаблон ядра
kernel_code = """
__kernel void monte_carlo_pi(__global const float* x_vals,
                             __global const float* y_vals,
                             __global float* inside_circle,
                             const int num_points) {
    int i = get_global_id(0);
    if (i >= num_points) return;

    float x = x_vals[i];
    float y = y_vals[i];

    // Проверяем, находится ли точка в круге
    float distance_squared = x * x + y * y;
    inside_circle[i] = (distance_squared <= 1.0f) ? 1.0f : 0.0f;
}
"""

# Компиляция ядра
program = cl.Program(ctx, kernel_code).build()

# Вызов ядра
global_size = (num_points,)
program.monte_carlo_pi(queue, global_size, None, x_buf, y_buf, inside_circle_buf, np.int32(num_points))

# Копируем результат в хост-память
inside_circle = np.zeros(num_points, dtype=np.float32)
cl.enqueue_copy(queue, inside_circle, inside_circle_buf).wait()

# Вычисляем приближённое значение числа Pi
points_inside_circle = np.sum(inside_circle)
pi_estimate = 4 * points_inside_circle / num_points

# Выводим результат
print(f"Приближённое значение числа Pi: {pi_estimate}")

# Визуализация (по желанию)
plt.figure(figsize=(6, 6))
plt.scatter(x_vals[inside_circle == 1], y_vals[inside_circle == 1], color="cyan", s=1, label="Inside circle")
plt.scatter(x_vals[inside_circle == 0], y_vals[inside_circle == 0], color="magenta", s=1, label="Outside circle")
plt.gca().set_aspect('equal', adjustable='box')
plt.title(f"Приближённое значение Pi: {pi_estimate}")
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid(True)
plt.show()
