import networkx as nx
import matplotlib.pyplot as plt

# Створюємо граф київського метро з вагами ребер
metro = nx.Graph()

# Додаємо станції з приблизним часом переміщення між ними (у хвилинах)
metro.add_weighted_edges_from([
    # Червона лінія (Святошинсько-Броварська)
    ("Академмістечко", "Житомирська", 3),
    ("Житомирська", "Святошин", 2),
    ("Святошин", "Нивки", 2),
    ("Нивки", "Берестейська", 2),
    ("Берестейська", "Шулявська", 2),
    ("Шулявська", "Політехнічний інститут", 1),
    ("Політехнічний інститут", "Вокзальна", 2),
    ("Вокзальна", "Університет", 2),
    ("Університет", "Театральна", 2),
    ("Театральна", "Хрещатик", 1),
    ("Хрещатик", "Арсенальна", 2),
    ("Арсенальна", "Дніпро", 3),
    ("Дніпро", "Гідропарк", 2),
    ("Гідропарк", "Лівобережна", 3),
    ("Лівобережна", "Дарниця", 3),
    ("Дарниця", "Чернігівська", 4),
    ("Чернігівська", "Лісова", 3),
    
    # Зелена лінія (Сирецько-Печерська)
    ("Почайна", "Тараса Шевченка", 2),
    ("Тараса Шевченка", "Контрактова площа", 2),
    ("Контрактова площа", "Площа Українських Героїв", 3),
    ("Площа Українських Героїв", "Театральная", 2),
    
    # Пересадки (додатковий час на пересадку)
    ("Театральна", "Театральная", 5)
])

# Візуалізація графа з вагами
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(metro, seed=42)
nx.draw(metro, pos, with_labels=True, node_color='lightblue', 
        edge_color='gray', node_size=800, font_size=10)
edge_labels = nx.get_edge_attributes(metro, 'weight')
nx.draw_networkx_edge_labels(metro, pos, edge_labels=edge_labels)
plt.title("Модель київського метро з часом переміщення (хвилини)")
plt.show()

# Реалізація алгоритму Дейкстри
def dijkstra(graph, start):
    # Ініціалізація
    shortest_paths = {node: float('inf') for node in graph.nodes()}
    shortest_paths[start] = 0
    visited = set()
    predecessors = {node: None for node in graph.nodes()}
    
    while len(visited) != len(graph.nodes()):
        # Знаходимо невідвідану вершину з найменшою відстанню
        current_node = None
        current_min = float('inf')
        for node in graph.nodes():
            if node not in visited and shortest_paths[node] < current_min:
                current_min = shortest_paths[node]
                current_node = node
        
        if current_node is None:
            break
            
        visited.add(current_node)
        
        # Оновлюємо відстані до сусідів
        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = shortest_paths[current_node] + weight
            if distance < shortest_paths[neighbor]:
                shortest_paths[neighbor] = distance
                predecessors[neighbor] = current_node
                
    return shortest_paths, predecessors

# Функція для відновлення шляху
def get_path(predecessors, start, end):
    path = []
    current_node = end
    while current_node != start:
        path.append(current_node)
        current_node = predecessors[current_node]
    path.append(start)
    path.reverse()
    return path

print("\nНайкоротші шляхи між станціями:")
all_stations = list(metro.nodes())

for i in range(len(all_stations)):
    for j in range(i+1, len(all_stations)):
        start = all_stations[i]
        end = all_stations[j]
        
        nx_path = nx.dijkstra_path(metro, start, end)
        nx_length = nx.dijkstra_path_length(metro, start, end)
        
        our_lengths, our_predecessors = dijkstra(metro, start)
        our_path = get_path(our_predecessors, start, end)
        
        print(f"\nЗ {start} до {end}:")
        print(f"Шлях: {' → '.join(our_path)}")
        print(f"Час: {our_lengths[end]} хв")
        print(f"Перевірка (NetworkX): {' → '.join(nx_path)}, {nx_length} хв")

start_station = "Академмістечко"
end_station = "Почайна"

print(f"\nПриклад: шлях від {start_station} до {end_station}")
shortest_path = nx.dijkstra_path(metro, start_station, end_station)
shortest_time = nx.dijkstra_path_length(metro, start_station, end_station)
print(f"Найкоротший шлях: {' → '.join(shortest_path)}")
print(f"Загальний час: {shortest_time} хвилин")