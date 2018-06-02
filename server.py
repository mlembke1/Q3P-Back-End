####### IMPORTING DEPENDENCIES #########
from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_session import Session
from flask_json import FlaskJSON, json_response
from wtforms import Form, StringField, TextAreaField, validators, PasswordField
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
import os

app = Flask(__name__)
# SET SECRET KEY
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
json = FlaskJSON(app)
Session(app)


# MYSQL CONFIGURATION WHEN DEPLOYED
app.config['MYSQL_HOST'] = process.env.MYSQL_HOST
app.config['MYSQL_USER'] = process.env.MYSQL_USER
app.config['MYSQL_PASSWORD'] = process.env.MYSQL_PASSWORD
app.config['MYSQL_DB'] = process.env.MYSQL_DB
app.config['MYSQL_PORT'] = process.env.MYSQL_PORT
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# INITIATES MYSQL
mysql = MySQL(app)

######## SERVER SIDE VALIDATION FOR FORMS ######
class newDeckForm(Form):
    subject = StringField('Author', [validators.Length(min=1, max=50)])
    title  = StringField('Title', [validators.Length(min=4, max=50)])

class updateDeckForm(Form):
    subject = StringField('Author', [validators.Length(min=1, max=50)])
    title  = StringField('Title', [validators.Length(min=4, max=50)])

class signupForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=1, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message="Passwords do not match"),
        validators.Length(min=4, max=50)
    ])
    confirm = PasswordField('Confirm Password')


class loginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=50)])
    password = StringField('Password', [validators.Length(min=4, max=50)])

############# ROUTES #############
# GET HOME PAGE
@app.route('/')
def getHome():
    if 'logged_in' in session:
        return redirect(url_for('read'))
    return render_template('home.html', home='home', whichPage='home')
    # return  render_template(url_for('read'))

# GET START PAGE --- LOGIN / SIGNUP
@app.route('/start')
def getStart():
    # if not session.username:
        return render_template('start.html', start='start', whichPage='start')
    # return  render_template(url_for('read'))
#  ABOUT ME PAGE
@app.route('/about')
def about():
    # if not session.username:
        return render_template('about.html', about='about', whichPage='about')
    # return  render_template(url_for('read'))

@app.route('/logout')
def logout():
    session.clear()
    return json_response(logoutStatus='success')

######################### CREATE #######################################
# CREATE A NEW USER
@app.route('/signup', methods=['POST'])
def signup():
    # if not session.username:
        form = signupForm(request.form)
        # if form.validate():
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.hash(form.password.data)

        #  CREATE CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE QUERY
        cur.execute('''INSERT INTO users(username, email, password) VALUES(%s, %s, %s)''', (username, email, password))

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        # CLOSE THE CONNECTION
        cur.close()

        session['logged_in'] = True
        session['username'] = username

        return json_response(signupStatus='success')


#  CREATE A NEW DECK
@app.route('/createDeck', methods=['POST'])
def createNewDeck():
    # if session.username:
        form = newDeckForm(request.form)
        if request.method == 'POST' and form.validate():
            title = form.title.data
            subject = form.subject.data
            username = session['username']

            #  CREATE CURSOR
            cur = mysql.connection.cursor()

            # EXECUTE QUERY
            cur.execute('''INSERT INTO decks(title, subject, username) VALUES(%s, %s, %s, %s)''', (title, subject, username))

            #  COMMIT TO DATABASE
            mysql.connection.commit()

            # CLOSE THE CONNECTION
            cur.close()

            return json_response(newDeckStatus='success')


# ######################## READ ###########################################
# LOGIN ROUTE
@app.route('/login', methods=['POST'])
def login():
    form = loginForm(request.form)
    username = form.username.data
    password = form.password.data


    if username:
        #  CREATE CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE QUERY
        cur.execute('''SELECT password FROM users WHERE username = %s''', [username])

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        hashed_password = cur.fetchall()
        app.logger.info(hashed_password)

        # CLOSE THE CONNECTION
        cur.close()

        if sha256_crypt.verify(password, hashed_password[0]['password']):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('read'))

        return json_response(loginStatus='success')

    return json_response(loginStatus='fail')


# GET ALL USERS
@app.route('/start/users')
def getAllUsers():
    #  CREATE CURSOR
    cur = mysql.connection.cursor()

    # EXECUTE QUERY
    cur.execute('''SELECT * FROM users''')

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    allUsers = cur.fetchall()

    # CLOSE THE CONNECTION
    cur.close()

    return json_response(allUsers=allUsers)


# VIEW ALL DECKS
@app.route('/getAllDecks')
def read():
    # if session.username:
        username = session['username']
        #  CREATE CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE QUERY
        cur.execute('''SELECT * FROM decks WHERE username = %s''', [username])

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        decks = cur.fetchall()

        # CLOSE THE CONNECTION
        cur.close()

        return json_response(allDecks=decks)


#  GET SPECIFIC DECK BY ITS ID
@app.route('/deck/<string:id>/')
def journal_entry(id):
    #  CREATE CURSOR
    cur = mysql.connection.cursor()

    # EXECUTE QUERY
    cur.execute('''SELECT * FROM entries WHERE id = %s''', [id])

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    entry = cur.fetchall()

    # CLOSE THE CONNECTION
    cur.close()
    return render_template('journal_entry.html', entry = entry[0])

# ######################## UPDATE ###########################################
 # UPDATE A JOURNAL ENTRY
@app.route('/update/<string:id>', methods=['PUT', 'GET'])
def update(id):
    form = updateEntryForm(request.form)
    if request.method == 'PUT':
        title = form.title.data
        author = form.author.data
        journal_entry = form.journal_entry.data
        # CREATE CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE QUERIES
        cur.execute ('''UPDATE entries SET title = %s, author = %s, journal_entry = %s WHERE id=%s''', (title, author, journal_entry, id))

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        # CLOSE THE CONNECTION
        cur.close()

        return json_response(message='success')

    # CREATE CURSOR
    cur = mysql.connection.cursor()

    # EXECUTE QUERIES
    cur.execute('''SELECT * FROM entries WHERE id=%s''', [id])

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    Entry = cur.fetchall()

    # CLOSE THE CONNECTION
    cur.close()

    return render_template('update.html', entry = Entry[0], whichPage='update', isLoggedIn=True)

# ######################## DELETE ###########################################
 # DELETE A JOURNAL ENTRY
@app.route('/delete/<string:id>', methods=['GET', 'DELETE'])
def delete(id):
    if request.method == 'DELETE':
        # CREATE CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE QUERIES
        cur.execute ('''DELETE FROM entries WHERE id=%s''', [id])

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        # CLOSE THE CONNECTION
        cur.close()

        return json_response(message='success')

    # CREATE CURSOR
    cur = mysql.connection.cursor()

    # EXECUTE QUERIES
    cur.execute('''SELECT * FROM entries WHERE id=%s''', [id])

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    Entry = cur.fetchall()

    # CLOSE THE CONNECTION
    cur.close()

    return render_template('delete.html', entry = Entry[0], whichPage='delete', isLoggedIn=True)

############## RUN THE APP ###############
if __name__ == '__main__':
    app.secret_key=os.environ.get('SECRET_KEY')
    app.run(debug=True)
