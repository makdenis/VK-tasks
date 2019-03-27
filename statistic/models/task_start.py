
from sqlalchemy import BigInteger, Column, String, DateTime, SmallInteger, ForeignKey, Boolean
from config.db_config import Base
import datetime


class Task_start(Base):
    __tablename__ = 'task_start'
    # task props
    id                  = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)

    start_date          = Column(DateTime, default=datetime.datetime.utcnow)

    task_id = Column(BigInteger, nullable=False)
    # message props

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    # reminder props


    def get_id(self):
        return self.id



    def set_start_date(self, start_date):
        self.start_date = start_date

