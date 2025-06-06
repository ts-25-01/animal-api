from database.database import get_db_connection, get_cursor

def get_owner_by_id(owner_id):
    con = get_db_connection()
    cur = get_cursor(con)
    cur.execute('SELECT * FROM Owners WHERE id = ?', (owner_id,))
    owner = cur.fetchone()
    con.close()
    return owner

def get_animal_by_id(animal_id):
    con = get_db_connection()
    cur = get_cursor(con)
    cur.execute('SELECT * FROM Animals WHERE id = ?', (animal_id,))
    animal = cur.fetchone()
    con.close()
    return animal

def get_animal_count():
    con = get_db_connection()
    cur = get_cursor(con)
    cur.execute('SELECT COUNT(*) AS count FROM Animals')
    animal_count = cur.fetchone()["count"]
    return animal_count

def get_owner_count():
    con = get_db_connection()
    cur = get_cursor(con)
    cur.execute('SELECT COUNT(*) AS count FROM Owners')
    owner_count = cur.fetchone()["count"]
    return owner_count