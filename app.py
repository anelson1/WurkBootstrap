from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_mail import Mail, Message
import psycopg2
import config as cfg
import random
import string
import json
import os
from waitress import serve
conn = psycopg2.connect(user=cfg.info["user"], password=cfg.info["passwd"],
                        host=cfg.info["host"], port="5432", database=cfg.info["db"])
cursor = conn.cursor()

app = Flask(__name__)
app.secret_key = cfg.info["SECRET"]

app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=cfg.MAIL_USERNAME,
    MAIL_PASSWORD=cfg.MAIL_PASSWORD
)
mail = Mail(app)


def getInfo(username):
    select = "SELECT * from users where username = '" + str(username) + "'"
    cursor.execute(select)
    records = cursor.fetchall()
    return records


def getService(tos):
    select = "SELECT description from services where name = '" + str(tos) + "'"
    cursor.execute(select)
    records = cursor.fetchall()
    return records


def sendemail(name):
    select = "SELECT * from clients where name = '" + str(name) + "'"
    cursor.execute(select)
    clientData = cursor.fetchall()
    select = "SELECT * from bookings natural join bookingtimes where stuname = '" + \
        str(name) + "'"
    cursor.execute(select)
    bookingData = cursor.fetchall()
    select = "SELECT * from address where name = '" + \
        str(name) + "'"
    cursor.execute(select)
    addressData = cursor.fetchall()
    msg = Message("Your booking has been made!",
                  sender=cfg.MAIL_USERNAME, recipients=[clientData[0][1]], bcc=["wurkservices@gmail.com"])
    msg.body = "a new booking has been made"
    msg.html = render_template('emailtemplate.html', name=clientData[0][0], service=bookingData[0]
                               [3], month=bookingData[0][5], day=bookingData[0][6], time=bookingData[0][7], email=clientData[0][1], pnum=clientData[0][2], address=addressData[0][0] + " " +
                               addressData[0][1] + " " + addressData[0][2] + " " +
                               addressData[0][3], comment=bookingData[0][4])
    mail.send(msg)


@app.route("/")
def index():
    return render_template("index.html", pagetitle="Wurk Services")


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = request.args.get('uErr')
    return render_template("login.html", uErr=error, pagetitle="Login")


@app.route("/register")
def register():
    return render_template("register.html", fn=True)


@app.route("/register2", methods=['POST', 'GET'])
def register2():
    error = request.args.get('err')
    if request.method == 'POST':
        session['fname'] = request.form['fname']
        session['lname'] = request.form['lname']
    return render_template("register2.html", err=error)


@app.route("/register3", methods=['post'])
def register3():
    session['uname'] = request.form['uname']
    session['pword'] = request.form['pword']
    account = getInfo(session['uname'])
    if not account:
        return render_template("register3.html")
    else:
        return redirect(url_for('register2', err=True))


@app.route("/registerComplete", methods=['post'])
def registerC():
    fname = session['fname']
    lname = session['lname']
    username = session['uname'].lower()
    password = session['pword']
    email = request.form['email']
    phonenumber = request.form['pnum']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    insert = "INSERT INTO users VALUES ('"+str(username)+"','"+str(password)+"','"+str(email)+"','"+str(
        phonenumber)+"','"+str(address)+"','"+str(city)+"','"+str(state) + "','"+str(fname)+"','"+str(lname)+"')"
    cursor.execute(insert)
    conn.commit()
    insert = "INSERT INTO address VALUES ('"+str(address)+"','"+str(
        city)+"','"+str(state) + "','" + " " + "','" + str(fname + " " + lname) + "')"
    cursor.execute(insert)
    conn.commit()
    return redirect(url_for("registered"))


@app.route("/registered")
def registered():
    return render_template('registered.html')


@app.route("/useraccount", methods=['post'])
def useraccount():
    username = request.form['uname'].lower()
    password = request.form['pwd']
    selecting = "SELECT * FROM users WHERE username = " + "'" + \
        str(username)+"' AND password = '"+str(password)+"'"
    cursor.execute(selecting)
    records = cursor.fetchall()
    if username == 'admin' and len(records) != 0:
        selecting12 = "select DISTINCT * from bookings join bookingtimes on bookings.bid = bookingtimes.bid join clients on clients.name = bookings.stuname join address on address.name = clients.name"
        cursor.execute(selecting12)
        records12 = cursor.fetchall()
        return render_template('adminpage.html', records=records12, len=len(records12), len2=len(records12[0]))
    elif len(records) != 0:
        session['hasaccount'] = True
        session['name'] = getInfo(username)[0][7] + \
            " " + getInfo(username)[0][8]
        session['uname'] = username
        return render_template('useraccount.html', uname=records[0][0], fTime=True, pagetitle="My Account")
    else:
        return redirect(url_for('login', uErr=True))


@app.route("/admino", methods=['post'])
def admin():
    FN = request.form['FN']
    LN = request.form['LN']
    TOT = request.form['TOT']
    TID = ''.join([random.choice(string.ascii_letters + string.digits)
                   for n in range(6)])
    insert1 = "INSERT INTO teacher VALUES ('"+str(TID) + \
        "','"+str(FN)+"','"+str(LN)+"','"+str(TOT)+"')"
    cursor.execute(insert1)
    conn.commit()
    return render_template('adminpage.html')


@app.route("/CheckBooking", methods=['post'])
def checkbooking():
    selecting = "SELECT * FROM bookings natural join bookingtimes WHERE bid = " + \
        "'"+str(request.form['bid'])+"'"
    cursor.execute(selecting)
    records = cursor.fetchall()
    if len(records) != 0:
        meetingIDSQL = records[0][0]
        teacherSQL = records[0][2]
        monthSQL = records[0][5]
        daySQL = records[0][6]
        startSQL = records[0][7]
        endSQL = records[0][8]
        tob = records[0][3]
        if teacherSQL:
            return render_template('useraccount.html', ftime=False, isAcedemic=True, hasMeeting=True, meetingID=meetingIDSQL, teacher=teacherSQL, month=monthSQL, start=startSQL, end=endSQL, day=daySQL, TOB=tob)
        else:
            return render_template('useraccount.html', ftime=False, isAcedemic=False, hasMeeting=True, meetingID=meetingIDSQL, teacher=teacherSQL, month=monthSQL, start=startSQL, end=endSQL, day=daySQL, TOB=tob)
    else:
        return render_template('useraccount.html', ftime=False, hasMeeting=False)


@app.route("/services")
def services():
    return render_template('services.html', pagetitle='services')


@app.route("/services/<TOS>")
def TOS(TOS):
    filedirectory = 'css/img/'+TOS
    desc = getService(TOS)[0][0]
    if TOS == "Lawn Care":
        return render_template('lawncare.html', service=TOS, filedirectory=filedirectory, desc=desc, pagetitle=TOS)

    return render_template('LC.html', service=TOS, filedirectory=filedirectory, desc=desc, pagetitle=TOS)


@app.route("/services/<TOS>/StartBooking")
def TOSBook(TOS):
    session['TOB'] = TOS
    session['hasaccount'] = False
    return render_template('CBpre.html', pagetitle="Start a booking")


@app.route("/BookingSelector")
def BookingSelector():
    return render_template('bookingselect.html')


@app.route("/TOBselector", methods=['POST'])
def BookingSelector2():
    session['TOB'] = request.form['TOB']
    return render_template('CB2.html')


@app.route("/CreateBooking", methods=['post'])
def CB():
    if not session['hasaccount']:
        session['name'] = request.form['name']
        session['email'] = request.form['email']
        session['pnum'] = request.form['pnum']
    else:
        info = getInfo(session['uname'])
        session['email'] = info[0][2]
        session['pnum'] = info[0][3]
        session['TOB'] = request.form['TOB']
    insert1 = "INSERT INTO clients VALUES ('"+str(session['name']) + \
        "','"+str(session['email'])+"','"+str(session['pnum'])+"')"
    cursor.execute(insert1)
    conn.commit()
    if session['hasaccount']:
        return render_template('CB2.html', tob=session['TOB'])
    else:
        return render_template('CB.html')


@app.route("/AddressEntry", methods=['post'])
def CB2():
    session['addr'] = request.form['addr']
    session['city'] = request.form['city']
    session['state'] = request.form['state']
    session['zip'] = request.form['zip']
    insert = "INSERT INTO address VALUES ('"+str(session['addr'])+"','"+str(session['city'])+"','"+str(session['state'])+"','"+str(
        session['zip'])+"','"+str(session['name'])+"')"
    cursor.execute(insert)
    conn.commit()
    return render_template('CB2.html', tob=session['TOB'])


@app.route("/CreateBooking3", methods=['post'])
def CB3():
    session['month'] = request.form['month']
    session['day'] = request.form['day']
    typeofbooking = session['TOB']
    day = session['day']
    month = session['month']
    if typeofbooking == 'Acedemic Tutoring' or typeofbooking == 'Music Lessons' or typeofbooking == 'ACT and SAT Prep' or typeofbooking == 'Sports Coaching':
        teachSelect = " SELECT firstname,lastname from teacher join teacherbook on teacher.tid = teacherbook.tid WHERE day = '" + \
            str(day)+"' AND month = '" + str(month) + \
            "' AND typeofteacher = '" + str(typeofbooking)+"'"
        cursor.execute(teachSelect)
        teacherList = cursor.fetchall()
        if len(teacherList) == 0:
            return render_template('CB2.html', noTeacher=True)
        newTeacherList = list(dict.fromkeys(teacherList))
        return render_template('CB3.html', nameList=newTeacherList)
    else:
        return render_template('CB3-NAC.html')


@app.route("/CreateBooking4", methods=['post'])
def CB5():
    typeofbooking = session['TOB']
    month = session['month']
    day = session['day']
    session['teacher'] = request.form['teachers']
    teacher = session['teacher']
    timeSelect = " SELECT starttime,endtime from teacher join teacherbook on teacher.tid = teacherbook.tid WHERE firstname = '" + \
        str(teacher)+"'"
    cursor.execute(timeSelect)
    times = cursor.fetchall()
    teachSelect = " SELECT firstname,lastname from teacher join teacherbook on teacher.tid = teacherbook.tid WHERE day = '" + \
        str(day)+"' AND month = '" + str(month) + \
        "' AND typeofteacher = '" + str(typeofbooking)+"'"
    cursor.execute(teachSelect)
    teacherList = cursor.fetchall()
    newTeacherList = list(dict.fromkeys(teacherList))
    for i in range(len(times)):
        for j in range(len(times[i])):
            if(times[i][j] == '1'):
                tempList = list(times[i])
                tempList[j] = "1am"
                times[i] = tuple(tempList)
            if(times[i][j] == '2'):
                tempList = list(times[i])
                tempList[j] = "2am"
                times[i] = tuple(tempList)
            if(times[i][j] == '3'):
                tempList = list(times[i])
                tempList[j] = "3am"
                times[i] = tuple(tempList)
            if(times[i][j] == '4'):
                tempList = list(times[i])
                tempList[j] = "4am"
                times[i] = tuple(tempList)
            if(times[i][j] == '5'):
                tempList = list(times[i])
                tempList[j] = "5am"
                times[i] = tuple(tempList)
            if(times[i][j] == '6'):
                tempList = list(times[i])
                tempList[j] = "6am"
                times[i] = tuple(tempList)
            if(times[i][j] == '7'):
                tempList = list(times[i])
                tempList[j] = "7am"
                times[i] = tuple(tempList)
            if(times[i][j] == '8'):
                tempList = list(times[i])
                tempList[j] = "8am"
                times[i] = tuple(tempList)
            if(times[i][j] == '9'):
                tempList = list(times[i])
                tempList[j] = "9am"
                times[i] = tuple(tempList)
            if(times[i][j] == '10'):
                tempList = list(times[i])
                tempList[j] = "10am"
                times[i] = tuple(tempList)
            if(times[i][j] == '11'):
                tempList = list(times[i])
                tempList[j] = "11am"
                times[i] = tuple(tempList)
            if(times[i][j] == '12'):
                tempList = list(times[i])
                tempList[j] = "12am"
                times[i] = tuple(tempList)
            if(times[i][j] == '13'):
                tempList = list(times[i])
                tempList[j] = "1pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '14'):
                tempList = list(times[i])
                tempList[j] = "2pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '15'):
                tempList = list(times[i])
                tempList[j] = "3pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '16'):
                tempList = list(times[i])
                tempList[j] = "4pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '17'):
                tempList = list(times[i])
                tempList[j] = "5pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '18'):
                tempList = list(times[i])
                tempList[j] = "6pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '19'):
                tempList = list(times[i])
                tempList[j] = "7pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '20'):
                tempList = list(times[i])
                tempList[j] = "8pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '21'):
                tempList = list(times[i])
                tempList[j] = "9pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '22'):
                tempList = list(times[i])
                tempList[j] = "10pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '23'):
                tempList = list(times[i])
                tempList[j] = "11pm"
                times[i] = tuple(tempList)
            if(times[i][j] == '24'):
                tempList = list(times[i])
                tempList[j] = "12am"
                times[i] = tuple(tempList)
    return render_template('CB4.html', timesList=times, teacherName=teacher)


@app.route("/Created", methods=['post'])
def BC():
    name = session['name']
    month = session['month']
    day = session['day']
    typeofbooking = session['TOB']
    comments = request.form['comments']
    comments = comments.replace("'", "")
    BID = ''.join([random.choice(string.ascii_letters + string.digits)
                   for n in range(6)])
    if typeofbooking == 'Acedemic Tutoring' or typeofbooking == 'Music Lessons' or typeofbooking == 'ACT and SAT Prep' or typeofbooking == 'Sports Coaching':
        teacher = session['teacher']
        session['times'] = request.form['times']
        times = session['times']
        goodtimes = times.split()
        insert1 = "INSERT INTO bookings VALUES ('"+str(BID)+"','"+str(
            name)+"','"+str(teacher)+"','"+str(typeofbooking)+"')"
        cursor.execute(insert1)
        conn.commit()
        insert2 = "INSERT INTO bookingtimes VALUES ('"+str(BID)+"','"+str(
            month)+"','"+str(day)+"','"+str(goodtimes[0])+"','"+str(goodtimes[1])+"')"
        cursor.execute(insert2)
        conn.commit()
        fixedst = goodtimes[0].replace('am', '')
        fixedet = goodtimes[1].replace('am', '')
        fixedst = goodtimes[0].replace('pm', '')
        fixedet = goodtimes[1].replace('pm', '')

        remove = "DELETE FROM teacherbook where starttime = '" + \
            str(fixedst)+"' AND endtime = '"+str(fixedet)+"'"
        cursor.execute(remove)
        conn.commit()
        return render_template('BookingComplete.html', BID=BID)
    else:
        starttime = request.form['st']
        insert1 = "INSERT INTO bookings VALUES ('"+str(BID)+"','"+str(
            name)+"','"+''+"','"+str(typeofbooking)+"','" + str(comments)+"')"
        cursor.execute(insert1)
        conn.commit()
        insert2 = "INSERT INTO bookingtimes VALUES ('"+str(
            BID)+"','"+str(month)+"','"+str(day)+"','"+str(starttime)+"')"
        cursor.execute(insert2)
        conn.commit()
        sendemail(name)
        print("Someone Made A Booking")
        return render_template('BookingComplete.html', BID=BID)


@app.route("/ContactUs")
def CU():
    return render_template("contact.html")


@app.route("/MeetTheTeam")
def MTT():
    return render_template("MTT.html")


@app.route("/Lawncare")
def LC():
    return render_template("LC.html")


@app.route("/WurkerPage")
def WP():
    return render_template('SSTP.html')


@app.route("/wurkerHandler", methods=['post'])
def create():
    tid = request.form['tid']
    month = request.form['month']
    day = request.form['day']
    st = request.form['st']
    et = request.form['et']
    name = "SELECT * FROM teacher WHERE tid = '"+str(tid)+"'"
    cursor.execute(name)
    records = cursor.fetchall()
    timeelapsed = 0
    if(len(records) == 0):
        return render_template('SSTP.html', error=True)
    else:
        intst = int(st)
        intet = int(et)
        if intst > intet:
            while intst < 24:
                insert1 = "INSERT INTO teacherbook VALUES ('"+str(tid)+"','"+str(
                    month)+"','"+str(day)+"','"+str(intst)+"','"+str(intst+1)+"')"
                cursor.execute(insert1)
                intst += 1
                conn.commit()
            intst = 1
            for i in range(intet - 1):
                insert1 = "INSERT INTO teacherbook VALUES ('"+str(tid)+"','"+str(
                    month)+"','"+str(day)+"','"+str(intst)+"','"+str(intst+1)+"')"
                cursor.execute(insert1)
                intst += 1
                conn.commit()
        else:
            timeelapsed = intet - intst
            for i in range(timeelapsed):
                insert1 = "INSERT INTO teacherbook VALUES ('"+str(tid)+"','"+str(
                    month)+"','"+str(day)+"','"+str(intst)+"','"+str(intst+1)+"')"
                cursor.execute(insert1)
                intst += 1
                conn.commit()
        return render_template('SSTP.html', created=True)


@app.route('/sitemap.xml')
def site_map():
    return render_template('sitemap.xml')


@app.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="69")
    #serve(app, listen ='*:80')
