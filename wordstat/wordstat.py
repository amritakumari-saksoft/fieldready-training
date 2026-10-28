# ruff: noqa: T201
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Count the most common words in a file")

parser.add_argument("filename")
parser.add_argument("--top", type=int, default=10)

args = parser.parse_args()

# Check invalid top value
if args.top <= 0:
    parser.error("--top must be a positive number")

# Read the file
try:
    text = Path(args.filename).read_text(encoding="utf-8")

except FileNotFoundError:
    print(f"Error: File '{args.filename}' not found.")
    exit(1)

# Convert all words to lowercase
words = text.lower().split()

# Count words
word_counts = {}

for word in words:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

# Sort by highest count
sorted_words = sorted(word_counts.items(), key=lambda item: item[1], reverse=True)

# Display top N words
for word, count in sorted_words[: args.top]:
    print(word, ":", count)
