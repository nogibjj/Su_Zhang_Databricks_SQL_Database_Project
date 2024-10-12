"""
Test goes here
"""

import os
from databricks import sql
import pandas as pd
from dotenv import load_dotenv
from mylib.extract import extract
from mylib.transform_load import load
from mylib.query import query


def test_extract():
    result = extract()
    assert result is not None, "Failed to extract the database"


def test_load():
    load_dotenv()
    server_h = os.getenv("SERVER_HOST")
    access_token = os.getenv("ACCESS_TOKEN")
    http_path = os.getenv("HTTP_PATH")
    with sql.connect(
        server_hostname=server_h,
        http_path=http_path,
        access_token=access_token,
    ) as connection:
        c = connection.cursor()
        c.execute("SHOW TABLES FROM default LIKE 'Drinks*'")
        result1 = c.fetchall()
        c.execute("SELECT * FROM Drinks")
        result2 = c.fetchall()
        c.execute("SHOW TABLES FROM default LIKE 'Countries*'")
        result3 = c.fetchall()
        c.execute("SELECT * FROM Countries")
        result4 = c.fetchall()
        c.close()
    assert result1 is not None
    assert result2 is not None
    assert result3 is not None
    assert result4 is not None


def test_query():
    result = query()
    assert result is not None, "Failed to query the database"


if __name__ == "__main__":
    test_extract()
    test_load()
    test_query()
