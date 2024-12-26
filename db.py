import os
import sqlite3

def initialize_database():
    db_path = 'app.db'
    tables = ['sets', 'inventory', 'minifigures', 'missing']
    row_counts = {}

    # Connect to the database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create the required tables if they do not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS wishlist (
        set_num TEXT,
        name TEXT,
        year INTEGER,
        theme_id INTEGER,
        num_parts INTEGER,
        set_img_url TEXT,
        set_url TEXT,
        last_modified_dt TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS sets (
        set_num TEXT,
        name TEXT,
        year INTEGER,
        theme_id INTEGER,
        num_parts INTEGER,
        set_img_url TEXT,
        set_url TEXT,
        last_modified_dt TEXT,
        mini_col BOOLEAN,
        set_check BOOLEAN,
        set_col BOOLEAN, 
        u_id TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
        set_num TEXT,
        id INTEGER,
        part_num INTEGER,
        name TEXT,
        part_img_url TEXT,
        part_img_url_id TEXT,
        color_id INTEGER,
        color_name TEXT,
        quantity INTEGER,
        is_spare BOOLEAN,
        element_id INTEGER,
        u_id TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS minifigures (
        fig_num TEXT,
        set_num TEXT,
        name TEXT,
        quantity INTEGER,
        set_img_url TEXT,
        u_id TEXT
    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS missing (
        set_num TEXT,
        id INTEGER,
        part_num TEXT,
        part_img_url_id TEXT,
        color_id INTEGER,
        quantity INTEGER,
        element_id INTEGER,
        u_id TEXT
    )''')
    
    # Commit the changes
    conn.commit()
    conn.close()

def get_rows():
    db_path = 'app.db'
    tables = ['sets', 'inventory', 'minifigures', 'missing']
    row_counts = {}

    # Connect to the database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get the row count for each table
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        row_count = cursor.fetchone()[0]
        row_counts[table] = row_count

    # Close the connection
    conn.close()

    return row_counts


def delete_tables():
    db_path = 'app.db'
    tables = ['sets', 'inventory', 'minifigures', 'missing']
    row_counts = {}

    # Connect to the database (this will create the file if it doesn't exist)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''DROP TABLE sets''')
    cursor.execute('''DROP TABLE inventory''')
    cursor.execute('''DROP TABLE minifigures''')
    cursor.execute('''DROP TABLE missing''')

    # Close the connection
    conn.close()

