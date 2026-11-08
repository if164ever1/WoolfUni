import heapq
import sys
from collections import defaultdict

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.vertices = set()
    
    def add_edge(self, u, v, weight):
        """Додає ребро між вершинами u та v з вагою weight"""
        self.edges[u].append((v, weight))
        self.vertices.update([u, v])
    
    def __str__(self):
        """Представлення графа у вигляді рядка"""
        result = []
        for u in self.edges:
            for v, weight in self.edges[u]:
                result.append(f"{u} -> {v} : {weight}")
        return "\n".join(result)

def dijkstra(graph, start):
    """
    Реалізація алгоритму Дейкстри з використанням бінарної купи
    Повертає словник з найкоротшими відстанями до всіх вершин
    """
    # Ініціалізація відстаней: нескінченність для всіх вершин, крім початкової
    distances = {vertex: float('infinity') for vertex in graph.vertices}
    distances[start] = 0
    
    # Пріоритетна черга (бінарна купа), що містить пари (відстань, вершина)
    priority_queue = [(0, start)]
    
    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)
        
        # Якщо знайдена відстань більша за збережену, пропускаємо
        if current_distance > distances[current_vertex]:
            continue
        
        # Оновлюємо відстані до сусідів поточної вершини
        for neighbor, weight in graph.edges[current_vertex]:
            distance = current_distance + weight
            
            # Якщо знайдено коротший шлях
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return distances

def input_graph():
    """Функція для введення графа з консолі"""
    graph = Graph()
    print("Введіть ребра у форматі 'вершина1 вершина2 вага' (пустий рядок для завершення):")
    while True:
        edge_input = input().strip()
        if not edge_input:
            break
        try:
            u, v, weight = edge_input.split()
            graph.add_edge(u, v, int(weight))
        except ValueError:
            print("Невірний формат. Спробуйте ще раз.")
    return graph

def input_start_vertex(graph):
    """Функція для введення початкової вершини"""
    while True:
        start = input("Введіть початкову вершину: ").strip()
        if start in graph.vertices:
            return start
        print(f"Вершина {start} не знайдена в графі. Доступні вершини: {', '.join(graph.vertices)}")

def print_results(distances, start):
    """Виводить результати роботи алгоритму Дейкстри"""
    print(f"\nНайкоротші шляхи від вершини {start}:")
    for vertex, distance in distances.items():
        if distance == float('infinity'):
            print(f"{vertex}: недосяжна")
        else:
            print(f"{vertex}: {distance}")

def main():
    print("Програма для знаходження найкоротших шляхів алгоритмом Дейкстри")
    
    # Введення графа
    graph = input_graph()
    print("\nЗаданий граф:")
    print(graph)
    
    # Введення початкової вершини
    start = input_start_vertex(graph)
    
    # Виконання алгоритму Дейкстри
    distances = dijkstra(graph, start)
    
    # Виведення результатів
    print_results(distances, start)

if __name__ == "__main__":
    main()