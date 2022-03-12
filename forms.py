from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, URL, Length
# from wtforms.fields.html5 import EmailField


class DataPicker(FlaskForm):
    query = SelectField('state', choices=["bitcoin", "ethereum", "dogecoin", "litecoin", "tether coin",
                                          "Binance coin", "nft"],  validators=[DataRequired()])
    date = DateField('Connection Start Date', format='%Y-%m-%d', validators=[DataRequired()], )

    submit = SubmitField('Submit')


class Update(FlaskForm):
    submit = SubmitField('Update Articles')

