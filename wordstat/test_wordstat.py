# ruff: noqa: S101, S603
import subprocess
import sys


def run_wordstat(filename, top=2):
    return subprocess.run(
        [sys.executable, "wordstat.py", str(filename), "--top", str(top)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


# Test 1: Normal word counting
def test_word_count(tmp_path):
    file = tmp_path / "normal.txt"
    file.write_text("apple apple apple banana banana mango")

    result = run_wordstat(file, 2)

    assert result.returncode == 0
    assert "apple : 3" in result.stdout
    assert "banana : 2" in result.stdout


# Test 2: Empty file
def test_empty_file(tmp_path):
    file = tmp_path / "empty.txt"
    file.write_text("")

    result = run_wordstat(file)

    assert result.returncode == 0
    assert result.stdout.strip() == ""


# Test 3: Unicode words
def test_unicode_words(tmp_path):
    file = tmp_path / "unicode.txt"
    file.write_text("café apple café banana café", encoding="utf-8")

    result = run_wordstat(file, 3)

    assert result.returncode == 0
    assert "café : 3" in result.stdout


# Test 4: Very long line
def test_very_long_line(tmp_path):
    file = tmp_path / "long.txt"
    file.write_text("apple " * 10000)

    result = run_wordstat(file, 1)

    assert result.returncode == 0
    assert "apple : 10000" in result.stdout


# Test 5: Uppercase and lowercase
def test_uppercase_lowercase(tmp_path):
    file = tmp_path / "case.txt"
    file.write_text("Apple apple APPLE banana")

    result = run_wordstat(file, 2)

    assert result.returncode == 0
    assert "apple : 3" in result.stdout


# Test 6: Missing file
def test_missing_file(tmp_path):
    file = tmp_path / "missing.txt"

    result = run_wordstat(file)

    assert result.returncode != 0
    assert "not found" in result.stdout.lower()


# Test 7: Top N words
def test_top_n_words(tmp_path):
    file = tmp_path / "top.txt"
    file.write_text("apple apple apple banana banana mango")

    result = run_wordstat(file, 2)

    assert result.returncode == 0
    assert len(result.stdout.strip().splitlines()) == 2
    assert "mango" not in result.stdout


# Test 8: Invalid top value
def test_invalid_top_value(tmp_path):
    file = tmp_path / "sample.txt"
    file.write_text("apple banana")

    result = run_wordstat(file, 0)

    assert result.returncode != 0
    assert "--top must be a positive number" in result.stderr
