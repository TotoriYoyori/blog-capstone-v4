import datetime as dt

from flask import render_template, redirect, url_for, flash, current_app
from flask_login import current_user
import bleach

from . import main
from .forms import CreatePostForm, CommentForm
from .. import ext
from ..models import BlogPost, Comment
from ..decorators import admin_required
from app import db

# --------------- Register this
@main.route('/')
def home():
    posts = ext.fetch_all_posts()
    return render_template("index.html", posts=posts)


@main.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    post_ = db.session.get(BlogPost, post_id)
    form = CommentForm()
    today = dt.datetime.now().date()
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("Go ahead and Login or Register to leave a comment!", "primary")
            return redirect(url_for("auth.login"))

        new_comment = Comment(
            text=bleach.clean(form.comment.data, tags=current_app.config["BLEACH_ALLOWED_TAGS"], strip=True),
            author=current_user,
            post= post_,
            create_time=dt.datetime.now(),
        )
        ext.create_comment(new_comment)
        return redirect(url_for("main.post", post_id=post_id))

    return render_template("post.html", form=form, post=post_, today=today)


@main.route("/new-post", methods=["GET", "POST"])
@admin_required
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )
        ext.create_post(new_post)
        return redirect(url_for("main.home"))

    return render_template("make-post.html", form=form)


@main.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("main.post", post_id=post.id))
    return render_template("main.make-post.html", form=edit_form, is_edit=True)


@main.route("/delete/<int:post_id>")
@admin_required
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('main.home'))


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/contact")
def contact():
    return render_template("contact.html")