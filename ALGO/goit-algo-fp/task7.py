import random
import matplotlib.pyplot as plt

def monte_carlo_dice_simulation(num_rolls):
    """
    Симуляція кидків двох кубиків методом Монте-Карло
    
    :param num_rolls: кількість кидків для симуляції
    :return: словник з кількістю випадінь кожної суми
    """
    sums_count = {i: 0 for i in range(2, 13)}
    
    for _ in range(num_rolls):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total = die1 + die2
        sums_count[total] += 1
    
    return sums_count

def calculate_probabilities(sums_count, num_rolls):
    """
    Обчислення ймовірностей кожної суми
    
    :param sums_count: словник з кількістю випадінь кожної суми
    :param num_rolls: загальна кількість кидків
    :return: словник з ймовірностями для кожної суми
    """
    probabilities = {}
    for total, count in sums_count.items():
        probabilities[total] = (count / num_rolls) * 100
    return probabilities

def theoretical_probabilities():
    """
    Теоретичні ймовірності для сум при киданні двох кубиків
    """
    return {
        2: 2.78, 3: 5.56, 4: 8.33, 5: 11.11, 6: 13.89,
        7: 16.67, 8: 13.89, 9: 11.11, 10: 8.33, 11: 5.56, 12: 2.78
    }

def print_results(probabilities, theoretical):
    """
    Виведення результатів у вигляді таблиці
    """
    print("| Сума | Імовірність (Монте-Карло) | Теоретична ймовірність | Відхилення |")
    print("|------|---------------------------|------------------------|------------|")
    for total in range(2, 13):
        mc_prob = probabilities.get(total, 0)
        th_prob = theoretical.get(total, 0)
        deviation = abs(mc_prob - th_prob)
        print(f"| {total:4} | {mc_prob:24.2f}% | {th_prob:22.2f}% | {deviation:9.2f}% |")

def plot_results(probabilities, theoretical):
    """
    Побудова графіка для порівняння результатів
    """
    totals = list(range(2, 13))
    mc_probs = [probabilities[total] for total in totals]
    th_probs = [theoretical[total] for total in totals]
    
    plt.figure(figsize=(10, 6))
    bar_width = 0.35
    index = range(len(totals))
    
    plt.bar(index, mc_probs, bar_width, label='Монте-Карло', color='blue', alpha=0.7)
    plt.bar([i + bar_width for i in index], th_probs, bar_width, label='Теоретична', color='red', alpha=0.7)
    
    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність (%)')
    plt.title('Порівняння ймовірностей сум при киданні двох кубиків')
    plt.xticks([i + bar_width/2 for i in index], totals)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def main():
    # Кількість кидків для симуляції
    num_rolls = 1000000
    
    print(f"Симуляція {num_rolls:,} кидків двох кубиків...\n")
    
    # Виконання симуляції
    sums_count = monte_carlo_dice_simulation(num_rolls)
    probabilities = calculate_probabilities(sums_count, num_rolls)
    theoretical = theoretical_probabilities()
    
    # Виведення результатів
    print_results(probabilities, theoretical)
    
    # Побудова графіка
    plot_results(probabilities, theoretical)

if __name__ == "__main__":
    main()