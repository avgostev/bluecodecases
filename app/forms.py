from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, SubmitField, DateField, PasswordField, SelectField, DecimalField
from wtforms.validators import DataRequired, EqualTo, Optional
from datetime import datetime

class LoginForm(FlaskForm):
    username = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    remember = BooleanField("Запомнить")
    submit = SubmitField("Войти")

class RegisterForm(FlaskForm):
    username = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    password2 = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo("password", "Пароли не совпадают!")])
    name = StringField("Имя", validators=[DataRequired()])
    submit = SubmitField("Зарегистрировать")

class SLRCaseForm(FlaskForm):
    d_slr = DateField("Дата СЛР", validators=[DataRequired()], default=datetime.now().date())
    sex = SelectField("Пол пациента", coerce=int)
    result = SelectField("Исход", coerce=int)
    place = SelectField("Место проведения СЛР", coerce=int)
    locate = SelectField("Локация СЛР относительно 59 меридиана (от Уральских гор)", coerce=int)
    d_bdate = DateField("Дата рождения пациента", validators=[Optional()])
    submit = SubmitField("Сохранить")