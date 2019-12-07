from app import app, login_man
import os.path,sys, json, requests, os, logging, bcrypt
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Text, create_engine, inspect, create_engine, MetaData, Table, Integer, String, ForeignKey
from .forms import PostForm, RegisterForm, LoginForm, PasswordForm
from .models import db, Items, Accounts, Cuisines, AccountsCuisines
from logging.handlers import RotatingFileHandler
from flask_login import current_user, login_user, logout_user, login_required

#create and set up logging path and message layout
if not os.path.exists('logs'):
    os.mkdir('logs')
file_handler = RotatingFileHandler('logs/flask.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s '))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

#error handling
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

@login_man.unauthorized_handler
def unauthorized_callback():
    return redirect('/login')


@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    #if user authenticated deny access to login page and redirect
    if current_user.is_authenticated:
        app.logger.warning('LOGIN PAGE DENIED ACCESS AS LOGGED IN ALREADY')
        return redirect(url_for('view_all'))
    else:
        app.logger.info('LOGIN PAGE LOADED')
        app.logger.propagate = False
        error = None
        form = LoginForm(request.form)

        #if login form button is submitted
        if request.method == 'POST':
            app.logger.info('SUBMITTED LOGIN DETAILS')

            #check if login details validated
            if form.validate_on_submit():
                user = Accounts.query.filter_by(username=request.form['username']).first()
                entered_password = str(request.form['password']).encode('utf-8')
                hashed = bcrypt.hashpw(entered_password, bcrypt.gensalt())

                #log in user is username found and password matches hashed one stored
                if user is not None and (bcrypt.checkpw(entered_password, user.password)):
                    login_user(user)
                    session['logged_in'] = True
                    session['username'] = request.form['username']
                    flash('You were logged in.')
                    app.logger.info('USER LOGGED IN')
                    return redirect(url_for('view_all'))
                else:
                    flash('Invalid username or password.')
                    app.logger.error("FAILED LOGIN")

            #no account found / wrong log in details
            else:
                flash('Sorry, no account located')
                app.logger.warning("NO ACCOUNT FOUND")
    return render_template('login.html', form=form,error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    #deny access to register page if user is logged in and redirect
    if current_user.is_authenticated:
        return redirect(url_for('view_all'))
    else:
        #loaded login page with form
        form = RegisterForm()
        app.logger.info('REGISTRATION PAGE LOADED')
        if form.validate_on_submit():
            password = str(form.password.data).encode('utf-8')
            hashed = bcrypt.hashpw(password,bcrypt.gensalt())
            user = Accounts(
                username=form.username.data,
                email=form.email.data,
                password=hashed)
            db.session.add(user)
            db.session.commit()
            app.logger.info('NEW ACCOUNT CREATED')

            login_user(user)
            id = int(session['user_id'])
            choices = request.form.getlist('mycheckbox')

            #extract the cuisines which user has selected upon reigistering
            if choices == []:
                pass
            else:
                for i in choices:
                    cuisine_choice(id,i)
                app.logger.info('NEW USER CUISINES STORED')

            return redirect(url_for('post_rev'))
    return render_template('register.html', form=form)


def cuisine_choice(acc,cui):
    #instead all cusines selected into database
    #many to many model
      insert_stmnt = AccountsCuisines.insert().values(accounts_id=acc,cuisines_id=cui)
      db.session.execute(insert_stmnt)
      db.session.commit()
      return


#log out the usser
@app.route("/logout")
@login_required
def logout():
    app.logger.info('USER LOGGED OUT ')
    logout_user()
    return redirect(url_for('login'))

@app.route('/post_rev', methods=['GET','POST'])
@login_required
def post_rev():
    #load form to post a review
    form = PostForm()

    #check if form has been validated
    if form.validate_on_submit():
        lat = form.location_lat.data;
        long = form.location_long.data;
        user_ids = session["user_id"]
        post = Items(restaurant=form.restaurant.data, content=form.content.data, location_lat=lat, location_long=long, user_id=user_ids)
        #store new review record in db
        db.session.add(post)
        db.session.commit()
        app.logger.info('USER REVIEW POSTED')
        flash('Your post has been created!', 'success')
        return redirect(url_for('view_all'))
    return render_template('post_rev.html', title='New Post',form=form, legend='New Post')


#ROUTE TO VIEW ALL THE RECORDS / TO DO ITEMS
@app.route("/view_all")
def view_all():
    #query all the reviews in db
    posts = Items.query.all()
    #if empty / no reviews yet - flash message
    if posts == []:
        flash('No reviews to display yet!')
        app.logger.warning("NO REVIEWS DISPLAYED")
    #show all reviews if not empty
    else:
        app.logger.info('DISPLAYING REVIEWS')
        for post in posts:
            post.username = (post.accounts.username).capitalize()
    return render_template('view_all.html', posts=posts)


#ROUTE TO VIEW ALL THE RECORDS / TO DO ITEMS
@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    #show all the selected cuisinses by user upon registering
    user_id = session['user_id']
    app.logger.info('USER REQUESTED PREFERENCES')
    cuisine_list = Cuisines.query.filter(Cuisines.Accounts.any(id=user_id)).all()

    if cuisine_list == []:
        #flash message if no cuisines were selected
        app.logger.warning("NO PREFERENCES AVAILABLE")
        flash('You have no preferences!')
    else:
        app.logger.info('DISPLAYING PREFERENCES')
    return render_template('preferences.html', cuisine_list=cuisine_list)

@app.route("/view_user",  methods=["GET", "POST"])
@login_required
def view_user():
    #view only the specific users posted reviews
    app.logger.info('USER VIEWING THEIR REVIEWS')
    name = session['username'].capitalize()
    posts = Items.query.filter_by(user_id=session['user_id'])
    empty = posts.first()
    #alternative message displayd in no reviews available
    if empty == None:
        flash('No reviews to display yet!')
        app.logger.warning("NO USER REVIEWS DISPLAYED")
    else:
        app.logger.info('DISPLAYING USER REVIEWS')
    return render_template('view_user.html', posts=posts)

@app.route("/password_change", methods=["GET", "POST"])
@login_required
#allow the user to reset their password
def user_password_change():
    form = PasswordForm()
    app.logger.info('LOADING PASSWORD RESET PAGE')
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            password = str(form.password.data).encode('utf-8')
            #hashes and encodes the password to be stored in database
            hashed = bcrypt.hashpw(password,bcrypt.gensalt())
            user.password = hashed
            db.session.commit()
            flash('Password has been updated!', 'success')
            app.logger.info('PASSWORD HAS BEEN UPDATED')
            return redirect(url_for('view_all'))

    return render_template('password_change.html', form=form)

@login_man.user_loader
def load_user(user_id):
    return Accounts.query.get(user_id)
