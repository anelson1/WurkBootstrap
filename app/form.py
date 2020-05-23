from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email
class dateEntry(FlaskForm):
    day = DateField('Date',
                    validators=[DataRequired()], format='% Y-%m-%d')
    submit = SubmitField("Submit")


class wurkerEntry(FlaskForm):
    WID = StringField('Wurker ID', validators=[DataRequired()])
    day = DateField('Date',
                    validators=[DataRequired()])
    time = TimeField('Time',
                    validators=[DataRequired()])
    JobType = StringField('Type Of Job', validators=[DataRequired()])
    clientName = StringField('Name of Client', validators=[DataRequired()])
    POTJ = StringField('People on the Job', validators=[DataRequired()])
    submit = SubmitField("Submit")

class loginform(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Sign In")
    register = SubmitField("Register")
    logout = SubmitField("Log Out")

class registerform(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    nextbutton = SubmitField("Next")
    confirmpassword = PasswordField('Confirm Password', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])


class bookingform(FlaskForm):
    services = SelectField("Service", choices=['Grocery Delivery','Acedemic Tutoring',"Landscaping","Music Lessons","ACT and SAT Prep","Sports Coaching","Junk Removal","Pet Care","House Sitting","Construction","Powerwashing","Painting/Staining","Deck and Roof Restoration"])
    day = DateField('Date',
                    validators=[DataRequired()])
    time = TimeField('Time',
                    validators=[DataRequired()])
    comments = StringField('Comments')

class UploadForm(FlaskForm):
    image = FileField('Image Upload', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    description = TextAreaField('Image Description')
    submit = SubmitField("Submit")
