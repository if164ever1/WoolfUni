import heapq

def minimal_cable_connection_cost(cables):
    if not cables:
        return 0
    
    heapq.heapify(cables)
    total_cost = 0
    
    while len(cables) > 1:
        first = heapq.heappop(cables)
        second = heapq.heappop(cables)
        
        cost = first + second
        total_cost += cost
        
        heapq.heappush(cables, cost)
    
    return total_cost

cables = [5, 4, 2, 8]
print("Мінімальні загальні витрати:", minimal_cable_connection_cost(cables))