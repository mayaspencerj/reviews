from app import app
import os.path
from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, jsonify, session, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect
from datetime import datetime
from .forms import PostForm, RegisterForm, LoginForm
from .models import db, Items, Accounts
import sys, json, requests, os
from flask_login import current_user, login_user

@app.route("/")

def index():
    return render_template('index.html')
