Initiate a Windows based python APP development environment
```
clone repository && cd into it
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
create .env file under root folder (see next chapter)
python uzenofal02.py --debug run
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
