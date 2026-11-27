# Database operations for the digital repository app with SQLite

import sqlite3
import os
import pandas as pd
from typing import Optional

def create_database(db_path: str):
    """ Create a new SQLite database and return the connection """
    conn = sqlite3.connect(db_path)
    return conn

def open_database(db_path: str):
    """ Open an existing SQLite database and return the connection """
    conn = sqlite3.connect(db_path)
    return conn

def create_table(conn, create_table_sql: str):
    """ Create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)
        
def create_insert_statement(table_name: str, data: dict) -> str:
    """ Create an SQL INSERT statement for the given table and data """
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    return sql

def update_folder_name(conn, carpeta_id: int, data: dict) -> bool:
    """Update the bookmark folder name"""
    cur = conn.cursor()
    cur.execute(
        # carpeta_id,nombre
        """UPDATE CARPETA
           SET nombre = ?
           WHERE id = ?""",
        (
            data['guardados'],
            data.get('nombre', ''),
            carpeta_id,
        ),
    )
    conn.commit()
    return cur.rowcount > 0

def insert_data(conn, table_name: str, data: dict):
    """ Insert data into the specified table """
    try:
        sql = create_insert_statement(table_name, data)
        cur = conn.cursor()
        cur.execute(sql, tuple(data.values()))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting data into {table_name}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        
def retrieve_data(conn, table_name: str) -> list:
    """ Retrieve all data from the specified table """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    return rows

def retrieve_data_with_query(conn, query: str) -> list:
    """ Retrieve data from the database using a custom SQL query
    Returns a list of dictionaries, where each dictionary represents a row in the result set.
    """
    cur = conn.cursor()
    cur.execute(query)
    fields = [description[0] for description in cur.description]
    rows = [dict(zip(fields, row)) for row in cur.fetchall()]
    return rows

# AQUI VAN LAS OTRAS PETICIONES


def close_database(conn):
    """ Close the database connection """
    conn.close()
    
def main():
    """ Main function """
    # Example usage
    db_path = os.path.join(os.path.dirname(__file__), 'movies.db')
    conn = create_database(db_path)

    # Create tables (example SQL statements)
    create_table_sql_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        created_at TEXT NOT NULL,
        full_name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    );
    """
    create_table(conn, create_table_sql_users)

    create_table_sql_stars = """
    CREATE TABLE IF NOT EXISTS stars (
        id INTEGER PRIMARY KEY,
        created_at TEXT NOT NULL,
        stage_name TEXT NOT NULL,
        real_name TEXT,
        date_of_birth TEXT,
        place_of_birth TEXT,
        image_url TEXT,
        username TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    );
    """
    create_table(conn, create_table_sql_stars)

    create_table_sql_connections = """
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY,
        created_at TEXT NOT NULL,
        movie_id INTEGER NOT NULL,
        star_id INTEGER NOT NULL,
        role TEXT,
        FOREIGN KEY (star_id) REFERENCES stars (id),
        FOREIGN KEY (movie_id) REFERENCES movies (id)
    );
    """
    create_table(conn, create_table_sql_connections)
    create_table_sql_movies = """
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        created_at TEXT NOT NULL,
        movie_title TEXT NOT NULL,
        release_date TEXT,
        poster_url TEXT,
        username TEXT,
        FOREIGN KEY (username) REFERENCES users (username)
    );
    """
    create_table(conn, create_table_sql_movies)

    # show the tables in the database
    tables = retrieve_data_with_query(conn, "SELECT name FROM sqlite_master WHERE type='table';")
    print("Tables in the database:")
    show_rows(tables)
    
    
    # Retrieve and show data

    close_database(conn)

if __name__ == "__main__":
    main()