import typing

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class RobotAssignment(Base):
    # Many to many: assignment | robot
    robot_id = Column(String, ForeignKey('robot.name'))
    assignment_id = Column(String, ForeignKey('assignment.id'))


class Assignment(Base):
    __tablename__ = 'assignment'

    id = Column(String, primary_key=True, nullable=False)
    robots = relationship("Robot", secondary=RobotAssignment,
                          back_populates="assignments")  # type: typing.List[Robot]


class Robot(Base):
    __tablename__ = 'robot'

    name = Column(String, primary_key=True, nullable=False)
    short_name = Column(String, nullable=False)
    remote_url = Column(String, nullable=False)
    local_path = Column(String, nullable=False)

    assignments: typing.List[Assignment]
