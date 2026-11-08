def get_cats_info(path):
    """
    Функція читає файл та повертає список словників з інформацією про котів.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            cats = [dict(zip(["id", "name", "age"], line.strip().split(','))) for line in file]
        return cats
    except FileNotFoundError:
        return "Файл не знайдено."
    except Exception as e:
        return f"Помилка: {e}"

if __name__ == "__main__":
    print(get_cats_info("cats_file.txt"))