# importiere Flask von dem Modul flask
from flask import Flask, jsonify

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

# App starten
if __name__ == "__main__":
    app.run(debug=True)