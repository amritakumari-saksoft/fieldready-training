# Evaluation Results

## Day 9 RAG retrieval baseline

Total evaluation questions: 15

| Metric | Result |
|---|---:|
| Recall@1 | 93.33% |
| Recall@3 | 100% |
| Recall@5 | 100% |

## Findings
14 of 15 expected chunks were retrieved at rank 1.

All 15 expected chunks were retrieved within the top 3 results.

## Database checks
- PostgreSQL running: PASS
- pg_isready: PASS
- Database connection: PASS
- psycopg import: PASS
- git diff --check: PASS

## Pending
Run the full project test suite and record its results.
