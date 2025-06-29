# String Search Algorithms: Performance Comparison (Boyer-Moore, KMP, Rabin-Karp)

This repository contains implementations and performance comparisons of three string search algorithms:
1. Boyer-Moore
2. Knuth-Morris-Pratt (KMP)
3. Rabin-Karp

## Project Structure
goit-algo-hw-05/
├── 1.txt # Text file for testing (Article 1)
├── 2.txt # Text file for testing (Article 2)
├── binarySearch.py # Binary search implementation (Task 2)
├── task1.py # Hash table with delete method (Task 1)
├── task3.py # Algorithm comparison (Task 3)
├── requirements.txt # Python dependencies
└── README.md # This file


## Key Features
- Automatic encoding detection for text files using `chardet`
- Time measurement with `timeit` for accurate performance comparison
- Support for both existing and non-existing search patterns
- Clear output of iterations count and upper bound in binary search

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/goit-algo-hw-05.git
   cd goit-algo-hw-05
2. Install dependencies:
   ```bash
   pip install chardet 
   | pip install -r requirements.txt

## Usage
python "file name".py