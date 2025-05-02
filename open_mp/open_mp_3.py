import os
import time
from concurrent.futures import ThreadPoolExecutor


# Функция для имитации работы потока
def process_task(thread_id):
    print(f"Поток {thread_id} начал работу")
    time.sleep(0.1)  # Имитация работы
    print(f"Поток {thread_id} завершил работу")


# Функция для определения максимального количества потоков
def get_max_threads():
    # Получаем количество доступных процессоров/ядер в системе
    max_threads = os.cpu_count()  # Получаем количество логических ядер
    return max_threads


# Функция для выполнения задач с максимальным количеством потоков
def execute_max_threads():
    max_threads = get_max_threads()
    print(f"Максимальное количество потоков, которое может быть запущено: {max_threads}")

    # Запускаем пул с максимальным количеством потоков
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = []

        # Создаём задачи для каждого потока
        for thread_id in range(max_threads):
            futures.append(executor.submit(process_task, thread_id))

        # Ожидаем завершения всех задач
        for future in futures:
            future.result()


# Основной блок
if __name__ == "__main__":
    execute_max_threads()
