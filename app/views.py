from app import app
import os.path
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Text, create_engine, inspect, create_engine, MetaData, Table, Integer, String, ForeignKey
from datetime import datetime
from .forms import PostForm, RegisterForm, LoginForm, PasswordForm
from .models import db, Items, Accounts, Cuisines, AccountsCuisines
import sys, json, requests, os
from flask_login import current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from app import login_man

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
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Accounts.query.filter_by(username=request.form['username']).first()
            if user is not None and (user.password == request.form['password']):
            #if user is not None and Bcrypt.check_password_hash(user.password, request.form['password']):
                login_user(user)
                session['logged_in'] = True
                session['username'] = request.form['username']
                flash('You were logged in.')
                return redirect(url_for('view_all'))
            #login_user(user, remember=form.remember_me.data)

            else:
                flash('Invalid username or password.')
        else:
            flash('Sorry, no account located')
    return render_template('login.html', form=form,error=error)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Accounts(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        id = int(session['user_id'])
        choices = request.form.getlist('mycheckbox')
        if choices == []:
            pass
        else:
            for i in choices:
                cuisine_choice(id,i)


        return redirect(url_for('post_rev'))
    return render_template('register.html', form=form)


def cuisine_choice(acc,cui):
      insert_stmnt = AccountsCuisines.insert().values(accounts_id=acc,cuisines_id=cui)
      db.session.execute(insert_stmnt)
      db.session.commit()
      return



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


#NOTES:
#THINK POST_REV AND LOCATION CAN BE COMBINED
#NEED TO SEND OVER CORDS TO BE ADDED TO RECORD
@app.route('/post_rev', methods=['GET','POST'])
@login_required
def post_rev():
    form = PostForm()
    if form.validate_on_submit():
        lat = session.get("lat")
        long = session.get("long")
        user_ids = session["user_id"]
        post = Items(restaurant=form.restaurant.data, content=form.content.data, location_lat=lat, location_long=long, user_id=user_ids)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('view_all'))
    return render_template('post_rev.html', title='New Post',form=form, legend='New Post')

@app.route('/location', methods=['POST'])
def location():
    form = PostForm()
    data = json.loads(request.data)
    lat = data.get('lat')
    long = data.get('long')
    session["lat"] = lat
    session["long"] = long
    return render_template('post_rev.html', lat=lat,long=long, form=form)


#ROUTE TO VIEW ALL THE RECORDS / TO DO ITEMS
@app.route("/view_all")
def view_all():
    posts = Items.query.all()
    if posts == []:
        flash('No reviews to display yet!')
    else:
        for post in posts:
            #name_id = "This review is by " + str(item.user_id)
            post.username = Accounts.query.filter_by(id=Items.id).first().username
    return render_template('view_all.html', posts=posts)


#ROUTE TO VIEW ALL THE RECORDS / TO DO ITEMS
@app.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    #VIEW PREFERENCES
    return render_template('preferences.html')


@app.route("/view_user")
@login_required
def view_user():
    name = session['username'].capitalize()
    posts = Items.query.filter_by(user_id=session['user_id'])
    return render_template('view_all.html', posts=posts,name=name)

@app.route("/password_change", methods=["GET", "POST"])
@login_required
def user_password_change():
    form = PasswordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = current_user
            user.password = form.password.data
            #db.session.add(user)
            db.session.commit()
            flash('Password has been updated!', 'success')
            return redirect(url_for('view_all'))

    return render_template('password_change.html', form=form)



@login_man.user_loader
def load_user(user_id):
    return Accounts.query.get(user_id)
