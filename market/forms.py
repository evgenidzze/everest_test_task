from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FileField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError

from market import photos
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, name_to_check):
        user = User.query.filter_by(username=name_to_check.data).first()
        if user:
            raise ValidationError('Username already exists! Please try another name.')

    def validate_email(self, email_to_check):
        email = User.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError('Email address already exists! Please try another email.')

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Sign Up')


class LogInForm(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class AddItem(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    price = IntegerField(label='Price', validators=[DataRequired()])
    weight = IntegerField(label='Volume', validators=[DataRequired()])
    color = StringField(label='Color', validators=[DataRequired()])
    image = FileField(validators=[FileAllowed(photos, 'Image only!'), FileRequired('File was empty!')])


class AddToCart(FlaskForm):
    quantity = IntegerField(label='Quantity')
    id = HiddenField('ID')


class CheckoutForm(FlaskForm):
    first_name = StringField(label='First Name', validators=[DataRequired(), Length(min=1)])
    last_name = StringField(label='Last Name', validators=[DataRequired(), Length(min=1)])
    country = StringField(label='Country', validators=[DataRequired(), Length(min=1)])
    city = StringField(label='City', validators=[DataRequired(), Length(min=1)])
    address = StringField(label='Street', validators=[DataRequired(), Length(min=1)])
    cvv = PasswordField(label='CVV', validators=[Length(min=3, max=3), DataRequired()])
    card_number = StringField(label='Card Number', validators=[Length(min=16, max=16), DataRequired()])



