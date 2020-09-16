from config import app
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class TodoListSechema(ma.Schema):

    class Meta:

        fields = ('id', 'title', 'description', 'status')


todo_list_schema = TodoListSechema()
todo_list_schemas = TodoListSechema(many=True)
