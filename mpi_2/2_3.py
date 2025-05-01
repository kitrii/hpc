from mpi4py import MPI
import numpy as np

# Получаем размер и ранг процесса
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# Разделим процессы на две группы
group1 = size // 2  # Количество процессов в первой группе
group2 = size - group1  # Количество процессов во второй группе

# Разделяем процессы на две группы
if rank < group1:
    group = 1  # Группа 1
else:
    group = 2  # Группа 2

# Первая группа - кольцевая топология (сдвиг в одномерной декартовой топологии)
if group == 1:
    # Используем кольцевую топологию для обмена сообщениями
    left = (rank - 1) % group1  # Ранг слева
    right = (rank + 1) % group1  # Ранг справа

    # Отправляем и принимаем данные
    send_data = np.array([rank], dtype='i')
    recv_data = np.empty(1, dtype='i')

    comm.Sendrecv(sendbuf=send_data, dest=right, recvbuf=recv_data, source=left)

    print(
        f"Процесс {rank} из группы 1 получил {recv_data[0]} от процесса {left} и отправил {send_data[0]} процессу {right}")

# Вторая группа - схема «мастер – рабочие» с топологией графа
if group == 2:
    # Если процесс с рангом 0, то он мастер, остальные - рабочие
    if rank == group1:
        # Мастер (процесс с рангом group1) отправляет сообщение рабочим процессам
        for worker in range(group1 + 1, size):
            comm.send(f"Сообщение от мастера для процесса {worker}", dest=worker)
        print(f"Мастер процесс {rank} отправил сообщения рабочим процессам.")
    else:
        # Рабочие процессы получают сообщения от мастера
        message = comm.recv(source=group1)
        print(f"Процесс {rank} получил: {message}")
