# Feature Specification: Show Source Passage

## 1. Problem

Customers receive answers from the parcel logistics RAG assistant,
but they cannot easily inspect the original policy passage
that supports an answer.

This makes it difficult to verify whether an answer is accurate.

## 2. Goal

Allow users to view the original policy passage used to
generate an answer.

## 3. User

A customer support agent or customer using the RAG assistant.

## 4. Functional requirements

- Display the original source passage.
- Display the source document filename.
- Display the source chunk ID.
- Support multiple citations.
- Preserve the exact original passage text.
- Do not display unrelated passages.
- Return no passages when the answer has no supporting citations.
- Handle missing or malformed citation data safely.

## 5. Input

A list of citation dictionaries containing:

- document
- chunk_id
- text

## 6. Output

A list of source passage dictionaries containing:

- document
- chunk_id
- passage

## 7. Acceptance criteria

1. A valid citation returns its original passage.
2. The filename is preserved.
3. The chunk ID is preserved.
4. Multiple citations return multiple passages.
5. Empty citations return an empty list.
6. Missing required fields raise a clear ValueError.
7. Original source text is not modified.

## 8. Out of scope

- Frontend user interface.
- PDF rendering.
- Editing policy documents.
- Generating new policy content.
- Changing the retrieval algorithm.

## 9. Success measurement

All source passage unit tests pass.
The displayed passage matches the original retrieved chunk.
