"""


if you are not sure which service should implement function
then implement it in it's return type service
e.g. get all user's tasks: return type is Task -> task_service.find_all_by_user_id
"""
from config.db_config import db_session
from models.category import Category
from models.project import Project
from models.task import Task
from models.task_create_date import Task_create_date
from models.task_end import Task_end
from models.task_remind import Task_remind
from models.task_userid import Task_userid
from utils.service_utils import save, find_all
from sqlalchemy import func


def find_tasks_by_title(title):
    all_tasks = find_all(Task)
    res = []
    for t in all_tasks:
        if title in t.title:
            res.append(t)

    return res


def find_tasks_by_category(cat):
    all_tasks = find_all(Task)
    res = []
    for t in all_tasks:
        if cat in t.category:
            res.append(t)

    return res


def find_tasks_by_id(id):
    all_tasks = find_all(Task)
    res = []
    for t in all_tasks:
        if id == t.id:
            res.append(t)

    return res


def find_tasks_by_user_id(user_id_value):
    user_id = int(user_id_value)
    all_tasks = find_all(Task)
    tasks_by_user = [t for t in all_tasks if user_id == t.get_user_id()]
    return tasks_by_user


def find_nearest_task(user_id):
    all_tasks = db_session.query(Task, Task_create_date).join(Task_create_date, Task_create_date.task_id == Task.id)
    sorted_by_remind_date = sorted(
        all_tasks, key=lambda t: t.Task_create_date.create_date)
    return sorted_by_remind_date[-1]


def update_text(task_id, text):
    entity_by_id = db_session.query(Task).filter_by(id=task_id).update({'description': text})
    db_session.commit()


def delete_task(task_id):
    db_session.query(Task).filter_by(id=task_id).delete()
    db_session.query(Task_create_date).filter_by(task_id=task_id).delete()
    db_session.query(Task_end).filter_by(task_id=task_id).delete()
    db_session.query(Task_remind).filter_by(task_id=task_id).delete()
    db_session.query(Task_userid).filter_by(task_id=task_id).delete()
    db_session.query(Category).filter_by(task_id=task_id).delete()
    db_session.commit()


def set_category(task_id, user, category):
    entity_by_id = db_session.query(Category).filter_by(id=task_id, user_id=user).update({'category': category})
    db_session.commit()


def get_info(id, user):
    all_tasks = find_all(Category)
    cat = list(filter(
        lambda t: t.task_id == id and t.user_id == user, all_tasks))
    all_tasks = find_all(Task_create_date)
    create = list(filter(
        lambda t: t.task_id == id and t.user_id == user, all_tasks))
    all_tasks = find_all(Task_remind)
    remind = list(filter(
        lambda t: t.task_id == id and t.user_id == user, all_tasks))
    all_tasks = find_all(Task_end)
    end = list(filter(
        lambda t: t.task_id == id and t.user_id == user, all_tasks))
    if len(cat) == 0:
        cat = "-"
    else:
        cat = cat[0].category
    if len(create) == 0:
        create = "-"
    else:
        create = create[0].create_date
    if len(remind) == 0:
        remind = "-"
    else:
        remind = remind[0].next_remind_date
    if len(end) == 0:
        end = "-"
    else:
        end = end[0].end_date
    return cat, create, remind, end


def get_date(id):
    all_tasks = find_all(Task_create_date)
    time = list(filter(
        lambda t: t.task_id == id, all_tasks))
    return time[0].create_date


def get_category(id, user):
    all_tasks = find_all(Category)
    cat = list(filter(
        lambda t: t.task_id == id and t.user_id == user, all_tasks))
    return cat[0].category


def get_stat(category, user_id):
    all_stat = find_all(Project)
    stat = list(filter(
        lambda t: t.title == category and t.user_id == user_id, all_stat))
    return stat


def create_task(user_id, text):
    user = user_id
    msg_text = text
    project = 1
    if project and user:
        new_task = Task(description=msg_text, user_id=user, project_id=1)
        saved_task = save(new_task)

        # project_service.update_nearest_task_for_project(project.get_id())

        return saved_task

    else:
        raise ValueError('Project/User could not be created')


def create_category(task_id, user_id):
    user = user_id
    if user:
        new_category = Category(user_id=user, task_id=task_id)
        saved_category = save(new_category)

        # project_service.update_nearest_task_for_project(project.get_id())

        return saved_category

    else:
        raise ValueError('Project/User could not be created')


def create_date(task_id, user_id):
    user = user_id
    if user:
        date = Task_create_date(user_id=user, task_id=task_id)
        saved_date = save(date)

        # project_service.update_nearest_task_for_project(project.get_id())

        return saved_date


def create_user_id(task_id, user_id):
    user = user_id
    if user:
        id = Task_userid(user_id=user, task_id=task_id)
        saved_id = save(id)

        # project_service.update_nearest_task_for_project(project.get_id())

        return saved_id


def get_remind(id):
    stat = db_session.query(Task, Task_remind, Category). \
        join(Task_remind, Task_remind.task_id == Task.id). \
        join(Category, Category.task_id == Task.id)
    # stat = db_session.execute('Select * from tasks t join task_remind r on t.id=r.task_id join category g on t.id=g.task_id')
    stat = list(stat)
    return stat


def create_end(task_id, user_id, date):
    user = user_id
    all = find_all(Task_end)
    all = list(filter(lambda t: t.task_id == task_id and t.user_id == user_id, all))
    if len(all) == 0:

        date = Task_end(user_id=user, task_id=task_id, date=date)
        saved_date = save(date)
        return saved_date
    else:
        entity_by_id = db_session.query(Task_end).filter_by(user_id=user, task_id=task_id).update(
            {'end_date': date})
        db_session.commit()


def create_remind(task_id, user_id, date):
    user = user_id
    all = find_all(Task_remind)
    all = list(filter(lambda t: t.task_id == task_id and t.user_id == user_id, all))
    if len(all) == 0:

        date = Task_remind(user_id=user, task_id=task_id, date=date)
        saved_date = save(date)
        return saved_date
    else:
        entity_by_id = db_session.query(Task_remind).filter_by(user_id=user, task_id=task_id).update(
            {'next_remind_date': date})
        db_session.commit()


def change_category(user_id, task_id, cat):
    all_cat = find_all(Category)
    category = [t for t in all_cat if user_id == t.user_id and task_id == t.task_id]
    category[0].category = cat
    entity_by_id = db_session.query(Category).filter_by(task_id=task_id, user_id=user_id).update({'category': cat})
    db_session.commit()


def add_category(category, user_id):
    all_category = find_all(Project)
    all = list(filter(lambda t: t.title == category and t.user_id == user_id, all_category))
    if len(all) == 0:
        project = Project(title=category, user_id=user_id)
        save(project)
