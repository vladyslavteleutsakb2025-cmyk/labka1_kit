import hashlib
import csv
import json
import os
from datetime import datetime


class ValidationError(Exception):
    pass


def generate_hash(password: str, salt: str = "00000") -> str:
    if not password or not salt:
        raise ValueError("Пароль або сіль не можуть бути порожніми")
    if len(password) < 16:
        raise ValidationError("Пароль занадто короткий для цього варіанта")

    hasher = hashlib.sha3_256()
    hasher.update((password + salt).encode('utf-8'))
    return hasher.hexdigest()


def log_event(func):
    def wrapper(username, password):
        result = func(username, password)
        status = "success" if result else "failure"
        log_data = {
            "event": "login",
            "user": username,
            "result": status,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "args": [],
            "kwargs": {}
        }

        os.makedirs("labs/labs1/data", exist_ok=True)
        try:
            with open("labs/labs1/data/log.json", "a", encoding="utf-8") as f:
                json.dump(log_data, f)
                f.write("\n")
        except IOError as e:
            print(f"Помилка запису логів: {e}")

        return result

    return wrapper


def create_users():
    users_to_register = [
        ("admin", "SuperSecretPassword123"),
        ("user1", "JustAnotherPassword!"),
        ("guest", "ShortPwd")  # Викличе помилку валідації
    ]

    os.makedirs("labs/labs1/data", exist_ok=True)
    try:
        with open("labs/labs1/data/users.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for username, pwd in users_to_register:
                try:
                    pwd_hash = generate_hash(pwd, "00005")
                    writer.writerow([username, pwd_hash])
                except (ValueError, ValidationError) as e:
                    print(f"Помилка створення {username}: {e}")
    except IOError as e:
        print(f"Помилка роботи з файлом: {e}")


@log_event
def login(username: str, password: str) -> bool:
    if not username or not password:
        raise ValueError("Логін і пароль обов'язкові")

    try:
        with open("labs/labs1/data/users.csv", "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == username:
                    return row[1] == generate_hash(password, "00005")
    except FileNotFoundError:
        print("База даних не знайдена!")
    return False


def run_task3():
    print("\n--- Завдання 3 ---")
    create_users()
    print("Спроба входу admin:", login("admin", "SuperSecretPassword123"))


if __name__ == "__main__":
    run_task3()
