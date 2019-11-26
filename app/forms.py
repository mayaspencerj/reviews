from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import db, Items, Accounts


class PostForm(FlaskForm):
    restaurant = StringField('Restaurant', validators=[DataRequired(), Length(min=2, max=50)])
    content = StringField('Review', validators=[DataRequired(), Length(min=2, max=10000)])
    location_lat = HiddenField('location_lat', render_kw={'id': 'input_lat'}) # set html id attribute to
    location_long = HiddenField('location_long', render_kw={'id': 'input_long'}) # allow value to be set
    submit = SubmitField('Publish Review')

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        account = Accounts.query.filter_by(username=username.data).first()
        if account:
            raise ValidationError('An account with that username already exists')
            app.logger.error("ACCOUNT WITH USERNAME GIVEN ALREADY EXISTS")


    def validate_email(self, email):
        account = Accounts.query.filter_by(email=email.data).first()
        if account:
            raise ValidationError('An account with that email already exists')
            app.logger.error("ACCOUNT WITH EMAIL GIVEN ALREADY EXISTS")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
