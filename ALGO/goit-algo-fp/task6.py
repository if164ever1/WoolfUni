def greedy_algorithm(items, budget):
    """
    Жадібний алгоритм для вибору їжі з максимальною калорійністю в межах бюджету.
    Вибирає страви з найвищим співвідношенням калорій до вартості.
    
    :param items: словник з інформацією про страви
    :param budget: доступний бюджет
    :return: список вибраних страв, сумарна калорійність, сумарна вартість
    """
    # Створюємо список страв з розрахунком калорій на одиницю вартості
    items_list = []
    for name, info in items.items():
        ratio = info['calories'] / info['cost']
        items_list.append((name, info['cost'], info['calories'], ratio))
    
    # Сортуємо за співвідношенням калорій до вартості (спадання)
    items_list.sort(key=lambda x: x[3], reverse=True)
    
    selected_items = []
    total_calories = 0
    total_cost = 0
    
    for item in items_list:
        name, cost, calories, _ = item
        if total_cost + cost <= budget:
            selected_items.append(name)
            total_cost += cost
            total_calories += calories
    
    return selected_items, total_calories, total_cost

def dynamic_programming(items, budget):
    """
    Алгоритм динамічного програмування для вибору їжі з максимальною калорійністю.
    
    :param items: словник з інформацією про страви
    :param budget: доступний бюджет
    :return: список вибраних страв, сумарна калорійність, сумарна вартість
    """
    # Перетворюємо словник у список для зручності
    items_list = []
    for name, info in items.items():
        items_list.append((name, info['cost'], info['calories']))
    
    n = len(items_list)
    # Створюємо таблицю DP де dp[i][j] - максимальні калорії для бюджету j з першими i стравами
    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        name, cost, calories = items_list[i-1]
        for j in range(1, budget + 1):
            if cost > j:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i-1][j-cost] + calories)
    
    # Відновлюємо набір страв
    selected_items = []
    j = budget
    total_calories = dp[n][budget]
    total_cost = 0
    
    for i in range(n, 0, -1):
        if dp[i][j] != dp[i-1][j]:
            name, cost, calories = items_list[i-1]
            selected_items.append(name)
            j -= cost
            total_cost += cost
    
    return selected_items, total_calories, total_cost

def main():
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }
    
    budget = 100
    
    print("Жадібний алгоритм:")
    greedy_items, greedy_cal, greedy_cost = greedy_algorithm(items, budget)
    print(f"Вибрано: {greedy_items}")
    print(f"Сумарна калорійність: {greedy_cal}")
    print(f"Сумарна вартість: {greedy_cost}\n")
    
    print("Динамічне програмування:")
    dp_items, dp_cal, dp_cost = dynamic_programming(items, budget)
    print(f"Вибрано: {dp_items}")
    print(f"Сумарна калорійність: {dp_cal}")
    print(f"Сумарна вартість: {dp_cost}")

if __name__ == "__main__":
    main()