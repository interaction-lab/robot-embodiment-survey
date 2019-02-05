import collections
import math
import random
import typing
from threading import Lock

from flask import request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from schema import Robot, Assignment, RobotAssignmentAssociation

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

class ParameterException(Exception):
    # TODO(Vadim)
    def __init__(self):
        super(ParameterException, self).__init__()
        print("AMT PARAMETER EXCEPTION")


class Survey(object):
    ROBOTS_PER_HIT = 30
    ROBOT_ANNOTATION_LIMIT = 30
    PREVIEW_ROBOTS = ['Ava', 'Bandit', 'RoboBee']

    def __init__(self, db: SQLAlchemy):
        self.db = db
        self.amt_params = AMTParams()
        self.robots = []  # type: typing.List[Robot]

        if self.amt_params.assignment_id is None or self.amt_params.preview:
            self.robots = map(self.get_robot_by_name, Survey.PREVIEW_ROBOTS)
        elif self.validate_params():
            self.robots = self.get_robots_from_assignment(self.lookup_assignment())

    def __repr__(self):
        return "Survey: Robots ({}) Params ({})".format(self.robots, repr(self.amt_params))

    def get_random_robots(self):
        """ do weighted probability that decreases when robot has more annotations """

        robots = collections.OrderedDict()

        c_col = func.count(RobotAssignmentAssociation.robot_id)
        for robot, num_assigned in self.db.session.query(Robot, c_col) \
                .outerjoin(RobotAssignmentAssociation, Robot.associations) \
                .group_by(Robot.name) \
                .order_by(c_col) \
                .all():

            if num_assigned >= Survey.ROBOT_ANNOTATION_LIMIT:
                continue

            if num_assigned not in robots:
                robots[num_assigned] = list()
            robots[num_assigned].append(robot)

        robot_names = set()
        while len(robot_names) < Survey.ROBOTS_PER_HIT:
            idx = math.floor(random.random() * Survey.ROBOT_ANNOTATION_LIMIT)
            for num_assigned, r_list in robots.items():
                # if idx is less than first thing in robots
                prob = Survey.ROBOT_ANNOTATION_LIMIT - num_assigned
                if idx < prob:
                    c = None
                    while c is None or c in robot_names:
                        c = random.choice(r_list)
                    robot_names.add(c)

        return robot_names

    def get_robot_by_name(self, name):
        return self.db.session.query(Robot).filter(Robot.name == name).one()

    def get_robots_from_assignment(self, assignment):
        return map(self.get_robot_by_name, map(lambda o: o.robot_id, assignment.associations))

    def create_assignment(self):
        a = Assignment()
        a.id = self.amt_params.assignment_id
        a.hit_id = self.amt_params.hit_id
        a.worker_id = self.amt_params.worker_id
        print("Creating Assignment")
        with robot_lock:
            robots = self.get_random_robots()
            for r in robots:
                association = RobotAssignmentAssociation()
                association.robot = r
                association.assignment = a
                # add robots and assignment via RobotAssociation
                self.db.session.add(association)
            self.db.session.commit()
            self.db.session.flush()
        return a

    def lookup_assignment(self):
        print("Finding Assignment")
        assignment = self.db.session.query(Assignment) \
            .filter(Assignment.id == self.amt_params.assignment_id) \
            .first()
        if assignment is None:
            assignment = self.create_assignment()
        return assignment

    def validate_params(self):
        # TODO(Vadim) optimize with loop over amt_param
        if self.amt_params.assignment_id is None or self.amt_params.hit_id is None or self.amt_params.worker_id is None:
            raise ParameterException()
        return True
