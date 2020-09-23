from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField,SelectMultipleField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Email, AnyOf
from app.servicedesc import services as dictofservices

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
    confirmationcode = StringField('Confirmation Code', validators=[DataRequired()])
    submit = SubmitField("Register")



class bookingform(FlaskForm):
    services = SelectField("Service", choices=['Grocery Delivery','Acedemic Tutoring',"Landscaping","Music Lessons","ACT and SAT Prep","Sports Coaching","Junk Removal","Pet Care","House Sitting","Construction","Powerwashing","Painting/Staining","Deck and Roof Restoration"])
    day = DateField('Date',
                    validators=[DataRequired()])
    time = TimeField('Time',
                    validators=[DataRequired()])
    comments = StringField('Comments')
    sportsoffered = SelectField("Sport", choices=['Soccer','Lacrosse',"Football","Golf","Tennis","Basketball","Wrestling"])
    nextbutton = SubmitField("Book")


class UploadForm(FlaskForm):
    bio = TextAreaField('Edit Bio')
    image = FileField('Image Upload', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    title = TextAreaField('Post Title (Optional)')
    description = TextAreaField('Post Description')
    submit = SubmitField("Submit")

class applicantform(FlaskForm):
    def tuple_gen():
        olddic = dictofservices.prop_dict.keys()
        tuplelist = []
        for i in olddic:
            if not ("Meta" in i or "landscaping" in i or "break" in i):
                tuplelist.append((i,i))
        return tuplelist
    fullname = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phonenumber = StringField('Phone Number', validators=[DataRequired()])
    jobs = SelectMultipleField("Jobs you are applying for", choices=tuple_gen())
    submit = SubmitField("Submit Application")
