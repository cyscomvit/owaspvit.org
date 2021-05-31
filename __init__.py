# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, redirect
import firebase_admin
from firebase_admin import db
import os
import random

from github import Github

from bot_token import github_token

# Initialize Flask app
app = Flask(__name__)
application = app


# Set the port for Flask app
port = int(os.environ.get('PORT', 5000))

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/var/www/FlaskApp/FlaskApp/firebase.json"

# GitHub Access Token
g = Github(github_token())


# Initialize Firebase app
firebase_admin.initialize_app(options={'databaseURL': 'https://vitask.firebaseio.com/'})
ref = db.reference('vitask')

def fetch_data():
    data = ref.child("owasp").child("leaderboard").get()
    return data

def project_data():
    data = ref.child("owasp").child("projects").get()
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

if __name__ == '__main__':
    app.run(port=port, debug=True)
