from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = None

if rank == 0:
    user_input = input("Введите целые числа через пробел (ровно {} чисел): ".format(size))
    numbers = list(map(int, user_input.strip().split()))
    if len(numbers) != size:
        print(f"Ошибка: вы должны ввести ровно {size} чисел.")
        numbers = None
else:
    numbers = None

# Распространяем список с помощью scatter
received_number = comm.scatter(numbers, root=0)

print(f"[Процесс {rank}] получил число: {received_number}")

# запускаемся mpirun -n 4 python mpi_1/1_2.py -> вводим 4 целых чисел (кол-во чисел = числу процессов -n)
