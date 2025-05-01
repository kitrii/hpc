from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Количество случайных точек на каждом процессе
N = 1000

# Генерация точек и подсчёт попаданий в круг
inside = 0
for _ in range(N):
    x, y = random.random(), random.random()
    if x*x + y*y <= 1.0:
        inside += 1

# Каждый процесс отправляет всем остальным одно и то же число (своё "inside")
send_data = [inside for _ in range(size)]  # каждый процесс отправляет своё значение всем

# Получение данных от всех процессов
recv_data = comm.alltoall(send_data)

# Суммируем все полученные значения
total_inside = sum(recv_data)
total_points = N * size

# Приближённое значение Пи
pi_approx = 4 * total_inside / total_points

# Вывод
print(f"[Процесс {rank}]")
print(f"  Своё значение: {inside}")
print(f"  Полученные от других: {recv_data}")
print(f"  Приближённое π: {pi_approx}\n")

# запускаемся mpirun -n 4 python mpi_1/1_1.py -> вводим целое число
