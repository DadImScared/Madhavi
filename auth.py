
from flask import g, abort

from flask_httpauth import HTTPBasicAuth

import models

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = models.User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = models.User.get_user(username_or_token)
        if not user or not user.verify_password(password):
            return abort(401)
    g.user = user
    return True
