"""Tests for the traveler-from-1800 entry.

Run from the repo root: python3 -m unittest discover -s tests -v
"""

import os
import re
import stat
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

import main  # noqa: E402

# Words coined after 1800 (or senses coined after 1800) that a traveler
# from that year could not know. The sentence must contain none of them.
FORBIDDEN_WORDS = [
    "internet", "computer", "website", "online", "digital", "electric",
    "electricity", "phone", "telephone", "screen", "app", "data",
    "network", "wifi", "wi-fi", "email", "e-mail", "video", "satellite",
    "pixel", "software", "hardware", "click", "cyber", "virtual",
    "electronic", "technology", "modem", "router", "browser", "download",
    "upload", "stream", "streaming", "chat", "social", "media", "web",
    "global", "instantly", "telegraph", "telegram", "radio", "television",
    "tv", "keyboard", "mouse", "server", "cloud", "link", "search",
    "engine", "algorithm", "code", "program", "machine", "robot",
    "artificial", "intelligence", "ai", "smartphone", "laptop", "tablet",
    "device", "gadget", "battery", "signal", "wireless", "cable",
    "fiber", "broadband", "dotcom", "homepage", "login", "password",
    "account", "profile", "feed", "tweet", "blog", "podcast",
    "meme", "emoji", "gif", "jpeg", "mp3", "file", "folder", "desktop",
    "window", "icon", "cursor", "usb", "bluetooth", "gps", "laser",
    "nuclear", "quantum", "plastic", "airplane", "aeroplane", "car",
    "train", "railway", "steam", "engine",
]

OUTPUT_PATH = "/output/entry.txt"


class TestSentence(unittest.TestCase):
    def test_length_within_limit(self):
        self.assertGreaterEqual(len(main.SENTENCE), 1)
        self.assertLessEqual(len(main.SENTENCE), 200)

    def test_exactly_one_sentence(self):
        text = main.SENTENCE
        # One terminal mark, at the very end, and no other sentence
        # terminator anywhere else in the text.
        self.assertTrue(text.endswith("."))
        self.assertEqual(len(re.findall(r"[.!?]", text)), 1)
        self.assertNotIn("\n", text)
        self.assertEqual(text, text.strip())
        self.assertNotIn("  ", text)

    def test_ascii_only(self):
        main.SENTENCE.encode("ascii")

    def test_no_post_1800_coinages(self):
        words = set(re.findall(r"[a-z]+", main.SENTENCE.lower()))
        bad = sorted(words & set(FORBIDDEN_WORDS))
        self.assertEqual(bad, [], f"modern words found: {bad}")

    def test_period_vocabulary_spot_checks(self):
        # The sentence is built only from things an 1800 reader knows.
        for word in ("post", "office", "letter", "ink", "book",
                     "printed", "shelves", "hand"):
            self.assertIn(word, main.SENTENCE.lower())

    def test_main_writes_valid_entry(self):
        for _ in range(2):
            result = subprocess.run(
                [sys.executable, os.path.join(REPO_ROOT, "main.py")],
                capture_output=True, text=True, check=True)
            self.assertEqual(result.returncode, 0)
        with open(OUTPUT_PATH, "rb") as f:
            raw = f.read()
        self.assertEqual(raw, main.SENTENCE.encode("utf-8"))
        self.assertEqual(os.stat(OUTPUT_PATH).st_mode & 0o777, 0o644)

    def test_byte_identical_across_runs(self):
        first = None
        for _ in range(2):
            subprocess.run(
                [sys.executable, os.path.join(REPO_ROOT, "main.py")],
                capture_output=True, check=True)
            with open(OUTPUT_PATH, "rb") as f:
                data = f.read()
            if first is None:
                first = data
            else:
                self.assertEqual(first, data)


if __name__ == "__main__":
    unittest.main()
