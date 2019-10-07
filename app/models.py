from enum import Enum

from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password, verify_password

from app import db


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id'))
)


class RoleNames(Enum):
    SUPERUSER = 'superuser'
    USER = 'user'


class BaseModel(db.Model):
    """
    Base database model.
    Defined id and timestamp (created, modified and deleted) fields.
    """

    __abstract__ = True

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    created = db.Column(
        db.DateTime,
        index=True,
        default=db.func.now()
    )
    modified = db.Column(
        db.DateTime,
        index=True,
        default=db.func.now(),
        onupdate=db.func.now()
    )
    deleted = db.Column(
        db.DateTime,
        index=True,
        nullable=True
    )

    def __commit_insert__(self):
        return

    def __commit_update__(self):
        return

    def __commit_delete__(self):
        return


class Role(BaseModel, RoleMixin):
    """
    Role database model.
    """

    __tablename__ = 'roles'

    name = db.Column(
        db.Enum(RoleNames),
        unique=True
    )
    description = db.Column(
        db.String(255)
    )

    def __str__(self):
        return self.name.name


class User(BaseModel, UserMixin):
    """
    User database model.
    """

    __tablename__ = 'users'

    first_name = db.Column(
        db.String(64)
    )
    last_name = db.Column(
        db.String(64)
    )
    email = db.Column(
        db.String(64),
        unique=True
    )
    ya_disc_token = db.Column(
        db.String(64)
    )
    password = db.Column(
        db.String(255)
    )
    active = db.Column(
        db.Boolean(),
    )
    confirmed_at = db.Column(
        db.DateTime()
    )
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __str__(self):
        return self.email

    @staticmethod
    def generate_hash(password):
        return hash_password(password)

    @staticmethod
    def verify_hash(password, _hash):
        return verify_password(password, _hash)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
