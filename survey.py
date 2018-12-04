import typing
from threading import Lock

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from schema import Robot, Assignment, RobotAssignment

robot_lock = Lock()


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
    ROBOTS_PER_HIT = 30

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.amt_params = AMTParams()
        self.robots = []  # type: typing.List[Robot]

        if not self.amt_params.preview:
            self.lookup_assignment()

    def get_robots(self):
        """fill with random robots based on least annotated robot"""
        c_col = func.count(RobotAssignment.robot_id).label('assignment_count')
        counts = self.db.session.query(RobotAssignment.robot_id,
                                       func.count(RobotAssignment.robot_id).label('assignment_count')) \
            .group_by(RobotAssignment.robot_id) \
            .order_by(c_col.asc()) \
            .count()
        robots = []
        for robot_name, low_count in counts:
            robots.append(robot_name)
            if len(robots) >= Survey.ROBOTS_PER_HIT:
                break
        return robots

    def create_assignment(self):
        a = Assignment()
        a.id = self.amt_params.assignment_id
        with robot_lock:
            a.robots = self.get_robots()
            self.db.session.add(a)

    def lookup_assignment(self):
        assignment = self.db.session.query(Assignment) \
            .filter(Assignment.id == self.amt_params.assignment_id) \
            .first()
        if assignment is None:
            self.create_assignment()
