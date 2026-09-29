import os
import sys

# Додаємо кореневу директорію проєкту до шляхів пошуку модулів
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from labs.lab01.task1 import main as run_task1
from labs.lab01.task2 import run_access_control
from labs.lab01.task3 import main as run_task3
from shared.student import (
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)


def main():
    print("=" * 70)
    print(f"ЛАБОРАТОРНА РОБОТА №1 | Студент: {STUDENT_NAME}")
    print(f"Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 70)

    print("\n>>> ЗАПУСК ЗАВДАННЯ 1: Аналіз паролів")
    run_task1()

    print("\n>>> ЗАПУСК ЗАВДАННЯ 2: Контроль доступу")
    run_access_control()

    print("\n>>> ЗАПУСК ЗАВДАННЯ 3: Хешування, CSV та JSON-логування")
    run_task3()


if __name__ == "__main__":
    main()
