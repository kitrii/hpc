import time
from concurrent.futures import ThreadPoolExecutor


# Функция, выполняющая вычисления в каждой итерации
def process_task(i, j, thread_id):
    print(f"Поток {thread_id} выполняет итерации i={i}, j={j}")
    time.sleep(0.1)  # Имитация работы


# Главная функция для параллельного выполнения с collapse
def parallel_for_collapse(n, m, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        thread_id = 0

        # Перебор всех возможных комбинаций (i, j) для collapse
        for i in range(n):
            for j in range(m):
                # Параллельная отправка задач с указанием текущего потока
                futures.append(executor.submit(process_task, i, j, thread_id))
                thread_id = (thread_id + 1) % num_threads  # Циклически меняем потоки

        # Ожидание завершения всех задач
        for future in futures:
            future.result()


# Пример использования
if __name__ == "__main__":
    n, m = 3, 4  # Размеры для двух вложенных циклов
    num_threads = 2  # Количество потоков

    print("Начало выполнения задачи с директивой collapse:")
    parallel_for_collapse(n, m, num_threads)
