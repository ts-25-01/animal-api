# importiere Flask von dem Modul flask
from flask import Flask, jsonify, request
# importiere Swagger vom flasgger Modul
from flasgger import Swagger

# initialisiere ein app-Objekt von der Klasse Flask
app = Flask(__name__)
# initialisiere ein swagger-Objekt von der Klasse Swagger, übergebe dabei das app-Objekt
swagger = Swagger(app)

## Tiere in einer Liste speichern -> Local Storage
animals = [
    { "id": 1, "name": "dog", "age": 3, "genus": "mammals"},
    { "id": 2, "name": "cat", "age": 2, "genus": "mammals"}
]

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
                    - 1: 20
                      name: Dog
                      age: 3
                      genus: mammals
                    - id: 2
                      name: Cat
                      age: 2
                      genus: mammals
    """
    return jsonify(animals), 200

## POST-Route implementieren, d.h. neue Tier hinzufügen
@app.route("/api/animals", methods=['POST'])
def add_animal():
    ## Funktion um die Daten im JSON-Format aus dem Request-Objekt zu bekommen
    new_animal = request.get_json() # Hole dir aus dem Request-Objekt die Daten im JSON-Format
    # { "id": 3, "name": .., "age": ..., "genus": ...}

    animals.append(new_animal) # hänge das Objekt im JSON-Format hinten dran
    return f"{new_animal} wurde erfolgreich hinzugefügt", 201

## DELETE-Route, um ein Tier aus der Liste zu löschen
@app.route("/api/animals/<name>", methods=['DELETE'])
def delete_animal(name):
    for animal in animals:
        if animal["name"] == name:
            animals.remove(animal)
            return f"{name} wurde gelöscht", 200
    return f"{name} wurde nicht gefunden", 404

## Baue eine Funktion, zum Updaten
## PUT-Route -> Ersetze alle Eigenschaften eines Tieres
## PATCH-Route

# App starten
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5050, debug=True)
