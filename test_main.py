"""
Test goes here

"""

from mylib.extract import extract
from mylib.transform_load import load
from mylib.query import create_data, read_data, delete_data, update_data


def test_extract():
    result = extract()
    assert result is not None, "Failed to extract the database"


def test_load():
    data = load()
    if data:
        print("Database 'Drinks.db' loading successful:")
        for row in data:
            print(row)
    else:
        print("Failed to load the database")


def test_read():
    test = read_data()
    assert test == "Read Success", "Failed to read the database"


def test_create():
    test = create_data()
    return test == "Create Success", "Failed to create the data"


def test_update():
    test = update_data()
    return test == "Update Success", "Failed to update the data"


def test_delete():
    test = delete_data()
    return test == "Delete Success", "Failed to delete the data"


if __name__ == "__main__":
    test_extract()
    test_load()
    test_read()
    test_create()
    test_update()
    test_delete()
