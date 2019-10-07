import click
from getpass import getpass

from flask import current_app as app

from . import database
from .models import (
    User, Role, RoleNames
)


@app.cli.command('create-superuser')
@click.argument('email')
def create_user(email: str):
    """
        Create superuser
        :param email:
    """

    if User.get_by_email(email):
        return print('User with you specified email already exists')

    password = getpass('Enter password: ')
    re_password = getpass('re-Enter password: ')
    if password != re_password:
        return print('Passwords does not match')

    role = Role.query.filter_by(name=RoleNames.SUPERUSER).first()
    user = database.add_instance(
        User,
        email=email,
        password=User.generate_hash(password),
        active=True,
        roles=[role]
    )
    print(f'User {user.email} was created')


@app.cli.command('change-password')
@click.argument('email')
def change_password(email: str):
    """
        Change user's password
        :param email:
    """

    user = User.get_by_email(email)
    if not user:
        return print(f"User {email} doesn't exist")

    password = getpass('Enter password: ')
    re_password = getpass('re-Enter password: ')
    if password != re_password:
        return print('Passwords does not match')

    database.edit_instance(
        User,
        user.id,
        password=User.generate_hash(password)
    )
    print(f'Password for {user.email} was changed')
