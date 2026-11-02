import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
POLICY_DIR = BASE_DIR / "policies"
OUTPUT_DIR = BASE_DIR / "chunks"


def fixed_chunks(text, size=20):
    words = text.split()
    return [" ".join(words[i : i + size]) for i in range(0, len(words), size)]


def overlapping_chunks(text, size=20, overlap=5):
    words = text.split()
    step = size - overlap

    return [" ".join(words[i : i + size]) for i in range(0, len(words), step)]


def paragraph_chunks(text):
    return [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    strategies = {
        "fixed": fixed_chunks,
        "overlap": overlapping_chunks,
        "paragraph": paragraph_chunks,
    }

    results = {name: [] for name in strategies}

    for path in sorted(POLICY_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")

        for strategy_name, chunk_function in strategies.items():
            chunks = chunk_function(text)

            for index, chunk in enumerate(chunks):
                results[strategy_name].append(
                    {
                        "document": path.name,
                        "chunk_id": f"{path.stem}_{index}",
                        "text": chunk,
                    }
                )

    for strategy_name, chunks in results.items():
        output_file = OUTPUT_DIR / f"{strategy_name}.json"

        output_file.write_text(
            json.dumps(chunks, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        logger.info("%s: %d chunks", strategy_name, len(chunks))

    logger.info("Chunking completed successfully!")


if __name__ == "__main__":
    main()
