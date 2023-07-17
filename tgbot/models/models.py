from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, BigInteger
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    connection_date = Column(DateTime, default=datetime.now, nullable=False)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    city_name = Column(String)
    city_geo = Column(String)

    def __repr__(self):
        return f'{self.tg_id}'

    # __mapper_args__ = {"eager_defaults": True}
