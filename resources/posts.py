
from flask import Blueprint, abort, jsonify, g

from flask_restful import (Resource, Api, reqparse,
                           inputs, fields, marshal,
                           marshal_with, url_for)
from auth import auth
import models

post_fields = {
    'content': fields.String,
    'page_name': fields.String,
    'page_display': fields.String,
    'page_order': fields.Integer
}


def post_or_404(post_name):
    try:
        post = models.Post.get(models.Post.page_name==post_name)
    except models.DoesNotExist:
        abort(404)
    else:
        return post


class PostList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
            required=True,
            help='No content provded',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'page_name',
            required=True,
            help='No page name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'page_display',
            required=True,
            help='No page display provded',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'page_order',
            required=True,
            help='No page order provided',
            location=['form', 'json']
        )
        super().__init__()

    def get(self):
        return {'pages': [
            marshal(page, post_fields)
            for page in models.Post.select()
        ]}

    @marshal_with(post_fields)
    @auth.login_required
    def post(self):
        args = self.reqparse.parse_args()
        new_post = models.Post.create_post(g.user, **args)
        return new_post, 200


class Post(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'content',
            help='No content provded',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'page_name',
            help='No page name provided',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'page_display',
            help='No page display provded',
            location=['form', 'json']
        )
        self.reqparse.add_argument(
            'page_order',
            help='No page order provided',
            location=['form', 'json']
        )
        super().__init__()

    @marshal_with(post_fields)
    def get(self, pagename):
        page = post_or_404(pagename)
        return page, 200,

    @marshal_with(post_fields)
    @auth.login_required
    def patch(self, pagename):
        args = self.reqparse.parse_args()
        new_post = models.Post.get_post(pagename)
        query = models.Post.update( **{x: args[x] for x in args if args[x]}).where(
            (models.Post.page_name==pagename) &
            (models.Post.user==g.user)
        )
        query.execute()
        return new_post, 200

    @auth.login_required
    def delete(self, pagename):
        try:
            new_post = models.Post.get(
                (models.Post.user==g.user) &
                (models.Post.page_name==pagename)
            )
        except models.DoesNotExist:
            # make response
            pass
        else:
            query = new_post.delete_instance()
            query.execute()
            return '', 204, {'Location': url_for('resources.posts.posts')}


post_api = Blueprint('resources.posts', __name__)
api = Api(post_api)
api.add_resource(
    PostList,
    '/posts',
    endpoint='posts'
)
api.add_resource(
    Post,
    '/posts/<pagename>',
    endpoint='post'
)
