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

app = Flask(__name__)
# SET SECRET KEY
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'
json = FlaskJSON(app)
Session(app)

# MYSQL_HOST = os.environ.get('MYSQL_HOST')
# MYSQL_USER = os.environ.get('MYSQL_USER')
# MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
# MYSQL_DB = os.environ.get('MYSQL_DB')
# MYSQL_PORT = os.environ.get('MYSQL_PORT')


# MYSQL CONFIGURATION WHEN DEPLOYED
app.config['MYSQL_HOST'] = 'us-cdbr-iron-east-04.cleardb.net'
app.config['MYSQL_USER'] = 'bd4527260a9719'
app.config['MYSQL_PASSWORD'] = '2b516563'
app.config['MYSQL_DB'] = 'heroku_aa291c01967962f'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# INITIATES MYSQL
mysql = MySQL(app)

############# ROUTES #############

@app.route('/')
def index():
    return json_response(doesItWork='yes')

@app.route('/getCurrentUser')
def currentUser():
    currentUser = session['username']
    return json_response(currentUser=currentUser)

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

@app.route('/logout')
def logout():
    session.clear()
    return json_response(logoutStatus='success')

######################### CREATE #######################################
# CREATE A NEW USER
@app.route('/signup', methods=['POST'])
def signup():
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
        json = request.get_json()
        title = json['title']
        subject = json['subject']
        author = session['username']
        public = json['public']
        user_id = session['id']

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


#  ADD A DECK TO THE USER'S LIST
@app.route('/addDeck', methods=['POST'])
def addDeck():
        json = request.get_json()
        user_id = session['id']
        deck_id = json['deck_id']

        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO users_decks(user_id, deck_id) VALUES(%s, %s)''', (user_id, deck_id))
        mysql.connection.commit()
        cur.close()

        return json_response(addDeckStatus='success')



#  CREATE A NEW CARD
@app.route('/createCard', methods=['POST'])
def createNewCard():
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

# ######################## READ ###########################################

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

# GET ALL CARDS
@app.route('/getAllCards', methods=['POST'])
def getAllCards():
    json = request.get_json()
    deck_id = json['deck_id']

    cur = mysql.connection.cursor()

    cur.execute('''SELECT * FROM cards WHERE deck_id = %s''', [deck_id])

    #  COMMIT TO DATABASE
    mysql.connection.commit()

    allCards = cur.fetchall()

    # CLOSE THE CONNECTION
    cur.close()

    return json_response(allCards=allCards)


# VIEW ALL DECKS
@app.route('/getAllDecksForUser')
def getAllDecksForUser():

        id = session['id']
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM decks
                       LEFT JOIN users_decks
                       ON decks.id = users_decks.deck_id
                       WHERE users_decks.user_id = %s''', [id])

        #  COMMIT TO DATABASE
        mysql.connection.commit()
        userDecks = cur.fetchall()
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


# ######################## UPDATE ###########################################
 # UPDATE A CARD
@app.route('/editCard', methods=['PUT'])
def update():
    json = request.get_json()
    title = json['title']
    subject = json['subject']
    card_id = json['card_id']
    deck_id = json['deck_id']

    cur = mysql.connection.cursor()
    cur.execute ('''UPDATE cards SET title = %s, subject = %s WHERE id=%s''', (title, subject, card_id))
    mysql.connection.commit()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM cards WHERE deck_id = %s''', [deck_id])
    mysql.connection.commit()
    updatedCards=cur.fetchall()
    cur.close()

    return json_response(updatedCards=updatedCards)

# ######################## DELETE ###########################################
# DELETE A DECK
@app.route('/deleteDeck', methods=['DELETE'])
def deleteDeck():

        # DELETE FROM DECKS
        json = request.get_json()
        deck_id = json['deck_id']
        cur = mysql.connection.cursor()
        cur.execute ('''DELETE FROM decks WHERE id=%s''', [deck_id])
        mysql.connection.commit()
        cur.close()

        # DELETE FROM USERS_DECKS
        cur = mysql.connection.cursor()
        cur.execute ('''DELETE FROM users_decks WHERE deck_id=%s''', [deck_id])
        mysql.connection.commit()
        cur.close()

        #  GET UPTATED DECKS
        id = session['id']
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM decks
                       LEFT JOIN users_decks
                       ON decks.id = users_decks.deck_id
                       WHERE users_decks.user_id = %s''', [id])
        mysql.connection.commit()
        updatedDecks = cur.fetchall()
        cur.close()

        return json_response(updatedDecks=updatedDecks)

# DELETE A DECK
@app.route('/removeDeckFromUser', methods=['DELETE'])
def deleteDeckFromUser():

        json = request.get_json()
        deck_id = json['deck_id']

        # DELETE FROM USERS_DECKS
        json = request.get_json()
        cur = mysql.connection.cursor()
        cur.execute ('''DELETE FROM users_decks WHERE deck_id=%s''', [deck_id])
        mysql.connection.commit()
        cur.close()

        #  GET UPDATED DECKS
        id = session['id']
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM decks
                       LEFT JOIN users_decks
                       ON decks.id = users_decks.deck_id
                       WHERE users_decks.user_id = %s''', [id])
        mysql.connection.commit()
        updatedDecks = cur.fetchall()
        cur.close()

        return json_response(updatedDecks=updatedDecks)

# DELETE A CARD
@app.route('/deleteCard', methods=['DELETE'])
def deleteCard():


        # DELETE FROM CARDS
        json = request.get_json()

        app.logger.info(json)

        id = json['card_id']
        deck_id = json['deck_id']
        cur = mysql.connection.cursor()
        cur.execute ('''DELETE FROM cards WHERE id=%s''', [id])
        mysql.connection.commit()
        cur.close()

        #  GET UPDATED CARDS
        cur = mysql.connection.cursor()
        cur.execute ('''SELECT * FROM cards WHERE deck_id = %s''', [deck_id])
        mysql.connection.commit()
        updatedCards = cur.fetchall()
        cur.close()

        return json_response(updatedCards=updatedCards)

############## RUN THE APP ###############
if __name__ == '__main__':
    app.secret_key=os.environ.get('SECRET_KEY')
    app.run(debug=True)
