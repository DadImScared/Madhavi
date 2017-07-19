
from flask import jsonify, Blueprint, abort, make_response, g, url_for, current_app
from flask_restful import (Resource, Api, reqparse, inputs)
from flask_mail import Message
from send_email.email import send_mail
import config


class MailService(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'name',
            type=str,
            required=True,
            help="Name required"
        )
        self.reqparse.add_argument(
            'email',
            type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"),
            required=True,
            help="email required"
        )
        self.reqparse.add_argument(
            'message',
            type=str,
            required=True,
            help="Message required"
        )
        super().__init__()

    def post(self):
        args = self.reqparse.parse_args()
        send_mail(
            "New message from relaxgville",
            recipients=[config.RECEIVER],
            text_body="Name: {} \n"
                      "Email: {} \n"
                      "Message: \n {}".format(args["name"],
                                              args["email"],
                                              args["message"])
        )
        return make_response(jsonify({"message": "Message sent!"}), 200)


services_api = Blueprint('resources.services', __name__)
api = Api(services_api)
api.add_resource(
    MailService,
    '/mail',
    endpoint='mail'
)
