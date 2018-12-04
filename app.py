from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from util import parse_robots_db


def create_app():
    _app = Flask(__name__)
    Bootstrap(_app)
    _app.config.from_object('config.Config')
    _db = SQLAlchemy(_app)
    # import base
    # base.Base.metadata.drop_all(_db.engine)
    # base.Base.metadata.create_all(_db.engine)
    return _app, _db


app, db = create_app()


@app.route('/parse_robots')
def parse_robots():
    return parse_robots_db(db)


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()

# assignmentId, hitId, turkSubmitTo, and workerId
# preview -  assignmentId: ASSIGNMENT_ID_NOT_AVAILABLE
# POST results back to https://www.mturk.com/mturk/externalSubmit
# (https://workersandbox.mturk.com/mturk/externalSubmit) (also record locally??)
