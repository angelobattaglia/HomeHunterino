import sqlite3

def create_table_utenti():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "utenti" (
            "id" INTEGER NOT NULL,
            "nickname" TEXT NOT NULL,
            "email" TEXT NOT NULL UNIQUE,
            "user_type" TEXT NON NULL,
            "password" TEXT NOT NULL,
            PRIMARY KEY("id")
        )
    ''')
    conn.commit()
    conn.close()

def create_table_raccolte():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "" (
        );
    ''')
    conn.commit()
    conn.close()

def create_table_donazioni():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "" (
        );
    ''')
    conn.commit()
    conn.close()
