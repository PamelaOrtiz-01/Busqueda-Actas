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

# ARCHIVOS DISPONIBLES
def contar_total_archivos (conn) -> int:
    """ Retrieve the number of files in the repository """
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(archivo_id) FROM ARCHIVO")
    rows = cur.fetchone()
    return rows[0]

def ver_archivos_disponibles (conn) -> list:
    query_vad = """
    SELECT
        ARCHIVO.archivo_id,
        ARCHIVO.titulo,
        AUTOR.nombre,
        FECHA.fecha_publicacion,
    FROM ARCHIVO    
    LEFT JOIN ARCHIVO_AUTOR ON ARCHIVO.archivo_id = ARCHIVO_AUTOR.archivo_id
    LEFT JOIN AUTOR ON ARCHIVO_AUTOR.autor_id = AUTOR.autor_id
    INNER JOIN FECHA ON ARCHIVO.fecha_id = FECHA.fecha_id
    ORDER BY ARCHIVO.titulo;
    """
    return retrieve_data_with_query(conn, query_vad)

# POR AUTOR
def contar_total_autores (conn) -> int:
    """ Retrieve the number of authors in the repository """
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(autor_id) FROM AUTOR")
    rows = cur.fetchone()
    return rows[0]

def listar_autor_numero_archivos(conn) -> list:
    """Retrieve the author and the number of files to their name """
    query_launa = """
    SELECT
        AUTOR.autor_id,
        AUTOR.nombre,    
        COUNT (ARCHIVO.archivo_id)
    FROM AUTOR
    LEFT JOIN ARCHIVO_AUTOR ON AUTOR.autor_id = ARCHIVO_AUTOR.autor_id
    LEFT JOIN ARCHIVO ON ARCHIVO_AUTOR.archivo_id = ARCHIVO.archivo_id
    GROUP BY AUTOR.autor_id, AUTOR.nombre
    ORDER BY AUTOR.nombre
    """
    return retrieve_data_with_query(conn, query_launa)

def ver_archivos_por_autor(conn, autor_id) -> list:
    query_vapau = """
    SELECT
        ARCHIVO.archivo_id,
        ARCHIVO.titulo,
        AUTOR.nombre,
        FECHA.fecha_publicacion,
    FROM AUTOR    
    LEFT JOIN ARCHIVO_AUTOR ON AUTOR.autor_id = ARCHIVO_AUTOR.autor_id
    LEFT JOIN ARCHIVO ON ARCHIVO_AUTOR.archivo_id = ARCHIVO.archivo_id
    INNER JOIN FECHA ON ARCHIVO.fecha_id = FECHA.fecha_id
    WHERE AUTOR.autor_id = ?
    ORDER BY ARCHIVO.titulo;
    """
    return retrieve_data_with_query(conn, query_vapau, (autor_id,))

# POR AÑO
def listar_anio_numero_archivos(conn) -> list:
    query_lanna = """
    SELECT
        FECHA.fecha_id
        FECHA.fecha_publicacion,    
        COUNT (ARCHIVO.archivo_id)
    FROM FECHA
    LEFT JOIN ARCHIVO ON FECHA.fecha_id = ARCHIVO.fecha_id
    GROUP BY FECHA.fecha_id, FECHA.fecha_publicacion
    ORDER BY FECHA.fecha_publicacion;
    """
    return retrieve_data_with_query(conn, query_lanna)

def ver_archivos_por_anio(conn, fecha_id) -> list:
    query_vapan = """
    SELECT
        ARCHIVO.archivo_id,
        ARCHIVO.titulo,
        AUTOR.nombre,
        FECHA.fecha_publicacion,
    FROM FECHA
    INNER JOIN ARCHIVO ON FECHA.fecha_id = ARCHIVO.fecha_id
    LEFT JOIN ARCHIVO_AUTOR ON ARCHIVO.archivo_id = ARCHIVO_AUTOR.archivo_id
    LEFT JOIN AUTOR ON ARCHIVO_AUTOR.autor_id = AUTOR.autor_id
    WHERE FECHA.fecha_id = ?
    ORDER BY ARCHIVO.titulo;
    """
    return retrieve_data_with_query(conn, query_vapan, (fecha_id,))

# DETALLES DEL ARCHIVO
def ver_detalles_archivo(conn, archivo_id) -> list:
    query_vda = """
    SELECT
        ARCHIVO.archivo_id,
        ARCHIVO.titulo,
        AUTOR.autor_id,
        AUTOR.nombre,
        FECHA.fecha_id,
        FECHA.fecha_publicacion,
        URL.url_id,
        URL.fecha_registro,
        URL.url_pegado
    FROM ARCHIVO
    LEFT JOIN ARCHIVO_AUTOR ON ARCHIVO.archivo_id = ARCHIVO_AUTOR.archivo_id
    LEFT JOIN AUTOR ON ARCHIVO_AUTOR.autor_id = AUTOR.autor_id
    INNER JOIN FECHA ON ARCHIVO.fecha_id = FECHA.fecha_id
    INNER JOIN URL ON ARCHIVO.url_id = URL.url_id
    WHERE ARCHIVO.archivo_id = ?;
    """
    return retrieve_data_with_query(conn, query_vda, (archivo_id,))

# BOOKMARKS
def contar_total_carpetas (conn) -> int:
    """ Retrieve the number of bookmark folders in the repository """
    cur = conn.cursor()
    cur.execute(f"SELECT COUNT(carpeta_id) FROM CARPETA")
    rows = cur.fetchone()
    return rows[0]

def listar_carpeta_numero_archivos(conn) -> list:
    query_lcna = """
    SELECT
        CARPETA.carpeta_id
        CARPETA.nombre,    
        COUNT (ARCHIVO.archivo_id)
    FROM CARPETA
    LEFT JOIN BOOKMARK ON CARPETA.carpeta_id = BOOKMARK.carpeta_id
    LEFT JOIN ARCHIVO ON BOOKMARK.archivo_id = ARCHIVO.archivo_id
    GROUP BY CARPETA.carpeta_id, CARPETA.nombre
    ORDER BY CARPETA.carpeta_id;
    """
    return retrieve_data_with_query(conn, query_lcna)

def archivos_guardados_en_carpetas(conn) -> list:
    query_agec = """
    SELECT
        CARPETA.carpeta_id,
        CARPETA.nombre,
        ARCHIVO.archivo_id,
        ARCHIVO.titulo,
        AUTOR.nombre,
        FECHA.fecha_publicacion
    FROM BOOKMARK
    INNER JOIN CARPETA ON BOOKMARK.carpeta_id = CARPETA.carpeta_id
    INNER JOIN ARCHIVO ON BOOKMARK.archivo_id = ARCHIVO.archivo_id
    LEFT JOIN ARCHIVO_AUTOR ON ARCHIVO.archivo_id = ARCHIVO_AUTOR.archivo_id
    LEFT JOIN AUTOR ON ARCHIVO_AUTOR.autor_id = AUTOR.autor_id
    INNER JOIN FECHA ON ARCHIVO.fecha_id = FECHA.fecha_id
    ORDER BY CARPETA.nombre, ARCHIVO.titulo;
    """
    return retrieve_data_with_query(conn, query_agec)

def ver_archivos_por_carpeta(conn, carpeta_id) -> list:
    query_vapc = """
    SELECT
        ARCHIVO.archivo_id,
        ARCHIVO.titulo,
        AUTOR.nombre,
        FECHA.fecha_publicacion
    FROM BOOKMARK
    INNER JOIN ARCHIVO ON BOOKMARK.archivo_id = ARCHIVO.archivo_id
    LEFT JOIN ARCHIVO_AUTOR ON ARCHIVO.archivo_id = ARCHIVO_AUTOR.archivo_id
    LEFT JOIN AUTOR ON ARCHIVO_AUTOR.autor_id = AUTOR.autor_id
    INNER JOIN FECHA ON ARCHIVO.fecha_id = FECHA.fecha_id
    WHERE BOOKMARK.carpeta_id = ?
    ORDER BY ARCHIVO.titulo;
    """
    return retrieve_data_with_query(conn, query_vapc, (carpeta_id,))

# DESCARGAS
def ver_archivos_descarga(conn) -> list:
    query_vad = """
    SELECT
        ARCHIVO.archivo_id,
        ARCHIVO.titulo,
        AUTOR.nombre,
        FECHA.fecha_publicacion
    FROM DESCARGA
    INNER JOIN ARCHIVO ON DESCARGA.archivo_id = ARCHIVO.archivo_id
    LEFT JOIN ARCHIVO_AUTOR ON ARCHIVO.archivo_id = ARCHIVO_AUTOR.archivo_id
    LEFT JOIN AUTOR ON ARCHIVO_AUTOR.autor_id = AUTOR.autor_id
    INNER JOIN FECHA ON ARCHIVO.fecha_id = FECHA.fecha_id
    ORDER BY ARCHIVO.titulo;
    """
    return retrieve_data_with_query(conn, query_vad)


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