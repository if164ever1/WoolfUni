class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def find_min_value(root):
    if root is None:
        return None  # якщо дерево порожнє
    
    current = root
    while current.left is not None:  # йдемо вліво до кінця
        current = current.left
    
    return current.value

# Приклад використання:
if __name__ == "__main__":
    # Створення дерева:
    #       10
    #      /  \
    #     5    15
    #    /      \
    #   2        20
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.left.left = TreeNode(2)
    root.right = TreeNode(15)
    root.right.right = TreeNode(20)

    min_value = find_min_value(root)
    print("Найменше значення в дереві:", min_value)  # Виведе: 2