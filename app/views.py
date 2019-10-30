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
#VIEW ALL POSTS
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('index.html', title='Sign In', form=form)  #login


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

