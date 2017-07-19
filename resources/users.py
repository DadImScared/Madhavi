import json

from flask import jsonify, Blueprint, abort, make_response, g

from flask_restful import (Resource, Api, reqparse,
                               inputs, fields, marshal,
                               marshal_with, url_for)
from auth import auth
import models

user_fields = {
    'username': fields.String,
}


def user_or_404(username):
    user = models.User.get_user(username)
    return user if user else abort(404)

class UserList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        super().__init__()

    def post(self):
        self.reqparse.add_argument(
            'username',
            required=True,
            help='No username provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )

        args = self.reqparse.parse_args()
        user = user_or_404(args["username"])
        if user.verify_password(args["password"]):
            token = user.generate_auth_token()
            return jsonify({'token': token.decode('ascii')})
        return make_response(
            json.dumps({
                'error': "Username or password doesn't match"
            }), 401)

    @auth.login_required
    def patch(self):
        self.reqparse.add_argument(
            'current_password',
            required=True,
            help='current password required',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'new_password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'confirm_new_password',
            required=True,
            help='No password provided',
            location=['form', 'json']
        )
        args = self.reqparse.parse_args()
        if args['new_password'] != args['confirm_new_password'] or not g.user.verify_password(args["current_password"]):
            return make_response(
                jsonify({"message": "passwords must match"}),
                401
            )
        g.user.update_password(args["new_password"])
        return make_response(
            jsonify(
                {
                    "message": "Info updated!",
                    "token": g.user.generate_auth_token().decode('ascii')
                }
            ),
            200
        )


users_api = Blueprint('resources.users', __name__)
api = Api(users_api)
api.add_resource(
    UserList,
    '/users',
    endpoint='users'
)