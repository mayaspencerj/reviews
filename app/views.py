from app import app
import os.path
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect
from datetime import datetime
from .forms import PostForm, RegisterForm, LoginForm
from .models import db, Items, Accounts
import sys, json, requests, os
from flask_login import current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from app import login_man

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
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Accounts(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('post_rev.html'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        flash('You were logged out.')
        return redirect(url_for('login'))

@app.route('/post_rev', methods=['GET','POST'])
@login_required
def post_review():
    form = PostForm()
    if form.validate_on_submit():
        lat = session.get("lat", None)
        long = session.get("long", None)
        user_ids = session["user_id"]
        post = Items(restaurant=form.restaurant.data, content=form.content.data, location_lat=lat, location_long=long, user_id=user_ids)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        session.clear()
        return redirect(url_for('view_all'))
    return render_template('post_rev.html', title='New Post',form=form, legend='New Post')

#ROUTE TO VIEW ALL THE RECORDS / TO DO ITEMS
@app.route("/view_all")
def view_all():
    posts = Items.query.all()
    post_ids = db.session.query(Items.user_id)
    for review in posts:
        name = review
        #id_num = db.session.query(Items.user_id)
        #name_id = post_ids[2] #that provides the user id
        #name = db.session.query(Accounts.username, name_id)
        #name = Query([Accounts, Items], session=some_session)

        #oAuthor = DBSession.query(User).filter_by(name="Sheena O'Connell")
        return render_template('view_all.html', posts=posts, name=name)

@login_required
@app.route("/view_user")
def view_user():
    name = session['username']
    posts = Items.query.filter_by(user_id=session['user_id'])
    post_ids = db.session.query(Items.user_id)

    return render_template('view_all.html', posts=posts,name=name)


@login_man.user_loader
def load_user(user_id):
    return Accounts.query.get(user_id)
