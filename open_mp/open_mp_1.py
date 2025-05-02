import numpy as np
import time
from concurrent.futures import ThreadPoolExecutor


# Функция для выполнения параллельного сложения двух векторов
def vector_addition(start_idx, end_idx, vector1, vector2, result):
    for i in range(start_idx, end_idx):
        result[i] = vector1[i] + vector2[i]


# Основная функция для выполнения параллельного сложения
def parallel_vector_addition(vector1, vector2):
    n = len(vector1)
    result = np.zeros(n)  # Массив для хранения результата

    # Определяем количество потоков
    num_threads = 8  # Количество потоков (можно изменить в зависимости от системы)
    chunk_size = n // num_threads  # Разделяем работу на части для каждого потока

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []

        # Разделяем задачу на несколько частей для каждого потока
        for i in range(num_threads):
            start_idx = i * chunk_size
            end_idx = (i + 1) * chunk_size if i < num_threads - 1 else n
            futures.append(executor.submit(vector_addition, start_idx, end_idx, vector1, vector2, result))

        # Ожидаем завершения всех задач
        for future in futures:
            future.result()

    return result


# Основной блок
if __name__ == "__main__":
    # Размер векторов (50 миллионов)
    n = 50_000_000

    # Генерация случайных вещественных чисел для векторов
    vector1 = np.random.random(n)
    vector2 = np.random.random(n)

    # Измеряем время параллельного сложения
    start_time = time.time()
    result_parallel = parallel_vector_addition(vector1, vector2)
    end_time = time.time()

    parallel_time = end_time - start_time
    print(f"Время выполнения параллельного сложения: {parallel_time:.6f} секунд")

    # Выводим размер и один элемент результирующего вектора
    print(f"Размер результирующего вектора: {len(result_parallel)}")
    print(f"Первый элемент результирующего вектора: {result_parallel[0]:.6f}")
