import click
from getpass import getpass

from flask import current_app as app
from flask_security.utils import hash_password

from . import database
from .models import (
    User, Role, RoleNames
)


@app.cli.command('createsuperuser')
@click.argument('email')
def create_user(email: str):
    """
        Create superuser
        :param email:
    """

    if User.query.filter_by(email=email).first():
        return print('User with you specified email already exists')

    password = getpass('Enter password: ')
    re_password = getpass('re-Enter password: ')
    if password != re_password:
        return print('Passwords does not match')

    role = Role.query.filter_by(name=RoleNames.SUPERUSER).first()
    user = database.add_instance(
        User,
        email=email,
        password=hash_password(password),
        active=True,
        roles=[role]
    )
    print(f'User {user.email} was created')
