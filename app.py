from flask import Flask, request, render_template, render_template_string
from models import db, Todo
from flask_migrate import Migrate
from ai import make_request


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    db.session.add(Todo(
        content=request.form['input'],
    ))
    db.session.commit()
    return render_template('list.html', items=Todo.query.all())


@app.route('/delete/<item_id>', methods=['DELETE'])
def delete(item_id):
    db.session.delete(Todo.query.get(item_id))
    db.session.commit()
    return render_template('list.html', items=Todo.query.all())


@app.route('/check/<item_id>', methods=['PUT'])
def check(item_id):
    item = Todo.query.get(item_id)
    item.completed = not item.completed
    db.session.commit()
    return render_template('list.html', items=Todo.query.all())


@app.route('/other', methods=['GET'])
def other():
    return render_template('list.html', items=Todo.query.all())


@app.route('/request_chat', methods=['POST'])
def request_chat():
    make_request(request.form['input'])
    return render_template('list.html', items=Todo.query.all())


if __name__ == '__main__':
    app.run(debug=True)
