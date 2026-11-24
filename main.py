#!/usr/bin/env python3
"""One Sentence for a Traveler from 1800 -- make.fun entry v1.

Writes the entry sentence to /output/entry.txt. Bare standard library
only, fully deterministic: the same bytes on every run.
"""

import os

SENTENCE = (
    "Picture a post office where every letter in the world arrives the "
    "moment the ink dries, and every book ever printed waits upon its "
    "shelves for any hand that asks."
)

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    text = SENTENCE
    assert text == text.strip()
    assert 1 <= len(text) <= 200
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
