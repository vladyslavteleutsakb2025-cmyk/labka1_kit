import random
import sys
import os

# Підключаємо спільні дані
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from shared.student import STUDENT_NAME, VARIANT_NUMBER


def run_task1():
    print(f"\n--- Завдання 1 (Студент: {STUDENT_NAME}, Варіант: {VARIANT_NUMBER}) ---")

    passwords = ["DataS3cur3!", "123", "Crypto@Analysis", "access", "Security@Pro", "password1", "Adv@nced123",
                 "test123", "Quantum#2023", "guest123"]
    criteria = {"min_length": 12, "require_digits": True, "require_upper": True, "require_special": True}
    forbidden_passwords = {"123", "test123", "access", "password1", "guest123", "admin"}

    # Генеруємо 3 випадкові індекси та дублюємо паролі
    for _ in range(3):
        passwords.append(passwords[random.randint(0, len(passwords) - 1)])

    for pwd in passwords:
        is_forbidden = pwd in forbidden_passwords or len(pwd) < criteria["min_length"]

        has_digit = any(c.isdigit() for c in pwd)
        has_upper = any(c.isupper() for c in pwd)
        has_lower = any(c.islower() for c in pwd)
        has_special = any(not c.isalnum() for c in pwd)

        meets_all = has_digit and has_upper and has_special and has_lower

        if is_forbidden:
            status = "Заборонений"
        elif meets_all and len(pwd) >= criteria["min_length"] + 4 and passwords.count(pwd) == 1:
            status = "Дуже сильний"
        elif meets_all and len(pwd) < criteria["min_length"] + 4:
            status = "Сильний"
        elif has_digit or has_upper or has_special or has_lower:
            status = "Середній"
        else:
            status = "Слабкий"

        print(f"Пароль: {pwd:<15} | Статус: {status}")


if __name__ == "__main__":
    run_task1()
