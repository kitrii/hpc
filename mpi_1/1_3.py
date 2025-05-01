from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

data = None

# Процесс 0 получает ввод
if rank == 0:
    user_input = input(f"Введите {size} целых чисел через пробел: ")
    numbers = list(map(int, user_input.strip().split()))

    if len(numbers) != size:
        print(f"Ошибка: нужно ввести ровно {size} чисел.")
        numbers = None
else:
    numbers = None

# Рассылаем числа по одному на каждый процесс
scattered_number = comm.scatter(numbers, root=0)

# Каждый процесс увеличивает число на 1
processed_number = scattered_number + 1

# Собираем обработанные числа обратно на процесс 0
gathered_numbers = comm.gather(processed_number, root=0)

# Процесс 0 выводит результат
if rank == 0:
    print(f"\nИсходные числа:  {numbers}")
    print(f"Обновлённые числа: {gathered_numbers}")

# запускаемся mpirun -n 4 python mpi_1/1_3.py -> вводим 4 целых чисел (кол-во чисел = числу процессов -n)
