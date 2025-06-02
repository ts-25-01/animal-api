import sqlite3

DATABASE = "tutorial.db"
con = sqlite3.connect(DATABASE) # hier machen wir die Verbindung auf

## Initialisiere das Cursor-Objekt, das später die SQL-Befehle an der DB ausführt
cur = con.cursor()

## Führe einfach mal einen SQL-Befehl aus
### IF NOT EXISTS überspringt das Erstellen der Tabelle sobald die Tabelle schon da ist
cur.execute("CREATE TABLE IF NOT EXISTS movie(title, year, score)")
# Verbindung nutzen, um SQL Befehl auszuführen
con.commit()
## SELECT name FROM sqlite_master gibt uns die angelegten Tabellen der DB wieder
res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())

## Jetzt wollen wir mal Daten hinzufügen
cur.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
""")
con.commit()
res = cur.execute("SELECT title FROM movie")
print(type(res.fetchall()))

data = [
    ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    ("Monty Python's The Meaning of Life", 1983, 7.5),
    ("Monty Python's Life of Brian", 1979, 8.0),
]
cur.executemany("INSERT INTO movie (title, year, score) VALUES(?, ?, ?)", data)
con.commit()  # Remember to commit the transaction after executing INSERT.

for row in cur.execute("SELECT year, title FROM movie ORDER BY year"):
    print(row)