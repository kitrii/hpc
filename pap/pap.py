def can_schedule(tasks, processors, D):
    max_loads = [speed * D for speed in processors]
    tasks.sort(reverse=True)

    def backtrack(i, loads):
        if i == len(tasks):
            return True
        for j in range(len(processors)):
            if loads[j] + tasks[i] <= max_loads[j]:
                loads[j] += tasks[i]
                if backtrack(i + 1, loads):
                    return True
                loads[j] -= tasks[i]
        return False

    return backtrack(0, [0] * len(processors))


# --- Ввод данных пользователем ---
def read_list(prompt):
    return list(map(int, input(prompt).strip().split()))


# Ввод
tasks = read_list("Введите количества инструкций для каждого процесса через пробел: ")
processors = read_list("Введите скорости процессоров (инструкций/сек) через пробел: ")
D = int(input("Введите максимальное допустимое время выполнения (в секундах): "))

# Проверка и вывод
if can_schedule(tasks, processors, D):
    print("Можно распределить задачи")
else:
    print("Невозможно распределить задачи")
