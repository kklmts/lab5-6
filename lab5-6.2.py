import json

JSON_FILE = "institutions.json"
RESULT_FILE = "found_institutions.json"
VALID_TYPES = ["школа", "технікум", "училище"]

# Словник із практичної роботи 3: назва закладу - тип, кількість учнів
institutions = {
    "Ліцей_№1": ["школа", 520],
    "Політехнічний": ["технікум", 340],
    "Гімназія_№5": ["школа", 610],
    "Будівельне": ["училище", 215],
    "ЗОШ_№12": ["школа", 450],
    "Медичний": ["технікум", 400]
}


def save_json(data, filename):
    #Зберігає словник у JSON-файл (кожен запис в одному рядку). Повертає True, якщо успішно
    try:#
        lines = []
        for name, value in data.items():
            # json.dumps формує коректний JSON для ключа і значення
            key_json = json.dumps(name, ensure_ascii=False)
            value_json = json.dumps(value, ensure_ascii=False)
            lines.append(f"    {key_json}: {value_json}")

        text = "{\n" + ",\n".join(lines) + "\n}\n"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(text)
    except (OSError, TypeError) as error:
        print("Помилка запису файлу:", error)
        return False
    return True


def print_json_file(filename):
    #Виводить зміст JSON-файлу на екран#
    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line not in ("{", "}", ""):
                    print(line)
    except FileNotFoundError:
        print(f"Помилка: файл {filename} не знайдено.")
    except OSError as error:
        print("Помилка відкриття файлу:", error)


def input_type():
    #Запитує тип закладу з перевіркою
    while True:
        type_inst = input("Введіть тип закладу для пошуку "
                          "(школа, технікум або училище): ").strip().lower()
        if type_inst in VALID_TYPES:
            return type_inst
        print("Помилка: дозволено лише школа, технікум або училище. "
              "Спробуйте ще раз.")


def search_by_type(data, type_inst):
    #Шукає заклади за типом. Повертає словник
    result = {}
    for name, value in data.items():
        if value[0] == type_inst:
            result[name] = value
    return result


def main():
    # Збереження словника у JSON та виведення на екран
    if not save_json(institutions, JSON_FILE):
        return
    print_json_file(JSON_FILE)

    # Пошук за полем "тип закладу"
    type_inst = input_type()
    result = search_by_type(institutions, type_inst)

    if not result:
        print("Закладів такого типу не знайдено, файл не створено.")
        return

    # Збереження результатів у новий JSON-файл
    if save_json(result, RESULT_FILE):
        print_json_file(RESULT_FILE)


if __name__ == "__main__":
    main()