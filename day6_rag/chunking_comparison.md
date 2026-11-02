# Day 6 — Chunking Comparison

## Objective

Compare three chunking strategies using 20 synthetic parcel-logistics policy documents, local embeddings, and ChromaDB retrieval.

## Tools Used

- Python 3.14
- Sentence Transformers (`all-MiniLM-L6-v2`)
- ChromaDB
- 10 test questions
- Top-k retrieval (k = 3)

## Chunking Comparison Results

| Strategy | Top-1 Accuracy | Top-3 Accuracy |
|---|---|---|
| Fixed-size (20 words) | 10/10 (100%) | 10/10 (100%) |
| Overlapping (20 words, 5-word overlap) | 10/10 (100%) | 10/10 (100%) |
| Paragraph-based | 10/10 (100%) | 10/10 (100%) |

## Observations

All three strategies retrieved the expected policy document for every test question.

Fixed-size chunking divides text into equal-sized word groups but may split related information.

Overlapping chunking repeats some words between adjacent chunks, helping preserve context across boundaries, but increases storage and processing.

Paragraph-based chunking keeps complete paragraphs together, preserving policy statements when paragraphs are short.

## Which Strategy Worked Best?

All three strategies tied at 100% accuracy. No strategy demonstrated better retrieval accuracy in this experiment.

Paragraph-based chunking is a reasonable choice for this small dataset because the policies are short and generally contain one main topic per document.

## Limitations

The dataset contains only 20 short synthetic policies and 10 straightforward questions. These results do not prove that any strategy will perform equally well on longer or more complex documents.

## Conclusion

Chunking affects how information is represented and retrieved. The best strategy depends on document structure, chunk size, overlap, and the types of questions users ask.
