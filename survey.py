import typing

from flask import request
from flask_sqlalchemy import SQLAlchemy

from schema import Robot, Assignment


class AMTParams(object):
    def __init__(self):
        self.assignment_id = request.args.get('assignmentId', None)  # type: str
        self.hit_id = request.args.get('hitId', None)  # type: str
        self.turk_submit_to = request.args.get('turkSubmitTo', None)  # type: str
        self.worker_id = request.args.get('workerId', None)  # type: str
        self.preview = self.assignment_id == 'ASSIGNMENT_ID_NOT_AVAILABLE'


# assignmentId, hitId, turkSubmitTo, and workerId
# preview -  assignmentId: ASSIGNMENT_ID_NOT_AVAILABLE
# POST results back to https://www.mturk.com/mturk/externalSubmit
# (https://workersandbox.mturk.com/mturk/externalSubmit) (also record locally??)

class Survey(object):
    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.amt_params = AMTParams()
        self.robots = []  # type: typing.List[Robot]

        if not self.amt_params.preview:
            self.lookup_assignment()

    def create_assignment(self):
        a = Assignment()
        a.id = self.amt_params.assignment_id
        a.robots = []  # TODO(Vadim) fill with random robots based on what need annotation
        self.db.session.add(a)

    def lookup_assignment(self):
        assignment = self.db.session.query(Assignment) \
            .filter(Assignment.id == self.amt_params.assignment_id) \
            .first()
        if assignment is None:
            self.create_assignment()
