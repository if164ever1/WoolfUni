class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def find_max_value(root):
    if root is None:
        return None  # якщо дерево порожнє
    
    current = root
    while current.right is not None:  # йдемо вправо до кінця
        current = current.right
    
    return current.value

# Приклад використання:
if __name__ == "__main__":
    # Створення дерева:
    #       10
    #      /  \
    #     5    15
    #          \
    #           20
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.right = TreeNode(15)
    root.right.right = TreeNode(20)

    max_value = find_max_value(root)
    print("Найбільше значення в дереві:", max_value)  # Виведе: 20