from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, Email, Length

# --------------- Register
class RegisterForm(FlaskForm):
    email = EmailField(label="Email", validators=[Email(), DataRequired(), Length(min=6)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=12)])
    name = StringField(label="Name", validators=[DataRequired()])
    submit = SubmitField(label="Register New User")

# --------------- Login
class LoginForm(FlaskForm):
    email = EmailField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="Log In")
