import csv

# Вхідний файл (створений у практичній роботі 5)
INPUT_FILE = "population.csv"
# Файл для збереження результатів пошуку
OUTPUT_FILE = "found_countries.csv"
# Назви стовпців
FIELDS = ["Country", "Code", "Year", "Population"]


def read_csv(filename):
    #Зчитує CSV-файл і повертає список рядків (словників). У разі помилки повертає None
    try:
        with open(filename, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except FileNotFoundError:
        print(f"Помилка: файл {filename} не знайдено. "
              "Спочатку запустіть програму з практичної роботи 5.")
        return None
    except (OSError, csv.Error) as error:
        print("Помилка відкриття або читання файлу:", error)
        return None


def input_countries():
    #Користувач вказує кількість країн, потім вводить їхні назви. Перевірка кількості
    while True:
        try:
            count = int(input("Скільки країн ви хочете знайти? "))
            if count <= 0:
                print("Помилка: кількість має бути більше нуля.")
                continue
            break
        except ValueError:
            print("Помилка: введіть ціле число.")

    print("Введіть назви країн англійською (наприклад, Ukraine).")
    names = []
    for i in range(1, count + 1):
        while True:
            name = input(f"Країна {i}: ").strip()
            if name == "":
                print("Помилка: назва не може бути порожньою.")
                continue
            break
        names.append(name)
    return names


def search_countries(rows, names):
    #Шукає країни в даних. Повертає (знайдені рядки, назви, яких не знайдено)
    found = []
    not_found = []
    for name in names:
        match = None
        for row in rows:
            if row["Country"].lower() == name.lower():
                match = row
                break
        if match is None:
            not_found.append(name)
        else:
            found.append(match)
    return found, not_found


def save_csv(filename, rows):
    #Зберігає знайдені рядки у новий CSV-файл. Повертає True, якщо успішно
    try:
        with open(filename, "w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    except OSError as error:
        print("Помилка запису файлу:", error)
        return False
    print(f"Результати збережено у файл {filename}")
    return True


def print_results(rows):
    #Виводить знайдені дані на екран
    print("\nРезультати пошуку:")
    print("-" * 50)
    for row in rows:
        print(f"{row['Country']}, {row['Code']}, {row['Year']}, {row['Population']}")


def main():
    rows = read_csv(INPUT_FILE)
    if rows is None:
        return
    if not rows:
        print("Помилка: файл не містить даних.")
        return

    names = input_countries()
    found, not_found = search_countries(rows, names)

    if not_found:
        print("\nНе знайдено країни:", ", ".join(not_found))

    if not found:
        print("Нічого не знайдено, файл не створено.")
        return

    if save_csv(OUTPUT_FILE, found):
        print_results(found)


if __name__ == "__main__":
    main()