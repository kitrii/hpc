import numpy as np
from concurrent.futures import ThreadPoolExecutor


# Функция, которая будет выполняться в каждой итерации цикла
def square_sum(start, end, data):
    partial_sum = 0
    for i in range(start, end):
        partial_sum += data[i] ** 2
    return partial_sum


# Главная функция
def parallel_sum_of_squares(data, num_threads):
    # Разделим данные на блоки для каждого потока
    chunk_size = len(data) // num_threads
    futures = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # Запускаем параллельно вычисления для каждого блока данных
        for i in range(num_threads):
            start = i * chunk_size
            # Для последнего блока добавим остаток, если есть
            end = (i + 1) * chunk_size if i != num_threads - 1 else len(data)
            futures.append(executor.submit(square_sum, start, end, data))

        # Получаем результаты всех потоков и выполняем редукцию (сложение)
        total_sum = sum(f.result() for f in futures)

    return total_sum


# Пример использования
if __name__ == "__main__":
    # Генерация массива случайных чисел
    data = np.random.randint(1, 100, size=1000000)

    # Определяем количество потоков
    num_threads = 4

    # Параллельное вычисление суммы квадратов
    total_sum = parallel_sum_of_squares(data, num_threads)

    print(f"Сумма квадратов чисел: {total_sum}")
