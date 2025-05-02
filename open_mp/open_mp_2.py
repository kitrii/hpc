import time
from concurrent.futures import ThreadPoolExecutor


# Функция для выполнения работы с общими векторами
def process_task(start_idx, end_idx, vector1, vector2, result):
    for i in range(start_idx, end_idx):
        result[i] = vector1[i] + vector2[i]


# Функция для выполнения параллельного сложения с shared векторами
def parallel_vector_addition(vector1, vector2):
    n = len(vector1)
    result = [0] * n  # Массив для хранения результатов

    # Определяем количество потоков (параллельных областей)
    num_threads = 4
    chunk_size = n // num_threads  # Разделим работу на части для каждого потока

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []

        # Разделим задачу на несколько частей для каждого потока
        for i in range(num_threads):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < num_threads - 1 else n
            futures.append(executor.submit(process_task, start_idx, end_idx, vector1, vector2, result))

        # Ожидаем завершения всех задач
        for future in futures:
            future.result()

    return result


# Основной блок
if __name__ == "__main__":
    # Пример векторов
    n = 1000000  # Размер векторов
    vector1 = [i for i in range(n)]
    vector2 = [i for i in range(n)]

    # Измеряем время параллельной операции с shared векторами
    start_time = time.time()
    result_parallel = parallel_vector_addition(vector1, vector2)
    end_time = time.time()

    parallel_time = end_time - start_time
    print(f"Время выполнения параллельного сложения с shared векторами: {parallel_time} секунд")

    # Для сравнения выполняем операцию без параллельности
    start_time = time.time()
    result_serial = [vector1[i] + vector2[i] for i in range(n)]
    end_time = time.time()

    serial_time = end_time - start_time
    print(f"Время выполнения последовательного сложения: {serial_time} секунд")

    # Сравниваем время
    print(f"Параллельная версия быстрее на {serial_time - parallel_time} секунд")
