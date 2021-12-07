import re

from flask import Flask, send_from_directory, render_template, request, flash, redirect, url_for, flash, Response, \
    session, jsonify
from flask_mysqldb import MySQL, MySQLdb
import bcrypt

app = Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_password'] = ""
app.config['MYSQL_DB'] = "school"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"
mysql = MySQL(app)


@app.route('/', methods=["POST", "GET"])
def homepage():
    return render_template('homepage.html')


@app.route('/admin_register', methods=["POST", "GET"])
def admin_register():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM administrationStaff WHERE username = % s', (username,))
        user = cur.fetchone()
        if user:
            msg = 'Account already exists !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:
            cur.execute('INSERT INTO administrationStaff VALUES (NULL, % s, % s)', (username, hash_password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    else:
        msg = 'Please fill out the form !'

        # return redirect(url_for('homepage'))
    return render_template('adminRegister.html', msg=msg)


@app.route('/accounts_register', methods=["POST", "GET"])
def accounts_register():
    msg = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM accountsstaff WHERE username = % s', (username,))
        user = cur.fetchone()
        if user:
            msg = 'Account already exists !'
        elif not username or not password:
            msg = 'Please fill out the form !'
        else:
            cur.execute('INSERT INTO accountstaff VALUES (NULL, % s, % s)', (username, hash_password,))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
        return redirect(url_for('homepage'))
    return render_template('accountsRegister.html', msg=msg)


@app.route('/staff_register', methods=["POST", "GET"])
def staff_register():
    read = ""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM staffregistry WHERE username = % s', (username,))
        user = cur.fetchone()
        if user:
            read = 'Account already exists !'
        elif not username or not password:
            read = 'Please fill out the form !'
        else:
            cur.execute('INSERT INTO staffregistry VALUES (NULL, % s, % s)', (username, hash_password,))
            mysql.connection.commit()
            read = 'You have successfully registered !'
    elif request.method == 'POST':
        read = 'Please fill out the form !'
        return redirect(url_for('homepage'))
    return render_template('staffRegister.html', read=read)


@app.route('/admin_login_page', methods=["POST", "GET"])
def admin_login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM administrationstaff WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()

        if not user:
            read = "Error password or user not matched"
            return render_template("adminLogin.html", read=read)
        if user:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['username'] = user['username']
                return redirect(url_for("admin_dashboard"))
            else:
                read = "Error password or user not matched"
                return render_template('homepage.html', read=read)

    return render_template("adminLogin.html")


@app.route('/staff_login_page', methods=["POST", "GET"])
def staff_login_page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM staffregistry WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        read = "Error password or user not matched"
        if not user:
            return render_template("staffLogin.html", read=read)

        if user:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['username'] = user['username']
                session['password'] = user['password']
                return redirect(url_for("staff_dashboard"))

            else:
                error = "Error password or user not matched"
                return render_template('staffLogin.html', read=read)

    return render_template("staffLogin.html")


@app.route('/accounts_login', methods=["POST", "GET"])
def accounts_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM accountsstaff WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        if not user:
            read = "Error password or user not matched"
            return render_template("accountsLogin.html", read=read)

        if user:
            if bcrypt.hashpw(password, user['password'].encode('utf-8')) == user['password'].encode('utf-8'):
                session['username'] = user['username']
                return redirect(url_for("accounts_dashboard"))
            else:
                return "Error password or user not matched"

    return render_template("accountsLogin.html")


@app.route('/admin_dashboard', methods=['POST', 'GET'])
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/accounts_dashboard', methods=['POST', 'GET'])
def accounts_dashboard():
    return render_template('accounts_dashboard.html')


@app.route('/staff_dashboard', methods=['POST', 'GET'])
def staff_dashboard():
    return render_template('staff_dashboard.html')


@app.route('/add_student', methods=['POST', 'GET'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        dateOfBirth = request.form['dateOfBirth']
        stage = request.form['stage']
        term = request.form['term']

        parentname = request.form['parentname']
        address = request.form['address']
        date = request.form['date']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO stud (name, dateOfBirth,stage, term, parentname, address, date) VALUES ( %s, %s, %s, %s, %s, %s, %s)",
            (name, dateOfBirth, stage, term, parentname, address, date,))
        mysql.connection.commit()
        session['name'] = name
        cur.close()

        return redirect(url_for('admin_dashboard'))

    return render_template('add_student.html')


@app.route('/updateFees', methods=['POST', 'GET'])
def updateFees():
    if request.method == 'POST':
        stages = request.form['stages']
        termFees = request.form['termFees']
        monthFees = request.form['monthFees']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO stagefees (stages, termFees,monthFees) VALUES (  %s, %s, %s)",
            (stages, termFees, monthFees)
        )
        mysql.connection.commit()
        session['stages'] = stages
        cur.close()

        return redirect(url_for('accounts_dashboard'))

    return render_template('stage_fees.html')


@app.route('/studentFees', methods=['POST', 'GET'])
def studentFees():
    if request.method == 'POST':
        studentName = request.form['studentName']
        # stage = request.form['stage']
        feesPaid = request.form['feesPaid']
        dateOfPayment = request.form['dateOfPayment']
        currentBalance = request.form['currentBalance']
        previousArears = request.form['previousArears']
        totalOwed = request.form['totalOwed']
        parentsContact = request.form['parentsContact']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO studentfees (studentName, feesPaid, dateOfPayment, currentBalance, previousArears,totalOwed,  parentsContact) VALUES (  %s, %s, %s, %s, %s, %s, %s)",
            (studentName, feesPaid, dateOfPayment, currentBalance, previousArears, totalOwed, parentsContact)
        )
        mysql.connection.commit()
        session['studentName'] = studentName
        cur.close()

        return redirect(url_for('accounts_dashboard'))

    return render_template('studentFees.html')


@app.route('/view_students', methods=['POST', 'GET'])
def view_students():
    if request.method == 'GET':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM stud")
        students = cur.fetchall()
        cur.close()

        return render_template('view_students.html', stud=students)


@app.route('/student_account', methods=['POST', 'GET'])
def student_account():
    if request.method == 'GET':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM studentfees")
        students = cur.fetchall()
        cur.close()

        return render_template('student_account.html', studentfees=students)


@app.route('/delStudent', methods=['POST', 'GET'])
def delStudent():
    if request.method == 'POST':
        student_name = request.form['student_name']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM stud WHERE name LIKE '{}%'".format(student_name))
        cur.execute("DELETE FROM studentfees WHERE studentName LIKE '{}%'".format(student_name))
        mysql.connection.commit()

        return redirect(url_for('admin_dashboard'))

    return render_template('delete_students.html')


@app.route('/delStaff', methods=['POST', 'GET'])
def delStaff():
    if request.method == 'POST':
        staf_name = request.form['staf_name']
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM staff WHERE staff_name LIKE '{}%'".format(staf_name))
        mysql.connection.commit()

        return redirect(url_for('admin_dashboard'))

    return render_template('delete_staff.html')


@app.route('/student_account_admin', methods=['POST', 'GET'])
def student_account_admin():
    if request.method == 'GET':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM studentfees")
        students = cur.fetchall()
        cur.close()

        return render_template('student_account_admin.html', studentfees=students)


@app.route('/add_staff', methods=['POST', 'GET'])
def add_staff():
    if request.method == 'POST':
        staff_name = request.form['staff_name']
        date_of_birth = request.form['date_of_birth']
        staffType = request.form['staffType']
        role = request.form['role']

        staffAddress = request.form['staffAddress']
        dateStarted = request.form['dateStarted']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO staff (staff_name, date_of_birth, staffType, role, staffAddress, dateStarted) VALUES ( "
            "%s, %s, %s, %s, %s, %s)",
            (staff_name, date_of_birth, staffType, role, staffAddress, dateStarted,))
        mysql.connection.commit()
        session['staff_name'] = staff_name

        return redirect(url_for('admin_dashboard'))

    return render_template('staff_list.html')


@app.route('/staff_list', methods=['POST', 'GET'])
def staff_list():
    if request.method == 'GET':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM staff")
        staff = cur.fetchall()
        cur.close()

        return render_template('staff_list.html', staff=staff)


@app.route('/view_student_score', methods=['POST', 'GET'])
def view_student_score():
    if request.method == 'GET':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM score")
        score = cur.fetchall()
        cur.close()

        return render_template('score.html', score=score)


@app.route('/view_attendance_score', methods=['POST', 'GET'])
def view_attendance_score():
    if request.method == 'GET':
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM attendance")
        attendance = cur.fetchall()
        cur.close()

        return render_template('attendance.html', attendance=attendance)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_word = request.form["search_word"]
        print(search_word)
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM studentfees WHERE studentName LIKE '{}%'".format(search_word))
        studentfees = cur.fetchall()
        return render_template('search.html', studentfees=studentfees)
    else:
        search_word = request.form["search_word"]
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM studentfees WHERE studentName LIKE '{}%'".format(search_word))
        studentfees = cur.fetchall()
        return render_template('search.html', studentfees=studentfees)


@app.route('/searched', methods=['POST', 'GET'])
def searched():
    if request.method == 'POST':
        search = request.form["search"]
        searcher = request.form["searcher"]
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM studentfees WHERE dateOfPayment BETWEEN '{}%' AND '{}%'".format(search, searcher))
        studentfees = cur.fetchall()
        return render_template('search.html', studentfees=studentfees)


@app.route('/search_attendance', methods=['POST', 'GET'])
def search_attendance():
    if request.method == 'POST':
        search = request.form["search"]
        # searcher = request.form["searcher"]
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM attendance WHERE dateTime LIKE '{}%' ".format(search))
        attendance = cur.fetchall()
        return render_template('attendance.html', attendance=attendance)


@app.route('/subjectScores', methods=['POST', 'GET'])
def subjectScores():
    if request.method == 'POST':
        studentName = request.form['studentName']
        stage = request.form['stage']
        subject = request.form['subject']
        score = request.form['score']
        scoreCategory = request.form['scoreCategory']
        teacherName = request.form['teacherName']
        date = request.form['date']

        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO score (studentName, stage, subject, score, scoreCategory,teacherName,  date) VALUES (  %s, %s, %s, %s, %s, %s, %s)",
            (studentName, stage, subject, score, scoreCategory, teacherName, date)
        )
        mysql.connection.commit()
        session['studentName'] = studentName
        cur.close()

        return redirect(url_for('staff_dashboard'))


@app.route('/search_score', methods=['POST', 'GET'])
def search_score():
    if request.method == 'POST':
        search = request.form["search"]
        # searcher = request.form["searcher"]
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM score WHERE studentName LIKE '{}%' ".format(search))
        score = cur.fetchall()
        return render_template('score.html', score=score)


@app.route('/attendance', methods=['POST', 'GET'])
def attendance():
    name = request.form['name']
    attendance = request.form['attendance']
    classTeacher = request.form['classTeacher']
    dateTime = request.form['dateTime']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO attendance (name, attendance, classTeacher,dateTime) VALUES ( %s, %s, %s, %s)",
        (name, attendance, classTeacher, dateTime)
    )
    mysql.connection.commit()
    session['name'] = name
    cur.close()

    return redirect(url_for('staff_dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
