class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node
    
    def print_list(self):
        current_node = self.head
        while current_node:
            print(current_node.data, end=" -> ")
            current_node = current_node.next
        print("None")

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def insertion_sort(self):
        if not self.head or not self.head.next:
            return
        
        sorted_list = None
        current = self.head
        
        while current:
            next_node = current.next
            if not sorted_list or sorted_list.data >= current.data:
                current.next = sorted_list
                sorted_list = current
            else:
                temp = sorted_list
                while temp.next and temp.next.data < current.data:
                    temp = temp.next
                current.next = temp.next
                temp.next = current
            current = next_node
        
        self.head = sorted_list


def merge_sorted_lists(list1, list2):
    dummy = Node()
    tail = dummy
    
    while list1 and list2:
        if list1.data <= list2.data:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    
    tail.next = list1 if list1 else list2
    
    merged_list = LinkedList()
    merged_list.head = dummy.next
    return merged_list

# Створення та тестування списків
if __name__ == "__main__":
    # Створення першого списку
    llist1 = LinkedList()
    llist1.append(3)
    llist1.append(1)
    llist1.append(5)
    print("Перший список:")
    llist1.print_list()
    
    # Сортування першого списку
    llist1.insertion_sort()
    print("Відсортований перший список:")
    llist1.print_list()
    
    # Створення другого списку
    llist2 = LinkedList()
    llist2.append(4)
    llist2.append(2)
    llist2.append(6)
    print("\nДругий список:")
    llist2.print_list()
    
    # Сортування другого списку
    llist2.insertion_sort()
    print("Відсортований другий список:")
    llist2.print_list()
    
    # Об'єднання двох відсортованих списків
    merged = merge_sorted_lists(llist1.head, llist2.head)
    print("\nОб'єднаний відсортований список:")
    merged.print_list()
    
    # Реверсування об'єднаного списку
    merged.reverse()
    print("Реверсований об'єднаний список:")
    merged.print_list()