"""
Test goes here
"""

from mylib.extract import extract
from mylib.transform_load import load
from mylib.query import query


def test_extract():
    result = extract()
    assert result is not None, "Failed to extract the database"


def test_load():
    test = load()
    assert test == "Load Success", "Failed to load the database"


def test_query():
    result = query()
    assert result is not None, "Failed to query the database"


if __name__ == "__main__":
    test_extract()
    test_load()
    test_query()
