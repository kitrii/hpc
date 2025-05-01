from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt


def initialize_grid(size):
    """Инициализация сетки с волной в центре."""
    grid = np.zeros(size)
    grid[size // 2] = 1  # Начальная волна в центре
    return grid


def print_grid(grid, rank):
    """Вывод сетки для текущего процесса."""
    print(f"Процесс {rank}:")
    print(grid)
    print()


def update_wave(grid, left, right, rank, size, comm):
    """Обновление состояния волны с учетом периодических граничных условий."""
    new_grid = grid.copy()

    # Граничные условия
    # Соседние значения для периодических границ
    new_grid[0] = grid[1]  # Периодическая граница слева
    new_grid[size - 1] = grid[size - 2]  # Периодическая граница справа

    # Распространение волны
    for i in range(1, size - 1):
        new_grid[i] = grid[i] + (grid[i - 1] - 2 * grid[i] + grid[i + 1])  # Простое обновление для волны

    # Обмен данными с соседями через MPI
    # Создаем массивы для граничных значений
    send_left = np.array([grid[0]], dtype=np.float64)
    send_right = np.array([grid[size - 1]], dtype=np.float64)
    recv_left = np.array([0.0], dtype=np.float64)
    recv_right = np.array([0.0], dtype=np.float64)

    # Обмен данными с соседями
    comm.Sendrecv(sendbuf=send_right, dest=right, recvbuf=recv_left, source=left)
    comm.Sendrecv(sendbuf=send_left, dest=left, recvbuf=recv_right, source=right)

    # Обновляем граничные значения
    new_grid[0] = recv_left[0]
    new_grid[size - 1] = recv_right[0]

    return new_grid


def main():
    # Инициализация MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Размер сетки для каждого процесса
    grid_size = 100  # Размер глобальной сетки
    local_size = grid_size // size  # Размер локальной сетки для каждого процесса

    # Инициализация сетки
    grid = initialize_grid(local_size)

    # Определяем соседей для периодических границ
    left = (rank - 1) % size
    right = (rank + 1) % size

    # Количество шагов
    steps = 50

    # Этап распространения волны
    for step in range(steps):
        grid = update_wave(grid, left, right, rank, local_size, comm)
        if step % 10 == 0:
            print(f"Шаг {step}:")
            print_grid(grid, rank)

    # После завершения моделирования, выводим итоговое состояние для каждого процесса
    print(f"Конечное состояние для процесса {rank}:")
    print_grid(grid, rank)

    # Визуализация для первого процесса
    if rank == 0:
        plt.plot(grid)
        plt.title("Конечное состояние волны")
        plt.xlabel("Позиция")
        plt.ylabel("Амплитуда")
        plt.show()


if __name__ == "__main__":
    main()
