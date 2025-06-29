import networkx as nx
from collections import deque

metro = nx.Graph()

stations = [
    "Академмістечко", "Житомирська", "Святошин", "Нивки", "Берестейська",
    "Шулявська", "Політехнічний інститут", "Вокзальна", "Університет",
    "Театральна", "Хрещатик", "Арсенальна", "Дніпро", "Гідропарк",
    "Лівобережна", "Дарниця", "Чернігівська", "Лісова",
    "Почайна", "Тараса Шевченка", "Контрактова площа", "Площа Українських Героїв", "Театральная"
]

metro.add_nodes_from(stations)

red_line = [
    ("Академмістечко", "Житомирська"), ("Житомирська", "Святошин"), 
    ("Святошин", "Нивки"), ("Нивки", "Берестейська"), 
    ("Берестейська", "Шулявська"), ("Шулявська", "Політехнічний інститут"),
    ("Політехнічний інститут", "Вокзальна"), ("Вокзальна", "Університет"),
    ("Університет", "Театральна"), ("Театральна", "Хрещатик"),
    ("Хрещатик", "Арсенальна"), ("Арсенальна", "Дніпро"),
    ("Дніпро", "Гідропарк"), ("Гідропарк", "Лівобережна"),
    ("Лівобережна", "Дарниця"), ("Дарниця", "Чернігівська"),
    ("Чернігівська", "Лісова")
]

green_line = [
    ("Почайна", "Тараса Шевченка"), ("Тараса Шевченка", "Контрактова площа"),
    ("Контрактова площа", "Площа Українських Героїв"), ("Площа Українських Героїв", "Театральная")
]

metro.add_edges_from(red_line)
metro.add_edges_from(green_line)
metro.add_edge("Театральна", "Театральная")

# Реалізація DFS
def dfs_path(graph, start, end, path=None):
    if path is None:
        path = []
    path = path + [start]
    
    if start == end:
        return [path]
    
    paths = []
    for neighbor in graph.neighbors(start):
        if neighbor not in path:
            new_paths = dfs_path(graph, neighbor, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    
    return paths

# Реалізація BFS
def bfs_path(graph, start, end):
    queue = deque()
    queue.append((start, [start]))
    
    while queue:
        (vertex, path) = queue.popleft()
        
        for neighbor in graph.neighbors(vertex):
            if neighbor not in path:
                if neighbor == end:
                    yield path + [neighbor]
                else:
                    queue.append((neighbor, path + [neighbor]))

start_station = "Академмістечко"
end_station = "Почайна"

# Знаходимо шляхи за допомогою DFS
dfs_paths = dfs_path(metro, start_station, end_station)
print(f"\nВсі можливі шляхи за допомогою DFS ({len(dfs_paths)} знайдено):")
for i, path in enumerate(dfs_paths[:3], 1):  # Виводимо перші 3 шляхи для прикладу
    print(f"Шлях {i}: {' → '.join(path)}")
    print(f"Кількість станцій: {len(path)-1}")

# Знаходимо шляхи за допомогою BFS
bfs_paths = list(bfs_path(metro, start_station, end_station))
print(f"\nВсі можливі шляхи за допомогою BFS ({len(bfs_paths)} знайдено):")
for i, path in enumerate(bfs_paths[:3], 1):  # Виводимо перші 3 шляхи для прикладу
    print(f"Шлях {i}: {' → '.join(path)}")
    print(f"Кількість станцій: {len(path)-1}")

# Аналіз різниці між алгоритмами
print("\nПорівняння алгоритмів DFS та BFS:")
print("- DFS (пошук в глибину):")
print("  * Знаходить всі можливі шляхи, рухаючись якомога далі по одній гілці")
print("  * Може знаходити довші шляхи першими")
print("  * Корисно, коли потрібно дослідити всі можливі варіанти")

print("\n- BFS (пошук в ширину):")
print("  * Завжди знаходить найкоротший шлях (за кількістю ребер)")
print("  * Досліджує всі сусідні вершини перед переходом на наступний рівень")
print("  * Ефективний для пошуку найкоротшого маршруту між станціями")

# Знаходимо найкоротший шлях за кількістю станцій
shortest_path = nx.shortest_path(metro, start_station, end_station)
print(f"\nНайкоротший шлях (за кількістю станцій): {' → '.join(shortest_path)}")
print(f"Кількість станцій: {len(shortest_path)-1}")