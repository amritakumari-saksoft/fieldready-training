# Day 9 - AI Assistance Log

## Tool used
ChatGPT

## Tasks assisted
- RAG implementation guidance.
- Context budget and citation testing.
- Golden set creation.
- Recall@k evaluation.
- Spec-driven development.
- Source passage feature implementation.
- Pytest troubleshooting.

## Prompts used
- How to implement RAG with citations?
- How to create a 15-question golden set?
- How to calculate recall@k?
- How to follow a spec-driven development process?
- How to implement show_source_passage()?

## Accepted suggestions
- Separate retrieval, context assembly and citations.
- Use dependency injection for testing.
- Create failing tests before implementation.
- Validate citation fields.
- Preserve original source passages.

## Rejected suggestions
- None recorded.

## Verification
- Ran pytest before implementation.
- Observed 7 expected failures.
- Implemented the feature.
- Ran 8 feature tests successfully.
- Ran all 15 Day 9 tests successfully.
- Manually verified source passage output.

## Learning
I learned how to implement a RAG service,
evaluate retrieval quality and follow a test-first,
spec-driven development workflow.

## Remaining limitations
The source passage function currently returns
structured data. Frontend integration is out of scope.
