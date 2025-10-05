from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class HotelSearchForm(FlaskForm):
    search = StringField('Search Hotels')
    city_id = SelectField('City', coerce=int, validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    min_price = FloatField('Min Price', validators=[Optional(), NumberRange(min=0)])
    max_price = FloatField('Max Price', validators=[Optional(), NumberRange(min=0)])
    min_rating = FloatField('Min Rating', validators=[Optional(), NumberRange(min=0, max=5)])
    submit = SubmitField('Search')

class AdminHotelForm(FlaskForm):
    name = StringField('Hotel Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    address = StringField('Address', validators=[Length(max=300)])
    rating = FloatField('Rating', validators=[NumberRange(min=0, max=5)])
    price_per_night = FloatField('Price per Night', validators=[DataRequired(), NumberRange(min=0)])
    amenities = TextAreaField('Amenities')
    image_url = StringField('Image URL', validators=[Length(max=500)])
    is_available = BooleanField('Available')
    city_id = SelectField('City', coerce=int, validators=[DataRequired()])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Create Hotel')

class AdminCityForm(FlaskForm):
    name = StringField('City Name', validators=[DataRequired(), Length(max=100)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Create City')

class AdminCategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Create Category')

class AdminUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])
    is_admin = BooleanField('Admin User')
    submit = SubmitField('Create User')

class AdminEditUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    is_admin = BooleanField('Admin User')
    submit = SubmitField('Update User')
