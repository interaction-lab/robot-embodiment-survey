from sqlalchemy import Column, String

from base import Base


class Robot(Base):
    __tablename__ = 'robot'

    name = Column(String, primary_key=True, nullable=False)
    short_name = Column(String, nullable=False)
    remote_url = Column(String, nullable=False)
    local_path = Column(String, nullable=False)
