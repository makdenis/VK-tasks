
from sqlalchemy import BigInteger, Column, String, DateTime, SmallInteger, ForeignKey, Boolean
from config.db_config import Base
import datetime


class Task_create_date(Base):
    __tablename__ = 'task_create_date'
    # task props
    id                  = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    task_id = Column(BigInteger, nullable=False)
    # message props

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    create_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # reminder props


    def __init__(self, user_id, task_id):
        # TODO get data from message (remove date?)

        self.user_id=user_id
        self.task_id=task_id
        # do not need it now



    def get_id(self):
        return self.id



    def get_create_date(self):
        return self.create_date

    def get_user_id(self):
        return self.user_id

