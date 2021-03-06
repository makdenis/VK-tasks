from sqlalchemy import BigInteger, Column, String, DateTime, SmallInteger, ForeignKey, Boolean
from config.db_config import Base
import datetime


class Task(Base):
    __tablename__ = 'tasks'
    # task props
    id = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    description = Column(String, nullable=False)

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)

    def __init__(self, description, user_id, project_id):
        # TODO get data from message (remove date?)
        self.set_description(description.capitalize())
        self.set_user_id(user_id)

        # do not need it now
        self.set_priority(1)
        # original message
        self.set_message_text(description)

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def set_description(self, descr):
        if not descr:
            raise ValueError('Task description text cannot be empty')
        self.description = descr

    def get_create_date(self):
        return self.create_date

    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

    def get_project_id(self):
        return self.project_id

    def set_project_id(self, proj_id):
        self.project_id = proj_id

    def set_priority(self, prior):
        self.priority = prior

    def set_message_text(self, msg_text):
        if not msg_text:
            raise ValueError('Message text cannot be empty')
        self.message_text = msg_text

    def set_start_date(self, start_date):
        self.start_date = start_date

    def set_end_date(self, end_date):
        if end_date < datetime.datetime.now():
            raise ValueError('End date cannot be in past')
        self.end_date = end_date

    def get_next_remind_date(self):
        return self.next_remind_date

    def set_next_remind_date(self, next_remind_date):
        if next_remind_date < datetime.datetime.now():
            raise ValueError('Next remind date cannot be in past')
        self.next_remind_date = next_remind_date

    def set_is_periodic(self, periodic_flag):
        self.is_periodic = periodic_flag

    def set_category(self, category):
        self.category = category

    def get_category(self):
        return self.category
