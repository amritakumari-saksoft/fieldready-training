# Day 6 — Chunking Comparison

## Objective

Compare three chunking strategies using 20 synthetic parcel-logistics policy documents, local embeddings, and a NumPy-based vector store.

## Tools Used

- Python 3.14
- Sentence Transformers (`all-MiniLM-L6-v2`)
- NumPy (vector storage and cosine similarity retrieval)
- 20 synthetic parcel-logistics policy documents
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

**Fixed-size chunking:** Divides text into groups of 20 words. It is simple to implement but may split related information across chunks.

**Overlapping chunking:** Uses 20-word chunks with a 5-word overlap. It helps preserve information across chunk boundaries but creates additional chunks and increases storage requirements.

**Paragraph-based chunking:** Keeps paragraphs together, preserving the meaning and structure of policy statements.

## Which Strategy Worked Best?

All three strategies achieved 100% Top-1 and Top-3 retrieval accuracy. Therefore, no strategy demonstrated better accuracy in this experiment.

Paragraph-based chunking is a reasonable choice for this dataset because the policies are short and generally contain one main topic per document.

However, this is a practical preference rather than a demonstrated accuracy advantage.

## Limitations

The experiment used only 20 short synthetic policies and 10 straightforward questions.

The results may differ with longer documents, ambiguous questions, or multiple policies covering similar topics.

## Conclusion

Chunking affects how information is divided, embedded, and retrieved.

In this experiment, all three strategies performed equally well. The best chunking method depends on document structure, chunk size, overlap, and the types of questions users ask.
