from flask import jsonify, Blueprint, abort, g

from flask_restful import (Resource, Api, reqparse, fields, marshal,marshal_with, url_for)
from flask_login import current_user

import models

comment_fields = {
    'id': fields.Integer,
    'comment': fields.String,
    'blog_id': fields.String,
    'created_by': fields.String,
}

class CommentList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'comment',
            required=False,
            help='No comment provided',
            location=['form', 'json']
        )  
        super().__init__()
    
    def get(self):
        new_comments = [marshal(comment, comment_fields)
            for comment in models.Comment.select()]
        return new_comments

    @marshal_with(comment_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args, 'args hitting')
        print(g.user._get_current_object().username, "<------- get current user")
        userId = g.user._get_current_object()
        print(userId, "<---------userId")
        comment = models.Comment.create(created_by=userId, **args)
        return (comment, 201)


class Comment(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            'comment',
            required=False,
            help='No comment provided',
            location=['form', 'json']
        )  
        super().__init__()

    @marshal_with(comment_fields)
    def get(self, id):
        try:
            comment = models.Comment.get(models.Comment.id==id)
        except models.Comment.DoesNotExist:
            abort(404)
        else:
            return (comment, 200)

    @marshal_with(comment_fields)
    def put(self, id):
        args = self.reqparse.parse_args()
        query = models.Comment.update(**args).where(models.Comment.id==id)
        query.execute()
        return (models.Comment.get(models.Comment.id==id), 200)
        
    def delete(self, id):
        query = models.Comment.delete().where(models.Comment.id==id)
        query.execute()
        return {'message': 'resource deleted'}


comments_api = Blueprint('resources.comments', __name__)
api = Api(comments_api)

api.add_resource(
    CommentList,
    '/comments',
    endpoint='comments'
)
api.add_resource(
    Comment,
    '/comments/<int:id>',
    endpoint='comment'
)
