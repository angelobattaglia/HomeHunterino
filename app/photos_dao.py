import sqlite3

def add_photos(advert):
    # Connect to the SQLite database
    con = sqlite3.connect('datas.db')
    # The following line configures the connection to return rows as dictionary-like objects. 
    # This allows accessing the columns of each row by names, 
    # making the code more readable and maintainable.
    con.row_factory = sqlite3.Row
    # Create a cursor object
    cur = con.cursor()

    # First I put into the database the advert
    sql = 'INSERT INTO advert() VALUES(?, ?, ?, ?, ?, ?, ?, ?) RETURNING id' # Returning id means that the
    cur.execute(sql, (advert['title_advert'], advert['address'], advert['property_type'], advert['rooms'], advert['description'], advert['price'], advert['furnished'], advert['id_user']))

    # If an image is submitted, then the first SQL statement is executed, otherwise the second one is executed.
    # TODO: to fix the folling if statements in its own context
    for image in advert['images']:
        sql = 'INSERT INTO photo() VALUES(?,?,?,?,?)'
        cur.execute(sql, ([''], [''], ['']))

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
