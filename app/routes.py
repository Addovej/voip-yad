from flask import current_app as app
from flask import request
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended.utils import (
    create_access_token,
    get_jwt_identity
)
from flask_restful import Api
from flasgger import SwaggerView

from app.database import (add_instance, edit_instance)
from app.models import User
from app.schemes import (
    UserSchema,
    CreateUserSchema,
    UpdateUserSchema,
    LoginUserSchema
)
from app.utils import response, YandexDisc

api = Api(app)


class BaseView(SwaggerView):
    """
        Base Resource class.
        Handle getting request data here.
    """

    default_schema = None
    schemes_map = {}

    def get_schema(self, action=None):
        if not action:
            return self.default_schema
        return self.schemes_map.get(action, None)

    def get_data(self, action=None):
        schema = self.get_schema(action)
        if not schema:
            raise NotImplementedError('Default schema not specified')
        request_data = request.get_json()
        errors = schema.validate(request_data)
        if errors:
            return None, errors
        return schema.load(request_data), None


@api.resource('/')
class MainView(BaseView):
    responses = {
        200: {
            'description': 'Working message',
            'examples': {'response': {'message': 'Service is works'}}
        }
    }

    def get(self):
        """
            Check service
            Returning a success message.
        """

        return response('Service is works', 200)


@api.resource('/register')
class UserRegistrationView(BaseView):
    default_schema = CreateUserSchema()
    schemes_map = {
        'res': UserSchema()
    }

    parameters = [{
        'in': 'body',
        'schema': CreateUserSchema,
    }]
    responses = {
        201: {
            'description': 'Success user registration message',
            'schema': UserSchema
        },
        400: {
            'description': 'Validation error',
            'examples': {'message': 'This email already taken'}
        }
    }

    def post(self):
        """
            User registration
        """

        data, errors = self.get_data()
        if errors:
            return response(errors, 400)

        user = User.get_by_email(data.get('email'))
        if user:
            return response('This email already taken', 400)

        data.update({'password': User.generate_hash(data['password'])})
        user = add_instance(
            User,
            **dict(active=True, **data)
        )

        schema = self.get_schema('res')
        result = schema.dump(user)
        result.update(dict(
            access_token=create_access_token(identity=data['email'])
        ))

        return response(result, 200)


@api.resource('/login')
class UserLoginView(BaseView):
    default_schema = LoginUserSchema()

    parameters = [{
        'in': 'body',
        'schema': LoginUserSchema,
    }]
    responses = {
        200: {
            'description': 'Success user login',
            'examples': {'access_token': 'secret'}
        },
        400: {
            'description': 'Validation error',
            'examples': {'message': 'User does not exists'}
        },
        401: {
            'description': 'Unauthorized',
            'examples': {'message': 'Wrong credentials'}
        }
    }

    def post(self):
        """
            User login
        """

        data, errors = self.get_data()
        if errors:
            return response(errors, 400)

        user = User.get_by_email(data.get('email'))
        if not user:
            return response(f"User {data.get('email')} does not exist", 400)

        if User.verify_hash(data['password'], user.password):
            return response(dict(
                access_token=create_access_token(identity=data['email'])
            ), 200)
        else:
            return response('Wrong credentials', 401)


@api.resource('/user')
class UserView(BaseView):
    default_schema = UserSchema()
    schemes_map = {
        'put': UpdateUserSchema()
    }

    definitions = {
        'UpdateUserSchema': UpdateUserSchema
    }
    responses = {
        200: {
            'description': 'User information',
            'schema': UserSchema
        },
        400: {
            'description': 'Validation error',
            'examples': {'message': 'This email already taken'}
        },
        401: {
            'description': 'Unauthorized',
            'examples': {'message': 'Wrong credentials'}
        }
    }

    @jwt_required
    def get(self):
        """
            Get user's data
            ---
            security:
              - Bearer: []
        """

        user = User.get_by_email(get_jwt_identity())
        return response(self.default_schema.dump(user), 200)

    @jwt_required
    def put(self):
        """
            Update user's data
            ---
            security:
              - Bearer: []
            parameters:
              - in: body
                schema:
                  $ref: '#/definitions/UpdateUserSchema'
        """

        data, errors = self.get_data('put')
        if errors:
            return response(errors, 400)

        user = User.get_by_email(get_jwt_identity())
        user = edit_instance(User, user.id, **data)
        schema = self.get_schema()
        return response(schema.dump(user), 200)


@api.resource('/calls')
class CallsView(BaseView):
    default_schema = None

    responses = {
        200: {
            'description': 'Calls list'
        },
        400: {
            'description': 'Yandex.Disk error',
            'examples': {'message': 'Token specified you not valid'}
        },
        401: {
            'description': 'Unauthorized',
            'examples': {'message': 'Wrong credentials'}
        }
    }

    @jwt_required
    def get(self):
        """
            Get calls
            ---
            security:
              - Bearer: []
        """

        user = User.get_by_email(get_jwt_identity())

        if not user.ya_disc_token:
            return response(
                'Please specify Yandex.Disk token in your profile', 400
            )

        yad = YandexDisc(user.ya_disc_token)
        if not yad.check_token():
            return response(
                'Token specified you not valid', 400
            )

        calls = yad.get_calls()

        return response(calls, 200)
