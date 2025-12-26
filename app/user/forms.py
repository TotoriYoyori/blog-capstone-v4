from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.fields.simple import SubmitField, URLField
from wtforms.validators import Length, EqualTo, DataRequired, URL, Optional


class EditUserForm(FlaskForm):
    name = StringField(label= "Name", validators=[Optional(), Length(min=6)],
                       render_kw={"placeholder": "Enter your name"})
    email = EmailField(label= "Email", render_kw={"readonly": True})
    subtitle = StringField(label="Subtitle", validators=[Optional(), Length(min=10)],
                           render_kw={"placeholder": "Type something cool you want to share"})
    avatar = URLField(label="Avatar Image URL", validators=[Optional(), URL()])
    masthead = URLField(label="Masthead Image URL", validators=[Optional(), URL()])
    submit = SubmitField(label="Submit Change")


class EditPasswordForm(FlaskForm):
    current_password = PasswordField(label="Current Password", validators=[DataRequired()],
                                     render_kw={"placeholder": "Enter current password"})
    new_password = PasswordField(label="Set New Password", validators=[DataRequired(), Length(min=12)],
                                 render_kw={"placeholder": "Enter new password"})
    confirm_password = PasswordField(label="Confirm New Password",
                                     validators=[DataRequired(), Length(min=12), EqualTo("new_password")],
                                     render_kw={"placeholder": "Confirm new password"})
    submit = SubmitField(label="Submit Password Change")

