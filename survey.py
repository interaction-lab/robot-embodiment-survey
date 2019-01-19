import typing
from threading import Lock

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from schema import Robot, Assignment

robot_lock = Lock()


class AMTParams(object):
    def __init__(self):
        self.assignment_id = request.args.get('assignmentId', None)  # type: str
        self.hit_id = request.args.get('hitId', None)  # type: str
        self.turk_submit_to = request.args.get('turkSubmitTo', None)  # type: str
        self.worker_id = request.args.get('workerId', None)  # type: str
        self.preview = self.assignment_id == 'ASSIGNMENT_ID_NOT_AVAILABLE'

    def __repr__(self):
        if self.preview:
            return "AMT PREVIEW"
        return "AMTRequest({}, {}, {}, {})".format(self.assignment_id, self.hit_id,
                                                   self.turk_submit_to, self.worker_id)


# assignmentId, hitId, turkSubmitTo, and workerId
# preview -  assignmentId: ASSIGNMENT_ID_NOT_AVAILABLE
# POST results back to https://www.mturk.com/mturk/externalSubmit
# (https://workersandbox.mturk.com/mturk/externalSubmit) (also record locally??)

class Survey(object):
    ROBOTS_PER_HIT = 30
    PREVIEW_ROBOTS = ['Ava', 'Bandit', 'RoboBee']

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.amt_params = AMTParams()
        self.robots = []  # type: typing.List[Robot]

        if self.amt_params.assignment_id is None or self.amt_params.preview:
            self.robots = map(self.get_robot_by_name, Survey.PREVIEW_ROBOTS)
        else:
            self.robots = self.lookup_assignment()

    def __repr__(self):
        return "Survey: Robots ({}) Params ({})".format(self.robots, repr(self.amt_params))

    def get_robots(self):
        # TODO(Vadim) do weighted probability that decreases when robot has more annotations

        """fill with robots based on least annotated robots"""
        c_col = func.count("robot_assignment_associations.robot_id").label('assignment_count')
        query = self.db.session.query("robot_assignment_associations.robot_id", c_col) \
            .group_by("robot_assignment_associations.robot_id") \
            .order_by(c_col.asc())
        # TODO(Vadim) improve via sql query?
        # c_col = func.count(Assignment.id).label('assignment_count')
        # query = self.db.session.query(Robot.name, c_col) \
        #     .outerjoin(Assignment.robots) \
        #     .group_by(Robot.name) \
        #     .order_by(c_col.asc())
        print(query)
        counts = query.all()
        print(counts)

        robots = []
        for robot_name, low_count in counts:
            robots.append(robot_name)
            if len(robots) >= Survey.ROBOTS_PER_HIT:
                break
        return robots

    def get_robot_by_name(self, name):
        return self.db.session.query(Robot).filter(Robot.name == name).one()

    def create_assignment(self):
        a = Assignment()
        a.id = self.amt_params.assignment_id
        a.hit_id = self.amt_params.hit_id
        a.worker_id = self.amt_params.worker_id
        with robot_lock:
            a.robots = self.get_robots()
            self.db.session.add(a)
        return a

    def lookup_assignment(self):
        assignment = self.db.session.query(Assignment) \
            .filter(Assignment.id == self.amt_params.assignment_id) \
            .first()
        if assignment is None:
            assignment = self.create_assignment()
        return assignment.robots
