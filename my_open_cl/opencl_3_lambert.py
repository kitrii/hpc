import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

# Настройка OpenCL
# === Контекст OpenCL (без выбора вручную) ===
platforms = cl.get_platforms()
devices = platforms[0].get_devices()
ctx = cl.Context(devices)
queue = cl.CommandQueue(ctx)

# Параметры изображения
width, height = 800, 600
max_iter = 100

# Буфер вывода
output = np.empty((height, width), dtype=np.uint8)

# Шаблон ядра OpenCL
kernel_code_template = """
__kernel void fractal(
    __global uchar *output,
    const int width,
    const int height,
    const float zoom,
    const float offset_x,
    const float offset_y,
    const int max_iter) 
{
    int x = get_global_id(0);
    int y = get_global_id(1);
    float zx, zy, tmp;
    float cx = ((float)x - width/2.0f)/zoom + offset_x;
    float cy = ((float)y - height/2.0f)/zoom + offset_y;
    int i = 0;

    {ITERATION_CODE}

    output[y * width + x] = (uchar)(255.0f * i / max_iter);
}
"""

# ======================
# ITERATION CODES FOR FRACTALS
# ======================

# Лямберт (используем exp(x)*x ≈ c)
lambert = """
    zx = cx;
    zy = cy;
    for(i = 0; i < max_iter; i++) {
        float r = sqrt(zx*zx + zy*zy);
        if (r == 0.0f) break;
        float theta = atan2(zy, zx);
        float new_r = log(r);
        zx = new_r * cos(theta);
        zy = new_r * sin(theta);
        if(zx*zx + zy*zy < 1e-6f) break;
    }
"""


# ======================
# РЕНДЕРИНГ ФУНКЦИИ
# ======================

def render_fractal(iteration_code, title):
    kernel_code = kernel_code_template.replace("{ITERATION_CODE}", iteration_code)

    program = cl.Program(ctx, kernel_code).build()
    output_buf = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, output.nbytes)

    program.fractal(
        queue, (width, height), None,
        output_buf,
        np.int32(width), np.int32(height),
        np.float32(300.0), np.float32(0.0), np.float32(0.0),
        np.int32(max_iter)
    )

    cl.enqueue_copy(queue, output, output_buf).wait()
    plt.imshow(output, cmap='inferno')
    plt.title(title)
    plt.axis('off')
    plt.show()


# ======================
# ВЫЗОВ ОТРИСОВКИ
# ======================
render_fractal(lambert, "Lambert")
