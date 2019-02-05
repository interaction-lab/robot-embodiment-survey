from flask import Flask, render_template, send_from_directory
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

import config
from survey import Survey
from util import parse_robots_db


def recreate_schema(_db):
    import base
    base.Base.metadata.drop_all(_db.engine)
    base.Base.metadata.create_all(_db.engine)


def create_app():
    _app = Flask(__name__, static_url_path='')
    Bootstrap(_app)
    _app.config.from_object('config.Config')
    _db = SQLAlchemy(_app)
    # recreate_schema(_db)
    return _app, _db


app, db = create_app()
c = config.Config


@app.route('/robots/<path:path>')
def send_robots(path):
    return send_from_directory('robots', path)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/bower/<path:path>')
def bower(path):
    return send_from_directory('bower_components', path)


@app.route('/parse_robots')
def parse_robots():
    return parse_robots_db(db)


@app.route('/survey')
def survey():
    # TODO(Vadim) use turkSubmitTo instead of submission_url
    return render_template('survey.html', survey=Survey(db), submission_url=c.SANDBOX_MTURK if c.DEBUG else c.MTURK)


if __name__ == '__main__':
    app.run()
