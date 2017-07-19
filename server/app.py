from flask import Flask, current_app, render_template, g, jsonify
from auth import auth
import os
from server.extensions import mail
from server.blueprints import register_blueprints
from server.settings import BaseConfig

server_dir = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__, static_folder='{}{}static'.format(server_dir, os.path.sep))


@app.errorhandler(404)
def page_not_found(e):
    return app.send_static_file('index.html')


@app.route('/')
@app.route('/<resource>')
def hello_world(resource=None):
    if os.path.isfile('{0}{1}static{1}{2}'.format(server_dir, os.path.sep, resource)):
        return app.send_static_file('{}'.format(resource))
    return app.send_static_file('index.html')


@app.route('/api/v1/users/token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii')})

register_blueprints(app)


def create_app(config=BaseConfig):
    app.config.from_object(config)
    register_extensions()
    return app


def register_extensions():
    mail.init_app(app)
