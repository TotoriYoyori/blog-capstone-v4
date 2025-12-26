from flask_login import current_user
from typing import Iterable
from app import db
from .models import User, BlogPost, Comment


def get_by_email(email: str) -> bool:
    stmt = (
        db.select(User)
        .where(User.email == email)
    )
    return db.session.execute(stmt).scalar()


def create_user(user: User) -> None:
    if not user:
        return
    db.session.add(user)
    db.session.commit()


def fetch_all_users() -> Iterable[User]:
    stmt = db.select(User)
    return db.session.execute(stmt).scalars()


def create_post(post: BlogPost) -> None:
    if not post:
        return
    db.session.add(post)
    db.session.commit()


def fetch_all_posts() -> Iterable[BlogPost]:
    stmt = db.select(BlogPost)
    return db.session.execute(stmt).scalars()


def create_comment(comment: Comment) -> None:
    if not comment:
        return
    db.session.add(comment)
    db.session.commit()


def fetch_all_post_comments(post_id: int) -> Iterable[Comment]:
    stmt = (
        db.select(Comment)
        .where(Comment.post_id == post_id)
        .order_by(Comment.id.desc())
    )
    return db.session.execute(stmt).scalars()


def parse_user_update(form_data: dict) -> dict:
    result = {}
    for attr, value in form_data.items():
        pass_rules = [
            lambda: not value,
            lambda: attr in ["submit", "csrf_token"],
            lambda: value == getattr(current_user, attr)
        ]
        if any(rule() for rule in pass_rules):
            continue

        result.update({attr: value})

    return result


def update_user(user: User, info: dict) -> None:
    for attr in info:
        setattr(user, attr, info.get(attr))
        print(f"{attr}: {getattr(user, attr)} >> {info.get(attr)}")

    db.session.commit()


def patch_user_password(user: User, new_password: str) -> None:
    user.password = new_password
    db.session.commit()
