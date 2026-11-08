def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = left + (right - left) // 2

        if arr[mid] < target:
            left = mid + 1
        elif arr[mid] > target:
            right = mid - 1
            upper_bound = arr[mid]
        else:
            upper_bound = arr[mid]
            return (iterations, upper_bound)
    if left < len(arr):
        upper_bound = arr[left]
    else:
        upper_bound = None

    return (iterations, upper_bound)

arr = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]
target = 5.0

result = binary_search(arr, target)
print(f"Кількість ітерацій: {result[0]}, Верхня межа: {result[1]}")