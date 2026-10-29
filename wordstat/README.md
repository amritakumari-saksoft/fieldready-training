# Wordstat – Python Word Counter

## About the Project

Wordstat is a simple Python command-line tool that reads a text file, counts how many times each word appears, and displays the most frequently used words.

This project was created as part of the Day 2 Python Core assignment.

## Features

- Reads words from a text file.
- Counts repeated words.
- Displays the top N most common words.
- Uses argparse to accept command-line arguments.
- Handles missing files with a clear error message.
- Supports Unicode words such as café.
- Treats uppercase and lowercase words as the same word.
- Handles empty files and very long lines.

## Requirements

- Python 3
- pytest (for running tests)

## How to Run

Open the terminal in VS Code.

To display the top 2 words:

```bash
python wordstat.py sample.txt --top 2
```

To display the top 3 words:

```bash
python wordstat.py sample.txt --top 3
```

## Example

Input file (`sample.txt`):

```text
apple banana apple mango apple banana
```

Command:

```bash
python wordstat.py sample.txt --top 3
```

Expected output:

```text
apple : 3
banana : 2
mango : 1
```

## Error Handling

If the file does not exist, the program displays a clear error message.

Example:

```bash
python wordstat.py missing.txt --top 2
```

Output:

```text
Error: File 'missing.txt' not found.
```

The program also rejects invalid values such as `--top 0`.

## Testing

This project uses pytest for automated testing.

Install pytest:

```bash
python -m pip install pytest
```

Run all tests:

```bash
python -m pytest -v
```

The project includes 8 tests:

1. Normal word counting
2. Empty file
3. Unicode words
4. Very long line
5. Uppercase and lowercase words
6. Missing file
7. Top N words
8. Invalid top value

**Test Result:** 8 tests passed.

## What I Learned

During this project, I learned:

- Basic Python programming
- Reading text files
- Working with strings and dictionaries
- Counting repeated words
- Using argparse
- Handling errors with try and except
- Writing and running pytest tests
- Using AI as a tutor to understand Python concepts

## Tools Used

- Python
- Visual Studio Code
- pytest
- ChatGPT (AI learning assistant)