import uuid
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, key, color="#1296F0"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Початковий колір вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph

def draw_tree(tree_root, title="Binary Tree"):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()

def generate_color(step, total_steps):
    """Генерує колір від темного до світлого на основі порядку обходу"""
    intensity = int(255 * (step / total_steps))
    return f"#{intensity:02x}{intensity:02x}{255:02x}"

def dfs_visualization(root):
    """Обхід у глибину (DFS) з візуалізацією кроків"""
    if not root:
        return
    
    stack = [root]
    visited = set()
    step = 0
    total_nodes = count_nodes(root)
    
    while stack:
        node = stack.pop()
        if node.id not in visited:
            # Оновлюємо колір вузла
            node.color = generate_color(step, total_nodes)
            step += 1
            visited.add(node.id)
            
            # Відображаємо поточний стан дерева
            draw_tree(root, title=f"DFS - Крок {step}")
            
            # Додаємо правого та лівого нащадка (у зворотньому порядку для коректного обходу)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

def bfs_visualization(root):
    """Обхід у ширину (BFS) з візуалізацією кроків"""
    if not root:
        return
    
    queue = deque([root])
    visited = set()
    step = 0
    total_nodes = count_nodes(root)
    
    while queue:
        node = queue.popleft()
        if node.id not in visited:
            # Оновлюємо колір вузла
            node.color = generate_color(step, total_nodes)
            step += 1
            visited.add(node.id)
            
            # Відображаємо поточний стан дерева
            draw_tree(root, title=f"BFS - Крок {step}")
            
            # Додаємо нащадків у чергу
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

def count_nodes(root):
    """Підраховує кількість вузлів у дереві"""
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)

# Створення дерева для демонстрації
def create_sample_tree():
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    return root

# Основна функція
def main():
    print("Візуалізація обходів бінарного дерева")
    
    # Створюємо дерево
    tree_root = create_sample_tree()
    
    # Відображаємо початкове дерево
    draw_tree(tree_root, title="Початкове дерево")
    
    # Візуалізація DFS
    print("\nПочаток візуалізації обходу в глибину (DFS)")
    dfs_visualization(tree_root)
    
    # Відновлюємо початкові кольори
    reset_tree_colors(tree_root)
    
    # Візуалізація BFS
    print("\nПочаток візуалізації обходу в ширину (BFS)")
    bfs_visualization(tree_root)

def reset_tree_colors(root):
    """Відновлює початкові кольори дерева"""
    if root:
        root.color = "#1296F0"
        reset_tree_colors(root.left)
        reset_tree_colors(root.right)

if __name__ == "__main__":
    main()