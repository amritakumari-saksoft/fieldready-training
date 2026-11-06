import logging

import tiktoken

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger(__name__)

encoding = tiktoken.get_encoding("cl100k_base")

texts = {
    "English prose": "The parcel will arrive tomorrow morning.",
    "Python code": "def add(a, b):\n    return a + b",
    "JSON": '{"parcel_id": 101, "status": "delayed"}',
    "Hindi": "आपका पार्सल कल पहुंचेगा।",
    "French": "Votre colis arrivera demain.",
    "Japanese": "荷物は明日届きます。",
}


def main():
    logger.info("DAY 6 - TOKEN COUNTING LAB")
    logger.info("-" * 50)

    for name, content in texts.items():
        tokens = encoding.encode(content)

        logger.info("\nType: %s", name)
        logger.info("Text: %s", content)
        logger.info("Characters: %d", len(content))
        logger.info("Tokens: %d", len(tokens))
        logger.info("Token IDs: %s", tokens)


if __name__ == "__main__":
    main()
