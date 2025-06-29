Here is the complete `README.md` file for your repository:

```markdown
# Python Project: Utilities and Console Bots

This repository contains various Python scripts to handle different tasks, including Fibonacci sequence generation, number parsing, log file analysis, and an interactive contact management bot with error handling.

## File Structure

- **fibonacci.py**: Computes Fibonacci numbers, with optimizations using caching.
- **generator_numbers.py**: Extracts and sums real numbers from text input using regular expressions.
- **input_error.py**: Implements a contact management bot with error handling using decorators.
- **logfile.log**: Sample log file used for log parsing and analysis.
- **parse_log_line.py**: Parses log lines and extracts useful information.
- **logfile.log**: Contains sample logs for testing log analysis.
  
## Getting Started

### Requirements

To run the scripts in this repository, you need Python installed on your system. If it's not already installed, you can download it from the [official Python website](https://www.python.org/downloads/).

### Installing Dependencies

Ensure you have the necessary dependencies installed for working with the scripts. You can install any required dependencies by running:

```bash
pip install -r requirements.txt
```

*Note: If there is no `requirements.txt` file, you can manually install any necessary packages (e.g., `re`, `os`, etc.) via pip.*

### Running the Scripts

#### 1. **Log File Parsing (`parse_log_line.py`)**

This script is designed to read and analyze log files. To run the log parsing and display statistics, use the following command:

```bash
python parse_log_line.py /path/to/logfile.log
```

Where `/path/to/logfile.log` is the path to your log file. The script will output statistics regarding the levels of logging (e.g., INFO, ERROR, DEBUG) and allow you to filter logs by specific levels.

Example of running the script with a log file:

```bash
python parse_log_line.py logfile.log
```

#### 2. **Fibonacci Sequence Calculation (`fibonacci.py`)**

This script computes Fibonacci numbers using a caching mechanism to optimize performance.

To run this script, simply execute:

```bash
python fibonacci.py
```

#### 3. **Number Generator from Text (`generator_numbers.py`)**

This script identifies and sums up real numbers from a given text file.

Run it using the following command:

```bash
python generator_numbers.py
```

#### 4. **Contact Management Bot with Error Handling (`input_error.py`)**

This is an interactive console bot that handles errors during user input via decorators. To run the bot, use the command:

```bash
python input_error.py
```

Follow the prompts to add contacts, retrieve phone numbers, and list all contacts.

### Example Usage of Log File Parser

1. **Running the Script**:

```bash
python parse_log_line.py /path/to/logfile.log
```

2. **Expected Output**:

```bash
Log Level | Count
-------------------
INFO      | 4
ERROR     | 2
DEBUG     | 3
WARNING   | 1

Details for ERROR logs:
2024-01-22 09:00:45 - Database connection failed.
2024-01-22 11:30:15 - Backup process failed.
```

### Contributing

Feel free to fork the repository, make improvements, and open a pull request. Contributions are always welcome!

### License

This project is open-source and available under the [MIT License](LICENSE).

```

You can save this content as `README.md` in your repository. Let me know if you need further adjustments or additional details!