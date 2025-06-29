from queue import Queue
import random
import time

class RequestProcessor:
    def __init__(self):
        self.queue = Queue()
        self.request_id = 1

    def generate_request(self):
        # Створюємо нову заявку з унікальним ID
        request = {
            'id': self.request_id,
            'type': random.choice(['repair', 'consultation', 'return', 'complaint']),
            'priority': random.randint(1, 5)
        }
        self.request_id += 1
        
        # Додаємо заявку до черги
        self.queue.put(request)
        print(f"Generated request: ID {request['id']}, Type: {request['type']}, Priority: {request['priority']}")

    def process_request(self):
        if not self.queue.empty():
            # Видаляємо заявку з черги
            request = self.queue.get()
            print(f"Processing request: ID {request['id']}, Type: {request['type']}, Priority: {request['priority']}")
            # Імітуємо час обробки
            time.sleep(random.uniform(0.5, 2))
            print(f"Request ID {request['id']} processed successfully!")
        else:
            print("Queue is empty - no requests to process")

    def run(self):
        print("Service center request processing system started")
        print("Press Ctrl+C to stop the program\n")
        
        try:
            while True:
                # Генеруємо нові заявки з певною ймовірністю
                if random.random() < 0.7:  # 70% chance to generate a new request
                    self.generate_request()
                
                # Обробляємо заявки
                self.process_request()
                
                # Невелика затримка для імітації реального часу
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\nSystem stopped by user")

if __name__ == "__main__":
    processor = RequestProcessor()
    processor.run()