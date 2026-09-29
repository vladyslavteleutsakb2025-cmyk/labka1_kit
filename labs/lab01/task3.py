# Завдання 3: Хешування, збереження у CSV та логування спроб входу у JSON.
import csv
import functools
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Додаємо кореневу директорію проєкту до шляхів пошуку модулів
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from shared.student import (
    GROUP_NAME,
    STUDENT_NAME,
    VARIANT_NUMBER,
)

HASH_ALGORITHM = "sha3_256"
MIN_PASSWORD_LENGTH = 16
PERSONAL_SALT = f"{VARIANT_NUMBER:0>5}"  # Форматує "5" -> "00005"

# Шляхи до файлів
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_CSV_PATH = DATA_DIR / "users.csv"
LOG_JSON_PATH = DATA_DIR / "log.json"


class ValidationError(Exception):
    pass


def generate_hash(password: str, salt: str = "00000") -> str:
    # Генерує шістнадцятковий хеш від конкатенації пароля та солі.
    if not password or not salt:
        raise ValueError("Пароль та сіль не можуть бути порожніми!")

    if len(password) < MIN_PASSWORD_LENGTH:
        raise ValidationError(
            f"Пароль закороткий! Мінімальна довжина: {MIN_PASSWORD_LENGTH} символів."
        )

    data_to_hash = f"{password}{salt}".encode()
    hasher = hashlib.new(HASH_ALGORITHM)
    hasher.update(data_to_hash)
    return hasher.hexdigest()


def log_event(func):
    # Декоратор для логування спроб входу у файл JSON

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        username = args[0] if args else kwargs.get("username", "unknown")
        result_status = "failure"

        try:
            res = func(*args, **kwargs)
            if res:
                result_status = "success"
            return res
        except Exception:
            result_status = "failure"
            raise
        finally:
            log_entry = {
                "event": "login",
                "user": username,
                "result": result_status,
                "timestamp": datetime.now(tz=timezone.utc).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "args": list(args),
                "kwargs": kwargs,
            }

            DATA_DIR.mkdir(parents=True, exist_ok=True)

            logs = []
            if LOG_JSON_PATH.exists():
                try:
                    with open(LOG_JSON_PATH, "r", encoding="utf-8") as f:
                        logs = json.load(f)
                except (json.JSONDecodeError, OSError):
                    logs = []

            logs.append(log_entry)

            with open(LOG_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4, ensure_ascii=False)

    return wrapper


USERS_TO_REGISTER = (
    ("admin_vlad", "SuperSecurePass123!_Extra"),
    ("analyst_alex", "AnalyticalPassword2026!#"),
    ("crypto_guru", "QuantumResistantPass999"),
    ("dev_mike", "DevelopmentAccess#2026_Key"),
    ("sec_officer", "TopSecretClearance_Level5"),
    ("audit_user", "AuditLogCheckingPass#100"),
    ("trainee_john", "ShortPass123!"),  # Не пройде за довжиною (< 16)
    ("guest_user", "GuestAccountValidation#99"),
    ("lead_forensic", "ForensicAnalysisData_2026"),
    ("test_account", "TestingPasswordForLab01_OK"),
)


def create_user(username: str, password: str) -> tuple[str, str]:
    # Створює запис користувача з хешем його пароля
    hash_value = generate_hash(password, PERSONAL_SALT)
    return (username, hash_value)


def create_users(users_list: tuple) -> list[tuple[str, str]]:
    # Обробляє список користувачів та зберігає їх у CSV-файл
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    created_records = []

    for username, password in users_list:
        try:
            record = create_user(username, password)
            created_records.append(record)
        except (ValidationError, ValueError) as e:
            print(f"[ПОМИЛКА РЕЄСТРАЦІЇ] Для {username}: {e}")

    with open(USERS_CSV_PATH, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password_hash"])
        writer.writerows(created_records)

    return created_records


def read_users_db() -> list[dict[str, str]]:
    # Зчитує вміст CSV-файлу та повертає його як список словників
    if not USERS_CSV_PATH.exists():
        raise FileNotFoundError(f"Файл {USERS_CSV_PATH} не знайдено.")

    with open(USERS_CSV_PATH, mode="r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def display_users_table(users_db: list[dict[str, str]]) -> None:
    # Виводить список користувачів у вигляді структурованої таблиці
    print("\n" + "=" * 85)
    print(f"{'Користувач':<20} | {'Хеш пароля (SHA3-256)':<60}")
    print("=" * 85)
    for user in users_db:
        print(f"{user['username']:<20} | {user['password_hash']:<60}")
    print("=" * 85)


@log_event
def login(username: str, password: str) -> bool:
    # Виконує автентифікацію користувача.
    if not username or not password:
        raise ValueError("Логін та пароль не можуть бути порожніми!")

    users_db = read_users_db()
    input_hash = generate_hash(password, PERSONAL_SALT)

    for user in users_db:
        if user["username"] == username:
            return user["password_hash"] == input_hash

    return False


def main():
    # Головна точка входу для демонстрації
    print("=" * 60)
    print(f"Студент: {STUDENT_NAME} | Група: {GROUP_NAME} | Варіант: {VARIANT_NUMBER}")
    print("=" * 60)

    try:
        print(f"Параметри: Хеш = {HASH_ALGORITHM} | Сіль = '{PERSONAL_SALT}'")

        # 1. Реєстрація користувачів
        print("\n1. Реєстрація користувачів та збереження у CSV...")
        create_users(USERS_TO_REGISTER)

        # 2. Читання та відображення бази
        print("\n2. Зчитування бази даних з CSV:")
        users_db = read_users_db()
        display_users_table(users_db)

        # 3. Тестування автентифікації
        print("\n3. Тестування автентифікації (з автоматичним логуванням у JSON):")

        # Успішний вхід
        u1, p1 = "admin_vlad", "SuperSecurePass123!_Extra"
        res1 = login(u1, p1)
        print(f"Вхід {u1}: {'УСПІШНО' if res1 else 'НЕВДАЛО'}")

        # Неправильний пароль
        u2, p2 = "admin_vlad", "WrongPassword123456"
        res2 = login(u2, p2)
        print(f"Вхід {u2} (невірний пароль): {'УСПІШНО' if res2 else 'НЕВДАЛО'}")

        # Неіснуючий користувач
        u3, p3 = "hacker_unknown", "SomeRandomPassword123!"
        res3 = login(u3, p3)
        print(f"Вхід {u3}: {'УСПІШНО' if res3 else 'НЕВДАЛО'}")

        # Тест винятку: порожні дані
        print("\n4. Перевірка обробки винятків (порожній логін):")
        try:
            login("", "SomePassword12345")
        except ValueError as e:
            print(f"[CПІЙМАНО ВИНЯТОК] ValueError: {e}")

    except (OSError, FileNotFoundError, PermissionError) as e:
        print(f"[КРИТИЧНА ПОМИЛКА ФАЙЛОВОЇ СИСТЕМИ]: {e}")
    except (ValidationError, ValueError) as e:
        print(f"[ПОМИЛКА ВАЛІДАЦІЇ/ДАНИХ]: {e}")


if __name__ == "__main__":
    main()
