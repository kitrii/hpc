import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

# Размер изображения
width, height = 800, 200
depth = 6

# OpenCL ядро
kernel_code = """
__kernel void cantor_set(
    __global uchar4 *output,
    const int width,
    const int height,
    const int max_depth)
{
    int x = get_global_id(0);
    int y = get_global_id(1);

    float fx = (float)x / (float)width;
    int level = y / (height / max_depth);

    if (level >= max_depth)
        return;

    int in_cantor = 1;
    float pos = fx;

    for (int i = 0; i < level; i++) {
        float scaled = pos * 3.0f;
        if (scaled >= 1.0f && scaled < 2.0f) {
            in_cantor = 0;
            break;
        }
        pos = fmod(scaled, 1.0f);
    }

    int idx = y * width + x;
    if (in_cantor) {
        output[idx] = (uchar4)(0, 0, 0, 255); // черный
    } else {
        output[idx] = (uchar4)(255, 255, 255, 255); // белый
    }
}
"""

# Подготовка контекста
# === Контекст OpenCL (без выбора вручную) ===
platforms = cl.get_platforms()
devices = platforms[0].get_devices()
ctx = cl.Context(devices)
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

# Буфер вывода
output_np = np.zeros((height, width, 4), dtype=np.uint8)
output_buf = cl.Buffer(ctx, mf.WRITE_ONLY, output_np.nbytes)

# Построение и запуск
program = cl.Program(ctx, kernel_code).build()
program.cantor_set(queue, (width, height), None,
                   output_buf,
                   np.int32(width),
                   np.int32(height),
                   np.int32(depth))

# Копирование результата на хост
cl.enqueue_copy(queue, output_np, output_buf)

# Отображение
plt.imshow(output_np)
plt.title("Множество Кантора (GPU через PyOpenCL)")
plt.axis("off")
plt.show()
