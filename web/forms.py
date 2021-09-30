from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms import validators
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError, DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf import Form

class signup(FlaskForm):
    uname=StringField(label=('Username'),validators=[DataRequired()])
    email=EmailField(label=('Email id'),validators=[DataRequired()])
    password=PasswordField(label=('Password'),validators=[DataRequired()])
    submit=SubmitField('Submit')

class loginf(FlaskForm):
    email=EmailField(label=('Email id'),validators=[DataRequired()])
    password=PasswordField(label=('Password'),validators=[DataRequired()])
    submit = SubmitField('Submit')

class password(FlaskForm):
    email=EmailField('Email id')

class challengeform(FlaskForm):
    user=StringField(label=('What is the user flag?'))
    root=StringField(label=('What is the root flag?'))
    file=FileField(label=('Upload writeup'), validators=[FileAllowed(['doc', 'docx', 'pdf'])])
    submit=SubmitField('Submit')