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

07-User-Registration

model.py átalakítása
data.py átalakítása
jwlazó kezelés init.py-ban gondoskodni 
routes.py átalakítása
idái megvagyunk userek adatai db-ben tároljik, inicializáljuk is az db-t, kurzus adato is helyesen jelennek meg a felületen

most pedig új felhasználót is szeretnénk regisztálni
forms.py
új html form ami megvalósítja a validációt
register.html
block content 2 nagy egységből épül fel
    h2 tag + form
form is 2 nagy egysb
    fieldset, beviteli mezők
fieldset
    4 egységet tudunk megkülönböztetni
    forsm osztály 4 attribútumának felel meg
    4 beviteli egység, ugyanolyan felépítésű
    username megadása

submit gomb

létre kell hozni a routes.py-ben hogy hívható legyen a registration.html

be kell kötni a register gombot az index.html-ben
index.html

08-login

flask-login import, példányosítás, inicializáljuk (__init__.py), session-öket használ az auth-hoz secret key-el rendelkezni kell
hogya tudjuk használni
1. definiálni kell egy fv-t visszatér egy User obketummal (user_id-t session-ből olvassa ki a pogram és ez alapján adja vissza a felhaználói objektumot)
    models.py
2. user oszátlynak meg kell valósítani az álbbi metóduksokat: pl is_authenticated, is_Active ..stb a flask_login web doksiban le van írva (mi mgunk is impelemntálhatjuk ezket a metódusokat, de használjuk inkán a UserMixin megoldást)
    models.py Class USer

webes felület, újabb form
    forms.py


