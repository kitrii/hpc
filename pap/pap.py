import multiprocessing as mp


def is_valid_distribution(start_index, tasks, processors, max_loads):
    # Попытка распределить задачи, начиная с первого процессора по индексу start_index
    loads = [0] * len(processors)
    return backtrack(tasks, max_loads, loads, 0, start_index)


def backtrack(tasks, max_loads, loads, i, start_index=0):
    if i == len(tasks):
        return True
    for j in range(start_index, len(loads)):
        if loads[j] + tasks[i] <= max_loads[j]:
            loads[j] += tasks[i]
            if backtrack(tasks, max_loads, loads, i + 1):
                return True
            loads[j] -= tasks[i]
    for j in range(start_index):
        if loads[j] + tasks[i] <= max_loads[j]:
            loads[j] += tasks[i]
            if backtrack(tasks, max_loads, loads, i + 1):
                return True
            loads[j] -= tasks[i]
    return False


def can_schedule_parallel(tasks, processors, D):
    max_loads = [p * D for p in processors]
    tasks.sort(reverse=True)

    with mp.Pool(processes=len(processors)) as pool:
        args = [(i, tasks, processors, max_loads) for i in range(len(processors))]
        results = pool.starmap(is_valid_distribution, args)

    return any(results)


# --- Ввод данных пользователем ---
def read_list(prompt):
    return list(map(int, input(prompt).strip().split()))


if __name__ == "__main__":
    mp.freeze_support()  # Для Windows
    tasks = read_list("Введите количества инструкций для каждого процесса через пробел: ")
    processors = read_list("Введите скорости процессоров (инструкций/сек) через пробел: ")
    D = int(input("Введите максимальное допустимое время выполнения (в секундах): "))

    result = can_schedule_parallel(tasks, processors, D)
    print("Можно распределить задачи" if result else "Невозможно распределить задачи")
