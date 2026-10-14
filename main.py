import requests
import json
import csv

# Код показника Світового банку: Population, total
INDICATOR = "SP.POP.TOTL"
# Рік, за який потрібні дані
YEAR = "2019"
# Шаблон URL-адреси API (усі країни)
BASE_URL = "https://api.worldbank.org/v2/country/all/indicator/{indicator}"
# Кількість записів на сторінці
PER_PAGE = 500
# Час очікування відповіді сервера (секунди)
TIMEOUT = 30
# Назви файлів
JSON_FILE = "population.json"
CSV_FILE = "population.csv"


def build_url(indicator, year, per_page):
# Формує URL-адресу API
    base = BASE_URL.format(indicator=indicator)
    return f"{base}?date={year}&format=json&per_page={per_page}"


def fetch_data(url):
# Надсилає HTTP-запит і повертає дані у вигляді структури Python.У разі помилки повертає None
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        print("Помилка: перевищено час очікування відповіді сервера.")
        return None
    except requests.exceptions.ConnectionError:
        print("Помилка: немає з'єднання з сервером (перевірте інтернет).")
        return None
    except requests.exceptions.RequestException as error:
        print("Помилка виконання HTTP-запиту:", error)
        return None

    # Перевірка успішності запиту
    if response.status_code != 200:
        print("Помилка отримання даних. Код відповіді:", response.status_code)
        return None

    print("Дані успішно отримано")

    try:
        return response.json()
    except ValueError:
        print("Помилка: відповідь сервера не є коректним JSON.")
        return None


def validate_data(data):
    # Перевіряє коректність отриманих даних. Повертає True або False
    # Дані мають бути списком: інформація про сторінку, записи
    if not isinstance(data, list) or len(data) < 2:
        print("Помилка: неправильна структура відповіді "
              "(можливо, API повернув повідомлення про помилку).")
        return False

    records = data[1]

    # Відсутність даних
    if not records:
        print("Помилка: дані за вказаними параметрами відсутні.")
        return False

    if not isinstance(records, list):
        print("Помилка: записи мають неправильний формат.")
        return False

    # Перевірка наявності потрібних полів у кожному записі
    for item in records:
        if not isinstance(item, dict):
            print("Помилка: запис має неправильний формат.")
            return False
        if ("country" not in item or "value" not in item
                or "date" not in item or "countryiso3code" not in item):
            print("Помилка: у записі відсутні необхідні поля.")
            return False
        if "value" not in item["country"]:
            print("Помилка: у записі відсутня назва країни.")
            return False

    print("Перевірку даних пройдено успішно")
    return True


def save_json(data, filename):
    # Зберігає дані у JSON-файл. Повертає True, якщо успішно
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    except (OSError, TypeError) as error:
        print("Помилка запису JSON-файлу:", error)
        return False

    print(f"Створено файл {filename}")
    return True


def convert_to_csv(filename_json, filename_csv):
    # Зчитує JSON-файл, виділяє потрібні поля та зберігає їх у CSV. Повертає True, якщо успішно.
    # Відкриття та читання JSON-файлу
    try:
        with open(filename_json, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Помилка: файл {filename_json} не знайдено.")
        return False
    except (OSError, json.JSONDecodeError) as error:
        print("Помилка відкриття або читання JSON-файлу:", error)
        return False

    # Вибираємо лише потрібні поля (записи без значення пропускаємо)
    rows = []
    for item in data[1]:
        if item["value"] is not None:
            rows.append([
                item["country"]["value"],
                item["countryiso3code"],
                item["date"],
                item["value"]
            ])

    if not rows:
        print("Помилка: немає даних для запису в CSV.")
        return False

    # Запис у CSV
    try:
        with open(filename_csv, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Country", "Code", "Year", "Population"])
            writer.writerows(rows)
    except OSError as error:
        print("Помилка запису CSV-файлу:", error)
        return False

    print(f"Створено файл {filename_csv} (рядків: {len(rows)})")
    return True

def print_file(filename, title):
    # Виводить на екран зміст файлу
    print()
    print(title)
    print("-" * 50)
    try:
        with open(filename, "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print(f"Помилка: файл {filename} не знайдено.")
    except OSError as error:
        print("Помилка відкриття файлу:", error)


def main():
    url = build_url(INDICATOR, YEAR, PER_PAGE)
    print("URL-адреса запиту:", url)

    # Одержання даних
    data = fetch_data(url)
    if data is None:
        return

    # Перевірка коректності
    if not validate_data(data):
        return

    # Збереження у JSON
    if not save_json(data, JSON_FILE):
        return

    # Перетворення у CSV
    if not convert_to_csv(JSON_FILE, CSV_FILE):
        return

    # Виведення результатів
    print_file(JSON_FILE, "Зміст JSON-файлу:")
    print_file(CSV_FILE, "Зміст CSV-файлу:")


if __name__ == "__main__":
    main()