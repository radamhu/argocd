from flask import Flask, redirect, url_for, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from data import courses
from forms import NewCoursesForm

db = SQLAlchemy()
app = Flask(__name__)
# A secret key is required to use CSRF.
app.config['SECRET_KEY'] = '12345'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db.init_app(app)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    teacher = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

# arra vigyázzunk hogyha fájl formátumban hozunk létre DB-t
# applikációt másodászorra futtatjuk akkor erre az iniciáliazáslára már nem lesz szükség
# nem kell újra és újra bővítani ezekkel az adatokkal a DB-t
# viszonz memória típusú DB esetén ez maradhatna
# with app.app_context():
#     db.create_all()
#     for course in courses:
#         course_obj = Course(title=course['title'], teacher=course['teacher'], date=course['date'])
#         db.session.add(course_obj)
#     db.session.commit()
#     # régebbi típusú lekérdezése az objektumoknak
#     print(Course.query.all())

@app.route('/')
@app.route('/home')
def home():
    # scalars = több objektumot kérek le vagy csak egyet
    courses_db = db.session.execute(db.select(Course)).scalars()
    # fordított logika, a courses.html-t adom át, nem az index.html-t, utóbbit majd a render-elés során megtalálja a courses.html kódja alapján
    # és feltölti a courses lista elemeivel
    return render_template('courses.html', courses=courses_db, title='Üzenőfal')


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
    form = NewCoursesForm()
    if request.method == 'POST':
        # megviszgáljuk hogy jól vannak e kitöltve
        if form.validate_on_submit():
            # kiolvassuk GET metódussal az adatokat a backendből
            # lista ami a kurzusokat tartalmazza : list elemei szótárak kulcsokkal, szótárt kell létrehozni és hozzáfűzni a listához
            # szótár, mindig a kulcsot adjuk meg aztán a változó tartalmát
            # létrehozunk egy objektumot
            #courses.append({'title': form.title.data, 'teacher': form.teacher.data, 'date': form.date.data})
            current_course = Course(title=form.title.data, teacher=form.teacher.data, date=form.date.data)
            db.session.add(current_course)
            db.session.commit()
            # flash package import, és az index.html-ben is meg kell határozni
            flash('A kurzus a megadott adatokkal mentésre került!', 'success')
            # valaki kitöltötte a form-ot hova küldjük, home által kezel utvonalra mondjuk visszirányxítjuk
            # home-hoz nem csapunk hozzá semmilyen adatot, mint a crate-html form objektum estén, hanem a flash függvényt hívjuk, központi tárolóba rakja be az üzenetet
            # ami üzenetet majd az index-html esetén  a get_flashed_messages fv-el olvasunk ki
            return redirect(url_for('home'))
    # ha nem PSOT-al hanem GET-el érkezett a request
    # most kell kiküldeni az üres űrlapot
    # az itt létrehozzott form objektumot átadjuk --> ilyen néven majd hivatkozukn rá a create.html-en  form = form <-- ilyen néven hoztuk itt létre az ogjektumot
    # a html doku rendeléséhez hozzacsapott form objektum viszi magával az adaokat a backend-ről a frontend felé
    return render_template('create.html', title='Új kurzus létrehozása', form=form)


if __name__ == '__main__':
    # debug=True arra jó hogy az adatbázishoz NE újra is újra  adja hozzá az adatokat
    # de akkor a debug funkciótol eleseünk
    # erre megoldás a user_reloader=True 
    app.run(debug=True, use_reloader=False)