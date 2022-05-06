

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.ext.declarative import declarative_base

from ebs.linuxnode.core.background import BackgroundSpec

Base = declarative_base()
metadata = Base.metadata


class BackgroundModel(Base):
    __tablename__ = 'bg'

    id = Column(Integer, primary_key=True)
    seq = Column(Integer, unique=True, index=True)
    target = Column(Text)
    bgcolor = Column(Text, nullable=True)
    duration = Column(Integer, nullable=True)

    def __init__(self, seq: int, spec: BackgroundSpec):
        self.seq = seq
        self.target = spec.target
        self.bgcolor = spec.bgcolor
        self.duration = spec.duration

    def native(self):
        return BackgroundSpec(target=self.target, bgcolor=self.bgcolor,
                              callback=None, duration=self.duration)

    def __repr__(self):
        return "{0:3} {1} {2} [{3}]".format(
            self.seq, self.target, self.bgcolor, self.duration or ''
        )
