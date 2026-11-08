# goit-de-hw-03 — PySpark Data Analysis

This project implements all six homework steps using PySpark DataFrame API.

## Setup

1. Install a compatible Java runtime and Python environment for your PySpark version.
2. Run `pip install -r requirements.txt`.
3. Download `users.csv`, `purchases.csv`, and `products.csv` from the homework links and place them beside `main.py`.
4. Run `python main.py`.

## Screenshots

Save screenshots of the corresponding `.show()` output as `p1_*.png`, `p2_*.png`, ..., `p6_*.png` in a `screenshots/` folder. Steps 1 and 2 show three DataFrames each.

## Calculation

`amount = quantity * price`. The percentage denominator is total spending by users aged 18 through 25, across all product categories. Percentages are rounded to two decimal places.