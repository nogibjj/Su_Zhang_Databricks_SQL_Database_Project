## Su Zhang SQL Database Project - IDS706 Week#5 Assignment

## Purpose of the Project:

* The purpose of this project is to build Python script that connects with a SQL database and performs CRUD operations. I used dataset on global alcohol consumption detailing each country's servings on beer, wine, and spirit as well as total liters of pure alcohol.  

## Project Structure:

* `Makefile`: 
    - **install**: install `requirements.txt`
    - **test**: runs **pytest** for both mylib and main; runs all test files matching the pattern test_*.py
    - **format**: format using black formatter
    - **lint**: this project used **Ruff** instead of pylint for testing, which makes the process faster

* `requirements.txt`: specify pinned packages needed for this project, including **ruff, requests**

* `mylib`: 
    - **extract.py**: extract a dataset from a URL and save the content to the specified file path
    - **transform_load**: load the csv file and insert into a new `SQLite3` database. In this project, the database is named as `Drinks.db`.
    - **queryt**: performs CURD operations by creating four functions to **read, create, update, and delete data**

* `main.py`: calling out functions in `mylib` folder, and execuate the `ETL-Query` pipeline - extract, transform, load data from url and query the database. 

* `test_main.py`: tests if the functions defined in `mylib` work normally

* `README.me`: project documentation that introduces purpose, data source, and structure

* `githubactions`: `cicd.yml` defines workflows that specify the sequence of tasks to automate and also tests if the project works in several versions of Python.

* `devcontainer`: set up a development environment in Github Codespace, and Dockerfile to define the base environment

* `Drinks.db`: SQL database loaded from data url

## Description of CRUD Operations：

* __`read`__ </br>:
Reads and displays all records from the Drinks.db table. Returns a success message upon completion.

* __`create`__ </br>:
Inserts a new record into the Drinks.db table with predefined values for a country. Returns a success message upon successful insertion.

* __`delete`__ </br>:
Deletes rows from the Drinks.db table where the country is 'Albania'. Returns a success message after the deletion is committed.

* __`update`__ </br>:
Updates the beer_servings field for the country 'Yemen' in the Drinks.db table. Returns a success message after the update is committed.

## Data Source and Reference

* Data source: https://github.com/fivethirtyeight/data/tree/master/alcohol-consumption
* https://github.com/nogibjj/sqlite-lab

