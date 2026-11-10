# Implementation Plan: Show Source Passage

## 1. Design

Implement a standalone function named
`show_source_passage()` in:

day9_rag/source_passage.py

## 2. Input

The function accepts a list of citation dictionaries.

Each citation contains:
- document
- chunk_id
- text

## 3. Processing

1. Validate that the input is a list.
2. Return an empty list when no citations exist.
3. Validate required citation fields.
4. Preserve the original passage text.
5. Build a clean source passage response.
6. Return the results.

## 4. Output structure

Each returned item contains:

- document
- chunk_id
- passage

## 5. Testing

Use pytest with mocked citation data.

Test:
- One valid citation.
- Multiple citations.
- Empty citations.
- Missing document.
- Missing chunk ID.
- Missing passage text.
- Exact text preservation.

## 6. Integration

Keep the function independent from the LLM.
It will consume the citations returned by ask().

## 7. Risks

Malformed citation data could cause incorrect source
display. Validate input before returning results.

## 8. Completion criteria

All feature tests pass and existing Day 9 tests remain passing.
