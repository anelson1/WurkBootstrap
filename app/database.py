from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique = True)
    password = db.Column(db.String(128))
    isemployee = db.Column(db.Integer)
    bio = db.Column(db.String(500))
    personalinfos = db.relationship('PersonalInfo',backref='user',lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.id)

class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64))
    phonenumber = db.Column(db.String(128))
    address = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    person = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Users Info {}>'.format(self.id)  

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(128))
    teachername = db.Column(db.String(128))
    typeofbooking = db.Column(db.String(128))
    comments = db.Column(db.String(1000))
    bookingid = db.Column(db.String(6),unique = True)
    bookingtime = db.relationship('BookingTime')


    def __repr__(self):
        return '<Booking {}>'.format(self.bookingid)  

class BookingTime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String(20))
    day = db.Column(db.String(10))
    starttime = db.Column(db.String(10))
    bookingid = db.Column(db.String(6), db.ForeignKey('booking.bookingid'))
    def __repr__(self):
        return '<Booking Times {}>'.format(self.bookingid)
        
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    phonenumber = db.Column(db.String(50))
    address = db.Column(db.String(128))
    city = db.Column(db.String(128))
    state = db.Column(db.String(128))
    bookingid = db.Column(db.String(6),unique = True)

    def __repr__(self):
        return '<Client {}>'.format(self.bookingid)

class BookedDays(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.String(20))
    month = db.Column(db.String(15))
    wid = db.Column(db.String(10))
    jobtype = db.Column(db.String(30))
    peopleonjob = db.Column(db.String(200))
    time = db.Column(db.String(10))
    clientname = db.Column(db.String(30))
    name = db.Column(db.String(40))
    
    def __repr__(self):
        return '<booked day {}>'.format(self.wid)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(128))
    desc = db.Column(db.String(500))
    poster = db.Column(db.Integer)
    def __repr__(self):
        return '<Post {}>'.format(self.id)
