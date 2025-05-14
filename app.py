# importiere Flask von dem Modul flask
from flask import Flask, jsonify, request

# initialisiere ein app-Objekt von der Klasse Flask
app = Flask(__name__)

## Tiere in einer Liste speichern -> Local Storage
animals = ["dog", "cat", "bird"]

## Test-Route für Startseite
@app.route("/")
def home():
    return "Hallo, das eine Tier-Api"

## GET-Route implementieren, d.h. Daten abrufen bzw. alle Tiere anzeigen
@app.route("/api/animals", methods=['GET'])
def show_animals():
    return jsonify(animals), 200

## POST-Route implementieren, d.h. neue Tier hinzufügen
@app.route("/api/animals", methods=['POST'])
def add_animal():
    ## Funktion um die Daten im JSON-Format aus dem Request-Objekt zu bekommen
    data = request.get_json()
    ## in new_animal ist dann der Value vom Key "name" enthalten
    new_animal = data.get("name").lower() #da unsere daten im localstorage einheitlich alle mit Kleinbuchstaben sind
    if new_animal not in animals:   #Prüfen ob das Tier schon vorhanden ist, wenn nicht, dann wirds hinzugefügt (schneller als alles auf ein Set umzubauen
        animals.append(new_animal)
        return f"{new_animal} wurde erfolgreich hinzugefügt", 201
    else:
        return f"{new_animal} wurde nicht hinzugefügt, da es bereits in der Liste vorhanden ist", 404

## DELETE-Route, um ein Tier aus der Liste zu löschen
@app.route("/api/animals/<name>", methods=['DELETE'])
def delete_animal(name):
    name = name.lower() #damit das was in der Route genannt wird im Lowercase geprüft wird, dass falls der User Dog eingibt, trotzdem dog gelöscht wird
    if name in animals:
        animals.remove(name)
        return f"{name} wurde aus der Liste gelöscht", 200
    else:
        return f"{name} ist nicht in der Liste enthalten", 404



# App starten
if __name__ == "__main__":
    app.run(debug=True)