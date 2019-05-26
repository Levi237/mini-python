from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    # 'location': fields.String,
    # 'entry': fields.String,
    # 'imageUrl': fields.String,
    # 'userId': fields.Integer,
}

class PostList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )
        # self.reqparse.add_argument(
        #     'location',
        #     required=False,
        #     help='No location provided',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'entry',
        #     required=False,
        #     help='No entry provided',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'imageUrl',
        #     required=False,
        #     help='No image url provided',
        #     location=['form', 'json']
        # )      
        # self.reqparse.add_argument(
        #     'userId',
        #     required=False,
        #     help='No userId provided',
        #     location=['form', 'json']
        # )     
        super().__init__()

    
    def get(self):
        new_posts = [marshal(post, post_fields)
                    for post in models.Post.select()]
        return new_posts

    @marshal_with(post_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, 'args hitting')
        post = models.Post.create(**args)
        return (post, 201)

class Post(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'title',
            required=False,
            help='No title provided',
            location=['form', 'json']
        )
        # self.reqparse.add_argument(
        #     'location',
        #     required=False,
        #     help='No title provided',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'entry',
        #     required=False,
        #     help='No title provided',
        #     location=['form', 'json']
        # )
        # self.reqparse.add_argument(
        #     'imageUrl',
        #     required=False,
        #     help='No title provided',
        #     location=['form', 'json']
        # )       
        # self.reqparse.add_argument(
        #     'userId',
        #     required=False,
        #     help='No userId provided',
        #     location=['form', 'json']
        # )  
        super().__init__()

    @marshal_with(post_fields)
    def get(self, id):
        try:
            post = models.Post.get(models.Post.id==id)
        except models.Post.DoesNotExist:
            abort(404)
        else:
            return (post, 200)

    @marshal_with(post_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Post.update(**args).where(models.Post.id==id)
        query.execute()
        return (models.Post.get(models.Post.id==id), 200)
    def delete(self, id):
        query = models.Post.delete().where(models.Post.id==id)
        query.execute()
        
        return {'message': 'resource deleted'}


posts_api = Blueprint('resources.posts', __name__)
api = Api(posts_api)

api.add_resource(
    PostList,
    '/posts',
    # endpoint='posts'
)
api.add_resource(
    Post,
    '/posts/<int:id>',
    # endpoint='post'
)