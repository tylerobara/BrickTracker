import sqlite3
from pathlib import Path # creating folders
import sys

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

if len(sys.argv) > 1:

    cursor.execute('DELETE FROM sets where u_id="' +sys.argv[1]+ '";')
    conn.commit()

    cursor.execute('DELETE FROM inventory where u_id="' +sys.argv[1]+ '";')
    conn.commit()

    cursor.execute('DELETE FROM minifigures where u_id="' +sys.argv[1]+ '";')
    conn.commit()

    cursor.execute('DELETE FROM missing where u_id="' +sys.argv[1]+ '";')
    conn.commit()

    cursor.close()
    conn.close()

    exit()





cursor.execute('''DROP TABLE sets''')
cursor.execute('''DROP TABLE inventory''')
cursor.execute('''DROP TABLE minifigures''')
cursor.execute('''DROP TABLE missing''')

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
    set_col, BOOLEAN, 
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
    part_num INTEGER,
    color_id INTEGER,
    quantity INTEGER,
    element_id INTEGER,
    u_id TEXT
)''')



conn.close()

