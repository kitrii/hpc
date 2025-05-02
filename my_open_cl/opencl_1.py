import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

# === Ввод от пользователя ===
print("Введите правую часть уравнения dy/dt = f(t, y)")
print("Например: -2*y + 1")
user_eq = input("f(t, y) = ")

# === Параметры ===
N = 1000
t0, y0 = 0.0, 1.0
t_end = 5.0
dt = (t_end - t0) / N

# === Контекст OpenCL (без выбора вручную) ===
platforms = cl.get_platforms()
devices = platforms[0].get_devices()
ctx = cl.Context(devices)
queue = cl.CommandQueue(ctx)

# === Подготовка данных ===
t_vals = np.linspace(t0, t_end, N).astype(np.float32)
y_vals = np.zeros(N, dtype=np.float32)
y_vals[0] = y0

mf = cl.mem_flags
t_buf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=t_vals)
y_buf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=y_vals)

# === Создание OpenCL-кода с пользовательским выражением ===
kernel_code_template = """
__kernel void euler_solver(__global const float* t_vals,
                           __global float* y_vals,
                           const float dt, const int N) {{
    int i = get_global_id(0);
    if (i >= N - 1) return;

    float t = t_vals[i];
    float y = y_vals[i];

    // Пользовательская функция
    float dy = {expr};
    y_vals[i + 1] = y + dt * dy;
}}
"""
# Вставка выражения
kernel_code = kernel_code_template.format(expr=user_eq)

# === Компиляция и запуск ===
program = cl.Program(ctx, kernel_code).build()
print("=== OpenCL код ===")
print(kernel_code)
program.euler_solver(queue, (N,), None, t_buf, y_buf, np.float32(dt), np.int32(N))

# === Копирование результата ===
cl.enqueue_copy(queue, y_vals, y_buf)

# === Визуализация ===
plt.figure(figsize=(8, 5))
plt.plot(t_vals, y_vals, label=f"dy/dt = {user_eq}", color="green")
plt.xlabel("t")
plt.ylabel("y(t)")
plt.title("Решение ОДУ методом Эйлера (PyOpenCL)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

for i in range(0, N, N // 10):
    print(f"t = {t_vals[i]:.2f}, y = {y_vals[i]:.4f}")