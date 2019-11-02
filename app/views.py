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



@app.route("/")
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

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
                flash('You were logged in.')
                return redirect(url_for('index'))
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
        return redirect(url_for('index'))

    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
        session.pop('logged_in', None)
        flash('You were logged out.')
        return redirect(url_for('login'))

@app.route('/post_rev')
@login_required
def post_review():
    form = PostForm()
    return render_template('post_rev.html',form=form)
