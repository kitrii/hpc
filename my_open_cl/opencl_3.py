import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt

# Настройка OpenCL
ctx = cl.create_some_context()
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

# Бернс-Шиппен
burns_ship = """
    zx = cx;
    zy = cy;
    for(i = 0; i < max_iter; i++) {
        tmp = zx*zx - zy*zy;
        zy = fabs(2.0f * zx * zy) + cy;
        zx = fabs(tmp + cx);
        if(zx*zx + zy*zy > 4.0f) break;
    }
"""

# Ньютона (корни x^3 - 1)
newton = """
float2 roots[3] = {(float2)(1.0f, 0.0f), (float2)(-0.5f, 0.866f), (float2)(-0.5f, -0.866f)};
zx = cx;
zy = cy;
for(i = 0; i < max_iter; i++) {
    float r2 = zx*zx + zy*zy;
    if (r2 == 0.0f) break;

    float denom = 3.0f * (zx*zx - zy*zy)*(zx*zx - zy*zy) + 12.0f*zx*zx*zy*zy + 1e-8f;
    float tmp = zx;
    zx = zx - (zx*zx*zx - 3.0f*zx*zy*zy - 1.0f) / denom;
    zy = zy - (3.0f*tmp*tmp*zy - zy*zy*zy) / denom;

    float dist;
    for (int k = 0; k < 3; k++) {
        dist = hypot(zx - roots[k].x, zy - roots[k].y);
        if (dist < 0.001f) {
            i = i + k * max_iter; // Encode root into brightness
            break;
        }
    }
}

"""

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

# Кантор (приближение через удаление среднего интервала)
cantor = """
float fx = (float)x / width;
float fy = (float)y / height;

int i = 0;
float val = fx;
for(int j = 0; j < max_iter; j++) {
    val *= 3.0f;
    if (val > 1.0f && val < 2.0f) {
        i = max_iter;
        break;
    }
    val = fmod(val, 1.0f);
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
# render_fractal(burns_ship, "Burning Ship")
# render_fractal(newton, "Newton")
# render_fractal(lambert, "Lambert")
render_fractal(cantor, "Cantor")
