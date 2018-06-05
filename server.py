####### IMPORTING DEPENDENCIES #########
from flask import jsonify, json
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
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# SET SECRET KEY
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
json = FlaskJSON(app)
Session(app)

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DB = os.environ.get('MYSQL_DB')
MYSQL_PORT = os.environ.get('MYSQL_PORT')


# MYSQL CONFIGURATION WHEN DEPLOYED
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-04.cleardb.net'
app.config['MYSQL_USER'] = 'bd4527260a9719'
app.config['MYSQL_PASSWORD'] = '2b516563'
app.config['MYSQL_DB'] = 'heroku_aa291c01967962f'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# INITIATES MYSQL
mysql = MySQL(app)

######## SERVER SIDE VALIDATION FOR FORMS ######
# class newDeckForm(Form):
#     author = StringField('Author', [validators.Length(min=1, max=50)])
#     title  = StringField('Title', [validators.Length(min=4, max=50)])
#
# class updateDeckForm(Form):
#     subject = StringField('Author', [validators.Length(min=1, max=50)])
#     title  = StringField('Title', [validators.Length(min=4, max=50)])
#
# class newCardForm(Form):
#     front = StringField('Front', [validators.Length(min=1, max=300)])
#     back  = StringField('Back', [validators.Length(min=4, max=300)])
#
# class updateCardForm(Form):
#     front = StringField('Front', [validators.Length(min=1, max=300)])
#     back  = StringField('Back', [validators.Length(min=4, max=300)])
#
# class newTagForm(Form):
#     name = StringField('Name', [validators.Length(min=1, max=25)])

############# ROUTES #############

@app.route('/logout')
def logout():
    session.clear()
    return json_response(logoutStatus='success')

######################### CREATE #######################################
# CREATE A NEW USER
@app.route('/signup', methods=['POST'])
def signup():
    # if not session.username:
        # FROM THE COMMAND LINE USE THIS TO CREATE A USER
        json = request.get_json()
        username = json['username']
        email = json['email']
        password = sha256_crypt.hash(json['password'])

        # INSERT NEW USER INTO USERS TABLE
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO users(username, email, password) VALUES(%s, %s, %s)''', (username, email, password))
        #  COMMIT TO DATABASE
        mysql.connection.commit()
        # CLOSE THE CONNECTION
        cur.close()

        # GET THE USER_ID TO PUT IT INTO THE SESSION
        cur = mysql.connection.cursor()
        cur.execute('''SELECT id FROM users WHERE username = %s''', [username])
        mysql.connection.commit()
        id = cur.fetchone()
        cur.close()

        session['logged_in'] = True
        session['username'] = username
        session['id'] = id

        return json_response(signupStatus='success')


#  CREATE A NEW DECK
@app.route('/createDeck', methods=['POST'])
def createNewDeck():
    # if session.username:
        form = newDeckForm(request.form)
        # if request.method == 'POST' and form.validate():
            # title = form.title.data
            # subject = form.subject.data
            # author = session['username']
            # user_id = session['id']

        # FROM THE COMMAND LINE USE THIS TO CREATE A DECK
        json = request.get_json()
        title = json['title']
        subject = json['subject']
        author = json['author']
        public = json['public']
        user_id = 1

        app.logger.info(public)

        cur = mysql.connection.cursor()

        cur.execute('''INSERT INTO decks(title, subject, author, public) VALUES(%s, %s, %s, %s)''', (title, subject, author, public))
        #  COMMIT TO DATABASE
        mysql.connection.commit()
        # CLOSE THE CONNECTION
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('''SELECT LAST_INSERT_ID()''')
        mysql.connection.commit()
        deck_id = cur.fetchone()['LAST_INSERT_ID()']
        cur.close()

        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO users_decks(user_id, deck_id) VALUES(%s, %s)''', (user_id, deck_id))
        mysql.connection.commit()
        cur.close()

        return json_response(newDeckStatus='success')

#  CREATE A NEW CARD
@app.route('/createCard', methods=['POST'])
def createNewCard():
    # if session.username:
        # form = newCardForm(request.form)
        # if request.method == 'POST' and form.validate():
        #     front = form.front.data
        #     back = form.back.data
        #     deck_id = form.deck_id.data

            # FROM THE COMMAND LINE USE THIS TO CREATE A CARD
            json = request.get_json()
            front = json['front']
            back = json['back']
            deck_id = json['deck_id']

            cur = mysql.connection.cursor()


            cur.execute('''INSERT INTO cards(front, back, deck_id) VALUES(%s, %s, %s)''', (front, back, deck_id))

            #  COMMIT TO DATABASE
            mysql.connection.commit()

            # CLOSE THE CONNECTION
            cur.close()

            return json_response(newCardStatus='success')

#  CREATE A NEW CARD
@app.route('/createTag', methods=['POST'])
def createNewTag():
    # if session.username:
        # form = newTagForm(request.form)
        # if request.method == 'POST' and form.validate():
        #
        #     name = form.name.data
        #     card_id = form.card_id.data

        # FROM THE COMMAND LINE USE THIS TO CREATE A CARD
        json = request.get_json()
        name = json['name']
        card_id = json['card_id']


        cur = mysql.connection.cursor()
        # FOR THE NEW TAG
        cur.execute('''INSERT INTO tags(name) VALUES(%s)''', [name])
        #  COMMIT TO DATABASE
        mysql.connection.commit()
        # CLOSE THE CONNECTION
        cur.close()

        #  GET TAG_ID
        cur = mysql.connection.cursor()
        cur.execute('''SELECT LAST_INSERT_ID()''')
        mysql.connection.commit()
        tag_id = cur.fetchone()['LAST_INSERT_ID()']
        cur.close()


        # FOR THE NEW CARDS_TAGS ENTRY
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO cards_tags(card_id, tag_id) VALUES(%s, %s)''', (card_id, tag_id))
        mysql.connection.commit()
        cur.close()

        return json_response(newTagStatus='success')



# ######################## READ ###########################################
# LOGIN ROUTE
@app.route('/login', methods=['POST'])
def login():

    json = request.get_json()
    username = json['username']
    password = json['password']

    if username:
        # GET THE USER_ID TO PUT IT INTO THE SESSION
        cur = mysql.connection.cursor()
        cur.execute('''SELECT id FROM users WHERE username = %s''', [username])
        mysql.connection.commit()
        id = cur.fetchall()
        cur.close()

        # GET STORED PASSWORD
        cur = mysql.connection.cursor()
        cur.execute('''SELECT password FROM users WHERE username = %s''', [username])
        mysql.connection.commit()
        hashed_password = cur.fetchall()
        cur.close()

        if sha256_crypt.verify(password, hashed_password[0]['password']):
            # SET THE SEESION
            session['logged_in'] = True
            session['username'] = username
            session['id'] = id[0]['id']

        return json_response(loginStatus='success')

    return json_response(loginStatus='fail')


# GET ALL USERS
@app.route('/getAllUsers')
def getAllUsers():
    cur = mysql.connection.cursor()

    result = cur.execute('''SELECT username FROM users''')

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    allUsers = cur.fetchall()

    # CLOSE THE CONNECTION
    cur.close()

    return json_response(allUsers=allUsers)


# VIEW ALL DECKS
@app.route('/getAllDecksForUser')
def readAllDecksForUser():
    # if session.username:
        username = session['username']
        cur = mysql.connection.cursor()

        cur.execute('''SELECT * FROM decks WHERE username = %s''', [username])

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        decks = cur.fetchall()

        # CLOSE THE CONNECTION
        cur.close()

        return json_response(userDecks=userDecks)


# VIEW ALL DECKS
@app.route('/getAllPublicDecks')
def readAllPublicDecks():
    # if session.username:
        cur = mysql.connection.cursor()
        public = 'T'

        cur.execute('''SELECT * FROM decks WHERE public = %s''', [public])

        #  COMMIT TO DATABASE
        mysql.connection.commit()

        decks = cur.fetchall()

        # CLOSE THE CONNECTION
        cur.close()

        return json_response(publicDecks=decks)


#  GET SPECIFIC DECK BY ITS ID
@app.route('/deck/<string:id>')
def deck_by_id(id):
    cur = mysql.connection.cursor()


    cur.execute('''SELECT * FROM decks WHERE id = %s''', [id])

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    deck = cur.fetchone()

    # CLOSE THE CONNECTION
    cur.close()
    return json_response(deck=deck)


# ######################## UPDATE ###########################################
 # UPDATE A JOURNAL ENTRY
@app.route('/update/<string:id>', methods=['PUT'])
def update(id):
    # form = updateDeckForm(request.form)
    # title = form.title.data
    # subject = form.subject.data

    json = request.get_json()
    title = json['title']
    subject = json['subject']

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
