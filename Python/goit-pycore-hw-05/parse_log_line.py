import sys
import os
import re
from collections import defaultdict
from typing import List, Dict


def parse_log_line(line: str) -> Dict:
    pattern = r'(?P<date>\d{4}-\d{2}-\d{2}) (?P<time>\d{2}:\d{2}:\d{2}) (?P<level>\w+) (?P<message>.+)'
    match = re.match(pattern, line.strip())
    if match:
        return match.groupdict()
    return {}

def load_logs(file_path: str) -> List[Dict]:
    if not os.path.exists(file_path):
        print(f"Файл {file_path} не знайдено.")
        sys.exit(1)
    
    logs = []
    with open(file_path, 'r') as file:
        for line in file:
            log = parse_log_line(line)
            if log:
                logs.append(log)
    return logs

def filter_logs_by_level(logs: List[Dict], level: str) -> List[Dict]:
    return [log for log in logs if log['level'].lower() == level.lower()]

def count_logs_by_level(logs: List[Dict]) -> Dict[str, int]:
    counts = defaultdict(int)
    for log in logs:
        counts[log['level']] += 1
    return dict(counts)

def display_log_counts(counts: Dict[str, int]):
    print(f"{'Рівень логування':<15}{'Кількість'}")
    print("-" * 30)
    for level, count in counts.items():
        print(f"{level:<15}{count}")

def display_log_details(logs: List[Dict], level: str):
    print(f"\nДеталі логів для рівня '{level}':")
    for log in logs:
        if log['level'].lower() == level.lower():
            print(f"{log['date']} {log['time']} - {log['message']}")

def main():
    if len(sys.argv) < 2:
        print("Використання: python main.py <шлях до файлу логів> [рівень логування]")
        sys.exit(1)
    
    file_path = sys.argv[1]
    level = sys.argv[2].lower() if len(sys.argv) > 2 else None
    
    logs = load_logs(file_path)
    counts = count_logs_by_level(logs)
    
    display_log_counts(counts)

    if level:
        display_log_details(logs, level)

if __name__ == "__main__":
    main()
