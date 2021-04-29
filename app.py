from flask import Flask, render_template, url_for, request, redirect
import firebase_admin
from firebase_admin import db
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc123@567$#'

# Initialize Firebase app
firebase_admin.initialize_app(options={'databaseURL': 'https://vitask.firebaseio.com/'})
ref = db.reference('vitask')

def fetch_data():
    data = ref.child("owasp").child("leaderboard").get()
    return data

@app.route('/', methods=['GET','POST'])
def index():
    users = fetch_data()
    ranking = []
    for i in users:
        ranking.append(users[i])
        
    for i in range(0,len(ranking)):
        for j in range(0,len(ranking)-i-1):
            if(ranking[j]["Rating"]<ranking[j+1]["Rating"]):
                ranking[j], ranking[j+1] = ranking[j+1], ranking[j]
    
    return render_template('index.html', users = ranking)


if __name__ == '__main__':
    app.run(debug=True)