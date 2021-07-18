from flask import Flask, render_template, url_for, request, redirect, session, make_response
import firebase_admin
from firebase_admin import credentials, db, storage
import os
import random
import urllib.request
from PIL import Image
import img2pdf
from github import Github
from bot_token import github_token, ctfconf
import sys
import pyrebase
import requests
from flask_session import Session
from getpass import getpass
from datetime import datetime
from requests.sessions import DEFAULT_REDIRECT_LIMIT
from forms import *
from zxcvbn import zxcvbn
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
application = app
app.secret_key = "secretKey1234#Abc"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

# GitHub Access Token

g = Github(github_token())


# Initialize Firebase app
cred = credentials.Certificate("firebase.json")
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


"""
------------------------------------------------------------
                    OWASP VITCC CTF
------------------------------------------------------------
"""
ctf_ref = db.reference("/vitask/owasp/ctf")
firebaseconf = ctfconf()
firebase = pyrebase.initialize_app(firebaseconf)
storage = firebase.storage()
auth = firebase.auth()

@app.route('/ctf/')
@app.route('/ctf/home')
def home_page():
    if "uname" in session:
        return redirect(url_for('timer')) 
    else: 
        return render_template('/ctf_templates/home.html', session=session)

@app.route('/ctf/register', methods=["GET", "POST"])
def register():
    form = signup()
    flags={}
    if (request.method == 'POST'):
        username=request.form.get("uname")
        email=request.form.get("email")
        password=request.form.get("password")
        dataset=ctf_ref.get()
        results = zxcvbn(password)
        if dataset != None:
            for keys in dataset:
                if dataset[keys]["username"]==username:
                    flags["uname_exists"]=True
                    return render_template('/ctf_templates/register.html', form=form, flag=flags)
        if(len(password)<6):
            flags["invalidpass"]=1
            return render_template('/ctf_templates/register.html', form=form, flag=flags)
        if(results["score"]<3):
            flags["weak"]=True
            return render_template('/ctf_templates/register.html', form=form, flag=flags)
        try:
            user=auth.create_user_with_email_and_password(email,password)
            auth.send_email_verification(user['idToken'])
            data={
                "username": username,
                "emailid": email,
                "isUserflag":False,
                "isRootflag":False,
                "isFile":False,
                "scores": 0
            }
            ctf_ref.push(data)
            flags["registered"]=1
            session["registered"]=1
            return redirect(url_for('login'))
        except Exception as e:
            flags["registered"]=0
    return render_template('/ctf_templates/register.html', form=form, flag=flags)


@app.route('/ctf/leaderboard')
def ctf_leaderboard():
    if "uname" in session:
        users=[]
        dataset=ctf_ref.get().items()
        for keys, value in dataset:
        	users.append(value["username"])
        
        return render_template('/ctf_templates/leaderboard.html', vals=users) 
    else:
        return redirect(url_for('home_page'))

'''
@app.route('/ctf/leaderboard/testing')
def ctf_leaderboard_testing():
    if "uname" in session:
        users=[]
        dataset=ctf_ref.get()
        final={}
        for keys1 in dataset:
            subuser=[]
            subuser.append(dataset[keys1]["scores"])
            subuser.append(dataset[keys1]["username"])
            subfinal={}
            if dataset[keys1]["isFile"]==True:
                subfinal["isFile"]=True
            else:
                subfinal["isFile"]=False
            if dataset[keys1]["isRootflag"]==True or dataset[keys1]["isUserflag"]==True or dataset[keys1]["isFile"]==True:
                subfinal["time"]=dataset[keys1]["time"]
            final[dataset[keys1]["username"]]=subfinal
            users.append(subuser)
        for i in range(len(users)):
            for j in range(i+1,len(users)):
                if(users[i][0]==users[j][0] and users[i][0]==0):
                    continue
                if(users[i][0]==users[j][0] and (users[i][0]==20 or users[i][0]==30 or users[i][0]==50)):
                    if(final[users[i][1]]["isFile"]==False and final[users[j][1]]["isFile"]==True and users[i][0]==50):
                        temp=users[i]
                        users[i]=users[j]
                        users[j]=temp
                    elif(datetime.strptime(final[users[i][1]]["time"],"%Y-%m-%d %H:%M:%S.%f")>datetime.strptime(final[users[j][1]]["time"],"%Y-%m-%d %H:%M:%S.%f")):
                        temp=users[i]
                        users[i]=users[j]
                        users[j]=temp
                if(users[i][0]<users[j][0]):
                    temp=users[i]
                    users[i]=users[j]
                    users[j]=temp
        print(users)
        return render_template('/ctf_templates/leaderboard_testing.html', vals=users) 
    else:
        return redirect(url_for('home_page'))
'''
@app.route('/ctf/login', methods=["GET", "POST"])
def login():
    flags={"verify":1,"credentials":0}
    form = loginf()
    if "loggedout" in flags:
        del flags["loggedout"]
    if "logged" and "email" and "uname" in session:
        flags["loggedout"]=True
        del session["logged"]
        del session["email"]
        del session["uname"]
        del session["isUserflag"]
        del session["isRootflag"]
        del session["isFile"]
    try:
        if(session["registered"]==1):
            flags["registered"]=1
            del session["registered"]
    except:
        flags["registered"]=0
    if (request.method == 'POST'):
        email=request.form.get("email")
        password=request.form.get("password")
        try:
            user=auth.sign_in_with_email_and_password(email,password)
            if(auth.get_account_info(user["idToken"])["users"][0]["emailVerified"]==True):
                dataset=ctf_ref.get()
                for keys in dataset:
                    if(dataset[keys]["emailid"]==email):
                        session["logged"]=True
                        session["email"]=email
                        session["uname"]=dataset[keys]["username"]
                        session["isUserflag"]=dataset[keys]["isUserflag"]
                        session["isRootflag"]=dataset[keys]["isRootflag"]
                        session["isFile"]=dataset[keys]["isFile"]
                        break
                return redirect(url_for('timer'))
            else:
                auth.current_user = None
                flags["verify"]=0
        except:
            flags["credentials"]=1
            return render_template('/ctf_templates/login.html', form=form, flag=flags)
    return render_template('/ctf_templates/login.html', form=form, flag=flags)

'''
@app.route('/ctf/challenge/testing', methods=["GET", "POST"])
def challenge():
    userans="USER FLAG"
    rootans="ROOT FLAG"
    forms=challengeform()
    flags={}
    if "uname" in session:
        if(request.method=="POST"):
            userflag=request.form.get("user")
            rootflag=request.form.get("root")
            upload = request.form.get("file")
            vals=ctf_ref.get()
            if(userflag==userans and session["isUserflag"]==False):
                for keys,values in vals.items():
                    if(values["username"]==session["uname"]):
                        temptime=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        ctf_ref.child(keys).update({"isUserflag":True,
                        "time":temptime,
                        "usertime":temptime})
                        dic={"scores":values["scores"]+20}
                        ctf_ref.child(keys).update(dic)
                        flags["userflag"]=True
                        newvalues=ctf_ref.get()
                        session["isUserflag"]=newvalues[keys]["isUserflag"]
                        session["isRootflag"]=newvalues[keys]["isRootflag"]
                        session["isFile"]=newvalues[keys]["isFile"]
                if "userflag" not in flags:
                    flags["userflag"]=False
            elif(userflag!="" and session["isUserflag"]==False):
                flags["userflag"]=False
            vals=ctf_ref.get()
            if(rootflag==rootans and session["isRootflag"]==False):
                for keys,values in vals.items():
                    if(keys=="file" or keys=="user" or keys=="root"):
                        continue
                    if(values["username"]==session["uname"]):
                        temptime=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                        ctf_ref.child(keys).update({"isRootflag":True,
                        "time":temptime,
                        "roottime":temptime})
                        flags["rootflag"]=True
                        dic={"scores":values["scores"]+30}
                        ctf_ref.child(keys).update(dic)
                        newvalues=ctf_ref.get()
                        session["isUserflag"]=newvalues[keys]["isUserflag"]
                        session["isRootflag"]=newvalues[keys]["isRootflag"]
                        session["isFile"]=newvalues[keys]["isFile"]
                if "rootflag" not in flags:
                    flags["rootflag"]=False
            elif(rootflag!="" and session["isRootflag"]==False):
                flags["rootflag"]=False
            vals=ctf_ref.get()
            try:
                for keys,values in vals.items():
                    if(keys=="file" or keys=="user" or keys=="root"):
                        continue
                    if(values["username"]==session["uname"]):
                        if forms.validate_on_submit():
                            file_upload = forms.file.data
                            file_name = secure_filename(file_upload.filename)
                            storage.child('TOVC').child(file_name).put(file_upload)
                            temptime=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                            ctf_ref.child(keys).update({"isFile":True,
                            "time":temptime,
                            "filetime":temptime})
                            flags["fileflag"]=True
                            newvalues=ctf_ref.get()
                            session["isUserflag"]=newvalues[keys]["isUserflag"]
                            session["isRootflag"]=newvalues[keys]["isRootflag"]
                            session["isFile"]=newvalues[keys]["isFile"]
            except Exception as e:
                print(e)

        return render_template('/ctf_templates/challenge.html',form=forms,flag=flags,session=session)
    else:
        return redirect(url_for('home_page')) 

'''
@app.route('/ctf/timer')
def timer():
    if "uname" in session:
        return render_template('/ctf_templates/timer.html') 
    else:
        return redirect(url_for('home_page'))   

@app.route('/ctf/reset_password', methods=["GET", "POST"])
def reset():
    form=password()
    data={"success":0,"wrongemail":0}
    if(request.method=='POST'):
        mail=request.form.get("email")
        try:
            auth.send_password_reset_email(mail)
            data["success"]=1
            return render_template('/ctf_templates/reset_password.html', value=data, form=form)
        except:
            data["wrongemail"]=1
            return render_template('/ctf_templates/reset_password.html', value=data, form=form)
    return render_template('/ctf_templates/reset_password.html', form=form, value=data)

@app.route('/ctf/email_verified')
def email_verified():
    return render_template('/ctf_templates/verified_email.html')

@app.route('/ctf/new_password')
def new_password():
    return render_template('/ctf_templates/new_password.html')


@app.route('/ctf/reset', methods=["GET","POST"])
def reset_password():
    return render_template('/ctf_templates/new_password.html')   
@app.route('/ctf/rules')
def rules():
    if "uname" in session:
        return render_template('/ctf_templates/rules.html') 
    else:
        return redirect(url_for('home_page'))   

@app.route('/ctf/not_started')
def challenge_not_started():
    if "uname" in session:
        return render_template('/ctf_templates/challenge_not_started.html')
    else:
        return redirect(url_for('home_page'))

if __name__ == '__main__':
    app.run()
