from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

app = Flask(__name__)
  
@app.route("/")
def hello_jovian():
  jobs = load_jobs_from_db()
  # jobs = jobs : az első jobs vairable amit a home.html-ben használunk
  # a második jobs az pedig jobs = load_...
  return render_template('home.html', 
                          jobs=jobs)
@app.route("/api/jobs")
def list_jobs():
  jobs = load_jobs_from_db()
  return jsonify(jobs)

@app.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  # return jsonify(job)
  
  if not job:
    return "Not found", 404
  
  return render_template('jobpage.html', 
                        job=job)

@app.route("/job/<id>/apply", methods=['GET', 'POST'])
def apply_to_job(id):
  data = request.form
  job = load_job_from_db(id)
  add_application_to_db(id, data)
  # return jsonify(data)
  # store this in the DB
  # send an email
  # display an acknowledgment
  return render_template('application_submitted.html',
                        application=data,
                        job=job
                        )
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)