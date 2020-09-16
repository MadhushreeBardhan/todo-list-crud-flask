from config import db


class Todo(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(200))
    status = db.Column(db.Boolean)

    def __repr__(self):
        return self.title


db.create_all()
