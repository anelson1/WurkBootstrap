from flask import *
from app import myapp, db, mail
from app.form import *
from app.database import *
from flask_login import current_user, login_user, login_required, logout_user
from flask_mail import Message
from app.servicedesc import services as dictofservices
import random
from random import randint
import string
import json
import os
from werkzeug.utils import secure_filename
from datetime import datetime

def sendemail(bid):
    booking = Booking.query.filter_by(bookingid=bid).first()
    bookingtime = BookingTime.query.filter_by(bookingid=bid).first()
    client = Client.query.filter_by(bookingid=bid).first()

    msg = Message("Your booking has been made!",
                  sender='wurkservices@gmail.com', recipients=[client.email], bcc=["bookings@wurkservices.com"])
    msg.body = "a new booking has been made"
    msg.html = render_template('emailtemplate.html', name=client.name, service=booking.typeofbooking, month=bookingtime.month, day=bookingtime.day, time=bookingtime.starttime, email=client.email, pnum=client.phonenumber, address=client.address + " " +
                               client.city + " " + client.state, comment=booking.comments)
    mail.send(msg)
def sendclaimemail(wurker, bid):
    booking = Booking.query.filter_by(bookingid=bid).first()
    bookingtime = BookingTime.query.filter_by(bookingid=bid).first()
    client = Client.query.filter_by(bookingid=bid).first()

    msg = Message("Someone has claimed your booking",
                  sender='wurkservices@gmail.com', recipients=[client.email], bcc=["bookings@wurkservices.com"])
    msg.body = wurker + " has claimed your booking!"
    msg.html = render_template('emailtemplateclaim.html', wurker = wurker, name=client.name, service=booking.typeofbooking, month=bookingtime.month, day=bookingtime.day, time=bookingtime.starttime, email=client.email, pnum=client.phonenumber, address=client.address + " " +
                               client.city + " " + client.state, comment=booking.comments)
    mail.send(msg)


def returnMonth(day):
    if day == '01':
        return 'January'
    if day == '02':
        return 'Feburary'
    if day == '03':
        return 'March'
    if day == '04':
        return 'April'
    if day == '05':
        return 'May'
    if day == '06':
        return 'June'
    if day == '07':
        return 'July'
    if day == '08':
        return 'August'
    if day == '09':
        return 'September'
    if day == '10':
        return 'October'
    if day == '11':
        return 'November'
    if day == '12':
        return 'December'

def get_employees():
    return User.query.filter_by(isemployee = 1)
@myapp.route("/")
def index():
    olddic = dictofservices.serviceDict.keys()
    listofservices = []
    for i in olddic:
        if not ("Meta" in i or "landscaping" in i):
            listofservices.append(i)
    return render_template("index.html", pagetitle="Wurk Services", listofservices = listofservices, types = ["Property Management", "Home Improvement", "Personal Services"])

#User Account Stuff --------------------------------------------------------------------------------------------------------------------------------------------
@myapp.route("/login", methods=['GET', 'POST'])
def login():
    error = request.args.get('uErr')
    form = loginform()
    return render_template("login.html", uErr=error, pagetitle="Login", form = form)

@myapp.route("/loginhandler", methods=['POST'])
def loginhandler():
    username = request.form['username']
    password = request.form['password']
    try:
        remember = request.form['remember']
    except:
        remember = False
    u = User.query.filter_by(username=username).first()
    if not u:
        flash("Error")
        return redirect(url_for("login", uErr=True))
    if u.password == password:
        login_user(u, remember=remember)
        if u.username == 'admin':
                return redirect(url_for("admin"))
        if u.username == 'wurker':
                return redirect(url_for('wurker'))
        return redirect(url_for("useraccount", username = username))
    else:
        flash("Error")
        return redirect(url_for("login", uErr=True))

@myapp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
    
@myapp.route("/register")
def register():
    form = registerform()
    return render_template("register.html", form = form)

@myapp.route("/register1Handler", methods = ["POST"])
def register1Handler():
    session['fname'] = request.form['firstname']
    session['lname'] = request.form['lastname']
    return redirect(url_for("register2"))

@myapp.route("/register2", methods = ['GET'])
def register2():
    error = request.args.get('err')
    form = registerform()
    return render_template("register2.html", err=error, form=form)

@myapp.route("/register2Handler", methods = ["POST"])
def register2Handler():
    session['uname'] = request.form['username']
    session['pword'] = request.form['password']
    u = User.query.filter_by(username=session['uname']).first()
    if u:
        return redirect(url_for("register2",err = True)) 
    return redirect(url_for("register3"))

@myapp.route("/register3")
def register3():
    form = registerform()
    return render_template("register3.html", form=form)


@myapp.route("/register3Handler", methods=['POST'])
def register3Handler():
    fname = session['fname']
    lname = session['lname']
    username = session['uname'].lower()
    password = session['pword']
    email = request.form['email']
    phonenumber = request.form['phonenumber']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    id = randint(1000000,9999999)
    u = User(id = id, username=username, password=password, isemployee = 0, bio = '')
    db.session.add(u)
    pi = PersonalInfo(id = id, email=email, phonenumber=phonenumber, city=city, state=state, address=address, person = id,firstname = fname, lastname=lname)
    db.session.add(pi)
    db.session.commit()
    return redirect(url_for("registered"))


@myapp.route("/registered")
def registered():
    return render_template('registered.html')


@myapp.route("/useraccount", methods=['GET'])
@login_required
def useraccount():
    if current_user.username == 'wurker':
        return redirect(url_for('wurker'))
    if current_user.isemployee == 1:
        return redirect(url_for('WP'))
    if current_user.username == 'admin':
        return redirect(url_for('admin'))
    hasMeeting = request.args.get('hasMeeting')
    hasError = request.args.get('hasError')
    month = request.args.get('month')
    day = request.args.get('day')
    TOB = request.args.get('TOB')
    start = request.args.get('start')
    cu = current_user
    print(cu.id)
    u = User.query.filter_by(id=cu.id).all()
    info = PersonalInfo.query.filter_by(id=cu.id).first()
    print(info)
    form = loginform()
    try:
        name = info.firstname
    except:
        name = 'Unknown'
    return render_template('useraccount.html', hasError= hasError, month=month, day=day,TOB=TOB,start=start,hasMeeting = hasMeeting, uname=name, fTime=True,form=form, pagetitle="My Account")

@myapp.route("/EmployeeRegister")
def EmpReg():
    form = registerform()
    error = request.args.get('error')
    return render_template('employeeregister.html', form = form, error=error, secret = "WurkServices2020*")
@myapp.route("/empreghandler", methods=['POST'])
def EmpRegHandle():
    confcode = request.form['confirmationcode']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    phonenumber = request.form['phonenumber']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    id = randint(1000000,9999999)
    u = User(id = id, username=username, password=password, isemployee = 1, bio = '')
    db.session.add(u)
    pi = PersonalInfo(id = id, email=email, phonenumber=phonenumber, city=city, state=state, address=address, person = id,firstname = firstname, lastname=lastname)
    db.session.add(pi)
    db.session.commit()
    return redirect(url_for('registered'))
#End Account Stuff---------------------------------------------------------------------------------------------------------------------------------------------------------
#Wurk in progess 
@myapp.route("/adminhandler", methods=['post'])
def adminhandler():
    FN = request.form['FN']
    LN = request.form['LN']
    TOT = request.form['TOT']
    TID = ''.join([random.choice(string.ascii_letters + string.digits)
                   for n in range(7)])
    insert1 = "INSERT INTO teacher VALUES ('"+str(TID) + \
        "','"+str(FN)+"','"+str(LN)+"','"+str(TOT)+"')"
    cursor.execute(insert1)
    conn.commit()
    return render_template('adminpage.html')

#Booking Creation -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@myapp.route("/CheckBooking", methods=['post'])
def checkbooking():
    bid = request.form['bid']
    booking = Booking.query.filter_by(bookingid=bid).first()
    bookingtime = BookingTime.query.filter_by(bookingid=bid).first()
    client = Client.query.filter_by(bookingid=bid).first()
    if booking is not None:
        return redirect(url_for('useraccount', hasMeeting=True, meetingID=bid, month = bookingtime.month, day = bookingtime.day, start = bookingtime.starttime, TOB = booking.typeofbooking))
    else:
        return redirect(url_for('useraccount', hasError=True))

@myapp.route("/services")
def services():
    return render_template('services.html', pagetitle='services')

@myapp.route("/services/<service>")
def servicesgeneric(service):
    return redirect(url_for("TOS",TOS=service))

@myapp.route("/services/<TOS>" + "-services-il")
def TOS(TOS):
    TOS = TOS.replace('-', ' ')
    TOS = TOS.title()
    desc = dictofservices()
    print(desc)
    try:
        meta = desc.serviceDict[TOS + " Meta"]
    except KeyError as e:
        meta = ''
    filedirectory = 'css/img/'+TOS
    if TOS == "Lawn Care":
        return redirect(url_for("Archal"))
    if TOS == 'Junk Removal Services':
        return render_template('LC.html', baa=True, service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle=TOS, meta=meta)
    return render_template('LC.html', service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle=TOS, meta=meta)

@myapp.route("/services/<TOS>" + "-barrington-il")
def TOSBarrington(TOS):
    TOS = TOS.replace('-', ' ')
    TOS = TOS.title()
    desc = dictofservices()
    print(TOS + " Meta")
    try:
        meta = desc.serviceDict[TOS + " Meta"]
    except KeyError as e:
        meta = ''
    print(meta)
    filedirectory = 'css/img/'+TOS
    if TOS == "Lawn Care":
        return redirect(url_for("Archal"))
    if TOS == 'Junk Removal Services':
        return render_template('LC.html', baa=True, service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle=TOS, meta=meta)
    return render_template('LC.html', service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle=TOS, meta=meta)

@myapp.route("/landscaping/<area>" + "-landscaping-services-il")
def Archal(area):
    area = area.replace("-", " ")
    TOS = area + " landscaping"
    print(TOS)
    desc = dictofservices()
    try:
        meta = desc.serviceDict[TOS + " Meta"]
    except KeyError as e:
        meta = ''
    filedirectory = 'css/img/Lawn Care'
    return render_template('lawncare.html', service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle=area + " Landscaping Services | Lawn Care Services |" + area + ", Il | Wurk " + area + " Services")
    
@myapp.route("/<area>" + "-landscaping-services-il")
def anytypeoflandscaping(area):
    return redirect(url_for('Archal', area = area.capitalize()))

@myapp.route("/landscaping-services-" + "<area>" + "-il"  )
def anytypeoflandscapingreverse(area):
    return redirect(url_for('Archal', area = area.capitalize()))
@myapp.route("/landscaping")
def sansscaping():
    return render_template('landscaping.html')
@myapp.route("/nanny-services-barrington-il")
def nannystuff():
    TOS = 'Nanny Services'
    desc = dictofservices()
    print(desc)
    try:
        meta = desc.serviceDict[TOS + " Meta"]
    except KeyError as e:
        meta = ''
    filedirectory = 'css/img/'+TOS
    return render_template('LC.html', service=TOS, filedirectory=filedirectory, desc=desc.serviceDict[TOS], pagetitle="Nanny Services Barrington Il | Compassionate, and Caring Nannies in Barrington Il Services")
   
@myapp.route("/services/<TOS>/SelectSport")
def SportSelect(TOS):
    form = bookingform()
    return render_template('sportpicker.html', pagetitle="Pick Your Sport", form=form)

@myapp.route("/services/<TOS>/StartBooking", methods = ['POST',"GET"])
def TOSBook(TOS):
    if request.method == "POST":
        session['TOB'] = request.form['sportsoffered'] + " Coaching"
    else:
        session['TOB'] = TOS
    if not current_user.is_anonymous:
        return redirect(url_for("CreateBookingTimeAndDate"))
    form = registerform()
    return render_template('CBpre.html', pagetitle="Start a booking", form=form)


@myapp.route("/BookingSelector")
def BookingSelector():
    form = bookingform()
    return render_template('bookingselect.html', form=form)


@myapp.route("/TOBselector", methods=['POST'])
def BookingSelector2():
    session['TOB'] = request.form['services']
    return redirect(url_for('CreateBookingTimeAndDate'))

@myapp.route("/bookinghandler", methods=['POST'])
def bookinghandler():
    session['name'] = request.form['firstname'] + " " + request.form['lastname']
    session['email'] = request.form['email']
    session['pnum'] = request.form['phonenumber']
    session['address'] = request.form['address']
    session['city'] = request.form['city']
    session['state'] = request.form['state']
    return redirect(url_for('CreateBookingTimeAndDate'))

@myapp.route("/CreateBookingFinal" ,methods=['GET'])
def CreateBookingTimeAndDate():
    form = bookingform()
    BID = ''.join([random.choice(string.ascii_letters + string.digits)
                   for n in range(6)])
    session['bid'] = BID
    error = request.args.get('error')
    return render_template("bookingtimeanddate.html", form = form, currentbooking = session['TOB'], error = error)

@myapp.route("/FinalizeBooking", methods=['POST'])
def FinalizeBooking():
    date = request.form['day']
    time = request.form['time']
    month = returnMonth(date[5:7])
    day = str(int(date[8:10]))
    check = BookedDays.query.filter_by(day=day).first()
    if check:
        return redirect(url_for("CreateBookingTimeAndDate",error = True))
    if not current_user.is_anonymous:
        cu = current_user
        u = User.query.filter_by(id=cu.id).all()
        info = PersonalInfo.query.filter_by(id=cu.id).first()
        name = info.firstname + " " + info.lastname
        session['email'] = info.email
        session['pnum'] = info.phonenumber
        session['address'] = info.address
        session['city'] = info.city
        session['state'] = info.state
    else:
        name = session['name']
    booking = Booking(bookingid=session['bid'], clientname=name, typeofbooking=session['TOB'], comments=request.form['comments'], isclaimed = False, claimedby = None)
    bookingtime = BookingTime(bookingid=session['bid'], month=month, day=day, starttime=request.form['time'])
    client = Client(name = name, email = session['email'], phonenumber = session['pnum'], address = session['address'], city = session['city'], state = session['state'], bookingid = session['bid'])
    
    db.session.add(booking)
    db.session.add(bookingtime)
    db.session.add(client)
    db.session.commit()
    sendemail(session['bid'])
    return redirect(url_for('created'))

@myapp.route("/BookingCreated")
def created():
    return render_template("BookingComplete.html", BID=session['bid'])
    
#End Of Booking Creation -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Stuff for the wurker--------------------------------------------------------------------------------------------------
@myapp.route("/WurkerPage", methods=['GET'])
@login_required
def WP():
    if current_user.isemployee == 0:
        return redirect(url_for('useraccount'))
    popupremove = request.args.get('popupremove')
    error = request.args.get('error')
    u = BookedDays.query.all()
    day = request.args.get('day')
    month = request.args.get('month')
    popup = request.args.get('popup')
    err = request.args.get('err')
    name = request.args.get('name')
    JCI = request.args.get('justclockedin')
    JCO = request.args.get('justclockedout')
    form = wurkerEntry()
    try:
        time = TimeSheet.query.get(current_user.currenttimesheet).timein
    except:
        time = None
    return render_template('wurker.html', time = time, justclockedin = JCI, justclockedout = JCO, clockedin = current_user.currenttimesheet, user = current_user, nameofemployee = PersonalInfo.query.filter_by(id= current_user.id).first().firstname, lst = u, popupremove = popupremove, form=form, day=day, month=month, err=err, popup=popup, name=name)

@myapp.route("/deletebookedday/<id>")
@login_required
def deleteslot(id):
    b = BookedDays.query.get(id)
    error=False
    try:
        db.session.delete(b)
        db.session.commit()
    except:
        error = True
    return redirect(url_for('WP', popupremove=True, error=error))
    

@myapp.route("/wurkerhandler", methods=['post'])
@login_required
def addSceudel():
    w= PersonalInfo.query.filter_by(id=current_user.id).first()
    date = request.form['day']
    time = request.form['time']
    CN = request.form['clientName']
    TOJ = request.form['JobType']
    POTJ = request.form['POTJ']
    print(date)
    month = returnMonth(date[5:7])
    day = int(date[8:10])
    bd = BookedDays(name=w.firstname, day = day, month = month, wid = current_user.username, jobtype = TOJ, peopleonjob = POTJ, clientname = CN, time = time)
    db.session.add(bd)
    db.session.commit()
    print(w.firstname + "has updated their avaliblity")
    return redirect(url_for('WP', day=day, month=month, popup=True, name=w.firstname))
@myapp.route("/clockin", methods = ['POST'])
@login_required
def clockin():
    currentTime = datetime.now()
    dt_string = currentTime.strftime("%d/%m/%Y %H:%M:%S")
    TOJ = request.form['JobType']
    TS = TimeSheet(timein=dt_string, wurker=current_user.id, jobtype = TOJ)
    db.session.add(TS)
    db.session.commit()
    u = User.query.get(current_user.id)
    u.currenttimesheet = TS.id
    db.session.commit()
    return redirect(url_for("WP", justclockedin=True))
@myapp.route("/clockout")
@login_required
def clockout():
    currentTime = datetime.now()
    dt_string = currentTime.strftime("%d/%m/%Y %H:%M:%S")
    TS = TimeSheet.query.get(current_user.currenttimesheet)
    TS.timeout = dt_string
    u = User.query.get(current_user.id)
    u.currenttimesheet = None
    db.session.commit()
    return redirect(url_for("WP", justclockedout = True))
@myapp.route('/<wurker>/profile', methods = ['GET', 'POST'])
def wurkerprofile(wurker):
    form = UploadForm()
    try:
        u = User.query.filter_by(username=wurker).first()
        p = PersonalInfo.query.filter_by(id=u.id).first()
        files = Post.query.filter_by(poster = u.id)
        if not current_user.is_anonymous and current_user.isemployee == 1 and current_user.username == wurker:
            myaccount = True
        else:
            myaccount = False
        #filelst = os.listdir('app/static/css/img/' + wurker)
        #print(filelst)
        return render_template('employeefeed.html', lst = files,username = u.username, form= form, name=p.firstname, bio=u.bio, myaccount = myaccount, title = p.firstname)
    except Exception as e:
        print(e)
        return redirect(url_for('genericerror'))

@myapp.route('/<wurker>/posthandler', methods=['POST'])
def posthandler(wurker):
    try:
        os.makedirs('app/static/css/img/' + wurker)
    except:
        print('Already exists')
    if request.method == 'POST':
        try:
            file = request.files['image']
            filename = secure_filename(file.filename)
            
            file.save(os.path.join('app/static/css/img/' + wurker, filename))
        except:
            filename = ''
        p = Post(pic=filename, desc=request.form['description'], title = request.form['title'], poster=current_user.id)
        db.session.add(p)
        db.session.commit()
    return redirect(url_for('wurkerprofile', wurker=wurker))

@myapp.route('/<wurker>/edit', methods = ['POST'])
def uploadphoto(wurker):
    newbio = request.form['bio']
    u = User.query.filter_by(username=wurker).first()
    u.bio = newbio
    db.session.commit()
    return redirect(url_for('wurkerprofile', wurker=wurker))
    
@myapp.route('/<wurker>/delete/<file>', methods = ['POST', 'Get'])
def deletephoto(wurker, file):
    pic = Post.query.filter_by(id=file).first()
    db.session.delete(pic)
    db.session.commit()
    return redirect(url_for('wurkerprofile', wurker=wurker))

@myapp.route('/<wurker>/bookingslist')
@login_required
def booklist(wurker):
    popup = request.args.get('popup')
    booking = Booking.query.all()
    bookingtime = BookingTime.query.all()
    client = Client.query.all()
    u = db.session.query(Booking,BookingTime,Client).filter(Booking.bookingid == BookingTime.bookingid).filter(BookingTime.bookingid == Client.bookingid).all() 
    popup = request.args.get('popup')
    return render_template('bookingslist.html', lst=u, popup=popup)

@myapp.route('/<wurker>/bookingslist/claim/<idofbooking>', methods = ['POST'])
def booklistclaimhandler(wurker, idofbooking):
    booking = Booking.query.filter_by(bookingid = idofbooking).first()
    booking.isclaimed = True
    booking.claimedby = wurker
    db.session.commit()
    sendclaimemail(wurker, idofbooking)
    return redirect(url_for('booklist', wurker=wurker, popup = True))
#End stuff for the wurker-------------------------------------------------------------------------------------------

#Start Stuff For Admin----------------------------------------------------------------------------------------------
@myapp.route("/deletebooking/<bookingid>")
def deletebooking(bookingid):
    booking = Booking.query.filter_by(bookingid=bookingid).first()
    bookingtime = BookingTime.query.filter_by(bookingid=bookingid).first()
    client = Client.query.filter_by(bookingid=bookingid).first()
    print(booking, bookingtime, client)
    db.session.delete(booking)
    db.session.delete(bookingtime)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for("admin", popup=True))

@myapp.route("/admin", methods=['GET'])
@login_required
def admin():
    if current_user.username != 'admin':
        return redirect(url_for("useraccount"))
    booking = Booking.query.all()
    bookingtime = BookingTime.query.all()
    client = Client.query.all()
    u = db.session.query(Booking,BookingTime,Client).filter(Booking.bookingid == BookingTime.bookingid).filter(BookingTime.bookingid == Client.bookingid).all() 
    popup = request.args.get('popup')
    return render_template('adminpage.html', lst=u, popup=popup)
@myapp.route("/admin/timesheet", methods=['GET'])
@login_required
def timesheet():
    if current_user.username != 'admin':
        return redirect(url_for("useraccount"))
    lst = TimeSheet.query.all()
    popup = request.args.get('popup')
    return render_template('timesheet.html', lst=lst, personalinfo = PersonalInfo, popup = popup)
#End Stuff For Admin----------------------------------------------------------------------------------------------------------------------------------------

#Static Pages -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@myapp.route("/ContactUs")
def CU():
    return render_template("contact.html")


@myapp.route("/MeetTheTeam")
def MTT():
    return render_template("MTT.html")

@myapp.route('/sitemap.xml')
def site_map():
    sitemap_template = render_template('sitemap.xml')
    response = make_response(sitemap_template)
    response.headers["Content-Type"] = "application/xml"
    return response


@myapp.route('/robots.txt')
def robots():
    return send_from_directory('static', 'robots.txt')
#End Of Static Pages -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#Error Handlers
@myapp.route('/error')
def genericerror():
    return render_template('application-error.html', errormessage ='That page could not be found, please go home and try again!')
    
@myapp.errorhandler(404)
def page_not_found(e):
    return render_template('application-error.html', error = e, errormessage = "That page could not be found, please go home and try again!"), 404

@myapp.errorhandler(500)
def interror(e):
    return render_template('application-error.html', error=e, errormessage = 'Our database is currently undergoing maintance, please try again later!'), 500
