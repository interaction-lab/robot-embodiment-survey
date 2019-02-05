from typing import List

from sqlalchemy import Column, String, ForeignKey, BigInteger, SmallInteger
from sqlalchemy.orm import relationship

from base import Base


# robot_assignment_associations = Table('robot_assignment', Base.metadata,
#                                       Column('robot_id', String, ForeignKey('robot.name')),
#                                       Column('assignment_id', String, ForeignKey('assignment.id')),
#                                       extend_existing=True)


class RobotAssignmentAssociation(Base):
    __tablename__ = 'robot_assignment'
    __table_args__ = {'extend_existing': True}

    robot_id = Column(String, ForeignKey('robot.name'), primary_key=True)
    assignment_id = Column(String, ForeignKey('assignment.id'), primary_key=True)

    robot = relationship("Robot", back_populates="associations")
    assignment = relationship("Assignment", back_populates="associations")


class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(String, primary_key=True, nullable=False)
    hit_id = Column(String, nullable=False)
    worker_id = Column(String, nullable=False)
    associations = relationship("RobotAssignmentAssociation")  # type: List[RobotAssignmentAssociation]
    submissions = relationship("Submission")  # type: List[Submission]

    # TODO(Vadim) fix
    # robots = relationship("Robot", secondary="RobotAssignmentAssociation",
    #                       primaryjoin="Assignment.id==RobotAssignmentAssociation.robot_id",
    #                       secondaryjoin="Robot.name==RobotAssignmentAssociation.robot_id", )


class Robot(Base):
    __tablename__ = 'robot'

    name = Column(String, primary_key=True, nullable=False)
    short_name = Column(String, nullable=False)
    remote_url = Column(String, nullable=False)
    local_path = Column(String, nullable=False)
    associations = relationship("RobotAssignmentAssociation")
    submissions = relationship("Submission")  # type: List[Submission]

    # assignments = relationship("Assignment", secondary="RobotAssignmentAssociation", back_populates="robots")

    def __repr__(self):
        return "{} <{}, {}, {}>".format(self.name, self.short_name, self.remote_url, self.local_path)


class Submission(Base):
    __tablename__ = 'submission'

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)

    assignment_id = Column(String, ForeignKey('assignment.id', ondelete='CASCADE', onupdate='CASCADE'))
    robot_id = Column(String, ForeignKey('robot.name', ondelete='CASCADE', onupdate='CASCADE'))

    design_metaphor = Column(String)
    abstraction_slider = Column(SmallInteger)

    assignment = relationship("Assignment", back_populates="submissions")
    robot = relationship("Robot", back_populates="submissions")

    def __repr__(self):
        return "Submission <#{} - {}: ({}) / ({})>".format(self.assignment_id, self.robot_id,
                                                           self.design_metaphor, self.abstraction_slider)
