from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
  {
    'id': 1,
    'title': 'Data Analyst',
    'location': 'Bengaluru, India',
    'salary': 'TS, 100.000'
  },
  {
    'id': 2,
    'title': 'Data Scientist',
    'location': 'Bengaluru, India',
    'salary': 'TS, 100.000'
  },
  {
    'id': 3,
    'title': 'Frontend Engineer',
    'location': 'Remote',
    'salary': ''
  },
  {
    'id': 4,
    'title': 'Backend Engineer',
    'location': 'San Fransico, USa',
    'salary': '$120.000'
  }
]

@app.route("/")
def hello_jovian():
    return render_template('home.html', 
                           jobs=JOBS,
                          company_name='Jovian')
@app.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)