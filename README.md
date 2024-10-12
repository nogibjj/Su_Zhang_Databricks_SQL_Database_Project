[![CI](https://github.com/nogibjj/Su_Zhang_Databricks_SQL_Database_Project/actions/workflows/cicd.yml/badge.svg)](https://github.com/nogibjj/Su_Zhang_Databricks_SQL_Database_Project/actions/workflows/cicd.yml)

## Su Zhang Databricks SQL Database Project - IDS706 Week#6 Assignment

## Purpose of the Project:

* This project is an extension on the `Week#5 Assignment - SQLite Project`. The purpose of this project is to build Python script that connects with Databricks database and perform a complex query containing aggregation, joins and sorting. I used two datasets: one is global alcohol consumption, and the other one is country-to-continent categorization. 
* 

## Project Structure:

* `Makefile`: 
    - **install**: install `requirements.txt`
    - **test**: runs **pytest** for both mylib and main; runs all test files matching the pattern test_*.py
    - **format**: format using black formatter
    - **lint**: this project used **Ruff** instead of pylint for testing, which makes the process faster

* `requirements.txt`: specify packages needed for this project, including **ruff, requests, pandas, python-dotenv, databricks-sql-connector**

* `mylib`: 
    - **extract.py**: extract two datasets from URLs and save the contents to the specified file path
    - **transform_load**: load the csv file, create table, and insert contents into a new database on Databricks. In this project, the tables are named as `Drinks` and `Countries`.
    - **query**: connect to Databricks databse and perform one complex query to **aggregate, join, and sort data**, more details will be provided in below section

* `main.py`: calling out functions in `mylib` folder, and execuate the `ETL-Query` pipeline - extract, transform, load data from url and query the database. 

* `test_main.py`: tests if the functions defined in `mylib` work normally

* `README.me`: project documentation that introduces purpose, data source, and structure

* `githubactions`: `cicd.yml` defines workflows that specify the sequence of tasks to automate. In this project, I added `secrets` to store sensitive information on `server hostname`, `http path`, and `access token`.

* `devcontainer`: set up a development environment in Github Codespace, and Dockerfile to define the base environment

## Description of the Query：

* `library/transform_load.py`</br>
```Python
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
```
* __`Queries`__ </br>: (1) Creates table of `Drinks` and `Countries` if not exist yet; (2) Insert values of two files to these two tables (I aggregated all the values in a list and run one query to save time)

* `library/query.py`</br>
```Python
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
```

* These lines mainly sets up a connection to a Databricks database using environment variables for credentials.

```Python
        try:
            c.execute("ALTER TABLE Drinks ADD COLUMN beer_percentage FLOAT")
            print("Column 'beer_percentage' added to Drinks table.")
        except Exception as e:
            if "FIELDS_ALREADY_EXISTS" in str(e):
                print("Column 'beer_percentage' already exists in Drinks table.")
            else:
                raise
```
* __`First query`__ </br>: add a column in `Drinks` table named as "beer_percentage", which will store floating point numbers. 

```Python
        c.execute(
            """
            UPDATE Drinks
            SET beer_percentage = 
            (beer_servings / (beer_servings + wine_servings + spirit_servings)) * 100
            WHERE (beer_servings + wine_servings + spirit_servings) > 0
        """
        )
```
* __`Second query`__ </br>: calculates the percentage of beer servings among total servings as the beer_percentage numbers (for all the positive total servings)

```Python
        
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
```
* __`Third query`__ </br>: (1) **Joining** the `Drinks` and `Countries` tables on the country name. (2) Calculating the total beer servings and average beer percentage for each continent. (3) Grouping (**aggregating**) the results by continent and ordering (**sorting**) them by average beer percentage in descending order (from highest to lowest).

## Data Source and Reference

* Data source: https://github.com/fivethirtyeight/data/tree/master/alcohol-consumption
               https://github.com/dbouquin/IS_608/blob/master/NanosatDB_munging/Countries-Continents.csv
* Template reference: https://github.com/nogibjj/sqlite-lab

