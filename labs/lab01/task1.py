# Завдання 1: Комплексний аналізатор надійності паролів.

import os
import random
import sys

# Додаємо кореневу директорію проєкту до шляхів пошуку модулів
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from shared.student import (
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)

PASSWORDS = [
    "DataS3cur3!",
    "123",
    "Crypt0@Analysis",
    "test123",
    "Quantum#2023",
    "access",
    "Secur1ty@Pro",
    "password1",
    "Adv@nced123",
    "guest123",
]

CRITERIA = {
    "min_length": 12,
    "require_digits": True,
    "require_upper": True,
    "require_special": True,
}

FORBIDDEN_PASSWORDS = {
    "123",
    "test123",
    "access",
    "password1",
    "guest123",
    "admin",
}

RANK_FORBIDDEN = "Заборонений"
RANK_WEAK = "Слабкий"
RANK_MEDIUM = "Середній"
RANK_STRONG = "Сильний"
RANK_VERY_STRONG = "Дуже сильний"

REUSE_COUNT = 3
STRONG_LENGTH_BONUS = 4


def simulate_password_reuse(passwords, reuse_count=REUSE_COUNT):
    # Дописує в кінець списку дублікати випадково обраних паролів.
    if not passwords:
        return []

    extended = list(passwords)
    # Використовуємо random.choice або random.randint для симуляції
    random_indices = [random.randint(0, len(passwords) - 1) for _ in range(reuse_count)]
    print(f"Індекси, обрані для повторного використання: {random_indices}\n")
    for index in random_indices:
        extended.append(passwords[index])
    return extended


def _character_flags(password):
    # Повертає словник з ознаками наявності груп символів у паролі.
    return {
        "digit": any(char.isdigit() for char in password),
        "upper": any(char.isupper() for char in password),
        "lower": any(char.islower() for char in password),
        "special": any(not char.isalnum() for char in password),
    }


def _required_groups_status(flags, criteria):
    # Рахує кількість виконаних обов'язкових критеріїв.

    # Повертає кортеж (скільки_виконано, скільки_всього_обов'язкових).
    required_map = {
        "digit": criteria.get("require_digits", False),
        "upper": criteria.get("require_upper", False),
        "special": criteria.get("require_special", False),
    }
    total_required = sum(1 for required in required_map.values() if required)
    met_required = sum(
        1 for group, required in required_map.items() if required and flags[group]
    )
    return met_required, total_required


def evaluate_password(password, criteria, forbidden, frequency):
    """Оцінює надійність одного пароля.

    password: пароль, що оцінюється.
    criteria: словник критеріїв (min_length, require_*).
    forbidden: множина заборонених паролів.
    frequency: скільки разів пароль трапляється у повному
        (розширеному дублікатами) списку.
    """
    min_length = criteria.get("min_length", 8)

    # Перевірка на заборонені паролі та базову довжину
    if password in forbidden or len(password) < min_length:
        return RANK_FORBIDDEN

    flags = _character_flags(password)
    met_required, total_required = _required_groups_status(flags, criteria)
    all_required_met = total_required > 0 and met_required == total_required

    # Визначення рівнів надійності
    if all_required_met:
        long_enough = len(password) >= min_length + STRONG_LENGTH_BONUS
        if long_enough and frequency == 1:
            return RANK_VERY_STRONG
        return RANK_STRONG

    if met_required >= 1:
        return RANK_MEDIUM

    return RANK_WEAK


def analyze_passwords(passwords, criteria, forbidden):
    # Оцінює список паролів (з дублікатами) і повертає результати.
    frequencies = {}
    for pwd in passwords:
        frequencies[pwd] = frequencies.get(pwd, 0) + 1

    results = []
    for pwd in passwords:
        rank = evaluate_password(pwd, criteria, forbidden, frequencies[pwd])
        results.append((pwd, rank))
    return results


def print_report(results):
    # Виводить результати аналізу у вигляді форматованої таблиці.
    header = f"{'№':<3} | {'Пароль':<20} | {'Оцінка надійності'}"
    print(header)
    print("-" * 50)
    for idx, (password, rank) in enumerate(results, 1):
        print(f"{idx:<3} | {password:<20} | {rank}")
    print("-" * 50)


def main():
    # Точка входу для демонстрації роботи аналізатора паролів.
    print("=" * 60)
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    # Встановлюємо фіксований seed для відтворюваності результатів під час запусків
    random.seed(42)

    extended_passwords = simulate_password_reuse(PASSWORDS)
    results = analyze_passwords(extended_passwords, CRITERIA, FORBIDDEN_PASSWORDS)
    print_report(results)


if __name__ == "__main__":
    main()
