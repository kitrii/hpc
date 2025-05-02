import time
from concurrent.futures import ThreadPoolExecutor


# Функция, выполняющая работу в каждой итерации
def process_task(i, thread_id):
    print(f"Поток {thread_id} выполняет итерацию i={i}")
    time.sleep(0.1)  # Имитация работы


# Главная функция для параллельного выполнения с nowait
def parallel_for_nowait(n, num_threads):
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []

        # Параллельный запуск задач в цикле
        for i in range(n):
            thread_id = i % num_threads  # Циклически назначаем потоки
            futures.append(executor.submit(process_task, i, thread_id))

        # Ожидание завершения всех задач (по желанию можно не использовать .result())
        for future in futures:
            future.result()


# Пример использования
if __name__ == "__main__":
    n = 10  # Число итераций цикла
    num_threads = 3  # Количество потоков

    print("Начало выполнения задачи с директивой nowait:")
    parallel_for_nowait(n, num_threads)
