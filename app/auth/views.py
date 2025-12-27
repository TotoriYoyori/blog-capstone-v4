from flask import render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from . import auth
from .. import ext
from .forms import RegisterForm, LoginForm
from ..models import User


# --------------- Authentication Route
@auth.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm(email=session.get("current_email"))
    if form.validate_on_submit():
        user = ext.get_by_email(form.email.data)
        session["current_email"] = form.email.data
        if user:
            flash("An account associated with this email already exists, please log in instead!", "warning")
            return redirect(url_for("auth.register"))

        new_user = User(
            email= form.email.data,
            password= generate_password_hash(password= form.password.data, method= "pbkdf2", salt_length= 8),
            name=form.name.data,
        )
        ext.create_user(new_user)
        login_user(new_user)
        session["current_email"] = None

        return redirect(url_for("main.home"))

    return render_template("register.html", form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm(email= session.get("current_email"))
    if form.validate_on_submit():
        user = ext.get_by_email(form.email.data)
        session["current_email"] = form.email.data
        if not user:
            flash("Email not found. Please double check and try again.", "warning")
            return redirect(url_for("auth.login"))

        if not check_password_hash(user.password, form.password.data):
            flash("Incorrect password. Please double check and try again.", "danger")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("main.home"))

    return render_template("login.html", form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))