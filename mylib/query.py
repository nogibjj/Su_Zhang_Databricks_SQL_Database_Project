"""Query the database"""

import os
from databricks import sql
from dotenv import load_dotenv


def query():
    """connections to Databricks database and execute a complex query
    that contains joins, aggregation, and sorting"""
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
        try:
            c.execute("ALTER TABLE Drinks ADD COLUMN beer_percentage FLOAT")
            print("Column 'beer_percentage' added to Drinks table.")
        except Exception as e:
            if "FIELDS_ALREADY_EXISTS" in str(e):
                print("Column 'beer_percentage' already exists in Drinks table.")
            else:
                raise
        c.execute(
            """
            UPDATE Drinks
            SET beer_percentage = 
            (beer_servings / (beer_servings + wine_servings + spirit_servings)) * 100
            WHERE (beer_servings + wine_servings + spirit_servings) > 0
        """
        )
        result = c.execute(
            """
            SELECT
                C.continent,
                SUM(D.beer_servings) AS total_beer_servings,
                AVG(D.beer_percentage) AS avg_beer_percentage
            FROM
                Drinks D
            JOIN
                Countries C ON D.country = C.country
            GROUP BY
                C.continent
            ORDER BY
                avg_beer_percentage DESC
        """
        ).fetchall()
        c.close()
    return result
