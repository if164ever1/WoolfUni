# Докази виконання

- `airflow-report.pdf` — короткий звіт зі скриншотами.
- `airflow-grid-5s.png` і `airflow-grid-35s.png` — Airflow Grid / Run Details із двома різними статусами.
- `airflow-sensor-5s.png` і `airflow-sensor-35s.png` — журнали SqlSensor з виміряним віком запису.
- `mysql-output-table.png` — результат фактичного запиту MySQL після двох запусків.
- `run-results.json` — експорт статусів із Airflow API та перевірених записів MySQL.

Запуски виконано в Airflow 2.10.5 і MySQL 8.4.4 на синтетичному наборі з `local/init-demo.sql`. Затримка 5 с дала `success` (вік 8,223 с), а 35 с дала `failed` (вік 38,482 с). В обох випадках збережено по одному рядку.
