import json

from flask_bcrypt import check_password_hash
from flask import jsonify, Blueprint, abort, make_response
from flask_restful import (Resource, Api, reqparse, inputs, fields, marshal, marshal_with, url_for)
from flask_login import login_user, logout_user, login_required, current_user

import models

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'password': fields.String,
}



class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=True,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()

    # @login_required # from flask_login modules
    def get(self):
        all_users = [marshal(user, user_fields) for user in models.User.select()]
        return all_users

    def post(self):
        args = self.reqparse.parse_args()
        if args['password'] == args['verify_password']:
            print(args, ' this is args')
            user = models.User.create_user(**args)
            login_user(user)
            return marshal(user, user_fields), 201

        return make_response(
            json.dumps({
                'error': 'Password and password verification do not match'
            }), 400)

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'verify_password',
            required=False,
            help='No password verification provided',
            location=['form', 'json']
        )
        super().__init__()


    @marshal_with(user_fields)
    def get(self, id):
        try:
            user = models.User.get(models.User.id==id)
        except models.User.DoesNotExist:
            abort(404)
        else:
            return (user, 200)

    @marshal_with(user_fields)
    def put(self, id):
        try:
            args = self.reqparse.parse_args()
            new_args = {key: value for key, value in args.items() if value is not None}
            query = models.User.update(**new_args).where(models.User.id==id)
            query.execute()
        except models.User.DoesNotExist:
            abort(404)
        else:
            return (models.User.get(models.User.id==id), 200)

    
    def delete(self, id):
        query = models.User.delete().where(models.User.id==id)
        query.execute()
        return {'message': 'user deleted'}


class Login(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'email',
            required=True,
            help='No email provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        super().__init__()
    def post(self):
        try:
            args = self.reqparse.parse_args()
            user = models.User.get(models.User.email==args['email'])
            login_user(user)
            if(user.email):
                if(check_password_hash(user.password, args['password'])):
                    return make_response(
                        json.dumps({
                            'user': marshal(user, user_fields),
                            'message': 'success', 
                        }), 200)
                else:
                    return make_response(
                        json.dumps({
                            'message': 'Incorrect password'
                        }), 200)
        except models.User.DoesNotExist:
            return make_response(
                json.dumps({
                    'message': 'Email does not exist'
                }), 200)


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/register',
    # endpoint='users'
)
api.add_resource(
    User,
    '/<int:id>',
    # endpoint='user'
)
api.add_resource(
    Login,
    '/login',
)