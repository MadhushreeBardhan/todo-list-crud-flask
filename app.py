#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, abort, request
from flask import make_response
from flask_httpauth import HTTPBasicAuth
import json
from flask_restful import Resource, Api
from config import db, app
from models import Todo
from serialize import todo_list_schema, todo_list_schemas

api = Api(app)

from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'user':
        return 'password'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

class TodoLists(Resource):

    decorators = [auth.login_required]

    def get(self):
        todo_lists = Todo.query.all()

        # res = []
        # for todo_list in todo_lists:
        #     data = {}
        #     data['id'] = todo_list.id
        #     data['title'] = todo_list.title
        #     data['descritption'] = todo_list.description
        #     data['sttaus'] = todo_list.status
        #     res.append(data)

        res = todo_list_schemas.dump(todo_lists)  # serialized data
        return make_response({'result': res}, 200)

    def post(self):
        payload = request.get_json()
        new_task = Todo(title=payload['title'],
                        description=payload['description'],
                        status=payload['status'])
        db.session.add(new_task)
        db.session.commit()

        return make_response({'result': 'Added todo list'}, 201)


class TodoList(Resource):
    decorators = [auth.login_required]

    def get(self, id):
        if id:
            data = Todo.query.filter_by(id=id).first()
            if data:

                # user_data = {}
                # user_data['id'] = data.id
                # user_data['title'] = data.title
                # user_data['description'] = data.description
                # user_data['status'] = data.status

                res = todo_list_schema.dump(data)  # serialized data
                return make_response(jsonify({'result': res}), 200)
            else:
                return make_response(jsonify({'result': 'not found'}),
                        404)
        else:
            return make_response(jsonify({'result': 'provide valid id'
                                 }), 500)

    def put(self, id):
        payload = request.get_json()
        data = Todo.query.filter_by(id=id).first()
        if data.id == id:
            data.title = payload['title']
            data.description = payload['description']
            data.status = payload['status']
            db.session.commit()
        else:
            return make_response(jsonify({'result': 'something went wrong'
                                 }), 500)
        return make_response(jsonify({'result': 'updated'}), 202)

    def delete(self, id):
        if not id:
            return make_response({'result': 'provide valid id'})

        data = Todo.query.filter_by(id=id).first()
        if data:
            data.delete()
            db.session.commit()
        else:
            return make_response({'result': 'not dound'}, 302)
        return make_response({'result': 'deleted'}, 202)


api.add_resource(TodoLists, '/todo/api/v1.0/tasks')
api.add_resource(TodoList, '/todo/api/v1.0/tasks/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
