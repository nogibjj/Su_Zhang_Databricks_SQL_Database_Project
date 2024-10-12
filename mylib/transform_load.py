"""
connect to Databricks and create queries
"""

import os
from databricks import sql
from dotenv import load_dotenv
import pandas as pd


def load(dataset="data/drinks.csv", dataset2="data/countries.csv"):
    """Transforms and loads data from Databricks database from API"""
    df = pd.read_csv(dataset, delimiter=",", skiprows=1)
    df2 = pd.read_csv(dataset2, delimiter=",", skiprows=1)
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
        result = c.fetchall()
        if not result:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS Drinks 
                (country string,
                beer_servings int,
                spirit_servings int,
                wine_servings int,
                total_litres_of_pure_alcohol int)
            """
            )
            # insert query
            values_list = [tuple(row) for _, row in df.iterrows()]
            insert_query = (
                f"INSERT INTO Drinks VALUES {','.join(str(x) for x in values_list)}"
            )
            c.execute(insert_query)
        c.execute("SHOW TABLES FROM default LIKE 'Countries*'")
        result = c.fetchall()
        if not result:
            c.execute(
                """
                CREATE TABLE IF NOT EXISTS Countries 
                (continent string,
                country string)
            """
            )
            # insert query
            values_list_2 = [tuple(row) for _, row in df2.iterrows()]
            insert_query_2 = (
                f"INSERT INTO Countries VALUES "
                f"{','.join(str(x) for x in values_list_2)}"
            )
            c.execute(insert_query_2)

        c.close()

    return "Load Success"
