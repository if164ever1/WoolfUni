import timeit
import chardet

def boyer_moore(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    last_occurrence = {pattern[i]: i for i in range(m)}
    i = m - 1
    j = m - 1
    iterations = 0

    while i < n:
        iterations += 1
        if text[i] == pattern[j]:
            if j == 0:
                return i
            else:
                i -= 1
                j -= 1
        else:
            last_occ = last_occurrence.get(text[i], -1)
            i += m - min(j, 1 + last_occ)
            j = m - 1
    return -1

def kmp(text, pattern):
    def compute_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    lps = compute_lps(pattern)
    i = 0
    j = 0
    iterations = 0

    while i < n:
        iterations += 1
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                return i - j
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    prime = 101
    d = 256
    h = pow(d, m - 1) % prime
    p_hash = 0
    t_hash = 0

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % prime
        t_hash = (d * t_hash + ord(text[i])) % prime

    for i in range(n - m + 1):
        if p_hash == t_hash:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if t_hash < 0:
                t_hash += prime
    return -1


def measure_time(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=100)

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
        return result['encoding']

encoding1 = detect_encoding('1.txt')
encoding2 = detect_encoding('2.txt')

with open('1.txt', 'r', encoding=encoding1) as f:
    text1 = f.read()

with open('2.txt', 'r', encoding=encoding2) as f:
    text2 = f.read()
    
existing_pattern = "алгоритм"
fake_pattern = "квантовий комп'ютер"

algorithms = {
    "Boyer-Moore": boyer_moore,
    "KMP": kmp,
    "Rabin-Karp": rabin_karp
}

results = {}
for name, algorithm in algorithms.items():
    time_existing_1 = measure_time(algorithm, text1, existing_pattern)
    time_fake_1 = measure_time(algorithm, text1, fake_pattern)
    time_existing_2 = measure_time(algorithm, text2, existing_pattern)
    time_fake_2 = measure_time(algorithm, text2, fake_pattern)
    results[name] = {
        "стаття 1 (existing)": time_existing_1,
        "стаття 1 (fake)": time_fake_1,
        "стаття 2 (existing)": time_existing_2,
        "стаття 2 (fake)": time_fake_2
    }


for algo, timings in results.items():
    print(f"\n{algo}:")
    for case, time in timings.items():
        print(f"{case}: {time:.6f} сек")