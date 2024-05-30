import sqlite3

def create_table_users():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "users" (
            "id" INTEGER NOT NULL,
            "email" TEXT NOT NULL UNIQUE,
            "user_type" TEXT NON NULL,
            "password" TEXT NOT NULL,
            PRIMARY KEY("id")
        );
    ''')
    conn.commit()
    conn.close()

def create_table_adverts():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "adverts" (
	        "id"	INTEGER NOT NULL,
	        "title"	TEXT NOT NULL,
	        "address"	TEXT NOT NULL,
	        "type"	TEXT NOT NULL,
	        "rooms"	INTEGER NOT NULL,
	        "description"	TEXT NOT NULL,
	        "price"	INTEGER NOT NULL,
	        "furnished"	INTEGER NOT NULL,
	        "id_landlord"	INTEGER NOT NULL,
	        "publicly_available"	INTEGER NOT NULL,
	        PRIMARY KEY("id")
        );
    ''')
    conn.commit()
    conn.close()

def create_table_photos():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "photos" (
	        "id" INTEGER NOT NULL,
	        "advert_id"	INTEGER NOT NULL,
	        "file_name"	TEXT,
	        FOREIGN KEY("advert_id") REFERENCES "annunci"("id"),
	        PRIMARY KEY("id")
        );
    ''')
    conn.commit()
    conn.close()


def create_table_bookings():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "bookings" (
        "id" INTEGER NOT NULL,
        "advert_id" INTEGER NOT NULL,
        "user_id" INTEGER NOT NULL,
        "status" TEXT NOT NULL CHECK(status IN ('request', 'accepted', 'refused')),
        "refusal_reason" TEXT,
        FOREIGN KEY("advert_id") REFERENCES "adverts"("id"),
        FOREIGN KEY("user_id") REFERENCES "users"("id"),
        PRIMARY KEY("id")
    );
    ''')
    conn.commit()
    conn.close()