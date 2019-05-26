from flask import jsonify, Blueprint, abort

from flask_restful import (Resource, Api, reqparse, fields, marshal,
                               marshal_with, url_for)

import models

blog_fields = {
    'id': fields.Integer,
    'title': fields.String
    # 'location': fields.String,
    # 'entry': fields.String,
    # 'imageUrl': fields.String,
    # 'userId': fields.Integer,
}

class BlogList(Resource):
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
        new_blogs = [marshal(blog, blog_fields)
                    for blog in models.Blog.select()]
        return new_blogs

    @marshal_with(blog_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, 'args hitting')
        blog = models.Blog.create(**args)
        return (blog, 201)

class Blog(Resource):

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

    @marshal_with(blog_fields)
    def get(self, id):
        try:
            blog = models.Blog.get(models.Blog.id==id)
        except models.Blog.DoesNotExist:
            abort(404)
        else:
            return (blog, 200)

    @marshal_with(blog_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Blog.update(**args).where(models.Blog.id==id)
        query.execute()
        return (models.Blog.get(models.Blog.id==id), 200)
    def delete(self, id):
        query = models.Blog.delete().where(models.Blog.id==id)
        query.execute()
        
        return {'message': 'resource deleted'}


blogs_api = Blueprint('resources.blogs', __name__)
api = Api(blogs_api)

api.add_resource(
    BlogList,
    '/blogs',
    # endpoint='blogs'
)
api.add_resource(
    Blog,
    '/blogs/<int:id>',
    # endpoint='blog'
)