import pytest
from app.services.transform import (
    extract_article,
)
from pathlib import Path

test_article_path = Path(__file__).resolve().parent / "test_article.html"

with open(test_article_path, "r") as test_article_file:
    test_article_raw_text = test_article_file.read()
