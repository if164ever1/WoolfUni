import timeit
import random

# Алгоритм сортування злиттям
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr

# Алгоритм сортування вставками
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

# Функція для тестування
def test_sorting_algorithms():
    
    sizes = [100, 1000, 10000]
    results = {}
    
    for size in sizes:
        random_array = [random.randint(0, 100000) for _ in range(size)]
        
        arr_merge = random_array.copy()
        arr_insertion = random_array.copy()
        arr_timsort = random_array.copy()
        
        merge_time = timeit.timeit(lambda: merge_sort(arr_merge), number=1)
        insertion_time = timeit.timeit(lambda: insertion_sort(arr_insertion), number=1)
        timsort_time = timeit.timeit(lambda: sorted(arr_timsort), number=1)
        
        results[size] = {
            'Merge Sort': merge_time,
            'Insertion Sort': insertion_time,
            'Timsort': timsort_time
        }
        
        print(f"\nРозмір масиву: {size}")
        print(f"Сортування злиттям: {merge_time:.6f} сек")
        print(f"Сортування вставками: {insertion_time:.6f} сек")
        print(f"Timsort: {timsort_time:.6f} сек")
    
    return results

if __name__ == "__main__":
    test_results = test_sorting_algorithms()