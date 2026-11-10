import re
from collections.abc import Callable

DEFAULT_TOKEN_BUDGET = 2000


def count_tokens(text: str) -> int:
    """Estimate tokens using word and punctuation units."""
    return len(re.findall(r"\w+|[^\w\s]", text))


def assemble_context(
    chunks: list[dict],
    token_budget: int = DEFAULT_TOKEN_BUDGET,
    token_counter: Callable[[str], int] = count_tokens,
) -> tuple[str, list[dict]]:
    """Build context without exceeding the configured token budget."""
    if token_budget <= 0:
        raise ValueError("Token budget must be positive")

    selected = []
    context_parts = []
    used_tokens = 0

    for chunk in chunks:
        document = chunk["document"]
        chunk_id = chunk["chunk_id"]
        content = chunk["text"]

        passage = f"Source: {document}\nChunk ID: {chunk_id}\nContent: {content}"

        cost = token_counter(passage)

        if used_tokens + cost > token_budget:
            continue

        selected.append(chunk)
        context_parts.append(passage)
        used_tokens += cost

    return "\n\n".join(context_parts), selected
