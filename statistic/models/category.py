
from sqlalchemy import BigInteger, Column, String, DateTime, SmallInteger, ForeignKey, Boolean
from config.db_config import Base
import datetime


class Category(Base):
    __tablename__ = 'category'
    # task props
    id                  = Column(BigInteger, primary_key=True, autoincrement=True, nullable=False)
    category = Column(String, default='Общее')
    task_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    def get_id(self):
        return self.id

    def set_category(self, category):
        self.category = category
    def get_category(self):
        return self.category
