from flask import Flask, redirect, url_for, render_template, request, flash
from data import courses
from forms import NewCoursesForm

app = Flask(__name__)
# A secret key is required to use CSRF.
app.config['SECRET_KEY'] = '12345'

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
    form = NewCoursesForm()
    if request.method == 'POST':
        # megviszgáljuk hogy jól vannak e kitöltve
        if form.validate_on_submit():
            # kiolvassuk GET metódussal az adatokat a backendből
            # lista ami a kurzusokat tartalmazza : list elemei szótárak kulcsokkal, szótárt kell létrehozni és hozzáfűzni a listához
            # szótár, mindig a kulcsot adjuk meg aztán a változó tartalmát
            courses.append({'title': form.title.data, 'teacher': form.teacher.data, 'date': form.date.data})
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
    app.run(debug=True)