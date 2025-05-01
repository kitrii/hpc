from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# Каждый процесс генерирует одно случайное число от 0 до 100
local_value = random.randint(0, 100)
print(f"[Процесс {rank}] сгенерировал: {local_value}")

# Используем reduce с операцией MAX
max_value = comm.reduce(local_value, op=MPI.MAX, root=0)

# Только процесс 0 выводит результат
if rank == 0:
    print(f"\nМаксимальное значение среди всех процессов: {max_value}")
