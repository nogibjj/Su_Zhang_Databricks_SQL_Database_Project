"""Query the database"""

import sqlite3


def read_data():
    """Read the database of the Drinks.db table"""
    conn = sqlite3.connect("Drinks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Drinks")
    print(cursor.fetchall())
    conn.close()
    return "Read Success"


def create_data():
    """Create data record of Drinks.db"""
    conn = sqlite3.connect("Drinks.db")
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO Drinks
        (country, beer_servings, 
        spirit_servings, wine_servings, 
        total_litres_of_pure_alcohol) 
        VALUES ("Country1",90,20,16,4.5)
        """
    )
    c.execute("SELECT * FROM Drinks WHERE country ='Country1'")
    print("create:", c.fetchall())
    conn.close()
    return "Create Success"


def delete_data():
    """delete certain rows of data from Drinks.dbs"""
    conn = sqlite3.connect("Drinks.db")
    c = conn.cursor()
    c.execute("DELETE FROM Drinks WHERE country='Albania'")
    print("rows deleted:", c.rowcount)
    conn.commit()
    conn.close()
    return "Delete Success"


def update_data():
    """update certain rows of data from Drinks.db"""
    conn = sqlite3.connect("Drinks.db")
    c = conn.cursor()
    c.execute(
        """
        UPDATE Drinks
        SET beer_servings=100
        WHERE country='Yemen'
        """,
    )
    print("rows updated:", c.rowcount)
    conn.commit()
    conn.close()
    return "Update Success"
