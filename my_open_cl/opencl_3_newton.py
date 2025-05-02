import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

# Размер изображения
width, height = 800, 800
max_iter = 50

# OpenCL ядро
kernel_code = """
__kernel void newton_fractal(
    __global float2* output,
    const int width,
    const int height,
    const int max_iter,
    const float zoom,
    const float moveX,
    const float moveY)
{
    int gid_x = get_global_id(0);
    int gid_y = get_global_id(1);

    float x0 = ((float)gid_x - width / 2.0f) / zoom + moveX;
    float y0 = ((float)gid_y - height / 2.0f) / zoom + moveY;

    float2 z = (float2)(x0, y0);
    float2 roots[3] = {(float2)(1.0f, 0.0f), (float2)(-0.5f, 0.866f), (float2)(-0.5f, -0.866f)};

    for (int i = 0; i < max_iter; i++) {
        float r2 = z.x*z.x + z.y*z.y;
        float denom = 3*(z.x*z.x - z.y*z.y)*(z.x*z.x + z.y*z.y) + 1e-6f;
        float2 f = (float2)(
            z.x*z.x*z.x - 3*z.x*z.y*z.y - 1,
            3*z.x*z.x*z.y - z.y*z.y*z.y
        );
        float2 df = (float2)(
            3*z.x*z.x - 3*z.y*z.y,
            6*z.x*z.y
        );
        float denom2 = df.x*df.x + df.y*df.y;
        z.x = z.x - (f.x*df.x + f.y*df.y) / denom2;
        z.y = z.y - (f.y*df.x - f.x*df.y) / denom2;
    }

    int index = gid_y * width + gid_x;
    output[index] = z;
}
"""

# Настройка PyOpenCL
# === Контекст OpenCL (без выбора вручную) ===
platforms = cl.get_platforms()
devices = platforms[0].get_devices()
ctx = cl.Context(devices)
queue = cl.CommandQueue(ctx)
mf = cl.mem_flags

# Параметры
zoom = 250.0
moveX, moveY = 0.0, 0.0

output_np = np.zeros((height * width, 2), dtype=np.float32)
output_buf = cl.Buffer(ctx, mf.WRITE_ONLY, output_np.nbytes)

# Построение программы и запуск ядра
program = cl.Program(ctx, kernel_code).build()
program.newton_fractal(queue, (width, height), None,
                       output_buf,
                       np.int32(width), np.int32(height),
                       np.int32(max_iter),
                       np.float32(zoom),
                       np.float32(moveX), np.float32(moveY))

cl.enqueue_copy(queue, output_np, output_buf)

# Постобработка и отображение
roots = [1 + 0j, -0.5 + 0.866j, -0.5 - 0.866j]


def get_root_index(z):
    z_complex = z[0] + 1j * z[1]
    dists = [abs(z_complex - r) for r in roots]
    return np.argmin(dists)


colors = np.array([get_root_index(z) for z in output_np])
image = colors.reshape((height, width))

plt.imshow(image, cmap="twilight", extent=[-2, 2, -2, 2])
plt.title("Множество Ньютона")
plt.axis("off")
plt.show()
