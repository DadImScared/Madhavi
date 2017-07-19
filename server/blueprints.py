from resources.posts import post_api
from resources.services import services_api
from resources.users import users_api


def register_blueprints(app):
    app.register_blueprint(post_api, url_prefix='/api/v1')
    app.register_blueprint(users_api, url_prefix='/api/v1')
    app.register_blueprint(services_api, url_prefix='/api/v1/services')
