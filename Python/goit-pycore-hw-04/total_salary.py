def total_salary(path):
    """
    Функція аналізує файл та повертає загальну і середню зарплату розробників.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            salaries = [int(line.strip().split(',')[1]) for line in file]
        total = sum(salaries)
        average = total / len(salaries) if salaries else 0
        return total, average
    except FileNotFoundError:
        return "Файл не знайдено."
    except Exception as e:
        return f"Помилка: {e}"

if __name__ == "__main__":
    print(total_salary("salary_file.txt"))