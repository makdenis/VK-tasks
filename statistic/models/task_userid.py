from sqlalchemy import BigInteger, Column, ForeignKey

from config.db_config import Base


class Task_userid(Base):
    __tablename__ = 'task_userid'
    # task props
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)

    # reminder props
    task_id = Column(BigInteger, nullable=False)
    # message props

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    def __init__(self, user_id, task_id):
        # TODO get data from message (remove date?)

        self.set_user_id(user_id)
        self.task_id = task_id

    def get_id(self):
        return self.id

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id
