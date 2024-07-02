# Note: it is important to add "render_template" to the imports
from flask import Flask, render_template
from flask import Flask, render_template, request
from flask import redirect, url_for, flash, abort

# Flask-Login is a Flask extension that provides a framework for handling user authentication
import flask_login
from flask_login import LoginManager
from flask_login import login_required
# Logs a user in. We should pass the actual user object to this method:
# returns True if the log in attempt succeeds, and False if it fails
from flask_login import login_user

# Security and Forms for the login
import werkzeug.security as ws
# from forms import LoginForm

# Import the Image module from the PIL (Python Imaging Library) package. 
# Used to preprocess the images uploaded by the users. 
# Ensure 'Pillow' is installed before running the application by using
# the command 'pip install Pillow'
from PIL import Image
PROFILE_IMG_HEIGHT = 130
POST_IMG_WIDTH = 300

# Import the datetime library to handle the pubblication date of the raccolte
import datetime

## Import the dao modules and the models module
import models
import users_dao
import adverts_dao

## Here I call these functions for the creation of the DB tables at startup time
from table_creation import *
create_table_users()
create_table_adverts()
create_table_photos()
create_table_bookings()

# create the application
app = Flask(__name__)

app.config['SECRET_KEY'] = 'gematria'

# This is for login_manager 
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def home():
    return render_template('home.html', title='Home')


#########################################################
#########################################################
#########################################################
####### Add a new advert to rent a house ################
#########################################################
#########################################################
#########################################################

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Dynamic routing, page for a SINGLE advert
@app.route('/advert/<int:advert_id>')
def advert(advert_id):
    adverts = []
    adverts = adverts_dao.get_all_adverts()

    advert = adverts[advert_id-1]

    if advert_id < 1 or advert_id > len(adverts):
        abort(404)  # Post not found, return a 404 error

    advert = adverts[advert_id-1]

    # I also have to pass it the landlord to whom the advert belongs, 
    # each advert has a id_landlord field, so I use adverts_dao's get_user_by_id method ..
    usr = users_dao.get_user_by_id(advert['id_landlord'])

    return render_template('advert.html', advert = advert, usr = usr, title='Advert')

@app.route('/new_advert', methods = ['GET', 'POST'])
@login_required
def new_advert():
    # I create a new data structure of 'dictionary' type to handle the data passed from the 'landlord' user from base.html
    new_advert = request.form.to_dict()

    ## Later on, I add also more data, or, better yet, 'meta-data', that are not sent directly by the form, but we need to collect
    ## them in order to add them to the database, so that we can properly store the informations that identify the advert.
    ## Among these 'meta-data' are: the User that posted the advert, the id of said user and the date-time of the advert's post:

    # flask_login.current_user.id is the id of the current user, and it's also important to save the user's email
    new_advert['id_user'] = int(flask_login.current_user.id)  
    new_advert['email'] = str(flask_login.current_user.email)
    # Appending also the date field, which is the current date and time when this advert was created
    seconds = int(datetime.datetime.now().timestamp())       
    new_advert.append('date')

    # I take from new_advert the images, by checking first if said image exists
    post_images = []
    new_advert['images'] = [] # the field 'images' of the dictionary new_advert is a list
    if new_advert['image1']:
        post_images.append(new_advert['image1'])
    if new_advert['image2']:
        post_images.append(new_advert['image2'])
    if new_advert['image3']:
        post_images.append(new_advert['image3'])
    if new_advert['image4']:
        post_images.append(new_advert['image4'])
    if new_advert['image5']:
        post_images.append(new_advert['image5'])

    ## All of the data that I pass from the form in base.html, made by a user whose type is 'landlord'
    # new_advert_form['title_advert']
    # new_advert_form['address']
    # new_advert_form['property_type']
    # new_advert_form['rooms'] # int type, from 1 to 5, the number of rooms
    # new_advert_form['description']
    # new_advert_form['price'] # int type, asking price for the room, from 100 to 500
    # new_advert_form['furnished'] # two values: 'yes' or 'no'
    
    ## I can make checks on these values passed from the base.html form
    if new_advert['description'] == '':
        app.logger.error('The description field can\'t be left empty!')
        return redirect(url_for('home'))
    # if new_advert['date'] == '':
        # app.logger.error('Devi selezionare una data')
        # return redirect(url_for('home'))
    # if datetime.datetime.strptime(new_advert['date'], '%Y-%m-%d').date() < datetime.date.today():
        # app.logger.error('Data errata')
        # return redirect(url_for('home'))

    # Handling the images inserted by the 'landlord' user
    # post_image = request.files['images[]'] # not a really smart move in my book
    # TODO: optimizing the for-if annidation
    for image in post_images:
        if image:
            # Open the user-provided image using the Image module
            img = Image.open(image)

            # Get the width and height of the image
            width, height = img.size

            # Calculate the new height while maintaining the aspect ratio based on the desired width
            new_height = height/width * POST_IMG_WIDTH

            # Define the size for thumbnail creation with the desired width and calculated height
            size = POST_IMG_WIDTH, new_height
            img.thumbnail(size, Image.Resampling.LANCZOS)

            # Extracting file extension from the image filename
            ext = image.filename.split('.')[-1]
            # Getting the current timestamp in seconds
            seconds = int(datetime.datetime.now().timestamp())       

            # Saving the image with a unique filename in the 'static' directory
            img.save('static/@' + flask_login.current_user.nickname.lower() + '-' + str(seconds) + '.' + ext)

            # TODO: to fix the following two lines in its context
            # Updating the 'immagine_post' field in the post dictionary with the image filename
            # new_advert['i']
            new_advert['images'].append('@' + flask_login.current_user.nickname.lower() + '-' + str(seconds) + '.' + ext)

    # After finishing making the checks, I put the "post" dictionary in the database
    success = adverts_dao.add_advert(new_advert)

    if success:
        app.logger.info('Advert created correctly')
    else:
        app.logger.error('Error in the advert creation: retry!')
    return redirect(url_for('home'))


#########################################################
#########################################################
#########################################################
###### First off the Login and Signup ###################
#########################################################
#########################################################
#########################################################
#########################################################

# Define the signup page
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup_function():

    # I take from the form the input datas and import them locally as a dictionary
    nuovo_utente_form = request.form.to_dict()

    # I try to retrieve the unique email of the nuovo_utente_form from the db ..
    user_in_db = users_dao.get_user_by_email(nuovo_utente_form.get('email'))

    # ... and I check weather it has already been registered ..
    if user_in_db:
        flash('There\'s already a user with these credentials', 'danger')
        return redirect(url_for('signup'))
    # .. and if it hasn't been registered ..
    else:
        # I generate an hash for the password that has been inserted by the form input
        nuovo_utente_form['password'] = ws.generate_password_hash(nuovo_utente_form.get('password'))

        # I add the user to the db using the method "add_user" from the users_dao.py
        success = users_dao.add_user(nuovo_utente_form)

        if success:
            flash('User created correctly', 'success')
            return redirect(url_for('home'))
        else:
            flash('Errore nella creazione del utente: riprova!', 'danger')
            return redirect(url_for('signup'))

@login_manager.user_loader
def load_user(user_id):
    db_user = users_dao.get_user_by_id(user_id)
    if db_user is not None:
        user = models.User(id=db_user['id'], 
                           email=db_user['email'],
                           user_type=db_user['user_type'],	
                           password=db_user['password'])
    else:
        user = None
    return user

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():

    # Retrieving the informations from the form @ /login
    utente_form = request.form.to_dict()
    # Using the "get_user_by_nickname" method from users_dao, which
    # retrieves the user from the database with the given nickname passed
    # from the form in /login
    utente_db = users_dao.get_user_by_email(utente_form['email'])

    # If there's no utente_db in the database (meaning the user just doesn't exist into the db)
    # or if the password given as input in the form /login isn't equal to the one in the database
    if not utente_db or not ws.check_password_hash(utente_db['password'], utente_form['password']):
        flash('Credenziali non valide, riprova', 'danger')
        return redirect(url_for('home'))
    else:
        # if, instead, it exists, we create a new user instance using the "User model" defined in models.py

        # Create a new user instance called "new"
        new = models.User(id=utente_db['id'], 
                          email=utente_db['email'],
                          user_type=utente_db['user_type'], 
                          password=utente_db['password'])
        # We log in said user called "new"
        flask_login.login_user(new, True)
        flash('Welcome back ' + utente_db['email'] + '!', 'success')
        return redirect(url_for('home'))

# Log out route
@app.route("/logout")
@login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html', title='About Us')
