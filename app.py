from flask import Flask, render_template, request
import psycopg2
import config as cfg
conn = psycopg2.connect(user =cfg.info["user"],password = cfg.info["passwd"],host = cfg.info["host"],port = "5432",database = cfg.info["db"])
cursor = conn.cursor()

app= Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/login")
def login():
    return render_template("login.html")
@app.route("/register")
def register():
    return render_template("register.html", fn=True)
@app.route("/register2", methods=['post'])
def register2():
    fname = request.form['fname']
    lname = request.form['lname']
    print(fname)
    return render_template("register2.html",fname = fname, lname = lname)
@app.route("/register3", methods=['post'])
def register3():
    fname = request.form['fname']
    lname = request.form['lname']
    uname = request.form['uname']
    pword = request.form['pword']
    return render_template("register3.html", fname = fname, lname = lname, uname = uname, pword = pword)
@app.route("/registerComplete", methods=['post'])
def registerC():
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['uname'].lower()
    password = request.form['pass']
    email = request.form['email']
    phonenumber = request.form['pnum']
    address = request.form['address']
    city = request.form['city']
    state = request.form['state']
    insert = "INSERT INTO users VALUES ('"+str(username)+"','"+str(password)+"','"+str(email)+"','"+str(phonenumber)+"','"+str(address)+"','"+str(city)+"','"+str(state)+ "','"+str(fname)+"','"+str(lname)+"')"
    cursor.execute(insert)
    conn.commit()
    return render_template('registered.html')
@app.route("/useraccount", methods=['post'])
def useraccount():
    username = request.form['uname'].lower()
    password = request.form['pwd']
    selecting = "SELECT * FROM users WHERE username = " + "'"+str(username)+"' AND password = '"+str(password)+"'"
    cursor.execute(selecting)
    records = cursor.fetchall()
    if username == 'admin' and len(records) != 0:
        selecting12 = "select * from bookings natural join bookingtimes"
        cursor.execute(selecting12)
        records12 = cursor.fetchall()
        return render_template('adminpage.html', uname = records[0][7], records = records12, len = len(records12), len2 = len(records12[0]))
    elif len(records) != 0:
        return render_template('useraccount.html', uname = records[0][7])
    else:
        return render_template('login.html', uErr = True)


if __name__ == "__main__":
    app.run(debug=True, host = "0.0.0.0" ,port="69")
