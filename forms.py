from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, PasswordField
from wtforms.validators import InputRequired


class CafeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    map_url = StringField('Map URL')
    img_url = StringField('Image URL')
    city = StringField('City')
    location = StringField('Location')
    seats = StringField('Seats')
    coffee_price = StringField('Coffee price')
    has_wifi = BooleanField('Has Wi-Fi')
    has_phone = BooleanField('Can take calls')
    has_sockets = BooleanField('Has sockets')
    has_toilet = BooleanField('Has toilet')
    submit_cafe = SubmitField('Submit')