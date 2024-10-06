"""
Transforms and Loads data into the local SQLite3 database

"""

import sqlite3
import csv
import os


# load the csv file and insert into a new sqlite3 database
def load(dataset="data/drinks.csv"):
    """Transforms and Loads data into the local SQLite3 database"""

    # prints the full working directory and path
    print(os.getcwd())
    payload = csv.reader(open(dataset, newline=""), delimiter=",")
    conn = sqlite3.connect("Drinks.db")
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS Drinks")
    c.execute(
        """CREATE TABLE Drinks (country,beer_servings,
        spirit_servings,wine_servings,
        total_litres_of_pure_alcohol)"""
    )
    # insert
    c.executemany("INSERT INTO Drinks VALUES (?,?,?,?,?)", payload)
    conn.commit()
    conn.close()
    return "Drinks.db"
