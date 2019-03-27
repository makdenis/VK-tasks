import datetime

from sqlalchemy import BigInteger, Column, DateTime, ForeignKey

from config.db_config import Base


class Task_end(Base):
    __tablename__ = 'task_end'
    # task props
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)

    # create_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # message props

    # user_id             = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    # reminder props
    # start_date          = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    task_id = Column(BigInteger, nullable=False)
    # message props

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    # reminder props
    def __init__(self, user_id, task_id):
        # TODO get data from message (remove date?)

        self.user_id = user_id
        self.task_id = task_id

    def get_id(self):
        return self.id

    def set_end_date(self, end_date):
        if end_date < datetime.datetime.now():
            raise ValueError('End date cannot be in past')
        self.end_date = end_date
