from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
# config.py KONFIGURÁCIÓS BEÁLLÍTÁSOK használata érzékeny adatok elrejtésére
app.config.from_object('config')
db.init_app(app)

# az útvonalakat; routes.py modult elérhető kell tennünk 
from uzenofal import routes