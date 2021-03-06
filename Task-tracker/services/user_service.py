from config.db_config import db_session
import datetime
from models.task import Task
from models.project import Project
from models.user import User
from utils.service_utils import save, flush, find_all


def find_one_by_username(username):
    users = find_all(User)
    for u in users:
        if username == u.get_username():
            return u
    return None


def find_one_by_id(id_value):
    users = find_all(User)
    for u in users:
        if id_value == u.get_id():
            return u
    return None


def create_or_get_user(id, username, first_name):
    chat_id = int(id)
    # check if user already exists
    user_by_id = find_one_by_id(chat_id)
    if user_by_id:
        return user_by_id

    else:
        # create new one
        username = username
        first_name = first_name
        user = flush(User(username=username, chat_id=chat_id, first_name=first_name))
        saved_user = save(user)
        return saved_user
