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
...
## Anlegen von Feature-Branches
1. Wenn wir ein neues Feature zu unserer Anwendung bauen wollen, sollten wir uns einen eigenen Branch dafür anlegen. Das geht mit dem folgenden Befehl:
```bash
git checkout -b feature/PUT-Route
```
Jetzt wird ein neuer Branch mit dem Namen erstellt und wir wechseln direkt auf diesen Branch innerhalb unseres Terminals.
2. Wenn wir diesen Branch pushen wollen, dann müssen wir folgendes beachten: Pro neuen Branch den wir uns anlegen, müssen wir auch den upstream vor dem Pushen jeweils einrichten mit
```bash
git push --set-upstream origin feature/PUT-Route
```
3. Danach kannst du immer weiter Veränderungen durchführen, committen, pushen...
4. Beachte, dass du mit jedem Commit ein Commit Ahead bist vom Main-Branch
5. Außerdem wenn etwas parallel auf dem Main-Branch verändert wird, dann bist du auch so viele Commit behind..
Behind und Ahead ist nicht gut wenn das zu groß wird, deswegen REGELMÄßIG mit dem main-Branch wieder mergen mit
```bash
git merge main
```
Dann öffnet sich ein VIM-Fenster für die Merge-Message. Das könnt ihr schließen und speichern mit ESC und :wq und ENTER. Das dann bitte wieder pushen