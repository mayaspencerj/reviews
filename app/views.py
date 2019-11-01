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



@app.route("/")
@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = Accounts.query.filter_by(username=form.username).first()
            if user is not None and bcrypt.check_password_hash(
                user.password, form['password']
            ):
                login_user(user)
                flash('You were logged in. Go Crazy.')
                return redirect(url_for('index'))

            else:
                error = 'Invalid username or password.'
    return render_template('login.html', form=form, error=error)


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
def logout():
    logout_user()
    return redirect(url_for('index'))
