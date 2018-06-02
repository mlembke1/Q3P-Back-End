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
            author = session['username']

            #  CREATE CURSOR
            cur = mysql.connection.cursor()

            # EXECUTE QUERY
            cur.execute('''INSERT INTO decks(title, subject, author) VALUES(%s, %s, %s, %s)''', (title, subject, author))

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
def deck_by_id(id):
    #  CREATE CURSOR
    cur = mysql.connection.cursor()

    # EXECUTE QUERY
    cur.execute('''SELECT * FROM decks WHERE id = %s''', [id])

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    deck = cur.fetchall()

    # CLOSE THE CONNECTION
    cur.close()
    return json_response(deck=deck)


# ######################## UPDATE ###########################################
 # UPDATE A JOURNAL ENTRY
@app.route('/update/<string:id>', methods=['PUT'])
def update(id):
    form = updateDeckForm(request.form)
        title = form.title.data
        subject = form.subject.data

        # CREATE CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE QUERIES
        cur.execute ('''UPDATE decks SET title = %s, subject = %s WHERE id=%s''', (title, subject, id))

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        # CLOSE THE CONNECTION
        cur.close()

        return json_response(updateStatus='success')

# ######################## DELETE ###########################################
 # DELETE A JOURNAL ENTRY
@app.route('/delete/<string:id>', methods=['DELETE'])
def delete(id):
        # CREATE CURSOR
        cur = mysql.connection.cursor()

        # EXECUTE QUERIES
        cur.execute ('''DELETE FROM decks WHERE id=%s''', [id])

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        # CLOSE THE CONNECTION
        cur.close()

        return json_response(deleteStatus='success')
    
############## RUN THE APP ###############
if __name__ == '__main__':
    app.secret_key=os.environ.get('SECRET_KEY')
    app.run(debug=True)
