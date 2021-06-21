# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect, session, make_response
import firebase_admin
from firebase_admin import credentials, db, storage
import os
import random
import urllib.request
from PIL import Image
import img2pdf

from github import Github

from bot_token import github_token

# Initialize Flask app
app = Flask(__name__)
application = app
#app.secret_key = "secret key"


# Set the port for Flask app
port = int(os.environ.get('PORT', 5000))

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/var/www/FlaskApp/FlaskApp/firebase.json"

# GitHub Access Token
g = Github(github_token())


# Initialize Firebase app
#cred = credentials.Certificate("firebase.json")
# Production
cred = credentials.Certificate("/var/www/FlaskApp/firebase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':'https://vitask.firebaseio.com/',
    'storageBucket': 'vitask.appspot.com',
})
ref = db.reference('vitask')
bucket = storage.bucket()
blob = bucket.blob('dynamic certificate/')

def fetch_data():
    data = ref.child("owasp").child("leaderboard").get()
    return data

def project_data():
    data = ref.child("owasp").child("projects").get()
    return data

def certificates_data():
    data = ref.child("owasp").child("certificates").get()
    return data

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('homepage.html')

@app.route('/leaderboard', methods=['GET','POST'])
def leaderboard():
    users = fetch_data()
    ranking = []
    for i in users:
        ranking.append(users[i])
        
    for i in range(0,len(ranking)):
        for j in range(0,len(ranking)-i-1):
            if(ranking[j]["Rating"]<ranking[j+1]["Rating"]):
                ranking[j], ranking[j+1] = ranking[j+1], ranking[j]
    
    return render_template('index.html', users = ranking)


@app.route('/projects', methods=['GET','POST'])
def projects():
    project_all = project_data()
    projects = []
    for i in project_all:
        projects.append(project_all[i])
        
    for i in projects:
        repo = g.get_repo(f"{i['Username']}/{i['RepoName']}")
        i['stars'] = repo.stargazers_count
        i['views'] = repo.get_views_traffic()['count']
        
    projects = random.sample(projects, len(projects))
    return render_template('projects.html', projects = projects)

@app.route("/locker")
def locker():
    return render_template('locker.html')

@app.route("/data",methods=["POST"])
def data():
    if request.method=="POST":
        identifier = request.form.get("id", False)
        id_arr = identifier.split("#")
        try:
            name = id_arr[0]
            discord_name = id_arr[1]
        except Exception as e:
            error = "Invalid Identifier"
            return render_template('locker.html', error = error)
    users = fetch_data()
    for i in users:
        if(users[i]["Name"].casefold()==name.casefold() and users[i]["Discord"].casefold()==discord_name.casefold()):
            session.clear()
            session['name'] = users[i]['Name']
            session['discord'] = users[i]['Discord']
            return redirect(url_for('dashboard'))
        
    error = "Invalid Identifier"
    return render_template('locker.html', error = error)

@app.route("/dashboard")
def dashboard():
    if "name" not in session or "discord" not in session:
        return redirect(url_for('locker'))
    user = {}
    user['identifier'] = session['name'].casefold() + "-" + session['discord'].casefold()
    middle = session['name'].casefold().replace(" ", "%20") + "-" + session['discord'].casefold().replace(" ", "%20")
    user['year'] = []
    user['url'] = []
    baseurl = "https://firebasestorage.googleapis.com/v0/b/vitask.appspot.com/o/dynamic%20certificate%2F"
    certificates = certificates_data()
    for i in certificates:
        if(user['identifier'] == i):
            for j in certificates[i]:
                year = certificates[i][j]['Year']
                user['year'].append(year)
                url = baseurl + middle + "-" + year + "?alt=media"
                user['url'].append(url)
    
    return render_template('dashboard.html', user = user)

@app.route("/certificate", methods=["POST", "GET"])
def landingpage():
    if request.method == "POST":
    	url = request.form.get("url")
    	a = urllib.request.urlretrieve(url)
    	image = Image.open(a[0])
    	pdf_bytes = img2pdf.convert(image.filename)
    	response = make_response(pdf_bytes)
    	response.headers['Content-Type'] = 'application/pdf'
    	response.headers['Content-Disposition'] = 'inline; filename=certificate.pdf'
    	return response
    return render_template('certificate.html')

if __name__ == '__main__':
    app.run(port=port)
