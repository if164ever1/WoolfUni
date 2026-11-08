from collections import deque

def is_palindrome(input_string):
    processed_string = ''.join(input_string.split()).lower()
    
    char_deque = deque(processed_string)
    
    while len(char_deque) > 1:
        if char_deque.popleft() != char_deque.pop():
            return False
    
    return True

# Тестування функції
test_cases = [
    "Racecar",
    "Анна",
    "Madam, I'm Adam",
    "Python",
    "   A man a plan a canal Panama   ",
    "12321",
    "No lemon, no melon",
    "Hello"
]

for test in test_cases:
    result = is_palindrome(test)
    print(f"'{test}': {'Так, це паліндром' if result else 'Ні, це не паліндром'}")