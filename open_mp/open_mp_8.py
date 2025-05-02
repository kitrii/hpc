import time
from concurrent.futures import ThreadPoolExecutor


def task1():
    print("Task 1 started")
    time.sleep(1)
    print("Task 1 finished")


def task2():
    print("Task 2 started")
    time.sleep(2)
    print("Task 2 finished")


def task3():
    print("Task 3 started")
    time.sleep(1)
    print("Task 3 finished")


def task4():
    print("Task 4 started")
    time.sleep(1.5)
    print("Task 4 finished")


# Обёртка для секции: task2 -> task3
def section_2_3():
    task2()
    task3()


if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Параллельный запуск task1, task4 и секции 2+3
        executor.submit(task1)
        executor.submit(section_2_3)
        executor.submit(task4)
