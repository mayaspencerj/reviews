from app import app
import os.path
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect
from datetime import datetime
from .forms import PostForm, RegisterForm, LoginForm
from .models import db, Items
import sys, json, requests, os

@app.route("/")
def login_page():
    if not session.get('logged_in'):
        return render_template('loginpage.html')
    else:
        return "Hello Boss!"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('Account not recognised!')
        return login_page()

@app.route("/view_all")
def view_all():
    posts = Items.query.order_by(Items.date_posted.desc()).all()
    return render_template('view_all.html', posts=posts)

@app.route("/create", methods=['GET', 'POST'])
def create():
    form = PostForm()
    if form.validate_on_submit():
        lat = session.get("lat", None)
        long = session.get("long", None)
        print(lat, long)
        post = Items(restaurant=form.restaurant.data, content=form.content.data, location_lat=lat, location_long=long )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        session.clear()
        return redirect(url_for('view_all'))

    return render_template('create.html', title='New Post',form=form, legend='New Post')
