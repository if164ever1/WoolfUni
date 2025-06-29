import os
import shutil
import argparse
from pathlib import Path

def copy_and_sort_files(src_dir, dest_dir='dist'):
    try:
        src_path = Path(src_dir)
        dest_path = Path(dest_dir)
        
        if not src_path.exists():
            raise FileNotFoundError(f"Вихідна директорія {src_dir} не існує")
            
        dest_path.mkdir(parents=True, exist_ok=True)
        
        for item in src_path.iterdir():
            if item.is_dir():
                copy_and_sort_files(item, dest_dir)
            elif item.is_file():
                ext = item.suffix[1:].lower() if item.suffix else 'no_extension'
                
                ext_dir = dest_path / ext
                ext_dir.mkdir(exist_ok=True)

                try:
                    shutil.copy2(item, ext_dir)
                    print(f"Скопійовано: {item} -> {ext_dir}")
                except (PermissionError, IOError) as e:
                    print(f"Помилка при копіюванні {item}: {e}")
                    
    except Exception as e:
        print(f"Сталася помилка: {e}")

def main():
    parser = argparse.ArgumentParser(description='Рекурсивне сортування файлів за розширеннями')
    parser.add_argument('source', help='Шлях до вихідної директорії')
    parser.add_argument('--dest', default='dist', help='Шлях до цільової директорії (за замовчуванням "dist")')
    
    args = parser.parse_args()
    
    copy_and_sort_files(args.source, args.dest)
    print("Сортування завершено!")

if __name__ == "__main__":
    main()