import uuid
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

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

def draw_heap_with_highlight(heap_list, highlight_indices=None, highlight_color="red"):
    if highlight_indices is None:
        highlight_indices = []
    
    nodes = [Node(val) for val in heap_list]
    
    for i in range(len(nodes)):
        if i in highlight_indices:
            nodes[i].color = highlight_color
        
        left_idx = 2 * i + 1
        right_idx = 2 * i + 2
        
        if left_idx < len(nodes):
            nodes[i].left = nodes[left_idx]
        if right_idx < len(nodes):
            nodes[i].right = nodes[right_idx]
    
    # Візуалізація дерева
    tree = nx.DiGraph()
    pos = {nodes[0].id: (0, 0)}
    tree = add_edges(tree, nodes[0], pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    plt.title("Візуалізація бінарної купи")
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


# Приклад використання
if __name__ == "__main__":
    # Приклади бінарних куп
    min_heap = [0, 4, 1, 5, 10, 3]
    max_heap = [10, 5, 3, 4, 0, 1]
    
    print("Візуалізація мінімальної купи:")
    draw_heap_with_highlight(min_heap)
    
    print("\nВізуалізація максимальної купи:")
    draw_heap_with_highlight(max_heap)