import sqlite3

def get_adverts():
    conn = sqlite3.connect('datas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # TODO
    sql = ''
    cursor.execute(sql)
    adverts = cursor.fetchall()

    cursor.close()
    conn.close()

    return adverts

def get_advert(id):
    conn = sqlite3.connect('datas.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # TODO
    sql = ''
    cursor.execute(sql, (id,))
    advert = cursor.fetchone()

    cursor.close()
    conn.close()

    return advert

# ------------------------------------------------
# ------------------------------------------------
# ------------------------------------------------
# Retrieving all the posts
# input: post, which is expected to be a dictionary containing the data for the new post.
def add_advert(advert):
    # Connect to the SQLite database
    con = sqlite3.connect('datas.db')
    # The following line configures the connection to return rows as dictionary-like objects. 
    # This allows accessing the columns of each row by names, 
    # making the code more readable and maintainable.
    con.row_factory = sqlite3.Row
    # Create a cursor object
    cur = con.cursor()

    # If an image is submitted, then the first SQL statement is executed, otherwise the second one is executed.
    # TODO: to fix the folling if statements in its own context
    if 'images' in advert:
        # the sql variable has its fields that have to corrispond to the fields of the database
        # the post['date'], post['text'], post['immagine_post'], post['id_utente'] are the fields of the dictionary post
        # hence these might not have the same name
        sql = 'INSERT INTO adverts() VALUES(?,?,?,?,?)'
        cur.execute(sql, (advert[''], advert[''], advert[''], advert[''], advert['']))
    else:
        sql = 'INSERT INTO adverts() VALUES(?,?,?,?)'
        cur.execute(sql, (advert[''], advert[''], advert[''], advert['']))

    # This method is focused on verifying that the changes are committed to the database,
    # hence, it's a good practice to structure an if-then-else statement to handle the commit.
    try: 
        con.commit()
        success = True
    # In case of exception, the code rolls back the transaction to the last commit point.
    except Exception as e:
        print('ERROR', str(e))
        con.rollback()

    # Close the cursor and the connection
    cur.close()
    con.close()

    return success
