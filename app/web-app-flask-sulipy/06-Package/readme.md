Initiate a Windows based python APP development environment
```
clone repository && cd into it
python -m venv .venv
.\.venv\Scripts\activate
# pip freeze > requirements.txt
pip install -r requirements.txt
create .env file under root folder (see next chapter)
python run.py --debug run
```

03 - jinja

- data.py beolvasás az uzenofal03.py-ben
- htlm fájlokban a következő jinja blokkok használata
```
{% extends 'index.html' %}
{% block content %}
```
- uzenofal03.py-ban ennek a route-ok átírása, hogy értsék a jinja template-s html fájlokat
- {{ title }} használata index.html-ben az uzenofal03.py szerint

04 - forms

<input ... name="változó neve" # name= amilyen néven majd a backend oldalon változóban tárolom az adatot
@app.route('/course/new', methods=['GET', 'POST'])

{{ url_for('message_board') }} 
# itt a message board a route alatti függvény neve és a hozzá tartozó URL, innen fogja tudni hogy melyik url-re kell irányítani 

04 - Advanced

Ali Gencay ChatGPT
Unofficial TabNine client (all-language autocomplete) for the VS Code.
https://github.com/humiaozuzu/awesome-flask

wtform extensions, validators
forms.py
create.html átalakítása
Flask flash  messaging
uzenofal04.py
index.html

05 - Database

TBD

06 - Package(s) / csomag(ok)

UZENOFAL PACKAGE LÉTREHOZSA

https://exploreflask.com/en/latest/ projekt struktúra
uzenofal package folder
    package : felmerül az az igény, hogy alegységekbe szervezzük, több fáklba, részbe elsoztva tárolódik a kódunk
    ezek a modulok / fájlok, megfelleő helyen gondoskodunk az importálásukról
    sok modul esetén a modulokat is csoportosítsuk, package-ekbe / csomagokba, logikailag egybe tartozó modulok
    most csak 1db csomag van, az uzenófal

# run.py

# config.py 

használata érzékeny adatok elrejtésére
instance config.py még ennél érézkenyebb adatok elrejtésére is használható
