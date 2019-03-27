
from sqlalchemy import BigInteger, Column, String, DateTime, SmallInteger, ForeignKey, Boolean
from config.db_config import Base
import datetime


class Task_remind(Base):
    __tablename__ = 'task_remind'
    # task props
    id                  = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)

    next_remind_date    = Column(DateTime)
    task_id = Column(BigInteger, nullable=False)
    # message props

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id, task_id, date):
        # TODO get data from message (remove date?)

        self.user_id = user_id
        self.task_id = task_id
        self.next_remind_date=date
    def get_id(self):
        return self.id


    def get_next_remind_date(self):
        return self.next_remind_date

    def set_next_remind_date(self, next_remind_date):
        if next_remind_date < datetime.datetime.now():
            raise ValueError('Next remind date cannot be in past')
        self.next_remind_date = next_remind_date


