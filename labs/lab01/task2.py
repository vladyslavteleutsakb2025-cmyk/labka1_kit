# Завдання 2: Система контролю доступу на основі рівнів допуску (MAC/RBAC).

import os
import sys

# Додаємо кореневу директорію проєкту до шляхів пошуку модулів
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from shared.student import (
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)

USERS = {
    "forensic_lead": {
        "role": "forensic_analyst",
        "clearance": 4,
        "department": "Forensics",
        "active": True,
    },
    "compliance_off": {
        "role": "compliance_officer",
        "clearance": 3,
        "department": "Compliance",
        "active": True,
    },
    "trainee_sec": {
        "role": "trainee",
        "clearance": 1,
        "department": "Training",
        "active": True,
    },
    "vendor_tech": {
        "role": "vendor_support",
        "clearance": 2,
        "department": "Vendor",
        "active": True,
    },
    "archived_usr": {
        "role": "archived",
        "clearance": 1,
        "department": "Archive",
        "active": False,
    },
}

RESOURCES = [
    ("forensic_images", 4),
    ("compliance_reports", 3),
    ("training_videos", 1),
    ("vendor_tools", 2),
    ("evidence_locker", 4),
    ("certification_docs", 1),
    ("audit_findings", 3),
    ("chain_of_custody", 4),
    ("support_tickets", 2),
    ("learning_modules", 1),
]

SECURITY_LEVELS = ("Basic", "Standard", "Protected", "Maximum")
BLOCKED_USERS = {"archived_usr", "terminated_vendor", "security_breach"}


def check_access(username: str, resource_name: str, resource_level: int) -> str:
    """Алгоритм перевірки доступу користувача до ресурсу.

    username: ім'я користувача для перевірки.
    resource_name: назва ресурсу.
    resource_level: числовий рівень безпеки ресурсу (1-4).
    return: відформатований рядок з результатом перевірки.
    """
    if username not in USERS:
        return (
            f"user=[{username:<15}] resource=[{resource_name:<20}] "
            "-> DENY (User not found)"
        )

    if username in BLOCKED_USERS:
        return (
            f"user=[{username:<15}] resource=[{resource_name:<20}] "
            "-> DENY (User is blocked)"
        )

    user_data = USERS[username]
    if not user_data.get("active", False):
        return (
            f"user=[{username:<15}] resource=[{resource_name:<20}] "
            "-> DENY (Account inactive)"
        )

    if user_data.get("clearance", 0) >= resource_level:
        return f"user=[{username:<15}] resource=[{resource_name:<20}] -> ALLOW"

    return (
        f"user=[{username:<15}] resource=[{resource_name:<20}] "
        "-> DENY (Insufficient clearance)"
    )


def print_resources_info():
    # Виводить список всіх ресурсів із відповідними текстовими рівнями
    print("=" * 65)
    print(f"СПИСОК РЕСУРСІВ ТА РІВНІВ БЕЗПЕКИ (Варіант {VARIANT_NUMBER})")
    print("=" * 65)
    print(f"{'Ресурс':<25} | {'Словесний рівень':<20} | {'Числовий рівень'}")
    print("-" * 65)
    for res_name, res_level in RESOURCES:
        level_name = SECURITY_LEVELS[res_level - 1]
        print(f"{res_name:<25} | {level_name:<20} | {res_level}")
    print("-" * 65)


def run_access_control():
    # симуляцію та перевірку доступу для всіх тест-кейсів
    print_resources_info()

    print("\n" + "=" * 65)
    print("РЕЗУЛЬТАТИ ПЕРЕВІРКИ ДОСТУПУ (ACCESS CONTROL MATRIX)")
    print("=" * 65)

    # Додаємо тестового користувача, якого немає у бази даних
    users_to_test = list(USERS.keys()) + ["hacker99"]

    for user in users_to_test:
        for res_name, res_level in RESOURCES:
            result = check_access(user, res_name, res_level)
            print(result)
    print("-" * 65)


def main():
    print(
        f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}\n"
    )
    run_access_control()


if __name__ == "__main__":
    main()
