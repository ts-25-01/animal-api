from flask import Flask
from database import init_db
from animals import register_animal_routes
from owners import register_owner_routes
from statistics_route import register_statistics_routes

flask_app = Flask(__name__)

init_db()
register_animal_routes(flask_app)
register_owner_routes(flask_app)
register_statistics_routes(flask_app)

if __name__ == "__main__":
    flask_app.run(debug=True, port=5050)

