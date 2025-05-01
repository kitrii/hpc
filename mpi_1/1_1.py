from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

if rank == 0:
    # Процесс с рангом 0 запрашивает у пользователя ввод
    try:
        user_input = input("Введите целое число: ")
        user_input = int(user_input)
    except ValueError:
        print("Ошибка: введено не целое число.")
        user_input = 0  # Можно также завершить выполнение или повторно запросить ввод
else:
    user_input = None

# Распространяем значение user_input от процесса 0 ко всем остальным
user_input = comm.bcast(user_input, root=0)

# Каждый процесс выводит свой ранг и полученное значение
print(f"Процесс {rank} получил значение: {user_input}")

# запускаемся mpirun -n 4 python mpi_1/1_1.py -> вводим целое число
