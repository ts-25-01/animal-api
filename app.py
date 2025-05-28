# importiere Flask von dem Modul flask
from flask import Flask, jsonify, request
# importiere Swagger vom flasgger Modul
from flasgger import Swagger
# importiere das sqlite3 Modul, das ist integriert in Python
import sqlite3

# initialisiere ein app-Objekt von der Klasse Flask
app = Flask(__name__)
# initialisiere ein swagger-Objekt von der Klasse Swagger, übergebe dabei das app-Objekt
swagger = Swagger(app)

# Lege Konstante an, der den Pfad zu Datenbank-Datei beschreibt
#DATABASE_URL = "http://127.0.0.1:5432" # später wird für unsere Postgres
DATABASE = "./animals.db" # hier liegt dann unsere DB-Datei 

# Datenbank-Hilfsfunktionen
## Funktion, um sich mit der Datenbank zu verbinden
def get_db_connection():
    con = sqlite3.connect(DATABASE)
    con.row_factory = sqlite3.Row # super praktische Einstellung, damit wir Ergebnisse von SQL-Befehlen im richtigen Datenformat (Dictionary bzw. JSON-Format) zurückbekommen
    return con
# Seeding-Skript für die Datenbank
## Funktion, um die Datenbank zu initialisieren
def init_db():
    # Initialisieren der DB
    con = get_db_connection() # rufe Hilfsfunktion auf
    cur = con.cursor()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS Animals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER,
                    genus TEXT    
                )
                ''')
    # Überprüfe, ob Zeilen, also Datensätze in der Animals-Tabelle drin sind
    count = cur.execute('SELECT COUNT(*) FROM Animals').fetchone()[0] # gibt uns ein Tupel zurück z.B. (1,), aber mit [0] greifen wir nur auf den ersten Index des Tupels zu
    if count == 0:
        data = [
            ('dog', 3, 'mammals'),
            ('cat', 2, 'mammals'),
            ('elephant', 20, 'mammals'),
            ('bird', 5, 'birds')
        ]
        cur.executemany('INSERT INTO Animals (name, age, genus) VALUES (?,?,?)', data) # das geht er jeweils für jeden Eintrag der data durch
        con.commit() # an dieser Stelle werden die Änderungen persistiert und gespeichert, d.h. Transaktion wird abgeschlossen
    con.close()
## Test-Route für Startseite
@app.route("/")
def home():
    return "Hallo, das eine Tier-Api"

## GET-Route implementieren, d.h. Daten abrufen bzw. alle Tiere anzeigen
@app.route("/api/animals", methods=['GET'])
def show_animals():
    """
    Liste aller Tiere
    ---
    responses:
        200:
            description: JSON-Liste aller Tiere
            examples:
                application/json:
                    - id: 1
                      name: Dog
                      age: 3
                      genus: mammals
                    - id: 2
                      name: Cat
                      age: 2
                      genus: mammals
    """
    # Daten abrufen von der DB
    con = get_db_connection() # Verbindung mit der DB
    cur = con.cursor()
    animals = cur.execute('SELECT * FROM Animals').fetchall()
    con.close()
    return jsonify([dict(animal) for animal in animals]), 200

## POST-Route implementieren, d.h. neue Tier hinzufügen
@app.route("/api/animals", methods=['POST'])
def add_animal():
    """
    Neues Tier hinzufügen
    ---
    consumes:
        - application/json
    parameters:
        - in: body
          name: tier
          required: true
          schema:
            type: object
            properties:
                name:
                    type: string
                    example: Elephant
                age:
                    type: integer
                    example: 10
                genus:
                    type: string
                    example: mammals
    responses:
        201:
            description: Name wurde erfolgreich hinzugefügt
        400:
            description: Fehler, kein Objekt übergeben
    """
    new_animal = request.get_json() # {"name": "turtle", "age:": 100, "genus": "reptile"}
    if not new_animal or 'name' not in new_animal:
        return jsonify({"message": "Keine oder fehlerhafte Daten übertragen"}), 400
    con = get_db_connection() # Schritt 1: DB-Verbindung
    cur = con.cursor() # Schritt 2: Cursor-Objekt definieren
    # Schritt 3: Befehl ausführen
    cur.execute('INSERT INTO Animals (name, age, genus) VALUES (?,?,?)', 
                (new_animal['name'],
                 new_animal['age'],
                 new_animal['genus'])
                ) # An dieser Stelle SQL-Befehl zum Hinzufügen des neuen Objektes
    con.commit() # Schritt 4: Persistieren der Veränderungen
    con.close() # Schritt 5: Verbindung zur DB wieder schließen
    return jsonify({"message": "Tier wurde erfolgreich hinzugefügt"}), 201

## DELETE-Route, um ein Tier aus der Liste zu löschen
@app.route("/api/animals/<int:animal_id>", methods=['DELETE'])
def delete_animal(animal_id):
    """
    Ein Tier löschen
    ---
    parameters:
        - name: id
          in: path
          type: integer
          required: true
          description: Der Name des zu löschenden Tieres
    responses:
        200:
            description: Tier wurde gelöscht
            examples:
                application/json:
                    - message: Tier wurde gelöscht
        404:
            description: Tier wurde nicht gefunden
    """
    con = get_db_connection() 
    cur = con.cursor()
    # Überprüfe, ob das Tier mit der angegebenen ID überhaupt existiert
    animal = cur.execute('SELECT * FROM Animals WHERE id = ?', (animal_id,)).fetchone() # 4 OR 1=! --
    if animal is None:
        return jsonify({"message": "Tier mit dieser ID existiert nicht"}), 404
    cur.execute('DELETE FROM Animals WHERE id = ?', (animal_id,) )
    ## Achtung: Nutz bitte die ?-Funktion, um SQL-Injection zu verhindern, sonst sähe es so aus:
    # cur.execute(f'DELETE FROM Animals WHERE id = {animal_id}') # 4 OR 1=! --
    con.commit()
    con.close()
    return jsonify({"message": "Tier wurde erfolgreich gelöscht"}), 200

## Baue eine Funktion, zum Updaten
## PUT-Route -> Ersetze alle Eigenschaften eines Tieres, d.h. hier schicken wir alle Eigenschaften im Body als JSON mit
@app.route("/api/animals/<name>", methods=['PUT'])
def put_animal(name):
    """
    Ganzes Tier ersetzen
    ---
    parameters:
        - name: name
          in: path
          type: string
          required: true
          description: Der Name des Tiers, das ersetzt werden soll
        - in: body
          name: tier
          required: true
          schema: 
            type: object
            properties:
                id:
                    type: integer
                    example: 3
                name:
                    type: string
                    example: elephant
                age:
                    type: integer
                    example: 20
                genus:
                    type: string
                    example: mammals
    responses:
        200:
            description: Tier wurde ersetzt
            examples:
                application/json:
                    - message: Tier wurde ersetzt
        404:
            description: Tier wurde nicht gefunden
            examples:
                application/json:
                    - message: Tier wurde nicht gefunden
    """
    updated_animal = request.get_json() # in data wird das Ganze JSON-Objekt gespeichert, das vom Client im Body übergeben wird
    # Suche nach dem Objekt, das wir updaten wollen
    for animal in animals:
        if animal["name"] == name:
            animal.clear() # Lösche alle Werte des gefundenen Tieres
            animal.update(updated_animal) # Setze die Werte auf die Werte, die wir im JSON-Format in der Variablen data speichern
            # return f"{name} wurde geupdated", 200
            return jsonify({"message": "Tier wurde geupdated"}), 200
    # return f"{name} wurde nicht gefunden", 404
    return jsonify({"message": "Tier wurde nicht gefunden"}), 404


## PATCH-Route -> Ersetze spezifisch einzelne Eigenschaften, d.h. hier schicken wir nur die zu ändernden Eigenschaften im Body als JSON mit
@app.route("/api/animals/<name>", methods=["PATCH"])
def patch_animal(name):
    """
    Tier teilweise ändern (z.B. nur das Alter)
    ---
    parameters:
        - name: name
          in: path
          type: string
          required: true
          description: Der Name des Tiers, das ersetzt werden soll
        - in: body
          name: tier
          required: anyOf
          schema: 
            type: object
            properties:
                id:
                    type: integer
                    example: 3
                name:
                    type: string
                    example: elephant
                age:
                    type: integer
                    example: 20
                genus:
                    type: string
                    example: mammals
    responses:
        200:
            description: Tier wurde geupdated
            examples:
                application/json:
                    - message: Tier wurde geupdated
        404:
            description: Tier wurde nicht gefunden
            examples:
                application/json:
                    - message: Tier wurde nicht gefunden

    """
    update_data = request.get_json()
    for animal in animals:
        if animal["name"] == name:
            animal.update(update_data)
            # return f"{name} wurde geupdated", 200
            return jsonify({"message": "Tier wurde geupdated"}), 200
    # return f"{name} wurde nicht gefunden", 404
    return jsonify({"message": "Tier wurde nicht gefunden"}), 404

# App starten
if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5050, debug=True)
