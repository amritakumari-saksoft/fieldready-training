# High-Level Design - Parcel Policy RAG Assistant

## 1. Problem
Customers and support agents need accurate answers
about parcel delivery policies.

## 2. Data
20 parcel policy documents are used.

The documents cover:
- Delivery times
- Delays
- Tracking
- Damaged parcels
- Refunds
- Returns
- International shipping
- Prohibited items

## 3. Users
- Customer support agents
- Parcel customers

## 4. Main components

1. Policy documents
2. Document chunking
3. Embedding generation
4. Vector storage
5. Similarity-based retrieval
6. Context assembly
7. Ollama answer generation
8. Citation generation
9. Source passage display

## 5. Technology
- Python
- NumPy
- Sentence Transformers
- Ollama
- Qwen 3.5 2B
- Pytest

## 6. Out of scope
- Frontend implementation
- Authentication
- Live parcel tracking
- Policy editing

## 7. Design decisions

- Local embeddings reduce external dependencies.
- Cosine similarity supports retrieval.
- Context budgets control prompt size.
- Citations improve answer traceability.
- Low similarity triggers an I don't know response.
- Source passage display improves transparency.

## 8. Evaluation

Golden set: 15 questions.

Recall@1: 93.33%
Recall@3: 100%
Recall@5: 100%

## 9. Testing

All 15 Day 9 tests passed.
