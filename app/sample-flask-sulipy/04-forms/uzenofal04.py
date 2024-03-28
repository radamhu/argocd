from flask import Flask, redirect, url_for, render_template, request
from data import courses


app = Flask(__name__)


@app.route('/')
@app.route('/home')
def home():
    # fordított logika, a courses.html-t adom át, nem az index.html-t, utóbbit majd a render-elés során megtalálja a courses.html kódja alapján
    # és feltölti a courses lista elemeivel
    return render_template('courses.html', courses=courses, title='Üzenőfal')


@app.route('/message_board')
def message_board():
    return redirect(url_for('home'))


@app.route('/course/<int:number>')
def course(number):
    return f'Ez a {number}. kurzus adatlapja.'


@app.route('/contact')
def contact():
    return render_template('contact.html', title='Elérhetőség')

# methods segítségével megadom hogy ez a route a POST és a GET methód-ot is kezeli egyben
@app.route('/course/new', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # kiolvassuk GET metódussal az adatokat a backendből
        title = request.form.get('title')
        teacher = request.form.get('teacher')
        date = request.form.get('date')
        # lista ami a kurzusokat tartalmazza : list elemei szótárak kulcsokkal, szótárt kell létrehozni és hozzáfűzni a listához
        # szótár, mindig a kulcsot adjuk meg aztán a változó tartalmát
        courses.append({'title': title, 'teacher': teacher, 'date': date})
        # valaki kitöltötte a form-ot hova küldjük, home által kezel utvonalra mondjuk visszirányxítjuk
        return redirect(url_for('home'))
    return render_template('create.html', title='Új kurzus létrehozása')


if __name__ == '__main__':
    app.run(debug=True)