from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=0, nullable=False)

    def __repr__(self):
        return f'<Task {self.id}>'