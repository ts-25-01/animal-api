## Einrichtung des Python-Projektes
1. VENV anlegen mit `python -m venv venv-animal-api`
2. VENV aktivieren mit `source venv-animal-api/Scripts/activate`
3. Flask installieren mit `pip install flask` 
4. Abhängigkeiten festhalten mit `pip freeze > requirements.txt'`
## Einrichtung des Git-Repositories
1. Git-Repository initialisieren mit `git init`
2. gitignore erstellen mit `touch .gitignore` oder direkt mit `echo "venv-animal-api" > .gitignore` 
3. Status überprüfen mit `git status` 
4. Füge Veränderungen zur Staging-Area hinzu mit `git add .`
5. Mache einen Commit mit `git commit -m "Initial Commit"`
6. Erstelle dir ein Repository auf Github.
7. Füge das erstellte Repository (Github) als Remote Repository hinzu mit `git remote add origin https://github.com/ts-25-01/animal-api.git`
8. Pushe deine Veränderungen mit `git push -u origin main` 
## Erstellen der app.py
1. Erstelle dir eine Datei mit dem Namen `app.py`