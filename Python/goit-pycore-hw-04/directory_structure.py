import sys
import os
from colorama import init, Fore

def list_directory_structure(path, indent=0):
    """
    Функція візуалізує структуру директорії з використанням кольорового форматування.
    """
    if not os.path.exists(path):
        print(Fore.RED + "Директорія не знайдена!")
        return
    
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            print(Fore.BLUE + "    " * indent + "📂 " + item)
            list_directory_structure(item_path, indent + 1)
        else:
            print(Fore.WHITE + "    " * indent + "📜 " + item)

if __name__ == "__main__":
    init(autoreset=True)
    if len(sys.argv) < 2:
        print(Fore.RED + "Будь ласка, вкажіть шлях до директорії.")
    else:
        list_directory_structure(sys.argv[1])