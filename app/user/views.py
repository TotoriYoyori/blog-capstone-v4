from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from . import user
from .. import ext
from .forms import EditUserForm, EditPasswordForm
from ..models import User


@user.route('/user/<int:user_id>', methods=["GET"])
def user_page(user_id):
    user_ = db.session.get(User, user_id)
    return render_template("user.html", user=user_)


@user.route('/user/edit/', methods=["GET", "POST"])
@login_required
def user_edit():
    name_form = EditUserForm(prefix="name")
    password_form = EditPasswordForm(prefix="password")
    if name_form.submit.data and name_form.validate():
        info_to_update = ext.parse_user_update(name_form.data)
        if not info_to_update:
            flash("No changes have been made", "info")
            return redirect(url_for("user.user_edit"))

        ext.update_user(current_user, info_to_update)
        flash("Your user information has been updated!", "success")
        return redirect(url_for("user.user_edit"))

    if password_form.submit.data and password_form.validate():
        if not check_password_hash(current_user.password, password_form.current_password.data):
            flash("Your input current password doesn't seem to be correct. Please double check "
                  "and try again!", "warning")
            return redirect(url_for("user.user_edit"))

        new_password = generate_password_hash(password_form.current_password.data, "pbkdf2", salt_length=8)
        ext.patch_user_password(current_user, new_password)
        flash("Your new password has been set!", "success")
        return redirect(url_for("user.user_edit"))

    return render_template("user-edit.html", name_form=name_form, password_form=password_form)
