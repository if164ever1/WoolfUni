class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def tree_sum(root):
    if root is None:
        return 0
    return root.value + tree_sum(root.left) + tree_sum(root.right)

# Приклад використання:
if __name__ == "__main__":
    # Створення дерева:
    #       10
    #      /  \
    #     5    15
    #    / \    \
    #   2   7    20
    root = TreeNode(10)
    root.left = TreeNode(5)
    root.left.left = TreeNode(2)
    root.left.right = TreeNode(7)
    root.right = TreeNode(15)
    root.right.right = TreeNode(20)

    total_sum = tree_sum(root)
    print("Сума всіх значень у дереві:", total_sum)  # Виведе: 10 + 5 + 2 + 7 + 15 + 20 = 59


def tree_sum_iterative(root):
    if not root:
        return 0
    
    stack = [root]
    total = 0
    
    while stack:
        node = stack.pop()
        total += node.value
        
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return total

# Приклад використання:
total_sum_iter = tree_sum_iterative(root)
print("Сума (ітеративно):", total_sum_iter)  # Теж 59