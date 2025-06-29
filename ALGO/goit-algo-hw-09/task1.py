def find_coins_greedy(amount):
    coins = [50, 25, 10, 5, 2, 1]
    result = {}
    
    for coin in coins:
        if amount >= coin:
            count = amount // coin
            result[coin] = count
            amount -= coin * count
            if amount == 0:
                break
                
    return result

def find_min_coins(amount):
    coins = [50, 25, 10, 5, 2, 1]
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    coin_used = [0] * (amount + 1)
    
    for i in range(1, amount + 1):
        for coin in coins:
            if i >= coin and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1
                coin_used[i] = coin
    
    result = {}
    remaining = amount
    
    if dp[amount] == float('inf'):
        return result
    
    while remaining > 0:
        coin = coin_used[remaining]
        result[coin] = result.get(coin, 0) + 1
        remaining -= coin
    
    return result

if __name__ == "__main__":
    test_amounts = [113, 1234, 5555, 100, 0, 9999]
    
    print("Тестування жадібного алгоритму:")
    for amount in test_amounts:
        print(f"Сума: {amount} -> {find_coins_greedy(amount)}")
    
    print("\nТестування алгоритму динамічного програмування:")
    for amount in test_amounts:
        print(f"Сума: {amount} -> {find_min_coins(amount)}")
    
    import time
    
    large_amount = 99999
    print(f"\nПорівняння часу для великої суми ({large_amount}):")
    
    start = time.time()
    greedy_result = find_coins_greedy(large_amount)
    greedy_time = time.time() - start
    print(f"Жадібний алгоритм: {greedy_time:.6f} сек")
    
    start = time.time()
    dp_result = find_min_coins(large_amount)
    dp_time = time.time() - start
    print(f"Динамічне програмування: {dp_time:.6f} сек")
    
    print("\nРезультати однакові?", greedy_result == dp_result)