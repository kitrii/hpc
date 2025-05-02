import time
from concurrent.futures import ThreadPoolExecutor


# Функция для имитации работы каждого потока
def process_task(level, thread_id):
    print(f"Уровень {level}, Поток {thread_id} начал работу")
    time.sleep(0.5)  # Имитация работы
    print(f"Уровень {level}, Поток {thread_id} завершил работу")


# Функция для параллельного выполнения с вложенными областями
def nested_parallel(level, max_level=3):
    if level > max_level:
        return

    print(f"Начало уровня {level}")

    # На каждом уровне создаём 2 потока
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []

        for thread_id in range(2):
            futures.append(executor.submit(process_task, level, thread_id))

        # Ожидаем завершения всех потоков на текущем уровне
        for future in futures:
            future.result()

        # Рекурсивно вызываем следующий уровень параллельности
        nested_parallel(level + 1)


# Основной блок
if __name__ == "__main__":
    print("Начало программы с трёхуровневыми параллельными областями")
    nested_parallel(1)  # Начинаем с уровня 1
    print("Конец программы с трёхуровневыми параллельными областями")
