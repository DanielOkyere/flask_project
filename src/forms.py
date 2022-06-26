from tokenize import String
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from src.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()

        if user:
            raise ValidationError(
                'Username already exist, Kindly use a different Username')

    def validate_email(self, email_to_check):
        user_email = User.query.filter_by(email=email_to_check.data).first()

        if user_email:
            raise ValidationError('Email Already Exist')

    username = StringField(label='User Name:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[
                        Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class Loginform(FlaskForm):
      username = StringField(label='User Name:', validators=[
                         DataRequired()])

      password = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    
      submit = SubmitField(label='Signin')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')