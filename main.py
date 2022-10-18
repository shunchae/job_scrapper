from flask import Flask, render_template, request, redirect, send_file
from extractors.remoteok import extract_jobs_remoteok
from extractors.wwr import extract_jobs_wwr
from extractors.indeed import extract_indeed_jobs
from file import save_to_file

app = Flask("JobScrapper")

db = {}

@app.route("/")
def home():
  return render_template("home.html")

@app.route("/search")
def search():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword in db:
    jobs = db[keyword]
  else:
    remoteok = extract_jobs_remoteok(keyword)
    wwr = extract_jobs_wwr(keyword)
    #indeed = extract_indeed_jobs(keyword)
    jobs = remoteok + wwr
    #jobs = remoteok + wwr + indeed
    
    db[keyword] = jobs
  return render_template("search.html", keyword=keyword, jobs=jobs)

@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword == None:
    return redirect("/")
  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
