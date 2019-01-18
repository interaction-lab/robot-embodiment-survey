from sqlalchemy import Column, String, ForeignKey
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
    assignment = child = relationship("Assignment", back_populates="associations")


class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(String, primary_key=True, nullable=False)
    hit_id = Column(String, nullable=False)
    worker_id = Column(String, nullable=False)
    associations = relationship("RobotAssignmentAssociation")

    # TODO(Vadim) fix
    robots = relationship("Robot", secondary="RobotAssignmentAssociation",
                          primaryjoin="Assignment.id==RobotAssignmentAssociation.robot_id",
                          secondaryjoin="Robot.name==RobotAssignmentAssociation.robot_id", )


class Robot(Base):
    __tablename__ = 'robot'

    name = Column(String, primary_key=True, nullable=False)
    short_name = Column(String, nullable=False)
    remote_url = Column(String, nullable=False)
    local_path = Column(String, nullable=False)
    associations = relationship("RobotAssignmentAssociation")

    # assignments = relationship("Assignment", secondary="RobotAssignmentAssociation", back_populates="robots")
