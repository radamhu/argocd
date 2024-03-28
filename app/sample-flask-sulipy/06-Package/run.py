from uzenofal import app

if __name__ == '__main__':
    # debug=True arra jó hogy az adatbázishoz NE újra is újra  adja hozzá az adatokat
    # de akkor a debug funkciótol eleseünk
    # erre megoldás a user_reloader=True 
    app.run(debug=True, use_reloader=False)